"""Retrieval over the knowledge store: vector, keyword, hybrid and graph-first.

graph_first() is the main strategy (ADR-0005): resolve the code entities a question
names, collect their graph facts, pull the document chunks linked to them, and fall
back to hybrid search when the question names no entity or the links are thin.
"""

import difflib
import re
from dataclasses import dataclass, field

from google.cloud.spanner_v1 import param_types

from legacylens.ingest.docs.embed import embed_one
from legacylens.ingest.docs.link import EntityMatcher, load_aliases
from legacylens.retrieval import graph_queries as gq

STOPWORDS = set(
    """a an and are as at be by can do does for from has have how i if in is it
its me my of on or so that the their them then there this to was what when where which who
why will with would you your about after any into job program file""".split()
)
RRF_K = 60


@dataclass
class Hit:
    chunk_id: str
    doc_id: str
    title: str
    heading: str
    text: str
    score: float
    via: str  # vector | keyword | hybrid | linked
    linked_to: list[str] = field(default_factory=list)


@dataclass
class Retrieval:
    question: str
    route: str  # graph | graph+docs | docs
    entities: list[dict]
    graph_facts: list[dict]
    chunks: list[Hit]

    @property
    def doc_ids(self) -> list[str]:
        return list(dict.fromkeys(h.doc_id for h in self.chunks))


def _chunk_sql(where: str, order: str, limit: int) -> str:
    return f"""
        SELECT c.chunk_id, c.doc_id, d.title, c.heading, c.text, {order} AS score
        FROM Chunk c JOIN Document d ON d.doc_id = c.doc_id
        WHERE {where} ORDER BY score {"ASC" if "DISTANCE" in order else "DESC"} LIMIT {limit}"""


def _rows(sql: str, params: dict, types: dict, db) -> list[dict]:
    db = db or gq.database()
    with db.snapshot() as snap:
        result = snap.execute_sql(sql, params=params, param_types=types)
        rows = list(result)
        names = [f.name for f in result.fields]
    return [dict(zip(names, r, strict=True)) for r in rows]


def vector_search(question: str, k: int = 5, db=None, only: list[str] | None = None) -> list[Hit]:
    where = "c.chunk_id IN UNNEST(@only)" if only is not None else "TRUE"
    params = {"q": embed_one(question)}
    types = {"q": param_types.Array(param_types.FLOAT32)}
    if only is not None:
        params["only"], types["only"] = only, param_types.Array(param_types.STRING)
    rows = _rows(_chunk_sql(where, "COSINE_DISTANCE(c.embedding, @q)", k), params, types, db)
    return [
        Hit(
            r["chunk_id"],
            r["doc_id"],
            r["title"],
            r["heading"],
            r["text"],
            1 - r["score"],
            "vector",
        )
        for r in rows
    ]


def keyword_query(question: str) -> str:
    words = [
        w
        for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9-]*", question)
        if w.lower() not in STOPWORDS and len(w) > 1
    ]
    return " OR ".join(dict.fromkeys(words))


def keyword_search(question: str, k: int = 5, db=None) -> list[Hit]:
    q = keyword_query(question)
    if not q:
        return []
    sql = _chunk_sql("SEARCH(c.text_tokens, @q)", "SCORE(c.text_tokens, @q)", k)
    rows = _rows(sql, {"q": q}, {"q": param_types.STRING}, db)
    return [
        Hit(r["chunk_id"], r["doc_id"], r["title"], r["heading"], r["text"], r["score"], "keyword")
        for r in rows
    ]


def hybrid_search(question: str, k: int = 5, db=None) -> list[Hit]:
    """Reciprocal Rank Fusion: each list votes 1 / (60 + rank) for each chunk it found."""
    lists = [vector_search(question, k * 2, db), keyword_search(question, k * 2, db)]
    scores: dict[str, float] = {}
    hits: dict[str, Hit] = {}
    for results in lists:
        for rank, hit in enumerate(results, start=1):
            scores[hit.chunk_id] = scores.get(hit.chunk_id, 0) + 1 / (RRF_K + rank)
            hits.setdefault(hit.chunk_id, hit)
    ranked = sorted(scores, key=scores.get, reverse=True)[:k]
    return [_with(hits[c], score=scores[c], via="hybrid") for c in ranked]


def _with(hit: Hit, **changes) -> Hit:
    return Hit(**{**hit.__dict__, **changes})


_matchers: dict[int, EntityMatcher] = {}


def matcher(db=None) -> EntityMatcher:
    key = id(db)
    if key not in _matchers:
        rows = gq.run(
            "SELECT node_id, node_type, name FROM Node WHERE node_type != 'Chunk' "
            "AND JSON_VALUE(props, '$.unresolved') IS NULL",
            db=db,
        )
        _matchers[key] = EntityMatcher(
            [(r["node_id"], r["node_type"], r["name"]) for r in rows], load_aliases()
        )
    return _matchers[key]


def resolve_entities(question: str, db=None) -> list[dict]:
    """Code entities a question names: exact names, then aliases, then near-miss names."""
    m = matcher(db)
    found = [
        {"node_id": x.node_id, "method": x.method, "surface": x.surface}
        for x in m.find(question.upper())
        if x.method == "exact_name"
    ]
    found += [
        {"node_id": x.node_id, "method": x.method, "surface": x.surface}
        for x in m.find(question)
        if x.method == "alias"
    ]
    if not found:  # typos such as CBTRN2C
        names = m.names()
        for token in re.findall(r"[A-Z0-9][A-Z0-9-]{4,}", question.upper()):
            for close in difflib.get_close_matches(token, names, n=1, cutoff=0.85):
                found += [
                    {"node_id": nid, "method": "fuzzy", "surface": token}
                    for nid in m.by_name[close]
                ]
    seen, out = set(), []
    for f in found:
        if f["node_id"] not in seen:
            seen.add(f["node_id"])
            out.append(f)
    return out


def graph_facts(node_ids: list[str], db=None) -> list[dict]:
    """A compact description of each entity and its direct relationships."""
    facts = []
    for nid in node_ids:
        node = gq.node(nid, db)
        if not node:
            continue
        fact = {
            "node_id": nid,
            "type": node["node_type"],
            "name": node["name"],
            "summary": node["summary"],
            "source": node["source_path"],
            "lines": [node["start_line"], node["end_line"]],
            "edges": gq.neighbourhood(nid, db)[:60],
        }
        if node["node_type"] == "Program":
            fact["rules"] = gq.rules_of(node["name"], db)
            fact["props"] = node["props"]
        if node["node_type"] == "Paragraph":
            fact["code"] = source_excerpt(node["source_path"], node["start_line"], node["end_line"])
        facts.append(fact)
    return facts


def source_excerpt(path: str | None, start: int | None, end: int | None, limit: int = 40) -> str:
    from legacylens.ingest.code.build import ROOT

    if not path or not start:
        return ""
    file = ROOT / "corpus" / "carddemo" / path
    if not file.exists():
        return ""
    lines = file.read_text(errors="replace").splitlines()[
        start - 1 : min(end or start, start + limit)
    ]
    return "\n".join(f"{start + i:5} {ln[6:72].rstrip()}" for i, ln in enumerate(lines))


def linked_chunks(node_ids: list[str], question: str, k: int = 6, db=None) -> list[Hit]:
    """Chunks with MENTIONS edges to the entities, ranked by link strength then similarity."""
    if not node_ids:
        return []
    rows = gq.run(
        """
        SELECT src_id AS chunk_id, ARRAY_AGG(dst_id) AS targets,
               MAX(FLOAT64(props.confidence)) AS confidence
        FROM Edge WHERE edge_type = 'MENTIONS' AND dst_id IN UNNEST(@ids)
        GROUP BY src_id""".replace("@ids", "[" + ",".join(f"'{n}'" for n in node_ids) + "]"),
        db=db,
    )
    if not rows:
        return []
    by_chunk = {r["chunk_id"]: r for r in rows}
    sims = {h.chunk_id: h for h in vector_search(question, len(rows), db, only=list(by_chunk))}
    ranked = []
    for cid, r in by_chunk.items():
        hit = sims.get(cid)
        if not hit:
            continue
        # entities covered and link confidence first, then semantic similarity
        score = 0.5 * len(r["targets"]) / len(node_ids) + 0.2 * r["confidence"] + hit.score
        ranked.append(_with(hit, score=score, via="linked", linked_to=list(r["targets"])))
    ranked.sort(key=lambda h: h.score, reverse=True)
    return ranked[:k]


def graph_first(question: str, k: int = 6, db=None, min_similarity: float = 0.25) -> Retrieval:
    entities = resolve_entities(question, db)
    ids = [e["node_id"] for e in entities]
    if not ids:
        return Retrieval(question, "docs", [], [], hybrid_search(question, k, db))
    facts = graph_facts(ids[:6], db)
    linked = [h for h in linked_chunks(ids, question, k, db) if h.score - 0.2 >= min_similarity]
    chunks = linked
    if len(linked) < 2:  # thin links: top up with hybrid search
        extra = [
            h
            for h in hybrid_search(question, k, db)
            if h.chunk_id not in {c.chunk_id for c in linked}
        ]
        chunks = linked + extra[: k - len(linked)]
    return Retrieval(question, "graph+docs" if linked else "graph", entities, facts, chunks)
