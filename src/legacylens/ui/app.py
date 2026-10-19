"""The chat page: a FastAPI app serving one HTML file and a small JSON API.

Run it with `make ui` and open http://localhost:8000. Each answer comes with its
evidence (route, entities, graph facts, document chunks), so you can check it.
"""

from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from legacylens.agents import llm, workflow_agent
from legacylens.okf.generate import page_path, read_page
from legacylens.retrieval import graph_queries as gq

STATIC = Path(__file__).parent / "static"
ROOT = Path(__file__).resolve().parents[3]

app = FastAPI(title="LegacyLens")


class Ask(BaseModel):
    question: str
    mode: str = "workflow"  # workflow | agentic


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/status")
def status():
    counts = {
        r["node_type"]: r["n"]
        for r in gq.run("SELECT node_type, COUNT(*) AS n FROM Node GROUP BY node_type")
    }
    return {
        "llm": llm.available(),
        "model": llm.model() if llm.available() else None,
        "small_model": llm.small_model(),
        "counts": counts,
    }


@app.get("/api/examples")
def examples():
    questions = yaml.safe_load((ROOT / "evals" / "questions.yaml").read_text())
    return [
        {"id": q["id"], "question": q["question"], "route": q["expected_route"]} for q in questions
    ]


@app.post("/api/ask")
def ask(body: Ask):
    question = body.question.strip()
    if not question:
        raise HTTPException(400, "Ask a question.")
    answer = workflow_agent.answer(question, use_llm=body.mode == "workflow")
    result = {
        "question": question,
        "mode": answer.mode,
        "strategy": "workflow",
        "text": answer.text,
        "model": answer.model,
        "model_reason": answer.model_reason,
        "route": answer.route,
        "retrieval": answer.retrieval,
        "tokens": answer.tokens,
        "trace": [],
    }
    if body.mode == "agentic":
        if not llm.available():
            result["text"] = (
                "_The agentic mode needs an LLM (set GEMINI_API_KEY). Here is the "
                "graph-first evidence instead._\n\n" + answer.text
            )
            return result
        from legacylens.agents import agentic_agent

        try:
            out = agentic_agent.ask(question)
            result.update(
                strategy="agentic", mode="llm", model=llm.model(), model_reason="agentic",
                text=out["text"] or "_The agent returned no text._", trace=out["trace"],
                tokens=out["tokens"],
            )  # fmt: skip
        except Exception as exc:
            result["text"] = f"_The agent failed ({type(exc).__name__})._\n\n" + answer.text
    return result


@app.get("/api/node/{node_id}")
def node(node_id: str):
    n = gq.node(node_id)
    if not n:
        raise HTTPException(404, f"No node {node_id}")
    owner = node_id
    if n["node_type"] in ("Paragraph", "BusinessRule"):  # these live on their program's page
        owner = f"PROGRAM:{n['name'].split('.')[0]}"
    page = page_path(owner) if read_page_exists(owner) else None
    return {"node": n, "edges": gq.neighbourhood(node_id)[:80], "page": page}


def read_page_exists(node_id: str) -> bool:
    try:
        return "error" not in read_page(page_path(node_id))
    except KeyError:
        return False


@app.get("/api/okf")
def okf(path: str = "index.md"):
    page = read_page(path)
    if "error" in page:
        raise HTTPException(404, page["error"])
    return page
