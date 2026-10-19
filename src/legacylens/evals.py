"""Score retrieval strategies (and, with an LLM, answers) on evals/questions.yaml.

Usage: uv run python -m legacylens.evals [--answers]
Writes evals/results/<date>-retrieval.md and prints the same table.
"""

import argparse
import datetime as dt
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
    }


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

        has_entities = name == "graph_first"
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
