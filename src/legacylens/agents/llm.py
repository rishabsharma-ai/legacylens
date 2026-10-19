"""The language model behind the answers, chosen by settings (ADR-0006).

LLM_MODEL is any LiteLLM model name, such as gemini/gemini-flash-latest (free key from
Google AI Studio) or ollama/qwen3:4b (local). LLM_MODEL=none turns the model off; the
app then answers with the evidence alone, so it works with no key at all.
LLM_MODEL_SMALL, when set, is a cheaper model for easy questions (see choose_model).
"""

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / "evals" / ".cache"


def model() -> str:
    return os.getenv("LLM_MODEL", "gemini/gemini-flash-latest")


def small_model() -> str | None:
    return os.getenv("LLM_MODEL_SMALL") or None


def available(name: str | None = None) -> bool:
    """True when the model can be called: a key is set, or it runs locally."""
    name = name or model()
    if name.lower() in ("", "none", "off"):
        return False
    if name.startswith("gemini/"):
        return bool(os.getenv("GEMINI_API_KEY"))
    return True  # ollama/... and other providers carry their own settings


def choose_model(route: str, n_facts: int, n_chunks: int) -> tuple[str, str]:
    """A tiny model router: a cheap model when the evidence is small and structural.

    Graph-only questions with one or two entities need the model to restate facts, not
    to reason over documents, so a smaller model is usually enough. Everything else goes
    to the main model. RouteLLM learns this choice instead; see ADR-0009.
    """
    small = small_model()
    if small and available(small) and route == "graph" and n_facts <= 2:
        return small, "graph-only question with little evidence"
    return model(), "default model"


def complete(system: str, prompt: str, name: str | None = None, cache: bool = False) -> dict:
    """One chat completion. Returns {text, model, tokens}. Cached by prompt hash if asked."""
    import litellm

    name = name or model()
    key = hashlib.sha256(f"{name}\n{system}\n{prompt}".encode()).hexdigest()[:24]
    path = CACHE / f"{key}.json"
    if cache and path.exists():
        return json.loads(path.read_text())
    response = litellm.completion(
        model=name,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=0,
    )
    usage = getattr(response, "usage", None)
    out = {
        "text": response.choices[0].message.content or "",
        "model": name,
        "tokens": getattr(usage, "total_tokens", None),
    }
    if cache:
        CACHE.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(out))
    return out
