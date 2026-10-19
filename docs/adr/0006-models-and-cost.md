# ADR-0006: Local embeddings, LLM through LiteLLM, zero cloud cost

- Status: accepted
- Date: 2026-10-19

## Context

The project must cost as little as possible, run on a personal laptop, and still use
Google ADK.

## Decision

- **Embeddings**: `BAAI/bge-small-en-v1.5` (384 dimensions) through fastembed. It runs
  on CPU via ONNX, with no PyTorch and no API key. Thread 3 may compare a second model.
- **LLM**: ADK agents use the LiteLLM model wrapper, so the model is a setting:
  - default: Gemini Flash on the Google AI Studio free tier (needs a free API key)
  - offline: a local model through Ollama, such as a small Qwen or Llama
- **Model routing** (cheap model for easy questions, strong one for hard ones) through
  RouteLLM is a later experiment, adopted only if the eval shows it saves cost without
  losing answer quality.

## Alternatives considered

- **Vertex AI models and embeddings**: the production path at work, but it needs a
  billed Google Cloud project.
- **Paid OpenAI or Anthropic APIs**: good quality, but not free.

## Consequences

- No credit card is needed anywhere.
- Free-tier rate limits make big eval runs slow. Cache LLM responses by prompt hash
  during evals.
- Swapping in a stronger model later is one setting, so quality ceilings can be tested
  cheaply.
