# ADR-0009: Two answering agents, an evidence-only mode, and a rule-based model router

- Status: accepted
- Date: 2026-10-19

## Context

Milestone 4 turns retrieval into answers. We wanted to learn the difference between a
fixed pipeline and an agent that plans its own tool calls, keep it free, and still
have something usable before anyone has created an LLM key. ADR-0006 left model
routing (a cheap model for easy questions) as a later experiment.

## Decision

- **Workflow agent** (`agents/workflow_agent.py`): `graph_first()` runs as plain code
  and picks the route; one LLM call turns labelled evidence (GRAPH FACTS, then
  DOCUMENTS) into an answer. The rules say code beats documents, cite every claim,
  and say "not found" instead of guessing. This is the default.
- **Agentic agent** (`agents/agentic_agent.py`): an ADK `LlmAgent` with six function
  tools (`find_entities`, `describe_entity`, `query_graph`, `linked_documents`,
  `search_documents`, `read_concept`). The model decides what to call. ADK reads each
  tool's name, type hints and docstring, so the docstrings are written for the model.
  `make adk` serves it in ADK's dev UI, which shows every tool call.
- **Evidence-only mode**: when no model is available (no `GEMINI_API_KEY`, or
  `LLM_MODEL=none`), the workflow agent writes a plain summary of the same evidence:
  each entity's relationships and rules, the COBOL of a paragraph, and the linked
  document snippets. Nothing breaks without a key; answers are just less fluent.
- **Model router**: `llm.choose_model()` sends graph-only questions with one or two
  entities to `LLM_MODEL_SMALL` when it is set, and everything else to `LLM_MODEL`.
  Restating graph facts doesn't need a strong model.
- **Answer scoring**: `make eval` scores answers by key-term coverage (do the
  program, file and job names and reason codes from `answer_facts` appear?), and with
  a key also by an LLM judge. LLM responses are cached by prompt hash in
  `evals/.cache/`, so reruns cost nothing.

## Alternatives considered

- **Only the agentic agent**: more flexible, but less predictable, more model calls
  per question, and unusable without a key.
- **RouteLLM**: it trains a router on preference data to choose between a strong and
  a weak model. That is worth trying once the eval has LLM-judged scores to compare;
  until then a two-line rule is easier to understand and to measure.
- **ADK's native Gemini model class**: slightly better Gemini support, but LiteLLM
  lets one setting swap Gemini for a local Ollama model (ADR-0006).

## Consequences

- The workflow agent makes exactly one model call per question; the agentic one makes
  one per step. The eval table reports calls and tokens per question.
- Key-term coverage can't tell a right sentence from a wrong one that uses the same
  names. Trust the LLM judge once a key is set.
- The tests run the agentic agent with a fake ADK model, so tool wiring is checked in
  CI without any network.
