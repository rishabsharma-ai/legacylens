# Decision records

Each file records one design decision: the problem, what we chose, what we rejected
and why. When a decision changes, write a new record that supersedes the old one
rather than editing history. Copy `0000-template.md` to start a new one.

| ADR | Decision |
|-----|----------|
| [0001](0001-public-corpus-only.md) | Use only public code (AWS CardDemo) and synthetic documents |
| [0002](0002-spanner-emulator-single-store.md) | One Spanner emulator database for graph, vectors and full-text |
| [0003](0003-graph-schema.md) | One `Node` and one `Edge` table with dynamic labels |
| [0004](0004-chunk-node-links.md) | Chunk-to-code links are `MENTIONS` edges with method and confidence |
| [0005](0005-graph-first-routing.md) | Route graph first, then linked chunks, then hybrid search |
| [0006](0006-models-and-cost.md) | Local embeddings, LLM through LiteLLM, zero cloud cost |
| [0007](0007-okf-knowledge-layer.md) | Generate an OKF bundle as a curated layer on top of the graph |
| [0008](0008-tooling.md) | Python 3.12, uv, ruff, pytest, and a Claude Code project setup |
