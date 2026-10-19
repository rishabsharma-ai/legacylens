"""Local sentence embeddings with all-MiniLM-L6-v2 (384 dimensions), run through ONNX.

The model (about 80 MB) is downloaded once into ~/.cache/legacylens/ from Chroma's
public bucket, then everything runs offline on CPU. Vectors are L2-normalised, so
cosine distance and dot product rank the same way.
"""

import hashlib
import io
import os
import tarfile
import urllib.request
from functools import lru_cache
from pathlib import Path

import numpy as np

MODEL_URL = "https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz"
MODEL_SHA256 = "913d7300ceae3b2dbc2c50d1de4baacab4be7b9380491c27fab7418616a16ec3"
CACHE = Path(os.getenv("LEGACYLENS_CACHE", Path.home() / ".cache" / "legacylens"))
DIM = 384
MAX_TOKENS = 256


def model_dir() -> Path:
    target = CACHE / "all-MiniLM-L6-v2"
    if (target / "model.onnx").exists():
        return target
    target.mkdir(parents=True, exist_ok=True)
    data = urllib.request.urlopen(MODEL_URL, timeout=120).read()
    if hashlib.sha256(data).hexdigest() != MODEL_SHA256:
        raise RuntimeError("embedding model download failed its checksum")
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar.getmembers():
            if member.isfile():
                (target / Path(member.name).name).write_bytes(tar.extractfile(member).read())
    return target


@lru_cache(maxsize=1)
def _model():
    import onnxruntime
    from tokenizers import Tokenizer

    d = model_dir()
    tok = Tokenizer.from_file(str(d / "tokenizer.json"))
    tok.enable_truncation(MAX_TOKENS)
    tok.enable_padding(pad_id=0, pad_token="[PAD]")
    opts = onnxruntime.SessionOptions()
    opts.log_severity_level = 3
    session = onnxruntime.InferenceSession(
        str(d / "model.onnx"), opts, providers=["CPUExecutionProvider"]
    )
    return tok, session


def embed(texts: list[str], batch: int = 32) -> list[list[float]]:
    tok, session = _model()
    out = []
    for i in range(0, len(texts), batch):
        enc = tok.encode_batch(texts[i : i + batch])
        ids = np.array([e.ids for e in enc], dtype=np.int64)
        mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
        feeds = {"input_ids": ids, "attention_mask": mask, "token_type_ids": np.zeros_like(ids)}
        hidden = session.run(None, feeds)[0]  # (batch, tokens, 384)
        m = mask[..., None].astype(np.float32)
        pooled = (hidden * m).sum(1) / np.clip(m.sum(1), 1e-9, None)  # mean over real tokens
        pooled /= np.linalg.norm(pooled, axis=1, keepdims=True)
        out += pooled.astype(np.float32).tolist()
    return out


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
