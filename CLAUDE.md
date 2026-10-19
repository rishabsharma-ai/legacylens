# LegacyLens

Context engineering for mainframe code. COBOL, JCL and copybooks from AWS CardDemo
become a Spanner property graph. Synthetic Confluence and Jira docs become embedded
chunks linked to graph nodes. Google ADK agents answer questions graph first. Version
1 is Q&A only, with no code conversion.

Start with `docs/architecture.md`. Decisions and their reasons are in `docs/adr/`.

## Rules

- Use only public code (CardDemo, pinned in `corpus/carddemo.lock`) and synthetic
  docs. Never add employer code, data or documents, even as an example.
- Keep it free: Spanner emulator, local embeddings, free-tier or local LLMs. Ask
  before adding anything that needs a paid account.
- Write the simplest code that works. Use the standard library and existing
  dependencies before adding new ones.
- The owner is learning this stack. When you make a design choice, explain it in plain
  words in the PR, and record lasting decisions as an ADR (use the `new-adr` skill).
- Code beats documents. When they disagree, answers and tests side with the code.

## Commands

```bash
make setup      # install deps (uv sync)
make emulator   # start the Spanner emulator in Docker on :9010
make corpus     # fetch the pinned CardDemo source into corpus/carddemo/
make db         # create the database and apply the schema
make load       # db + load the code graph + load the documents
make okf        # regenerate knowledge/ (commit it; a test checks it matches the graph)
make ui         # chat page on :8000
make adk        # agentic agent in ADK's dev UI
make eval       # score retrieval and answers
make test       # all tests; emulator tests skip if it isn't running
make lint       # ruff check + format check
```

Set `SPANNER_EMULATOR_HOST=localhost:9010` (in `.env`) before anything touches Spanner.

## Layout

- `src/legacylens/store/schema.sql`: the whole schema. Statements are separated by a
  line holding only `;`.
- `src/legacylens/store/spanner.py`: connect, create the instance, reset the database.
- `src/legacylens/ingest/code/` (parsers, `build.py`), `ingest/docs/` (chunk, embed,
  link), `retrieval/` (GQL templates, `search.graph_first`), `agents/` (workflow and
  agentic agents, tools, judge), `okf/generate.py`, `ui/` (FastAPI + one HTML file).
- `adk/lens/`: ADK dev UI entry point. `knowledge/`: generated OKF bundle.
- `corpus/docs/`: synthetic Confluence pages (Markdown with frontmatter) and Jira
  tickets (`jira/tickets.jsonl`).
- `evals/questions.yaml`: questions with expected route, entities, facts and sources.

## Conventions

- Node IDs are `TYPE:NAME` in upper case, for example `PROGRAM:CBTRN02C` and
  `PARAGRAPH:CBACT04C.1400-COMPUTE-FEES`. Chunk IDs are `CHUNK:<doc_id>#<n>`.
- Node and edge types: see ADR-0003 and the tables in `docs/architecture.md`.
- Every loader is idempotent, because the emulator forgets everything on restart.
- Mark emulator tests with `pytestmark = pytest.mark.emulator`. Tests that call the
  default database use the `knowledge_db` fixture.
- Everything must work with no LLM key (`LLM_MODEL=none`): the evidence-only answer.
- Before changing a synthetic doc or eval question, run `make test`. The corpus
  tests check they still agree with each other and with CardDemo.
