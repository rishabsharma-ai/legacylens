# RAG patterns, and where each lives in LegacyLens

RAG (retrieval-augmented generation) means fetching relevant facts first, then asking
the LLM to answer from them. The patterns below differ in how they fetch. LegacyLens
builds all of them so the eval set can compare them on the same questions.

## 1. Naive RAG

Embed the question, find the k most similar chunks, and paste them into the prompt.

- **Good at**: "what does S0C7 mean", where the answer sits in one paragraph.
- **Bad at**: "which programs copy CVACT01Y". That answer is spread across 11 files
  and is never written down anywhere.
- **Here**: `hybrid_search` with the keyword half turned off.

## 2. Hybrid RAG

Run vector search and keyword search, then merge the two ranked lists. Reciprocal Rank
Fusion scores each chunk as the sum of 1 / (60 + rank) over the lists it appears in.

- **Why**: embeddings miss exact codes like `102` or `CBTRN02C`, and keywords miss
  paraphrases. Each covers the other's blind spot.
- **Here**: `Chunk.embedding` with `COSINE_DISTANCE`, plus `Chunk.text_tokens` with
  `SEARCH`, in the same database.

## 3. Graph RAG

Store entities and relationships as a graph, and answer from traversals.

- **Good at**: impact and dependency questions, like "what breaks if I change this
  copybook".
- **The catch**: the graph knows *what*, but rarely *why*.
- **Here**: `LegacyGraph`, queried with GQL templates.

## 4. Graph-linked RAG (graph-first)

Resolve the entities in the question, pull their graph neighbourhood, then pull only
the document chunks linked to those entities. This is the main design here and the
same idea as the chunk-node link table at work. See [ADR-0005](../adr/0005-graph-first-routing.md).

## 5. Agentic RAG

Give an LLM agent the retrieval tools and let it decide what to call, in what order,
and when it has enough. It is more flexible, but slower, costlier and less
predictable. Thread 4 builds it next to the fixed workflow version so the difference
can be measured.

## 6. OKF browse

Instead of retrieving raw chunks, the agent reads curated Markdown concept pages
generated from the graph, starting at `index.md` and following links. See
[ADR-0007](../adr/0007-okf-knowledge-layer.md).

## How they are compared

`evals/questions.yaml` tags every question with the route that should win. For each
strategy we measure:

- **Entity recall**: did it find the right code entities?
- **Source recall**: did it fetch the documents the answer needs?
- **Answer facts**: does the answer contain the checked facts?
- **Cost**: LLM calls and tokens per question.
