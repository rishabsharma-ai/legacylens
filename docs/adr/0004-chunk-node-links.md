# ADR-0004: Chunk-to-code links are MENTIONS edges with method and confidence

- Status: accepted
- Date: 2026-10-19

## Context

Graph-first retrieval needs to know which document chunks talk about which code
entity. The work system builds a separate link table: for each chunk it finds the
entities it mentions, checks they exist in the graph tables, and writes chunk-to-node
rows. That idea is right. The open questions are where the links live and how much we
trust each one.

## Decision

- A link is an `Edge` row: `src_id` = chunk node, `edge_type = 'MENTIONS'`,
  `dst_id` = code node, and `props` = `{method, confidence, surface}`.
- Links are found in three passes, in order of trust:
  1. `exact_name` (confidence 1.0): a known entity name appears as a whole word.
  2. `alias` (0.8): a known nickname appears ("the posting job" for `JOB:POSTTRAN`).
     Aliases come from `corpus/aliases.yaml` (added in thread 3) and program header
     comments.
  3. `llm` (0.5 to 0.7): for chunks with no hits, an LLM picks entities from a
     candidate list the retriever supplies. It can't invent node IDs.
- A link is only written if its target node exists. The foreign key enforces this.

## Alternatives considered

- **A separate link table outside the graph**: the same data, but GQL could not
  traverse it, so every graph-to-docs hop would need hand-written SQL joins.
- **Embedding similarity between chunks and code summaries**: useful later as a fourth
  pass, but it is fuzzy and hard to explain, so it shouldn't be the base layer.

## Consequences

- One GQL pattern goes from a job to its programs to the chunks about them.
- `method` and `confidence` let the eval measure what each linking pass is worth, and
  let retrieval drop weak links when there are strong ones.
- Linking quality is now a thing to test, with its own small labelled set.
