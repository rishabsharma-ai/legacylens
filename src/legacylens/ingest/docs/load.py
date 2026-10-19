"""Chunk, embed and link the synthetic documents, then load them into Spanner.

Run after the code graph is loaded, because links point at code nodes.
Usage: uv run python -m legacylens.ingest.docs.load
"""

import json
from collections import Counter

from legacylens.ingest.code.load import write_rows
from legacylens.ingest.docs.chunk import all_documents
from legacylens.ingest.docs.embed import embed
from legacylens.store.spanner import database


def load_docs(db=None) -> Counter:
    db = db or database()
    docs = all_documents()
    chunks = [c for _, cs in docs for c in cs]
    vectors = embed([c.embed_text for c in chunks])
    matcher = _matcher(db)
    doc_rows = [
        (d.doc_id, d.source_type, d.title, d.url, d.updated_at, json.dumps(d.props))
        for d, _ in docs
    ]
    node_rows, chunk_rows, edge_rows = [], [], []
    methods: Counter = Counter()
    for c, vec in zip(chunks, vectors, strict=True):
        node_rows.append(
            (
                c.chunk_id,
                "Chunk",
                c.heading,
                None,
                None,
                None,
                None,
                json.dumps({"doc_id": c.doc_id, "seq": c.seq}),
            )
        )
        chunk_rows.append((c.chunk_id, c.doc_id, c.seq, c.heading, c.text, vec))
        for m in matcher.find(c.embed_text):
            methods[m.method] += 1
            edge_rows.append(
                (
                    c.chunk_id,
                    "MENTIONS",
                    m.node_id,
                    json.dumps(
                        {"method": m.method, "confidence": m.confidence, "surface": m.surface}
                    ),
                )
            )
    write_rows(
        db, "Document", ("doc_id", "source_type", "title", "url", "updated_at", "props"), doc_rows
    )
    write_rows(
        db,
        "Node",
        (
            "node_id",
            "node_type",
            "name",
            "source_path",
            "start_line",
            "end_line",
            "summary",
            "props",
        ),
        node_rows,
    )
    write_rows(
        db, "Chunk", ("chunk_id", "doc_id", "seq", "heading", "text", "embedding"), chunk_rows
    )
    write_rows(db, "Edge", ("src_id", "edge_type", "dst_id", "props"), edge_rows)
    return Counter(documents=len(doc_rows), chunks=len(chunk_rows), **methods)


def _matcher(db):
    from legacylens.ingest.docs.link import EntityMatcher, load_aliases
    from legacylens.retrieval.graph_queries import run

    rows = run(
        "SELECT node_id, node_type, name FROM Node WHERE node_type != 'Chunk' "
        "AND JSON_VALUE(props, '$.unresolved') IS NULL",
        db=db,
    )
    return EntityMatcher([(r["node_id"], r["node_type"], r["name"]) for r in rows], load_aliases())


if __name__ == "__main__":
    print("Loaded:", dict(load_docs(database())))
