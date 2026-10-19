"""Chunking, linking and retrieval over the synthetic documents."""

from pathlib import Path

import pytest

from legacylens.ingest.code.build import CORPUS, build_graph
from legacylens.ingest.code.load import load_graph
from legacylens.ingest.docs.chunk import all_documents
from legacylens.ingest.docs.link import EntityMatcher, load_aliases
from legacylens.ingest.docs.load import load_docs
from legacylens.retrieval import search
from legacylens.store.spanner import reset_database


def test_chunks_follow_structure():
    docs = dict((d.doc_id, cs) for d, cs in all_documents())
    headings = [c.heading for c in docs["CONFLUENCE:2003"]]
    assert "Transaction Posting Rules > Reject reason codes" in headings
    table = next(c for c in docs["CONFLUENCE:2003"] if c.heading.endswith("Reject reason codes"))
    assert "| 102" in table.text and "| 103" in table.text  # the table stays whole
    jira = docs["JIRA:CARD-102"]
    assert [c.chunk_id for c in jira] == ["CHUNK:JIRA:CARD-102#0", "CHUNK:JIRA:CARD-102#1"]


def test_matcher_prefers_longest_alias():
    m = EntityMatcher(
        [("PROGRAM:CBTRN02C", "Program", "CBTRN02C"), ("JOB:POSTTRAN", "Job", "POSTTRAN")],
        {"posting job": ["JOB:POSTTRAN", "PROGRAM:CBTRN02C"], "posting": ["PROGRAM:CBTRN02C"]},
    )
    found = {(x.node_id, x.method, x.surface) for x in m.find("Rerun the posting job tonight")}
    assert found == {
        ("JOB:POSTTRAN", "alias", "posting job"),
        ("PROGRAM:CBTRN02C", "alias", "posting job"),
    }
    assert m.find("CBTRN02C-X is not CBTRN02C")[0].method == "exact_name"


needs_db = [
    pytest.mark.emulator,
    pytest.mark.skipif(not Path(CORPUS).exists(), reason="run make corpus first"),
]


@pytest.fixture(scope="module")
def db():
    db = reset_database("test_docs")
    graph = build_graph()
    load_graph(db, graph)
    load_docs(db)
    return db


@pytest.mark.usefixtures("db")
class TestRetrieval:
    pytestmark = needs_db

    def test_alias_targets_exist(self, db):
        known = {r["node_id"] for r in search.gq.run("SELECT node_id FROM Node", db=db)}
        for phrase, targets in load_aliases().items():
            assert set(targets) <= known, phrase

    def test_mentions_have_method_and_confidence(self, db):
        rows = search.gq.run(
            "SELECT JSON_VALUE(props, '$.method') AS method FROM Edge "
            "WHERE edge_type = 'MENTIONS' AND src_id = 'CHUNK:JIRA:CARD-102#0'",
            db=db,
        )
        assert {r["method"] for r in rows} >= {"exact_name"}

    def test_conflict_question_gets_both_sides(self, db):
        r = search.graph_first("Does the interest job charge late fees?", 6, db)
        assert {"CONFLUENCE:2004", "JIRA:CARD-102"} <= set(r.doc_ids)
        assert "PARAGRAPH:CBACT04C.1400-COMPUTE-FEES" in [e["node_id"] for e in r.entities]

    @pytest.mark.parametrize(
        "question,doc",
        [
            ("What does S0C7 mean?", "CONFLUENCE:2007"),
            ("What is the order of the nightly batch jobs?", "CONFLUENCE:2002"),
            ("When is the weekly change board?", "CONFLUENCE:2008"),
        ],
    )
    def test_no_entity_questions_use_hybrid(self, db, question, doc):
        r = search.graph_first(question, 3, db)
        assert r.route == "docs"
        assert doc in r.doc_ids

    def test_posting_rejects(self, db):
        r = search.graph_first("Why would a transaction be rejected during posting?", 3, db)
        assert r.route == "graph+docs"
        assert "CONFLUENCE:2003" in r.doc_ids
        rules = r.graph_facts[0]["rules"]
        assert any(x["rule"].startswith("Reason 102") for x in rules)

    def test_typo_resolves_fuzzily(self, db):
        ents = search.resolve_entities("what does CBTRN2C do", db)
        assert ents and ents[0]["node_id"] == "PROGRAM:CBTRN02C"
