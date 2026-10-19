# ADR-0002: One Spanner emulator database for graph, vectors and full-text

- Status: accepted
- Date: 2026-10-19

## Context

We need a graph store for code, a vector store for chunks, and keyword search. The
work system uses Spanner Graph, and the goal is to learn it. Cost must stay at zero.

## Decision

Use one database in the Cloud Spanner emulator (tested with version 1.5.59). It holds
the property graph, the chunk embeddings (`ARRAY<FLOAT32>(vector_length=>384)`) and a
full-text search index. Run it with Docker (`make emulator`) or the prebuilt Linux
binary.

Vector search uses exact nearest neighbours (`ORDER BY COSINE_DISTANCE(...) LIMIT k`).
With a few hundred chunks that is instant, and it gives perfect recall to compare
approximate search against later.

## Alternatives considered

- **Real Spanner**: the same features plus vector indexes, but it costs money even at
  the smallest size.
- **Neo4j plus a separate vector DB**: popular, but it isn't the stack being learned,
  and two stores mean every graph-to-chunk hop crosses systems.
- **pgvector plus Apache AGE**: free and capable, but different query languages from
  Spanner.

## Consequences

- One query can join graph results with chunk text. Graph-linked retrieval needs no
  second system.
- The emulator stores data in memory only. Loading must be scripted and repeatable
  (`make load`), which is good discipline anyway.
- The emulator doesn't enforce every production limit, and graph algorithms return
  empty results there. Moving to real Spanner later means changing only the
  connection settings, but behaviour must be rechecked.
