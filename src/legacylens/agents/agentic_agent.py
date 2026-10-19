"""The agentic agent: one ADK LlmAgent that decides which tools to call.

Compare it with workflow_agent.py. There, code picks the route; here the model reads
the tool docstrings and routes itself, which is more flexible and less predictable.
`make adk` serves root_agent in ADK's own web UI; the custom chat page calls ask().
"""

import asyncio
import os

from google.adk.agents import LlmAgent
from google.adk.models import BaseLlm
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

from legacylens.agents import llm
from legacylens.agents.tools import TOOLS
from legacylens.agents.workflow_agent import ANSWER_RULES

ROUTING = """
How to work:
1. Call find_entities with the question.
2. For each entity that matters, call describe_entity (or query_graph for a specific
   relationship such as every program that includes a copybook).
3. For "why", "how" or business questions, call linked_documents with the entity IDs.
   If the question names no entity, call search_documents instead.
4. read_concept opens the generated knowledge page for an entity, such as
   "programs/CBTRN02C.md", when you want its whole neighbourhood at once.
Stop calling tools as soon as you can answer."""

APP = "legacylens"
# LiteLLM is a deliberate choice (ADR-0006): one setting swaps Gemini for Ollama.
os.environ.setdefault("ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS", "true")


def build_agent(model: str | BaseLlm | None = None) -> LlmAgent:
    """model is a LiteLLM name, or any ADK model object (the tests pass a fake one)."""
    if not isinstance(model, BaseLlm):
        model = LiteLlm(model=model or llm.model())
    return LlmAgent(
        name="legacylens",
        description="Answers questions about the CardDemo mainframe code and its documents.",
        model=model,
        instruction=ANSWER_RULES + "\n" + ROUTING,
        tools=TOOLS,
    )


root_agent = build_agent()


async def ask_async(question: str, model: str | BaseLlm | None = None) -> dict:
    """Run the agent once. Returns the answer text and a trace of the tool calls."""
    runner = InMemoryRunner(agent=build_agent(model), app_name=APP)
    session = await runner.session_service.create_session(app_name=APP, user_id="local")
    message = types.Content(role="user", parts=[types.Part(text=question)])
    text, trace, tokens = "", [], 0
    async for event in runner.run_async(
        user_id="local", session_id=session.id, new_message=message
    ):
        usage = getattr(event, "usage_metadata", None)
        tokens += getattr(usage, "total_token_count", None) or 0
        for part in (event.content.parts if event.content else None) or []:
            if part.function_call:
                trace.append({"tool": part.function_call.name, "args": part.function_call.args})
            elif part.function_response:
                trace.append({"result_of": part.function_response.name})
            elif part.text and event.is_final_response():
                text += part.text
    return {"text": text, "trace": trace, "tokens": tokens or None}


def ask(question: str, model: str | BaseLlm | None = None) -> dict:
    return asyncio.run(ask_async(question, model))
