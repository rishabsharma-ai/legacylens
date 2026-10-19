"""Score retrieval strategies (and, with an LLM, answers) on evals/questions.yaml.

Usage: uv run python -m legacylens.evals [--answers]
Writes evals/results/<date>-retrieval.md and prints the same table.
"""

import argparse
import datetime as dt
import re
from pathlib import Path

import yaml

from legacylens.retrieval import search

ROOT = Path(__file__).resolve().parents[2]
QUESTIONS = ROOT / "evals" / "questions.yaml"
RESULTS = ROOT / "evals" / "results"


def questions() -> list[dict]:
    return yaml.safe_load(QUESTIONS.read_text())


def strategies(k: int = 6):
    return {
        "naive": lambda q: search.Retrieval(q, "docs", [], [], search.vector_search(q, k)),
        "hybrid": lambda q: search.Retrieval(q, "docs", [], [], search.hybrid_search(q, k)),
        "graph_first": lambda q: search.graph_first(q, k),
        "okf_browse": lambda q: okf_browse(q, k),
    }


FOLDER_TYPES = {"programs": "PROGRAM", "jobs": "JOB", "transactions": "TRANSACTION",
                "screens": "SCREEN", "copybooks": "COPYBOOK", "datasets": "DATASET"}  # fmt: skip


def okf_browse(question: str, k: int) -> search.Retrieval:
    """Answer from the OKF bundle alone: open each entity's page, follow its links.

    No vector index and no database queries after entity lookup, so questions that
    name no entity find nothing. That gap is the point of comparing it.
    """
    from legacylens.okf.generate import read_page

    entities = search.resolve_entities(question)
    facts, doc_ids = [], []
    for e in entities:
        kind, name = e["node_id"].split(":", 1)
        if kind in ("PARAGRAPH", "BUSINESSRULE"):  # these live on their program's page
            kind, name = "PROGRAM", name.split(".")[0]
        folder = next((f for f, t in FOLDER_TYPES.items() if t == kind), None)
        page = read_page(f"{folder}/{name}.md") if folder else {"error": "no page"}
        if "error" in page:
            continue
        links = re.findall(r"\]\(\.\./(\w+)/([^)]+)\.md\)", page["text"])
        edges = [{"src": e["node_id"], "edge": "LINK", "dst": f"{FOLDER_TYPES[f]}:{n}"}
                 for f, n in links if f in FOLDER_TYPES]  # fmt: skip
        facts.append({"node_id": e["node_id"], "edges": edges})
        doc_ids += re.findall(r"`((?:CONFLUENCE|JIRA):[A-Z0-9-]+)`", page["text"])
    hits = [search.Hit(d, d, "", "", "", 0.0, "okf") for d in list(dict.fromkeys(doc_ids))[:k]]
    route = "graph+docs" if hits else ("graph" if facts else "docs")
    return search.Retrieval(question, route, entities, facts, hits)


def recall(expected: list[str], got: list[str]) -> float | None:
    if not expected:
        return None
    return len(set(expected) & set(got)) / len(set(expected))


def score_retrieval(k: int = 6) -> dict:
    rows = {}
    for name, fn in strategies(k).items():
        per_q = []
        for q in questions():
            r = fn(q["question"])
            expected_route = {"conflict": "graph+docs"}.get(
                q["expected_route"], q["expected_route"]
            )
            per_q.append(
                {
                    "id": q["id"],
                    "route_expected": q["expected_route"],
                    "route": r.route,
                    "route_ok": r.route == expected_route
                    or (expected_route == "graph" and r.route == "graph+docs"),
                    "entity_recall": recall(q["entities"], found_entities(r)),
                    "source_recall": recall(q.get("sources", []), r.doc_ids),
                }
            )
        rows[name] = per_q
    return rows


def found_entities(r: search.Retrieval) -> list[str]:
    """Entities the question resolved to, plus their direct graph neighbours."""
    found = [e["node_id"] for e in r.entities]
    for fact in r.graph_facts:
        for edge in fact.get("edges", []):
            found += [edge["src"], edge["dst"]]
    return found


def mean(values) -> float | None:
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def fmt(v) -> str:
    return "–" if v is None else f"{v:.2f}"


def report(rows: dict) -> str:
    lines = [
        "| Strategy | Source recall (all) | Source recall (graph+docs, conflict) | "
        "Source recall (docs) | Entity recall | Route accuracy |",
        "|---|---|---|---|---|---|",
    ]
    for name, per_q in rows.items():

        def sr(routes, per_q=per_q):
            return mean(p["source_recall"] for p in per_q if p["route_expected"] in routes)

        has_entities = name in ("graph_first", "okf_browse")
        lines.append(
            "| {} | {} | {} | {} | {} | {} |".format(
                name,
                fmt(mean(p["source_recall"] for p in per_q)),
                fmt(sr({"graph+docs", "conflict"})),
                fmt(sr({"docs"})),
                fmt(mean(p["entity_recall"] for p in per_q)) if has_entities else "–",
                fmt(mean(1.0 if p["route_ok"] else 0.0 for p in per_q)) if has_entities else "–",
            )
        )
    lines += [
        "",
        "Per question (graph_first):",
        "",
        "| Question | Expected route | Route | Entity recall | Source recall |",
        "|---|---|---|---|---|",
    ]
    for p in rows["graph_first"]:
        lines.append(
            f"| {p['id']} | {p['route_expected']} | {p['route']} | "
            f"{fmt(p['entity_recall'])} | {fmt(p['source_recall'])} |"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--answers", action="store_true", help="also score LLM answers")
    parser.add_argument("-k", type=int, default=3, help="chunks per question (context budget)")
    args = parser.parse_args()
    text = "## Retrieval\n\n" + report(score_retrieval(args.k))
    if args.answers:
        from legacylens.agents.judge import answer_report

        text += "\n\n## Answers\n\n" + answer_report(questions())
    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / f"{dt.date.today().isoformat()}-eval.md"
    out.write_text(f"# Eval run {dt.date.today().isoformat()}\n\n{text}\n")
    print(text)
    print(f"\nWrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
