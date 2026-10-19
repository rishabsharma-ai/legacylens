"""The workflow agent: retrieval runs as fixed code, then one LLM call writes the answer.

This is the predictable version (ADR-0005). graph_first() decides the route and
gathers evidence; the model only turns labelled evidence into prose with citations.
Without a model, evidence_answer() writes a plain summary of the same evidence.
"""

import json
from dataclasses import asdict, dataclass, field

from legacylens.agents import llm
from legacylens.retrieval import search

ANSWER_RULES = """You answer questions about the AWS CardDemo mainframe application.
Rules:
- Use only the evidence given. If it doesn't answer the question, say "Not found in the
  code or documents" and say what is missing. Never guess.
- Code beats documents. GRAPH FACTS come from the parsed COBOL and JCL. If a document
  disagrees with them, give the code's answer and say the document is out of date.
- Cite every claim: node IDs in backticks for code facts, like `PROGRAM:CBTRN02C`
  (with source path and lines when you have them), and [doc_id] for documents, like
  [CONFLUENCE:2003] or [JIRA:CARD-102].
- Be short: a direct answer first, then the supporting points as a list."""

OUT_LABELS = {
    "RUNS": "Runs",
    "STARTS": "Starts",
    "CALLS": "Calls",
    "XCTL": "Transfers control to (XCTL)",
    "LINK": "Links to",
    "READS": "Reads",
    "WRITES": "Writes",
    "INCLUDES": "Includes copybook",
    "USES_SCREEN": "Uses screen",
    "DEFINES_RULE": "Defines rule",
}
IN_LABELS = {
    "RUNS": "Run by job",
    "STARTS": "Started by transaction",
    "CALLS": "Called by",
    "XCTL": "Reached by XCTL from",
    "LINK": "Linked from",
    "READS": "Read by",
    "WRITES": "Written by",
    "INCLUDES": "Included by",
    "USES_SCREEN": "Screen of",
    "DEFINES_RULE": "Defined in",
}


@dataclass
class Answer:
    question: str
    text: str
    mode: str  # llm | evidence
    model: str | None
    model_reason: str | None
    route: str
    retrieval: dict
    tokens: int | None = None
    trace: list[dict] = field(default_factory=list)


def short(node_id: str) -> str:
    return node_id.split(":", 1)[-1]


def relationships(fact: dict) -> dict[str, list[str]]:
    """The fact's edges grouped into readable labels, like {"Reads": [...]}."""
    groups: dict[str, list[str]] = {}
    for e in fact["edges"]:
        if e["src"] == fact["node_id"]:
            label, other = OUT_LABELS.get(e["edge"], e["edge"]), e["dst"]
        else:
            label, other = IN_LABELS.get(e["edge"], e["edge"]), e["src"]
        if other not in groups.setdefault(label, []):
            groups[label].append(other)
    return groups


def context(r: search.Retrieval) -> str:
    """The evidence as labelled sections, the only thing the model sees."""
    parts = ["GRAPH FACTS (from the code):"]
    if not r.graph_facts:
        parts.append("(none: the question names no known program, job, file or copybook)")
    for f in r.graph_facts:
        lines = f"{f['source']}:{f['lines'][0]}-{f['lines'][1]}" if f["source"] else "no source"
        parts.append(f"\n`{f['node_id']}` ({f['type']}, {lines})")
        if f["summary"]:
            parts.append(f"  Summary: {f['summary']}")
        for label, others in relationships(f).items():
            parts.append(f"  {label}: {', '.join(short(o) for o in others[:25])}")
        for rule in f.get("rules", [])[:15]:
            parts.append(
                f"  Rule in {short(rule['paragraph'])} line {rule['line']}: {rule['rule']}"
            )
        if f.get("code"):
            parts.append("  Code:\n" + f["code"])
    parts.append("\nDOCUMENTS (synthetic Confluence and Jira; may be out of date):")
    if not r.chunks:
        parts.append("(none)")
    for h in r.chunks:
        parts.append(f"\n[{h.doc_id}] {h.heading}\n{h.text}")
    return "\n".join(parts)


def evidence_answer(r: search.Retrieval) -> str:
    """A readable answer built from the evidence alone, for when no LLM is configured."""
    out = []
    if not r.graph_facts and not r.chunks:
        return "Not found in the code or documents."
    for f in r.graph_facts:
        head = f"**`{f['node_id']}`**"
        if f["summary"]:
            head += f": {f['summary']}"
        if f["source"]:
            head += f" (`{f['source']}` lines {f['lines'][0]}-{f['lines'][1]})"
        out.append(head)
        for label, others in relationships(f).items():
            names = ", ".join(short(o) for o in others[:12])
            more = f" and {len(others) - 12} more" if len(others) > 12 else ""
            out.append(f"- {label}: {names}{more}")
        for rule in f.get("rules", [])[:8]:
            out.append(f"- Rule ({short(rule['paragraph'])}, line {rule['line']}): {rule['rule']}")
        if f.get("code"):
            out.append(f"```cobol\n{f['code']}\n```")
        out.append("")
    if r.chunks:
        out.append("**From the documents** (code wins if they disagree):")
        for h in r.chunks[:4]:
            first = " ".join(h.text.split())[:240]
            out.append(f"- [{h.doc_id}] *{h.heading}*: {first}…")
    return "\n".join(out).strip()


def retrieval_dict(r: search.Retrieval) -> dict:
    d = asdict(r)
    d["doc_ids"] = r.doc_ids
    for f in d["graph_facts"]:
        if isinstance(f.get("props"), str):
            f["props"] = json.loads(f["props"])
    return d


def answer(question: str, k: int = 4, use_llm: bool = True, cache: bool = False) -> Answer:
    r = search.graph_first(question, k)
    name, reason = llm.choose_model(r.route, len(r.graph_facts), len(r.chunks))
    if use_llm and llm.available(name):
        prompt = f"Question: {question}\n\n{context(r)}"
        try:
            out = llm.complete(ANSWER_RULES, prompt, name, cache=cache)
            return Answer(
                question,
                out["text"],
                "llm",
                name,
                reason,
                r.route,
                retrieval_dict(r),
                out["tokens"],
            )
        except Exception as exc:  # rate limit or network: still show the evidence
            text = f"_The model call failed ({type(exc).__name__}); showing the evidence._\n\n"
            return Answer(
                question, text + evidence_answer(r), "evidence", None, None, r.route,
                retrieval_dict(r),
            )  # fmt: skip
    return Answer(question, evidence_answer(r), "evidence", None, None, r.route, retrieval_dict(r))
