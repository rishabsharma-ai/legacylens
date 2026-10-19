# ADR-0007: Generate an OKF bundle as a curated layer on top of the graph

- Status: accepted
- Date: 2026-10-19

## Context

Open Knowledge Format (OKF, v0.1, Google Cloud, June 2026) is a plain-Markdown spec
for giving agents curated context. A bundle is a folder of `.md` files, one per
concept. Each has YAML frontmatter (`type` is required; `title`, `description`,
`resource`, `tags` and `timestamp` are reserved) and links to other concepts with
normal Markdown links. Agents start at `index.md` and follow links, which is called
progressive disclosure. It is a format, not a database or service.

RAG retrieves raw fragments at question time. OKF stores pre-digested knowledge that
agents and people can read and correct.

## Decision

Treat OKF as an output of the knowledge store, not a replacement for it:

- A generator walks the graph and writes `knowledge/` as an OKF bundle: `index.md`,
  then `programs/CBTRN02C.md`, `jobs/POSTTRAN.md`, `copybooks/CVACT01Y.md`,
  `datasets/ACCTDATA.md` and so on. Each page holds facts from the graph (calls, files,
  jobs), a short LLM-written summary marked as generated, and links to the documents
  that mention it.
- Uses:
  1. **Agent context**: a `read_concept` tool lets the agent open a page and follow
     links, so it gets an entity's whole neighbourhood in one short Markdown page
     instead of many query results.
  2. **Human docs**: the bundle is readable on GitHub as an auto-generated wiki of the
     codebase.
  3. **Portability**: another tool (an IDE assistant, a coding agent) can use the bundle
     with no access to Spanner.
  4. **Eval strategy**: "OKF browse" is scored next to naive, hybrid and graph-first RAG.
- Build it after graph-first retrieval works (milestone 5), because it depends on a
  good graph.

## Alternatives considered

- **OKF as the primary store**: Markdown files can't answer "every program that copies
  CVACT01Y" as reliably or as fast as a graph query.
- **Skip OKF**: it costs little to generate, and it is a skill to learn.

## Consequences

- Pages go stale when the graph changes, so the generator must be rerunnable and its
  output diffable in git.
- Generated summaries can be wrong. They are marked as generated, and graph facts
  come from queries, never from the LLM.
- The spec is v0.1, so recheck it before building.

## Implementation notes (milestone 5)

- Rechecked the spec on 2026-10-19: still v0.1. `type` is the only required field;
  `title`, `description`, `resource`, `tags` and `timestamp` are optional common
  fields. `index.md` per folder is optional; we write one per folder.
- Links are relative (`../jobs/POSTTRAN.md`), so they work on GitHub and on disk. The
  spec's example uses root-relative links, which GitHub would resolve against the repo
  root instead of the bundle.
- `resource` is the source file on GitHub at the pinned CardDemo commit.
- No `timestamp` field and no `log.md`: both change on every run and would break the
  clean-diff rule. The commit history is the log.
- Pages hold graph facts only. The LLM summary is left out for now, so the bundle
  needs no key and never contains generated claims.
- A test fails when the committed bundle no longer matches the graph; run `make okf`.
