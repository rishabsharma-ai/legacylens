"""Find which code entities a piece of text talks about (ADR-0004).

Pass 1, exact_name (confidence 1.0): a known entity name appears as a whole word.
Pass 2, alias (0.8): a nickname from corpus/aliases.yaml appears.
Pass 3, llm (0.6): off by default; for chunks with no hits, an LLM chooses from a
candidate list, so it can't invent node IDs.

The same matcher resolves entities in user questions (legacylens.retrieval).
"""

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
ALIASES = ROOT / "corpus" / "aliases.yaml"
LINKABLE = {"Program", "Copybook", "Dataset", "Job", "Transaction", "Screen", "Paragraph"}
MIN_PARAGRAPH_NAME = 10  # short paragraph names like MAIN-PARA are too common to link
STOP_NAMES = {"JCL", "LOADLIB", "CNTL", "PROC", "DATA", "SYSOUT"}  # library names, not entities


@dataclass(frozen=True)
class Mention:
    node_id: str
    method: str
    confidence: float
    surface: str


def load_aliases(path: Path = ALIASES) -> dict[str, list[str]]:
    return {k.lower(): v for k, v in yaml.safe_load(path.read_text()).items()}


class EntityMatcher:
    """Built from (node_id, node_type, name) rows of the code graph."""

    def __init__(self, nodes: list[tuple[str, str, str]], aliases: dict[str, list[str]]):
        self.by_name: dict[str, list[str]] = {}
        para_names: dict[str, list[str]] = {}
        for node_id, node_type, name in nodes:
            if node_type not in LINKABLE:
                continue
            if node_type == "Paragraph":
                short = name.split(".", 1)[1]
                para_names.setdefault(short, []).append(node_id)
                continue
            if name.upper() not in STOP_NAMES and len(name) >= 4:
                self.by_name.setdefault(name.upper(), []).append(node_id)
        for name, ids in self.by_name.items():
            # Jobs that define a file share its name (DALYREJS); the text means the file.
            if any(i.startswith("DATASET:") for i in ids):
                self.by_name[name] = [i for i in ids if not i.startswith("JOB:")]
        for short, ids in para_names.items():
            if len(ids) == 1 and len(short) >= MIN_PARAGRAPH_NAME:
                self.by_name.setdefault(short, []).extend(ids)
        known = {n for n, _, _ in nodes}
        self.aliases = {k: [i for i in v if i in known] for k, v in aliases.items()}
        names = sorted(self.by_name, key=len, reverse=True)
        self._name_re = (
            re.compile(r"(?<![A-Z0-9-])(" + "|".join(map(re.escape, names)) + r")(?![A-Z0-9-])")
            if names
            else None
        )
        phrases = sorted(self.aliases, key=len, reverse=True)
        self._alias_re = (
            re.compile(r"\b(" + "|".join(map(re.escape, phrases)) + r")\b", re.I)
            if phrases
            else None
        )

    def find(self, text: str) -> list[Mention]:
        found: dict[str, Mention] = {}
        if self._name_re:
            for m in self._name_re.finditer(text):
                for nid in self.by_name[m.group(1)]:
                    found.setdefault(nid, Mention(nid, "exact_name", 1.0, m.group(1)))
        if self._alias_re:
            # longest phrase wins: "posting job" before "posting"
            covered: list[tuple[int, int]] = []
            for m in self._alias_re.finditer(text):
                if any(s <= m.start() < e for s, e in covered):
                    continue
                covered.append(m.span())
                for nid in self.aliases[m.group(1).lower()]:
                    found.setdefault(nid, Mention(nid, "alias", 0.8, m.group(1)))
        return list(found.values())

    def names(self) -> list[str]:
        return list(self.by_name)


@lru_cache(maxsize=1)
def matcher_from_db() -> EntityMatcher:
    from legacylens.retrieval.graph_queries import run

    rows = run(
        "SELECT node_id, node_type, name FROM Node "
        "WHERE node_type != 'Chunk' AND JSON_VALUE(props, '$.unresolved') IS NULL"
    )
    return EntityMatcher([(r["node_id"], r["node_type"], r["name"]) for r in rows], load_aliases())
