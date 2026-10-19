"""Agents: evidence-only answers, the prompt context, and ADK tool plumbing."""

import asyncio

import pytest
from google.adk.models import BaseLlm, LlmResponse
from google.genai import types

from legacylens.agents import agentic_agent, llm, workflow_agent

pytestmark = [pytest.mark.emulator, pytest.mark.usefixtures("knowledge_db")]


def test_no_key_means_evidence_mode(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "none")
    assert not llm.available()
    a = workflow_agent.answer("Which job runs the transaction posting program?")
    assert a.mode == "evidence"
    assert "POSTTRAN" in a.text and "DALYREJS" in a.text


def test_context_labels_sections_and_cites():
    r = workflow_agent.search.graph_first("How are late fees charged?", 4)
    ctx = workflow_agent.context(r)
    assert ctx.startswith("GRAPH FACTS")
    assert "DOCUMENTS" in ctx
    assert "`PARAGRAPH:CBACT04C.1400-COMPUTE-FEES`" in ctx
    assert "[JIRA:CARD-102]" in ctx


def test_model_router_uses_small_model_for_graph_only(monkeypatch):
    monkeypatch.setenv("LLM_MODEL", "ollama/big")
    monkeypatch.setenv("LLM_MODEL_SMALL", "ollama/small")
    assert llm.choose_model("graph", 1, 0)[0] == "ollama/small"
    assert llm.choose_model("graph+docs", 1, 3)[0] == "ollama/big"


class FakeLlm(BaseLlm):
    """Calls find_entities, then describe_entity, then answers from what it saw."""

    async def generate_content_async(self, llm_request, stream=False):
        responses = [p.function_response for c in llm_request.contents for p in c.parts or []]
        responses = [r for r in responses if r]
        if not responses:
            call = types.FunctionCall(name="find_entities", args={"question": "CBTRN02C"})
        elif len(responses) == 1:
            call = types.FunctionCall(name="describe_entity", args={"node_id": "PROGRAM:CBTRN02C"})
        else:
            edges = responses[-1].response["edges"]
            jobs = sorted({e["src"] for e in edges if e["edge"] == "RUNS"})
            text = f"Run by {', '.join(jobs)}."
            yield LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))
            return
        yield LlmResponse(
            content=types.Content(role="model", parts=[types.Part(function_call=call)])
        )


def test_agentic_agent_calls_tools():
    out = asyncio.run(agentic_agent.ask_async("Which job runs CBTRN02C?", FakeLlm(model="fake")))
    assert [t["tool"] for t in out["trace"] if "tool" in t] == ["find_entities", "describe_entity"]
    assert "JOB:POSTTRAN" in out["text"]
