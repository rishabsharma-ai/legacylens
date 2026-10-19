"""Score answers against the answer_facts in evals/questions.yaml.

Two scores, because one of them must work with no LLM at all:
- key-term coverage: a fact counts as covered when most of its key terms (program,
  file and job names, numbers such as reason codes) appear in the answer. Cheap,
  deterministic, and blind to wording, so it can't tell a right claim from a wrong one.
- LLM judge: the model marks each fact present or absent. Better, but it needs a key.
LLM responses are cached by prompt hash in evals/.cache, so reruns are free.
"""

import json
import re

from legacylens.agents import llm, workflow_agent

JUDGE_RULES = """You grade answers. For each numbered fact, say whether the answer states
it (same meaning, any wording). Reply with JSON only: {"present": [true, false, ...]}."""


def key_terms(fact: str) -> set[str]:
    terms = set(re.findall(r"\b[A-Z][A-Z0-9-]{2,}\b|\b\d{2,}\b", fact))
    return {t for t in terms if t not in {"THE", "AND", "JCL", "CICS", "XCTL", "EXEC"}}


def coverage(answer: str, facts: list[str]) -> float | None:
    scored = [f for f in facts if key_terms(f)]
    if not scored:
        return None
    text = answer.upper()
    covered = 0
    for f in scored:
        terms = key_terms(f)
        if sum(t in text for t in terms) >= max(1, round(len(terms) * 0.67)):
            covered += 1
    return covered / len(scored)


def judged(answer: str, facts: list[str], question: str) -> float | None:
    if not facts or not llm.available():
        return None
    numbered = "\n".join(f"{i + 1}. {f}" for i, f in enumerate(facts))
    prompt = f"Question: {question}\n\nAnswer:\n{answer}\n\nFacts:\n{numbered}"
    try:
        out = llm.complete(JUDGE_RULES, prompt, cache=True)
        found = json.loads(re.search(r"\{.*\}", out["text"], re.S).group(0))["present"]
        return sum(bool(x) for x in found) / len(facts)
    except Exception:
        return None


def strategies() -> dict:
    def workflow(q):
        a = workflow_agent.answer(q, cache=True)
        return a.text, a.mode, a.tokens, 1 if a.mode == "llm" else 0

    out = {"workflow": workflow}
    if llm.available():
        from legacylens.agents import agentic_agent

        def agentic(q):
            res = agentic_agent.ask(q)
            calls = sum(1 for t in res["trace"] if "tool" in t)
            return res["text"], "llm", res["tokens"], calls + 1

        out["agentic"] = agentic
    return out


def answer_report(questions: list[dict]) -> str:
    def fmt(v):
        return "–" if v is None else f"{v:.2f}"

    def mean(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / len(xs) if xs else None

    lines = [
        "| Strategy | Mode | Key-term coverage | LLM judge | Tokens / question | "
        "Model+tool calls / question |",
        "|---|---|---|---|---|---|",
    ]
    for name, fn in strategies().items():
        rows = []
        for q in questions:
            text, mode, tokens, calls = fn(q["question"])
            facts = q.get("answer_facts", [])
            rows.append((coverage(text, facts), judged(text, facts, q["question"]), tokens, calls))
            last_mode = mode
        lines.append(
            f"| {name} | {last_mode} | {fmt(mean(r[0] for r in rows))} | "
            f"{fmt(mean(r[1] for r in rows))} | {fmt(mean(r[2] for r in rows))} | "
            f"{fmt(mean(r[3] for r in rows))} |"
        )
    if not llm.available():
        lines += ["", "No LLM configured, so answers are evidence-only and there is no judge."]
    return "\n".join(lines)
