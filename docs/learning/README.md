# Learning notes

These notes explain the ideas behind LegacyLens in plain terms, and say where each
one shows up in the code. Suggested reading order:

1. [Mainframe primer](mainframe-primer.md): just enough COBOL, CICS and JCL to read
   CardDemo, and how each piece becomes a graph node.
2. [RAG patterns](rag-patterns.md): naive, hybrid, graph, agentic and OKF retrieval,
   and how this project compares them.
3. [Architecture](../architecture.md): how the pieces fit together.
4. [Decision records](../adr/README.md): why each choice was made.

To learn from the code itself, run `make test` and read `tests/test_store.py`. It
shows the four ways of reading the knowledge store in about 100 lines.
