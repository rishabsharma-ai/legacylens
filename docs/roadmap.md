# Roadmap

All six milestones are built. Milestone 1 is PR #1; milestones 2 to 6 are PR #2.

| # | Milestone | Status | What exists |
|---|-----------|--------|-------------|
| 1 | Corpus and architecture | done | Schema proven on the emulator, docs and eval seed |
| 2 | Code to graph | done | CardDemo (base app and sub-apps) as nodes and edges; q01, q06 and q14 answered by GQL alone |
| 3 | Docs to chunks | done | Chunks embedded and linked; naive, hybrid and graph-first retrieval scored |
| 4 | Agents and chat | done | Workflow and agentic ADK agents with cited evidence, `make adk`, answer scoring |
| 5 | OKF layer | done | `knowledge/` generated from the graph; `okf_browse` scored next to the others |
| 6 | Extensions | done | Db2, IMS and MQ edges; rule-based model routing; custom chat page (`make ui`) |

## Next

- Create a free Gemini key and run `make eval` to get LLM-judged answer scores for
  the workflow and agentic agents. Then decide whether RouteLLM is worth trying.
- Close the two parser gaps in `docs/architecture.md` (MQ input queues, batch IMS
  `CBLTDLI` calls).
- Grow `evals/questions.yaml` with questions about the sub-applications.
- Text-to-GQL as an extra tool, guarded by the templates.

Modernization (code conversion) is not on the roadmap until Q&A scores well.
