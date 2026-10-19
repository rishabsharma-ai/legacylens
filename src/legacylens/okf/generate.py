"""Write the knowledge graph out as an Open Knowledge Format (OKF v0.1) bundle (ADR-0007).

An OKF bundle is a folder of Markdown files with YAML frontmatter, one per concept,
linked with ordinary Markdown links. Agents (and people) start at index.md and follow
links. Every fact here comes from a graph query, never from an LLM, and the output is
sorted so a rerun on the same graph gives a clean git diff.

Usage: uv run python -m legacylens.okf.generate   (or: make okf)
"""

import json
import shutil
from collections import defaultdict
from pathlib import Path

import yaml

from legacylens.retrieval import graph_queries as gq

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "knowledge"
LOCK = dict(
    line.split("=", 1)
    for line in (ROOT / "corpus" / "carddemo.lock").read_text().splitlines()
    if "=" in line and not line.startswith("#")
)
SOURCE_URL = LOCK["repo"].removesuffix(".git") + "/blob/" + LOCK["commit"] + "/"

FOLDERS = {
    "Program": "programs",
    "Job": "jobs",
    "Transaction": "transactions",
    "Screen": "screens",
    "Copybook": "copybooks",
    "Dataset": "datasets",
}
OUT_LABELS = {
    "RUNS": "Runs",
    "STARTS": "Starts",
    "CALLS": "Calls",
    "XCTL": "Transfers control to (XCTL)",
    "LINK": "Links to",
    "READS": "Reads",
    "WRITES": "Writes",
    "INCLUDES": "Includes",
    "USES_SCREEN": "Uses screen",
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
    "USES_SCREEN": "Used by",
}
INTRO = {
    "Program": "COBOL programs. Online ones run under CICS; batch ones run from JCL jobs.",
    "Job": "JCL jobs: the batch schedule's units of work, each a list of steps.",
    "Transaction": "CICS transaction IDs: the four-letter codes a user types to start a program.",
    "Screen": "BMS mapsets: the 3270 screens online programs send and receive.",
    "Copybook": "Copybooks: shared record layouts and constants that programs COPY in.",
    "Dataset": "Data stores: VSAM files, sequential files and GDGs, Db2 tables, IMS "
    "segments and MQ queues.",
}


def page_path(node_id: str) -> str:
    kind, name = node_id.split(":", 1)
    folder = {k.upper(): v for k, v in FOLDERS.items()}[kind]
    return f"{folder}/{name}.md"


def load(db=None) -> dict:
    nodes = gq.run(
        "SELECT node_id, node_type, name, source_path, start_line, end_line, summary, "
        "TO_JSON_STRING(props) AS props FROM Node WHERE node_type != 'Chunk'",
        db=db,
    )
    for n in nodes:
        n["props"] = json.loads(n["props"] or "{}")
    edges = gq.run(
        "SELECT src_id, edge_type, dst_id, TO_JSON_STRING(props) AS props FROM Edge", db=db
    )
    for e in edges:
        e["props"] = json.loads(e["props"] or "{}")
    docs = gq.run("SELECT doc_id, title, url FROM Document", db=db)
    return {"nodes": {n["node_id"]: n for n in nodes}, "edges": edges, "docs": docs}


def has_page(node: dict | None) -> bool:
    if not node or node["node_type"] not in FOLDERS:
        return False
    p = node["props"]
    return not (p.get("unresolved") or p.get("external") or p.get("system"))


def link(node_id: str, nodes: dict) -> str:
    name = node_id.split(":", 1)[1]
    if has_page(nodes.get(node_id)):
        return f"[{name}](../{page_path(node_id)})"
    return f"`{name}`"  # external or system names, such as CEE3ABD or DFHAID


def doc_link(doc: dict) -> str:
    if doc["url"].startswith("jira/"):
        target = "../../corpus/docs/jira/tickets.jsonl"
    else:
        target = f"../../corpus/docs/{doc['url']}"
    return f"[{doc['title']}]({target}) (`{doc['doc_id']}`)"


def frontmatter(meta: dict) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n"


def build_pages(data: dict) -> dict[str, str]:
    nodes, edges = data["nodes"], data["edges"]
    docs = {d["doc_id"]: d for d in data["docs"]}
    out_edges, in_edges = defaultdict(list), defaultdict(list)
    for e in edges:
        out_edges[e["src_id"]].append(e)
        in_edges[e["dst_id"]].append(e)

    def owner(node_id: str) -> str:
        """Roll paragraph and rule mentions up to their program."""
        n = nodes.get(node_id)
        if n and n["node_type"] in ("Paragraph", "BusinessRule"):
            return f"PROGRAM:{n['props'].get('program') or n['name'].split('.')[0]}"
        return node_id

    mentions = defaultdict(set)
    for e in edges:
        if e["edge_type"] == "MENTIONS":
            doc_id = e["src_id"].removeprefix("CHUNK:").split("#")[0]
            mentions[owner(e["dst_id"])].add(doc_id)

    for nid, n in nodes.items():  # jobs have no header comment; say what they run
        if n["node_type"] == "Job" and not n["summary"]:
            runs = sorted(
                e["dst_id"].split(":", 1)[1] for e in out_edges[nid] if e["edge_type"] == "RUNS"
            )
            n["summary"] = (
                f"Batch job that runs {', '.join(runs)}." if runs else "Batch job (utilities only)."
            )

    pages = {}
    by_type = defaultdict(list)
    for nid in sorted(nodes):
        n = nodes[nid]
        if not has_page(n):
            continue
        by_type[n["node_type"]].append(n)
        pages[page_path(nid)] = concept_page(n, nodes, out_edges, in_edges, mentions, docs)

    for kind, folder in FOLDERS.items():
        rows = [f"- [{n['name']}]({n['name']}.md): {describe(n)}" for n in by_type[kind]]
        pages[f"{folder}/index.md"] = (
            frontmatter(
                {
                    "type": "index",
                    "title": folder.title(),
                    "description": INTRO[kind],
                }
            )
            + f"\n# {folder.title()}\n\n{INTRO[kind]}\n\n"
            + "\n".join(rows)
            + "\n"
        )
    pages["index.md"] = index_page(by_type)
    return pages


def describe(n: dict) -> str:
    p = n["props"]
    if n["summary"]:
        return n["summary"]
    if n["node_type"] == "Dataset":
        return {
            "db2_table": "Db2 table.",
            "ims_segment": "IMS database segment.",
            "mq_queue": "MQ queue.",
        }.get(p.get("kind"), f"Dataset `{p['dsn']}`." if p.get("dsn") else "Dataset.")
    if n["node_type"] == "Copybook":
        return "BMS symbolic map." if p.get("kind") == "bms_symbolic_map" else "Record layout."
    return f"{n['node_type']} {n['name']}."


def concept_page(n, nodes, out_edges, in_edges, mentions, docs) -> str:
    nid, p = n["node_id"], n["props"]
    tags = sorted({t for t in (p.get("app"), p.get("kind"), n["node_type"].lower()) if t})
    meta = {
        "type": n["node_type"].lower(),
        "title": n["name"],
        "description": describe(n),
        "tags": tags,
    }
    if n["source_path"]:
        meta["resource"] = SOURCE_URL + n["source_path"]
    body = [f"# {n['name']}", "", describe(n), ""]
    if n["source_path"]:
        lines = f" lines {n['start_line']}-{n['end_line']}" if n["end_line"] else ""
        body += [f"Source: [{n['source_path']}]({meta['resource']}){lines}", ""]

    groups = defaultdict(set)
    for e in out_edges[nid]:
        if e["edge_type"] in OUT_LABELS:
            groups[OUT_LABELS[e["edge_type"]]].add(e["dst_id"])
    for e in in_edges[nid]:
        if e["edge_type"] in IN_LABELS:
            groups[IN_LABELS[e["edge_type"]]].add(e["src_id"])
    if groups:
        body += ["## Relationships", ""]
        for label in sorted(groups):
            items = ", ".join(link(x, nodes) for x in sorted(groups[label]))
            body.append(f"- {label}: {items}")
        body.append("")

    if n["node_type"] == "Job":
        steps = sorted(
            (s, e["dst_id"]) for e in out_edges[nid] if e["edge_type"] == "RUNS"
            for s in e["props"].get("steps", [])
        )  # fmt: skip
        if steps:
            body += ["## Steps", ""] + [f"- `{s}` runs {link(d, nodes)}" for s, d in steps]
            body.append("")
        if p.get("utility_steps"):
            body += [f"Utility steps (IDCAMS, SORT and so on): {', '.join(p['utility_steps'])}", ""]

    if n["node_type"] == "Program":
        paras = sorted(
            (nodes[e["dst_id"]]["start_line"] or 0, nodes[e["dst_id"]]["name"].split(".", 1)[1])
            for e in out_edges[nid]
            if e["edge_type"] == "HAS_PARAGRAPH" and e["dst_id"] in nodes
        )
        rules = []
        for e in out_edges[nid]:
            if e["edge_type"] != "HAS_PARAGRAPH":
                continue
            for r in out_edges[e["dst_id"]]:
                if r["edge_type"] == "DEFINES_RULE" and r["dst_id"] in nodes:
                    rule = nodes[r["dst_id"]]
                    rules.append(
                        (rule["start_line"], e["dst_id"].split(".", 1)[1], rule["summary"])
                    )
        if rules:
            body += ["## Business rules", ""]
            body += [f"- `{para}` line {line}: {text}" for line, para, text in sorted(rules)]
            body.append("")
        if paras:
            body += [f"## Paragraphs ({len(paras)})", ""]
            body += [f"- `{name}` (line {line})" for line, name in paras]
            body.append("")
        if p.get("unresolved_transfers"):
            body += [
                "## Transfers the parser could not resolve",
                "",
                *[
                    f"- {u['command']} at line {u['line']}, operand `{u['operand']}`"
                    for u in p["unresolved_transfers"]
                ],
                "",
            ]

    if mentions.get(nid):
        body += ["## Documents that mention it", ""]
        body += [f"- {doc_link(docs[d])}" for d in sorted(mentions[nid]) if d in docs]
        body += [
            "",
            "Documents can be out of date. When they disagree with the code, the code wins.",
            "",
        ]
    return frontmatter(meta) + "\n" + "\n".join(body).rstrip() + "\n"


def index_page(by_type: dict) -> str:
    meta = {
        "type": "index",
        "title": "CardDemo knowledge bundle",
        "description": "Generated map of the AWS CardDemo mainframe application.",
        "resource": LOCK["repo"].removesuffix(".git"),
    }
    lines = [
        "# CardDemo knowledge bundle",
        "",
        "Generated from the LegacyLens code graph by `make okf`; don't edit by hand.",
        f"Source: CardDemo at commit `{LOCK['commit'][:12]}`.",
        "",
        "Start with a folder, then follow the links between pages.",
        "",
    ]
    for kind, folder in FOLDERS.items():
        lines.append(
            f"- [{folder.title()}]({folder}/index.md) ({len(by_type[kind])}): {INTRO[kind]}"
        )
    return frontmatter(meta) + "\n" + "\n".join(lines) + "\n"


def write(pages: dict[str, str], out: Path = OUT) -> None:
    if out.exists():
        shutil.rmtree(out)
    for rel, text in pages.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def read_page(path: str, out: Path = OUT) -> dict:
    """Read one bundle page; used by the agent's read_concept tool and the chat UI."""
    target = (out / path).resolve()
    if not target.is_relative_to(out.resolve()) or not target.is_file():
        return {"error": f"No page {path}. Start at index.md.", "path": path}
    return {"path": path, "text": target.read_text()}


def main() -> None:
    pages = build_pages(load())
    write(pages)
    print(f"Wrote {len(pages)} pages to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
