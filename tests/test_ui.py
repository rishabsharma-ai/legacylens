"""The chat page's API, with no LLM configured (the evidence-only mode)."""

import pytest
from fastapi.testclient import TestClient

from legacylens.ui.app import app

pytestmark = [pytest.mark.emulator, pytest.mark.usefixtures("knowledge_db")]
client = TestClient(app)


def test_page_and_status(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "none")
    assert "LegacyLens" in client.get("/").text
    status = client.get("/api/status").json()
    assert status["llm"] is False and status["counts"]["Program"] > 40


def test_ask_returns_answer_and_evidence(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "none")
    a = client.post(
        "/api/ask", json={"question": "Why would a transaction be rejected during posting?"}
    ).json()
    assert a["mode"] == "evidence" and a["route"] == "graph+docs"
    assert "Reason 102" in a["text"]
    assert "CONFLUENCE:2003" in a["retrieval"]["doc_ids"]
    agentic = client.post("/api/ask", json={"question": "What is CBTRN02C?", "mode": "agentic"})
    assert "needs an LLM" in agentic.json()["text"]


def test_paragraph_opens_its_program_page():
    n = client.get("/api/node/PARAGRAPH:CBACT04C.1400-COMPUTE-FEES").json()
    assert n["page"] == "programs/CBACT04C.md"
    assert client.get("/api/okf", params={"path": n["page"]}).status_code == 200
    assert client.get("/api/okf", params={"path": "../../pyproject.toml"}).status_code == 404
