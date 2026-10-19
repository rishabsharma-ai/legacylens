# LegacyLens architecture

LegacyLens answers questions about a mainframe codebase and the documents written
about it. It never sends the whole codebase to an LLM. Instead it builds a knowledge
store ahead of time and hands the model only the few facts a question needs. That
practice is called context engineering, and it is the point of this project.

Version 1 is question answering only. Modernization (rewriting COBOL into another
language) is out of scope until Q&A is measurably good.

## The picture

```mermaid
flowchart LR
  subgraph Ingest["Ingest (offline, rerunnable)"]
    COBOL["CardDemo source<br/>COBOL, copybooks, JCL, BMS"] --> Parser["Code parser"]
    Docs["Synthetic Confluence + Jira"] --> Chunker["Chunker + embedder"]
    Parser --> Linker
    Chunker --> Linker["Entity linker"]
  end
  subgraph Store["Spanner emulator: one database"]
    G[("Node + Edge<br/>property graph")]
    C[("Chunk<br/>text, vector, full-text")]
  end
  Parser -->|nodes, edges| G
  Chunker -->|chunks| C
  Linker -->|MENTIONS edges| G
  subgraph Serve["Answer (online)"]
    UI["Chat UI"] --> Router["ADK router agent"]
    Router --> T1["resolve_entities"] & T2["graph_query"] & T3["linked_chunks"] & T4["hybrid_search"]
    T1 & T2 & T3 & T4 --> Store
    Router --> LLM["LLM via LiteLLM<br/>Gemini free tier or Ollama"]
  end
  Store -. generate .-> OKF["OKF bundle<br/>Markdown concept pages"]
  OKF -.-> Router
```

## The pieces

### 1. Corpus ([ADR-0001](adr/0001-public-corpus-only.md))

- **Code**: AWS CardDemo, an Apache-2.0 sample credit card app with about 44 COBOL
  programs, 62 copybooks, 55 JCL jobs and 21 BMS screens. It is pinned to one commit in
  `corpus/carddemo.lock` and downloaded by `scripts/fetch_corpus.py`.
- **Documents**: `corpus/docs/` holds 8 Confluence-style pages and 12 Jira-style tickets
  written for this project. They name programs exactly, by nickname ("the posting
  job"), or not at all, and one page is deliberately out of date. Each of those cases
  tests a different part of retrieval.

### 2. Knowledge store ([ADR-0002](adr/0002-spanner-emulator-single-store.md), [ADR-0003](adr/0003-graph-schema.md))

One Spanner database, running in the free local emulator, holds everything. The
schema is in [`src/legacylens/store/schema.sql`](../src/legacylens/store/schema.sql).

| Table      | Holds                                                         |
|------------|---------------------------------------------------------------|
| `Node`     | Every graph node: programs, paragraphs, copybooks, datasets, jobs, screens, transactions, business rules, and one row per document chunk |
| `Edge`     | Every relationship: `CALLS`, `XCTL`, `INCLUDES`, `READS`, `WRITES`, `RUNS`, `PERFORMS`, `DEFINES_RULE`, and `MENTIONS` (chunk to code) |
| `Document` | One row per Confluence page or Jira ticket                    |
| `Chunk`    | Chunk text, a 384-number embedding, and a full-text index     |

`LegacyGraph` is a property graph over `Node` and `Edge`. `node_type` and `edge_type`
become labels, so you can write `MATCH (j:Job)-[:RUNS]->(p:Program)`.

Node IDs are readable and stable: `PROGRAM:CBTRN02C`, `COPYBOOK:CVACT01Y`,
`DATASET:ACCTDATA`, `JOB:POSTTRAN`, `PARAGRAPH:CBACT04C.1400-COMPUTE-FEES`,
`CHUNK:JIRA:CARD-102#0`. A dataset is named by the distinctive part of its DSN, so
`AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS` becomes `DATASET:ACCTDATA`.

`tests/test_store.py` proves the schema supports all four retrieval paths on the
emulator: graph traversal, graph-linked chunks, vector search and keyword search.

### 3. Code to graph (thread 2)

The parser turns each source file into nodes and edges. What it must extract:

| Source            | Nodes                          | Edges                                       |
|-------------------|--------------------------------|---------------------------------------------|
| COBOL program     | Program, Paragraph             | `PERFORMS`, `CALLS`, `XCTL`/`LINK`, `INCLUDES`, `READS`/`WRITES` (from `SELECT ... ASSIGN`, `OPEN` mode and CICS `READ`/`WRITE` `DATASET`) |
| Copybook          | Copybook                       | `INCLUDES` (copybook to copybook)           |
| JCL               | Job                            | `RUNS` (with step name), `READS`/`WRITES` (DD to DSN, from `DISP`) |
| BMS map           | Screen                         | `USES_SCREEN` (program to map)              |
| CICS CSD          | Transaction                    | `STARTS` (transaction to program)           |
| Business rules    | BusinessRule                   | `DEFINES_RULE` (paragraph to rule)          |

Business rules start simple: the reject reason codes and `COMPUTE` statements an
extractor can see, each pointing at its source lines. LLM-written rule summaries come
later and are always marked as generated.

Two known traps: some `XCTL` targets come from data, not code (the main menu reads
them from copybook `COMEN02Y`), and many `EXEC CICS` statements span several lines.

### 4. Docs to chunks (thread 3, [ADR-0004](adr/0004-chunk-node-links.md))

1. **Chunk** by structure, not fixed size. A Confluence page splits at headings and a
   Jira ticket becomes one chunk for the description plus one per comment. Each
   chunk keeps its heading path and the document title, because "102" means nothing
   without "Reject reason codes" above it.
2. **Embed** each chunk locally with `all-MiniLM-L6-v2` (384 dimensions), run through
   ONNX Runtime. It's free, runs on a laptop CPU, needs no PyTorch, and downloads once
   (about 80 MB) from a public bucket.
3. **Link** each chunk to the code entities it talks about, as `MENTIONS` edges with a
   `method` and `confidence`:
   - `exact_name` (1.0): the text contains a known name such as `CBTRN02C`.
   - `alias` (0.8): the text contains a known nickname such as "the posting job".
     Aliases come from a small hand-kept file plus program comment headers.
   - `llm` (0.5 to 0.7): an LLM proposes links for chunks with no exact or alias hit.
     They're stored separately so their value can be measured.

This is the same idea as the chunk-to-node link table you use at work. The difference
is that here the link rows are edges in the graph, so one query can go from a job to
its programs to the documents that discuss them.

### 5. Retrieval and routing ([ADR-0005](adr/0005-graph-first-routing.md))

Every question goes through the same four steps:

```mermaid
flowchart TD
  Q[Question] --> R["1. Resolve entities<br/>exact names, aliases, fuzzy match"]
  R -->|found entities| G["2. Graph context<br/>1 to 2 hop neighbourhood"]
  G --> L["3. Linked chunks<br/>MENTIONS edges, ranked by confidence and similarity"]
  R -->|no entities| H["4. Hybrid search<br/>vector + full-text, fused with RRF"]
  L -->|too few or weak| H
  L --> A[Answer with citations]
  H --> A
```

- **Graph first.** If the question names a program, job, file or copybook, the graph
  gives exact facts (what calls what, which files a job touches) that vector search
  can only guess at.
- **Then linked chunks.** The graph says what the code does. The documents say why,
  what went wrong and what is planned. Only chunks linked to the resolved entities are
  candidates, so an unrelated page that happens to use similar words can't crowd out
  the right one.
- **Hybrid fallback.** Questions with no code entity, such as "what does S0C7 mean",
  go to vector search plus keyword search, merged with Reciprocal Rank Fusion.
- **Code wins conflicts.** When a document disagrees with the graph (the interest
  page says fees are computed, but the paragraph is an empty stub), the answer states
  what the code does and cites the document as out of date.

Every answer lists its evidence: node IDs with source lines and chunk IDs with titles.

### 6. Agents (thread 4)

Google ADK hosts a single router agent with four tools: `resolve_entities`,
`graph_query`, `linked_chunks` and `hybrid_search`. We build it twice, on purpose:

1. **Workflow version**: the four steps above run in fixed order as plain Python, and
   the LLM only writes the final answer. It's predictable and cheap.
2. **Agentic version**: the LLM decides which tools to call and when to stop.

The eval set decides which one wins, and the difference between them is one of the
main lessons of the project. `graph_query` starts as a set of named, parameterised
GQL templates (`callers_of`, `files_of_job`, `impact_of_copybook`). Free-form
text-to-GQL comes later as a stretch goal, because a template can't hallucinate a
label.

The model sits behind LiteLLM, which ADK supports directly, so one setting switches
between Gemini's free tier and a local Ollama model ([ADR-0006](adr/0006-models-and-cost.md)).

### 7. OKF knowledge layer ([ADR-0007](adr/0007-okf-knowledge-layer.md))

After the graph and chunks exist, a generator writes an Open Knowledge Format bundle:
one Markdown page per program, job, copybook and dataset, with YAML frontmatter, a
plain-language summary, and links to its neighbours. Agents can browse it starting
at `index.md`, people can read it on GitHub, and it is a fifth retrieval strategy to
compare in the eval.

### 8. Chat UI (thread 4)

The first UI is ADK's built-in dev web UI (`adk web`), which costs nothing and shows
every tool call. That makes it the best place to learn how the agent works. A small
custom chat page with an evidence panel (graph path plus cited chunks) follows once
the agent is stable.

### 9. Evaluation

`evals/questions.yaml` holds 16 seed questions, each tagged with the route that
should answer it best, the entities to resolve, checked answer facts and expected
sources. Retrieval is scored on entity recall and source recall, and answers on
whether they contain the facts. Each strategy is run on the same set: naive vector,
hybrid, graph only, graph-first with linked chunks, agentic, and OKF browse.

## Cost

Everything runs on your laptop for free: the Spanner emulator, local ONNX embeddings,
and either Ollama or Gemini's free tier. Nothing needs a Google Cloud project or a
credit card. The one limit is that the emulator keeps data in memory only, so
`make load` rebuilds the store from source in seconds after each restart.

## Where the code lives

```
src/legacylens/
  config.py          settings from environment variables
  store/             Spanner schema and connection helpers        (thread 1)
  ingest/code/       COBOL, copybook, JCL, BMS parsers           (thread 2)
  ingest/docs/       chunking, embedding, entity linking         (thread 3)
  retrieval/         graph templates, hybrid search, fusion      (threads 3-4)
  agents/            ADK router agent and tools                  (thread 4)
  okf/               OKF bundle generator                        (later)
corpus/              CardDemo lock file and synthetic documents
evals/               questions and scoring
docs/                this file, decision records, learning notes
```
