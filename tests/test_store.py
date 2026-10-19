"""Proves the schema supports the three retrieval paths in docs/architecture.md:
graph traversal, graph-linked chunks, and vector / full-text fallback."""

import json

import pytest
from google.cloud.spanner_v1 import param_types

from legacylens.store.spanner import reset_database

pytestmark = pytest.mark.emulator


def vec(*head: float) -> list[float]:
    return list(head) + [0.0] * (384 - len(head))


@pytest.fixture(scope="module")
def db():
    db = reset_database("test_store")
    nodes = [
        ("JOB:POSTTRAN", "Job", "POSTTRAN", None),
        ("PROGRAM:CBTRN02C", "Program", "CBTRN02C", json.dumps({"kind": "batch"})),
        ("DATASET:ACCTDATA", "Dataset", "ACCTDATA", None),
        ("CHUNK:JIRA:CARD-101#0", "Chunk", "Overlimit rejects", None),
        ("CHUNK:CONFLUENCE:2001#0", "Chunk", "Statement layout", None),
    ]
    edges = [
        ("JOB:POSTTRAN", "RUNS", "PROGRAM:CBTRN02C", json.dumps({"step": "STEP15"})),
        ("PROGRAM:CBTRN02C", "READS", "DATASET:ACCTDATA", None),
        (
            "CHUNK:JIRA:CARD-101#0",
            "MENTIONS",
            "PROGRAM:CBTRN02C",
            json.dumps({"method": "exact_name", "confidence": 1.0}),
        ),
    ]
    docs = [
        ("JIRA:CARD-101", "jira", "Overlimit rejects"),
        ("CONFLUENCE:2001", "confluence", "Statement layout"),
    ]
    chunks = [
        (
            "CHUNK:JIRA:CARD-101#0",
            "JIRA:CARD-101",
            0,
            "Posting rejects transactions over the credit limit with reason 102.",
            vec(1.0),
        ),
        (
            "CHUNK:CONFLUENCE:2001#0",
            "CONFLUENCE:2001",
            0,
            "Monthly statements list each transaction.",
            vec(0.0, 1.0),
        ),
    ]
    with db.batch() as b:
        b.insert("Node", ("node_id", "node_type", "name", "props"), nodes)
        b.insert("Document", ("doc_id", "source_type", "title"), docs)
    with db.batch() as b:
        b.insert("Edge", ("src_id", "edge_type", "dst_id", "props"), edges)
        b.insert("Chunk", ("chunk_id", "doc_id", "seq", "text", "embedding"), chunks)
    return db


def query(db, sql, params=None, types=None):
    with db.snapshot() as s:
        return list(s.execute_sql(sql, params=params, param_types=types))


def test_graph_traversal(db):
    rows = query(
        db,
        """
        GRAPH LegacyGraph
        MATCH (j:Job {name: 'POSTTRAN'})-[:RUNS]->(p:Program)-[:READS]->(d:Dataset)
        RETURN p.name AS program, d.name AS dataset""",
    )
    assert rows == [["CBTRN02C", "ACCTDATA"]]


def test_graph_first_linked_chunks(db):
    rows = query(
        db,
        """
        SELECT c.text, g.confidence
        FROM GRAPH_TABLE(LegacyGraph
          MATCH (ch:Chunk)-[m:MENTIONS]->(p:Program {name: 'CBTRN02C'})
          RETURN ch.node_id AS chunk_id, FLOAT64(m.confidence) AS confidence) g
        JOIN Chunk c ON c.chunk_id = g.chunk_id""",
    )
    assert rows == [["Posting rejects transactions over the credit limit with reason 102.", 1.0]]


def test_vector_fallback(db):
    rows = query(
        db,
        """
        SELECT chunk_id FROM Chunk
        ORDER BY COSINE_DISTANCE(embedding, @q) LIMIT 1""",
        {"q": vec(0.1, 0.9)},
        {"q": param_types.Array(param_types.FLOAT32)},
    )
    assert rows == [["CHUNK:CONFLUENCE:2001#0"]]


def test_full_text(db):
    rows = query(db, "SELECT chunk_id FROM Chunk WHERE SEARCH(text_tokens, 'credit limit')")
    assert rows == [["CHUNK:JIRA:CARD-101#0"]]
