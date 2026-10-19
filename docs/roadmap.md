# Roadmap

Each milestone is one project thread and ends in a pull request.

| # | Milestone | Done when |
|---|-----------|-----------|
| 1 | Corpus and architecture | Schema proven on the emulator, docs and eval seed in place (this PR) |
| 2 | Code to graph | CardDemo base app loaded as nodes and edges; q01, q06 and q14 answerable by GQL alone |
| 3 | Docs to chunks | Chunks embedded and linked; naive, hybrid and graph-linked retrieval scored on the eval set |
| 4 | Agents and chat | ADK router (workflow and agentic) answering in `adk web` with cited evidence |
| 5 | OKF layer | Bundle generated from the graph; "OKF browse" scored next to the others |
| 6 | Extensions | Db2, IMS and MQ parts of CardDemo; RouteLLM model routing experiment; custom chat UI |

Modernization (code conversion) is not on the roadmap until Q&A scores well.
