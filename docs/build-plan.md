# Build plan: milestones 2 to 5

This is the work left for LegacyLens to answer questions end to end. It is written
for Claude Code to follow one milestone at a time. Read `CLAUDE.md`,
`docs/architecture.md` and the ADRs in `docs/adr/` first; this plan does not repeat
them.

## How to work through it

- Do one milestone per branch and pull request, in order. Each one builds on the last.
- At the start of each milestone, restate its goal and plan in two or three lines, then
  build. Stop and ask only at a real fork.
- Each milestone is done when its "Done when" list passes and `make lint test` is green.
- Explain each design choice in plain words in the PR description, because the owner
  is learning the stack. Record lasting choices with the `new-adr` skill.
- Keep loaders idempotent: running one twice gives the same database.
- Never use paid services. Gemini's free tier is the default LLM (ADR-0006).

---

## Milestone 2: Code to graph

**Goal:** load the CardDemo base app into `Node` and `Edge`.

**Scope:** `app/cbl`, `app/cpy`, `app/cpy-bms`, `app/jcl`, `app/bms`, `app/csd` under
`corpus/carddemo/`. Leave out the Db2, IMS and MQ subfolders for now.

### Build

1. `src/legacylens/ingest/code/model.py`: dataclasses `NodeRow` and `EdgeRow` that
   match the tables. Add a `node_id(type, name)` helper that applies the `TYPE:NAME`
   convention, with upper-case names.
2. `src/legacylens/ingest/code/cobol.py`: a line-based COBOL extractor. Handle the
   fixed format: columns 1 to 6 are a sequence area, column 7 is the indicator (`*`
   marks a comment), and columns 8 to 72 hold the code. Join continuation lines and
   multi-line `EXEC ... END-EXEC` blocks before matching. Extract:
   - `Program` from `PROGRAM-ID`, with `props.kind` set to `online` if the program
     has `EXEC CICS`, else `batch`. Take `summary` from the comment header's
     `Function :` line.
   - `Paragraph` nodes from PROCEDURE DIVISION labels, with start and end lines.
     Name them `PARAGRAPH:<PROGRAM>.<PARA>`.
   - Edges:
     - `HAS_PARAGRAPH` from a program to each of its paragraphs.
     - `PERFORMS` between paragraphs, including `PERFORM ... THRU`.
     - `INCLUDES` for `COPY x`, from the program to `COPYBOOK:X`.
     - `CALLS` for `CALL 'X'`.
     - `XCTL` and `LINK` for `EXEC CICS XCTL|LINK PROGRAM('X')`, when the target is a
       literal.
   - Files:
     - Batch: map `SELECT f ASSIGN TO DD`, record the DD name in `props.dd`, and use
       the `OPEN` mode for `READS` (INPUT), `WRITES` (OUTPUT, EXTEND) or both (I-O).
     - CICS: `READ`, `READNEXT` and `STARTBR` mean `READS`; `WRITE`, `REWRITE` and
       `DELETE` mean `WRITES`. The `DATASET` or `FILE` value may be a literal or a
       `VALUE` clause of a working-storage variable, so resolve simple
       `05 WS-X PIC X(8) VALUE 'NAME'.` cases.
   - `USES_SCREEN` from `SEND MAP` and `RECEIVE MAP` with `MAPSET('X')`.
3. `src/legacylens/ingest/code/copybook.py`: `Copybook` nodes, plus `INCLUDES`
   edges for any nested `COPY`.
4. `src/legacylens/ingest/code/jcl.py`: a `Job` node per member. For each
   `EXEC PGM=X` step, add `RUNS` with `props.step`. For each `DD DSN=` in that step,
   add `Dataset` nodes and `READS` or `WRITES` from `DISP`: `SHR` and `OLD` mean
   reads, `NEW` and `MOD` mean writes. A dataset is named by the distinctive part of
   its DSN: drop `AWS.M2.CARDDEMO.` and the type suffixes `.VSAM.KSDS`, `.PS`,
   `.AIX.PATH` and the GDG `(+1)`. Put the full DSN in `props.dsn` and mark GDGs. Skip
   utility programs (`IDCAMS`, `SORT`, `IEFBR14`, `IEBGENER`) as `RUNS` targets, but
   keep them in `Job.props.utility_steps`. Handle `EXEC PROC=X` by recording it in
   props.
5. `src/legacylens/ingest/code/csd.py`: `Transaction` nodes, with `STARTS` edges from
   `DEFINE TRANSACTION(x) PROGRAM(y)`.
6. `src/legacylens/ingest/code/bms.py`: `Screen` nodes from `DFHMSD` mapset names.
7. Batch-to-JCL file join: when a job step runs program P and P's `SELECT` uses DD
   `D`, add the edge `P -READS/WRITES-> Dataset` using that step's DD-to-DSN mapping.
   Keep the job-level edges too.
8. `src/legacylens/ingest/code/load.py`, run as `python -m legacylens.ingest.code.load`:
   - parse everything
   - check each node type is one of Program, Paragraph, Copybook, Dataset, Job,
     Transaction, Screen
   - create placeholder nodes (`props.unresolved = true`) for edge targets that weren't
     parsed, such as IBM copybooks like `DFHAID`
   - write nodes, then edges, with `insert_or_update`
   - print counts per type
9. Add a `make load-code` target.
10. Business rules (keep it small): add `BusinessRule` nodes for the reject reason
    codes in CBTRN02C (`MOVE 1nn TO WS-VALIDATION-FAIL-REASON` with the description on
    the next lines) and for `COMPUTE` statements in CBACT04C. Each one gets a
    `DEFINES_RULE` edge from its paragraph and its source lines in props.

### Tests

- Unit tests on small inline COBOL and JCL snippets, one per extractor rule.
- An integration test (emulator) that loads the real corpus and checks:
  - `JOB:POSTTRAN -RUNS{step: STEP15}-> PROGRAM:CBTRN02C`
  - `PROGRAM:CBSTM03A -CALLS-> PROGRAM:CBSTM03B`
  - `PROGRAM:COSGN00C -XCTL->` both `COADM01C` and `COMEN01C`
  - `PROGRAM:CBTRN02C -READS-> DATASET:CARDXREF`
  - the 13 programs that include `COPYBOOK:CVACT01Y` (the list is in `evals/questions.yaml` q06)
  - `PARAGRAPH:CBACT04C.1400-COMPUTE-FEES` exists
- Add `src/legacylens/retrieval/graph_queries.py` with named GQL templates, so the
  graph-only eval questions can be checked:
  - `jobs_running(program)`
  - `files_of(program)`
  - `callers_of(program)`
  - `callees_of(program)`
  - `programs_including(copybook)`
  - `neighbourhood(node_id, hops=1)`

### Done when

- Eval questions q01, q06 and q14 are answered correctly by templates alone, in a test.
- The PR explains the parser's known blind spots, such as data-driven XCTL in COMEN01C.

---

## Milestone 3: Docs to chunks, linking and retrieval

**Goal:** fill `Document` and `Chunk`, create `MENTIONS` edges, and score retrieval
strategies on the eval set.

### Build

1. `ingest/docs/chunk.py`:
   - Confluence pages: split at `##` headings, keeping the page title and heading path
     as `Chunk.heading`. Keep a table whole within its section.
   - Jira tickets: one chunk for summary plus description, then one per comment, each
     prefixed with the key and summary.
   - Target 100 to 400 tokens; split longer sections at paragraph breaks.
   - IDs follow `CHUNK:<doc_id>#<n>`.
2. `ingest/docs/embed.py`: use `all-MiniLM-L6-v2` through ONNX Runtime (384
   dimensions). Embed the heading and text together. Cache vectors in
   `.cache/embeddings/` keyed by text hash, so reloads are instant.
3. `corpus/aliases.yaml`: hand-kept nicknames to node IDs, for example "posting job",
   "the posting program", "interest job", "sign-on screen", "main menu", "bill
   payment", "statement job", "nightly batch". Add a corpus test that every alias
   target exists in the graph.
4. `ingest/docs/link.py`: create `MENTIONS` edges, per ADR-0004:
   - pass 1, `exact_name`: a whole-word match against every non-placeholder node
     name. Skip paragraph names shorter than 8 characters.
   - pass 2, `alias`, using `aliases.yaml`.
   - pass 3, `llm`: off by default behind a flag, for chunks with no hits. Give the
     LLM the top 20 candidate nodes by name similarity and accept only IDs from that
     list.
   Store `method`, `confidence` and `surface` in `props`.
5. `ingest/docs/load.py` and a `make load-docs` target. Add `make load`, which runs
   `db`, `load-code` and `load-docs`.
6. `retrieval/`:
   - `vector_search(q, k)` with `COSINE_DISTANCE`
   - `keyword_search(q, k)` with `SEARCH` and `SCORE`
   - `hybrid_search(q, k)` with RRF, `1/(60+rank)`
   - `resolve_entities(q)`: exact names, then aliases, then fuzzy matching with
     `difflib`, returning node IDs and the matched text
   - `linked_chunks(node_ids, q, k)`: the `MENTIONS` neighbours, ranked by confidence
     then cosine similarity
   - `graph_first(q)`: the full ADR-0005 flow, returning `{route, entities,
     graph_facts, chunks}`
7. `evals/run.py`, run with `make eval`: run each strategy over
   `evals/questions.yaml`. Score entity recall, source recall (expected `sources`
   found among the retrieved chunks' docs) and route accuracy. Print a table and write
   `evals/results/<date>-retrieval.md`. Strategies: `naive` (vector only), `hybrid`,
   `graph_only`, and `graph_first`.

### Done when

- `graph_first` beats `naive` on source recall for the graph+docs questions, with the
  numbers in the PR.
- q05 (conflict) retrieves both CONFLUENCE:2004 and JIRA:CARD-102.
- q09, q10 and q15 route to hybrid search, not to the graph.

---

## Milestone 4: Agents and chat

**Goal:** answer questions in a chat UI, with cited evidence.

### Build

1. Add `google-adk` and `litellm`. Read the model from `LLM_MODEL` in `.env`, with
   the default `gemini/gemini-flash-latest` and `GEMINI_API_KEY` from Google AI
   Studio. The owner has to create that free key; ask for it when needed.
2. `agents/tools.py`: wrap `resolve_entities`, the graph templates, `linked_chunks`
   and `hybrid_search` as ADK function tools. Give them clear docstrings, since the
   LLM reads those. Every result includes node IDs, source paths and lines, or chunk
   IDs with titles.
3. `agents/workflow_agent.py`, the workflow version: run `graph_first(q)` in code,
   then one LLM call that writes the answer from labelled sections (GRAPH FACTS,
   DOCUMENTS). The instructions say code beats documents, to cite every claim, and to
   say "not found" rather than guess.
4. `agents/agentic_agent.py`, the agentic version: one `LlmAgent` with the tools,
   which decides what to call. It has the same answer rules.
5. Set `root_agent` so `adk web` serves it from `src/legacylens/agents/`. Add
   `make chat`, which runs `adk web`.
6. Extend `evals/run.py` with answer scoring. An LLM judge checks each `answer_facts`
   item as present or absent. Cache LLM responses by prompt hash so reruns are free.
   Add the `workflow` and `agentic` strategies, plus calls and tokens per question.

### Done when

- `make chat` opens ADK's web UI, and q03 and q05 are answered correctly with
  citations. Put screenshots or transcripts in the PR.
- The eval table compares workflow and agentic on answer facts and cost.

---

## Milestone 5: OKF layer

**Goal:** generate an Open Knowledge Format bundle from the graph (ADR-0007).

1. First, recheck the OKF spec (v0.1, Google Cloud, June 2026) for any changes.
2. `okf/generate.py`, with `make okf`: write `knowledge/`:
   - `index.md`
   - one page each under `programs/`, `jobs/`, `copybooks/`, `datasets/`, `screens/`
   - frontmatter with `type`, `title`, `description`, `resource` (the source path)
     and `tags`
   - a body with graph facts as lists of Markdown links to other concepts, linked
     documents, and an optional LLM summary under a "Generated summary" heading
   The output must be deterministic, so the git diff stays clean.
3. An agent tool `read_concept(path)`, and an `okf_browse` eval strategy.

### Done when

- `knowledge/` is committed, renders on GitHub, and every internal link resolves.
  Add a test for the links.
- OKF browse is in the eval table.

---

## Later (milestone 6, not needed for end-to-end Q&A)

- The Db2, IMS and MQ parts of CardDemo.
- A RouteLLM experiment.
- A custom chat page with an evidence panel.
