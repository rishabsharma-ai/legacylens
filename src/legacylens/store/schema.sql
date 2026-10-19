-- LegacyLens knowledge store: one Spanner database holds the code graph,
-- the document chunks with their embeddings, and the links between them.
-- See docs/adr/0003-graph-schema.md and docs/adr/0004-chunk-node-links.md.
-- Statements are separated by a line holding only ";".

-- Every node in the graph is one row: code entities (Program, Paragraph,
-- Copybook, Dataset, Job, ...) and document chunks (Chunk). node_type becomes the
-- graph label, so a new entity kind needs no DDL change.
CREATE TABLE Node (
  node_id     STRING(MAX) NOT NULL,  -- "<TYPE>:<NAME>", e.g. "PROGRAM:CBTRN02C"
  node_type   STRING(64)  NOT NULL,  -- Program, Paragraph, Copybook, Chunk, ...
  name        STRING(MAX) NOT NULL,
  source_path STRING(MAX),           -- corpus file this came from
  start_line  INT64,
  end_line    INT64,
  summary     STRING(MAX),           -- optional one-paragraph description
  props       JSON,                  -- type-specific extras (kind, dsn, step, ...)
) PRIMARY KEY (node_id)
;
CREATE INDEX NodeByTypeName ON Node (node_type, name)
;
-- Every relationship is one row: CALLS, INCLUDES, READS, WRITES, RUNS, ...
-- and MENTIONS (Chunk -> code entity), which is the chunk-to-node link table.
CREATE TABLE Edge (
  src_id    STRING(MAX) NOT NULL,
  edge_type STRING(64)  NOT NULL,
  dst_id    STRING(MAX) NOT NULL,
  props     JSON,                    -- MENTIONS: {method, confidence, surface}
  CONSTRAINT FK_EdgeSrc FOREIGN KEY (src_id) REFERENCES Node (node_id),
  CONSTRAINT FK_EdgeDst FOREIGN KEY (dst_id) REFERENCES Node (node_id),
) PRIMARY KEY (src_id, edge_type, dst_id)
;
CREATE INDEX EdgeByDst ON Edge (dst_id, edge_type)
;
-- A source document (Confluence page, Jira ticket, ...). Not a graph node:
-- its chunks are.
CREATE TABLE Document (
  doc_id      STRING(MAX) NOT NULL,  -- "CONFLUENCE:<page_id>", "JIRA:<key>"
  source_type STRING(32)  NOT NULL,
  title       STRING(MAX) NOT NULL,
  url         STRING(MAX),
  updated_at  TIMESTAMP,
  props       JSON,
) PRIMARY KEY (doc_id)
;
-- The heavy part of a chunk: its text, embedding and full-text tokens.
-- chunk_id equals the node_id of its "Chunk" row in Node.
CREATE TABLE Chunk (
  chunk_id    STRING(MAX) NOT NULL,  -- "CHUNK:<doc_id>#<n>"
  doc_id      STRING(MAX) NOT NULL,
  seq         INT64       NOT NULL,
  heading     STRING(MAX),
  text        STRING(MAX) NOT NULL,
  embedding   ARRAY<FLOAT32>(vector_length=>384),
  text_tokens TOKENLIST AS (TOKENIZE_FULLTEXT(text)) HIDDEN,
  CONSTRAINT FK_ChunkNode FOREIGN KEY (chunk_id) REFERENCES Node (node_id),
  CONSTRAINT FK_ChunkDoc  FOREIGN KEY (doc_id)   REFERENCES Document (doc_id),
) PRIMARY KEY (chunk_id)
;
CREATE SEARCH INDEX ChunkText ON Chunk (text_tokens)
;
-- One graph over code and chunks, so a single GQL query can hop code -> docs.
-- Spanner allows dynamic labels only with exactly one node and one edge table,
-- which is why chunks live in Node too.
CREATE PROPERTY GRAPH LegacyGraph
  NODE TABLES (
    Node DYNAMIC LABEL (node_type) DYNAMIC PROPERTIES (props)
  )
  EDGE TABLES (
    Edge
      SOURCE KEY (src_id) REFERENCES Node (node_id)
      DESTINATION KEY (dst_id) REFERENCES Node (node_id)
      DYNAMIC LABEL (edge_type) DYNAMIC PROPERTIES (props)
  )
