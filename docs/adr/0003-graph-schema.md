# ADR-0003: One Node and one Edge table with dynamic labels

- Status: accepted
- Date: 2026-10-19

## Context

Spanner Graph maps ordinary tables onto a property graph. We have about ten kinds of
code entity, more will appear (Db2 tables, MQ queues, IMS segments), and every chunk
must be able to link to any of them.

## Decision

Use the "schemaless" pattern: one `Node` table and one `Edge` table. `node_type` and
`edge_type` are declared as `DYNAMIC LABEL`, and a JSON `props` column as
`DYNAMIC PROPERTIES`. Chunks are rows in `Node` too (`node_type = 'Chunk'`), and their
heavy fields (text, embedding) live in the separate `Chunk` table under the same ID.

Spanner allows dynamic labels only when the graph has exactly one node table and one
edge table. That is why chunks are nodes in `Node` instead of a second node table.

## Alternatives considered

- **One table per entity type** (Program, Copybook, ...): stronger typing and clearer
  SQL, but every new type needs DDL, and a chunk link needs a separate edge table for
  each target type.
- **One generic label with a type property** (`MATCH (n:Node {node_type: 'Program'})`):
  works, but queries read worse and lose label-based planning.

## Consequences

- Queries read naturally: `MATCH (c:Chunk)-[:MENTIONS]->(p:Program {name: 'CBTRN02C'})`.
- New entity and relationship kinds need no schema change.
- Type checking moves into the loader. It must validate node types, edge types and
  required props, and the tests must cover it.
- Foreign keys on `Edge` stop edges pointing at nodes that don't exist. Nodes must be
  loaded before edges.
