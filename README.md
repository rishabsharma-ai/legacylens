# LegacyLens

Ask questions about a mainframe codebase and get answers grounded in its code and its
documentation.

LegacyLens parses COBOL, JCL and copybooks into a Spanner property graph, chunks and
embeds the surrounding docs (Confluence pages, Jira tickets), links each chunk to the
code it talks about, and uses Google ADK agents to answer questions graph first. It
is a learning project in context engineering, built only on public sample code
([AWS CardDemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo))
and synthetic documents. Everything runs locally for free.

## Quick start

You need [uv](https://docs.astral.sh/uv/) and Docker.

```bash
cp .env.example .env
make setup       # install Python deps
make emulator    # start the Spanner emulator (keeps data in memory only)
make corpus      # fetch CardDemo
make load        # create the database, load the code graph and the documents
make ui          # chat page at http://localhost:8000
```

That works with no API key: answers show the evidence (graph facts and document
snippets). For written answers, get a free key at
[Google AI Studio](https://aistudio.google.com/apikey) and set `GEMINI_API_KEY` in
`.env`, or point `LLM_MODEL` at a local Ollama model such as `ollama/qwen3:4b`.

Other commands:

```bash
make adk         # the agentic agent in ADK's dev UI, showing every tool call
make okf         # regenerate the knowledge/ pages after the graph changes
make eval        # score retrieval and answers; writes evals/results/
make test        # all tests (emulator tests skip if it isn't running)
```

The emulator forgets everything when it stops, so run `make load` after each restart.

## Read next

- [Architecture](docs/architecture.md): the whole system on one page
- [Decision records](docs/adr/README.md): why it is built this way
- [Learning notes](docs/learning/README.md): mainframe primer and RAG patterns
- [Knowledge pages](knowledge/index.md): the generated OKF bundle
- [Roadmap](docs/roadmap.md)
