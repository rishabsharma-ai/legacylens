# ADR-0005: Route graph first, then linked chunks, then hybrid search

- Status: accepted
- Date: 2026-10-19

## Context

There are two kinds of evidence: exact structure from the graph and explanation from
documents. Querying both every time wastes context and lets loosely related chunks in.
Querying only one misses half the answer.

## Decision

1. **Resolve entities** in the question: exact names, then aliases, then fuzzy matches
   against `Node.name`.
2. If entities are found, fetch their **graph neighbourhood** (1 to 2 hops, using
   named query templates) and their **linked chunks** (`MENTIONS`), ranked by link
   confidence and then by vector similarity to the question.
3. If no entity is found, or fewer than *k* linked chunks score above a threshold,
   run **hybrid search**: vector top-k plus full-text top-k, merged with Reciprocal
   Rank Fusion (score = sum of 1 / (60 + rank)).
4. The answer prompt receives graph facts and chunks in separate, labelled sections,
   and is told that code beats documents when they disagree.

## Alternatives considered

- **Always query both and merge**: simple, but noisy, and the graph and vector scores
  aren't comparable.
- **An LLM classifier picks one store**: an extra call per question, and a wrong pick
  loses the answer entirely.
- **Vector first, graph as an add-on**: weakest on "what calls X" questions, which are
  the main reason to have a graph.

## Consequences

- Entity resolution is the most important component. If it misses, the question falls
  through to hybrid search, so the system degrades instead of failing.
- Routing is deterministic and testable, and the eval set tags the expected route.
- Thread 4 also builds an agentic version where the LLM picks tools, and compares it
  with this one.
