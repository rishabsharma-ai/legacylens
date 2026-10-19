"""The real CardDemo graph, loaded into the emulator, answers the graph-only eval
questions (q01, q06, q14) through the named query templates alone."""

from pathlib import Path

import pytest

from legacylens.ingest.code.build import CORPUS, build_graph
from legacylens.ingest.code.load import load_graph
from legacylens.retrieval import graph_queries as q
from legacylens.store.spanner import reset_database

pytestmark = [
    pytest.mark.emulator,
    pytest.mark.skipif(not Path(CORPUS).exists(), reason="run make corpus first"),
]


@pytest.fixture(scope="module")
def db():
    db = reset_database("test_code_graph")
    load_graph(db, build_graph())
    return db


def test_q01_posting_job_and_files(db):
    assert q.jobs_running("CBTRN02C", db) == [
        {"job": "POSTTRAN", "steps": '["STEP15"]', "source": "app/jcl/POSTTRAN.jcl"}
    ]
    access = {(r["dataset"], r["access"]) for r in q.files_of("CBTRN02C", db)}
    assert {(d, "READS") for d in ("DALYTRAN", "CARDXREF", "ACCTDATA", "TCATBALF")} <= access
    assert {(d, "WRITES") for d in ("TRANSACT", "ACCTDATA", "TCATBALF", "DALYREJS")} <= access


def test_q06_programs_including_cvact01y(db):
    base = {r["program"] for r in q.programs_including("CVACT01Y", db) if r["app"] == "base"}
    assert base == {
        "CBACT01C",
        "CBACT04C",
        "CBEXPORT",
        "CBIMPORT",
        "CBSTM03A",
        "CBTRN01C",
        "CBTRN02C",
        "COACTUPC",
        "COACTVWC",
        "COBIL00C",
        "COTRN02C",
    }


def test_q14_statements(db):
    assert {r["job"] for r in q.jobs_running("CBSTM03A", db)} == {"CREASTMT"}
    assert "CBSTM03B" in {r["callee"] for r in q.callees_of("CBSTM03A", db)}


def test_signon_transfers(db):
    callees = {r["callee"]: r["how"] for r in q.callees_of("COSGN00C", db)}
    assert callees == {"COADM01C": "XCTL", "COMEN01C": "XCTL"}


def test_menu_transfers_come_from_data(db):
    rows = q.callees_of("COMEN01C", db)
    from_table = {r["callee"] for r in rows if r["method"] == "data_table"}
    assert {"COACTVWC", "COBIL00C", "COTRN00C"} <= from_table


def test_interest_writes_systran_and_has_fee_stub(db):
    assert ("SYSTRAN", "WRITES") in {
        (r["dataset"], r["access"]) for r in q.files_of("CBACT04C", db)
    }
    assert q.node("PARAGRAPH:CBACT04C.1400-COMPUTE-FEES", db) is not None


def test_reject_rules(db):
    rules = [r["rule"] for r in q.rules_of("CBTRN02C", db)]
    for code in ("100", "101", "102", "103"):
        assert any(r.startswith(f"Reason {code}:") for r in rules)
