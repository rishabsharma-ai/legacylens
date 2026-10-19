# ADR-0010: A FastAPI chat page with an evidence panel, no front-end build

- Status: accepted
- Date: 2026-10-19

## Context

ADK's dev UI is great for watching tool calls, but it doesn't show *why* an answer is
right: the route, the entities found, their graph neighbourhood, and the document
chunks. The owner also wants a page to use day to day.

## Decision

`src/legacylens/ui/` is a FastAPI app (`make ui`, then http://localhost:8000) with a
small JSON API (`/api/ask`, `/api/status`, `/api/node/{id}`, `/api/okf`) and one
static HTML file with plain JavaScript and CSS. The page shows the chat on the left
and the evidence for the selected answer on the right, including an SVG drawing of the
entity's neighbourhood. Clicking an entity opens its generated OKF page in a drawer.

## Alternatives considered

- **React or another framework**: a build step, a `node_modules` folder and a second
  language toolchain for one page. Not worth it at this size.
- **Streamlit or Gradio**: quick, but they hide the request and response, which is
  the part worth learning, and they are harder to style.
- **Only ADK's dev UI**: still available through `make adk`.

## Consequences

- No new dependencies beyond FastAPI and Uvicorn, which ADK already pulls in.
- The page works with no LLM key (evidence-only answers); the agentic mode is turned
  off in the page until a key is set.
- If the page grows past a few hundred lines of script, revisit the framework choice.
