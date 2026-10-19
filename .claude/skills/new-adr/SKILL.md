---
name: new-adr
description: Record a design decision as a new ADR in docs/adr. Use when a choice about storage, schema, retrieval, models, agents or tooling is made or changed.
---

1. Find the next number: the highest `docs/adr/NNNN-*.md` plus one.
2. Copy `docs/adr/0000-template.md` to `docs/adr/NNNN-short-kebab-title.md`.
3. Fill in Context, Decision, Alternatives considered and Consequences in plain
   words. Explain any term a newcomer to graph databases or RAG would not know.
4. If it replaces an earlier ADR, set the old one's status to
   `superseded by ADR-NNNN`. Don't rewrite the old one's content.
5. Add a row to the table in `docs/adr/README.md`.
6. If the decision changes the picture in `docs/architecture.md`, update that too.
