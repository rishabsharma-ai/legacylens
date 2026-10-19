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
make emulator    # start the Spanner emulator
make corpus      # fetch CardDemo
make db          # create the database
make test
```

## Read next

- [Architecture](docs/architecture.md): the whole system on one page
- [Decision records](docs/adr/README.md): why it is built this way
- [Learning notes](docs/learning/README.md): mainframe primer and RAG patterns
- [Roadmap](docs/roadmap.md)
