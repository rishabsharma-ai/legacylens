"""Split Confluence pages and Jira tickets into retrievable chunks.

Chunks follow the document's own structure: a Confluence page splits at its
headings, and a Jira ticket becomes one chunk for the description plus one per
comment. Each chunk keeps its title and heading path, because a section like
"Reject reason codes" means little without the page it sits on.
"""

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "corpus" / "docs"
MAX_WORDS = 300


@dataclass
class Doc:
    doc_id: str
    source_type: str
    title: str
    url: str
    updated_at: datetime | None
    props: dict


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    seq: int
    heading: str
    text: str

    @property
    def embed_text(self) -> str:
        return f"{self.heading}\n{self.text}"


def _ts(value) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    return None


def split_long(text: str) -> list[str]:
    """Split text over MAX_WORDS at paragraph breaks, keeping tables whole."""
    if len(text.split()) <= MAX_WORDS:
        return [text]
    parts, current = [], []
    for para in re.split(r"\n\s*\n", text):
        if current and len(" ".join(current + [para]).split()) > MAX_WORDS:
            parts.append("\n\n".join(current))
            current = []
        current.append(para)
    if current:
        parts.append("\n\n".join(current))
    return parts


def confluence(path: Path) -> tuple[Doc, list[Chunk]]:
    _, front, body = path.read_text().split("---\n", 2)
    meta = yaml.safe_load(front)
    doc_id = f"CONFLUENCE:{meta['page_id']}"
    doc = Doc(
        doc_id,
        "confluence",
        meta["title"],
        f"confluence/{path.name}",
        _ts(meta.get("updated")),
        {
            "space": meta.get("space"),
            "author": meta.get("author"),
            "labels": meta.get("labels", []),
            "path": str(path.relative_to(ROOT)),
        },
    )
    sections: list[tuple[str, list[str]]] = [(meta["title"], [])]
    for line in body.splitlines():
        if line.startswith("# "):
            continue  # the page title, already in heading
        m = re.match(r"(#{2,3})\s+(.*)", line)
        if m:
            sections.append((f"{meta['title']} > {m.group(2).strip()}", []))
        else:
            sections[-1][1].append(line)
    chunks = []
    for heading, lines in sections:
        text = "\n".join(lines).strip()
        if not text:
            continue
        for part in split_long(text):
            chunks.append(
                Chunk(f"CHUNK:{doc_id}#{len(chunks)}", doc_id, len(chunks), heading, part)
            )
    return doc, chunks


def jira(ticket: dict) -> tuple[Doc, list[Chunk]]:
    key = ticket["key"]
    doc_id = f"JIRA:{key}"
    title = f"{key}: {ticket['summary']}"
    doc = Doc(
        doc_id,
        "jira",
        title,
        f"jira/{key}",
        _ts(ticket.get("created")),
        {
            "status": ticket["status"],
            "issuetype": ticket["issuetype"],
            "labels": ticket.get("labels", []),
            "reporter": ticket.get("reporter"),
        },
    )
    chunks = [
        Chunk(
            f"CHUNK:{doc_id}#0",
            doc_id,
            0,
            f"{title} ({ticket['issuetype']}, {ticket['status']})",
            ticket["description"],
        )
    ]
    for n, comment in enumerate(ticket.get("comments", []), start=1):
        chunks.append(
            Chunk(
                f"CHUNK:{doc_id}#{n}",
                doc_id,
                n,
                f"{title} > comment by {comment['author']}",
                comment["body"],
            )
        )
    return doc, chunks


def all_documents(docs: Path = DOCS) -> list[tuple[Doc, list[Chunk]]]:
    out = [confluence(p) for p in sorted((docs / "confluence").glob("*.md"))]
    for line in (docs / "jira" / "tickets.jsonl").read_text().splitlines():
        out.append(jira(json.loads(line)))
    return out
