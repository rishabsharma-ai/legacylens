"""Keeps the synthetic docs and the eval set consistent with each other and with
the CardDemo source, so nobody evaluates against a typo."""

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "corpus" / "docs"
CARDDEMO = ROOT / "corpus" / "carddemo" / "app"


def confluence_pages() -> dict[str, dict]:
    pages = {}
    for path in sorted((DOCS / "confluence").glob("*.md")):
        _, front, _ = path.read_text().split("---\n", 2)
        meta = yaml.safe_load(front)
        pages[f"CONFLUENCE:{meta['page_id']}"] = meta
    return pages


def jira_tickets() -> dict[str, dict]:
    lines = (DOCS / "jira" / "tickets.jsonl").read_text().splitlines()
    return {f"JIRA:{t['key']}": t for t in map(json.loads, lines)}


def questions() -> list[dict]:
    return yaml.safe_load((ROOT / "evals" / "questions.yaml").read_text())


def test_every_doc_is_marked_synthetic():
    for meta in [*confluence_pages().values(), *jira_tickets().values()]:
        assert meta["synthetic"] is True


def test_eval_sources_exist():
    known = confluence_pages() | jira_tickets()
    for q in questions():
        for source in q.get("sources", []):
            assert source in known, f"{q['id']} cites unknown {source}"


def test_eval_ids_unique_and_routes_valid():
    qs = questions()
    assert len({q["id"] for q in qs}) == len(qs)
    assert {q["expected_route"] for q in qs} <= {"graph", "graph+docs", "docs", "conflict"}


@pytest.mark.skipif(not CARDDEMO.exists(), reason="run scripts/fetch_corpus.py first")
def test_eval_entities_exist_in_carddemo():
    files = [p for p in CARDDEMO.rglob("*") if p.is_file()]
    names = {p.stem.upper() for p in files}
    all_text = "\n".join(p.read_text(errors="ignore") for p in files)
    for q in questions():
        for node_id in q["entities"]:
            kind, name = node_id.split(":", 1)
            if kind == "PARAGRAPH":
                program, para = name.split(".", 1)
                source = next(CARDDEMO.rglob(f"{program}.*")).read_text()
                assert para in source, f"{q['id']}: {node_id}"
            elif kind == "DATASET":  # datasets are named in JCL DSNs, not files
                assert f".{name}." in all_text or f"'{name}" in all_text, f"{q['id']}: {node_id}"
            else:
                assert name in names, f"{q['id']}: {node_id}"
