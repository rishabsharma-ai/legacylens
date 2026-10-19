"""Extract programs, paragraphs, calls, copybooks, files and rules from COBOL source.

CardDemo uses fixed-format COBOL: columns 1-6 are a sequence area, column 7 is the
indicator (* or / marks a comment), and columns 8-72 hold code. We blank comments
but keep every line, so regex matches can be mapped back to line numbers.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

VERBS = {
    "ACCEPT",
    "ADD",
    "CALL",
    "CLOSE",
    "COMPUTE",
    "CONTINUE",
    "DELETE",
    "DISPLAY",
    "DIVIDE",
    "ELSE",
    "END-IF",
    "END-EVALUATE",
    "END-PERFORM",
    "EVALUATE",
    "EXEC",
    "EXIT",
    "GO",
    "GOBACK",
    "IF",
    "INITIALIZE",
    "INSPECT",
    "MOVE",
    "MULTIPLY",
    "OPEN",
    "PERFORM",
    "READ",
    "RETURN",
    "REWRITE",
    "SEARCH",
    "SET",
    "SORT",
    "START",
    "STOP",
    "STRING",
    "SUBTRACT",
    "UNSTRING",
    "WHEN",
    "WRITE",
}
CICS_READS = {"READ", "READNEXT", "READPREV", "STARTBR"}
CICS_WRITES = {"WRITE", "REWRITE", "DELETE"}
# COPY name. -- but not "REQUEST-MSG-COPY REPLACING ..." inside an INITIALIZE.
COPY_RE = r"(?<![A-Z0-9-])COPY\s+'?([A-Z0-9][A-Z0-9-]*)'?(?=\s*\.|\s+REPLACING)"


@dataclass
class Source:
    """A COBOL file split into code lines (comments blanked) and comment lines."""

    path: Path
    code: list[str]
    comments: list[str]

    @classmethod
    def read(cls, path: Path) -> "Source":
        code, comments = [], []
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.ljust(72)
            if line[6] in "*/":
                code.append("")
                comments.append(line[7:72].rstrip())
            else:
                code.append(line[7:72].rstrip())
                comments.append("")
        return cls(path, code, comments)

    @property
    def text(self) -> str:
        return "\n".join(self.code)

    def line_of(self, offset: int) -> int:
        """1-based line number of a character offset in self.text."""
        return self.text.count("\n", 0, offset) + 1


@dataclass
class Paragraph:
    name: str
    start: int
    end: int
    performs: list[tuple[str, int]] = field(default_factory=list)


@dataclass
class Program:
    name: str
    path: Path
    kind: str
    summary: str | None
    end_line: int
    paragraphs: list[Paragraph]
    copies: list[str]
    calls: list[tuple[str, int]]
    cics: list[dict]  # {command, line, program, dataset, mapset, unresolved}
    selects: dict[str, str]  # COBOL file name -> DD name
    opens: dict[str, set[str]]  # COBOL file name -> {"READS", "WRITES"}
    values: dict[str, str]  # working-storage variable -> VALUE literal
    moves: dict[str, list[str]]  # variable -> every 'LITERAL' or variable MOVEd into it
    rules: list[dict]
    sql: list[tuple[str, str, int]] = field(default_factory=list)  # (READS|WRITES, table, line)
    dli: list[tuple[str, str, int]] = field(default_factory=list)  # IMS segments
    mq: list[tuple[str, str, int]] = field(default_factory=list)  # MQ queues


def header_summary(src: Source) -> str | None:
    """The 'Function :' line from the comment header, with its continuation lines."""
    for i, comment in enumerate(src.comments[:40]):
        m = re.match(r"\s*Function\s*:\s*(.+)", comment)
        if m:
            parts = [m.group(1).strip()]
            for nxt in src.comments[i + 1 : i + 4]:
                cont = re.match(r"\s{3,}([^:*]+)$", nxt)
                if not cont:
                    break
                parts.append(cont.group(1).strip())
            return " ".join(parts).rstrip("* ").strip()
    return None


def value_literals(text: str) -> dict[str, str]:
    """Variables declared with a literal VALUE, e.g. 05 WS-FILE PIC X(8) VALUE 'ACCTDAT '."""
    pattern = r"\b\d\d\s+([A-Z0-9][A-Z0-9-]*)\s+PIC\s+[^.]*?VALUE\s+'([^']*)'"
    return {m.group(1): m.group(2).strip() for m in re.finditer(pattern, text, re.S)}


def cics_blocks(src: Source) -> list[dict]:
    blocks = []
    for m in re.finditer(r"EXEC\s+CICS\s+(.*?)END-EXEC", src.text, re.S):
        body = " ".join(m.group(1).split())
        words = body.split()
        command = words[0] if words else ""
        if command in ("SEND", "RECEIVE") and len(words) > 1:
            command = f"{command} {words[1]}"
        opts = {}
        for key in ("PROGRAM", "DATASET", "FILE", "MAPSET", "MAP", "TRANSID"):
            om = re.search(rf"\b{key}\s*\(\s*('?[^()']*'?|[A-Z0-9-]+\([^)]*\))\s*\)", body)
            if om:
                opts[key.lower()] = om.group(1).strip()
        blocks.append({"command": command, "line": src.line_of(m.start()), **opts})
    return blocks


def sql_tables(src: Source) -> tuple[list[tuple[str, str, int]], list[str]]:
    """Db2 tables used in EXEC SQL blocks as (edge, table, line), plus EXEC SQL INCLUDEs."""
    uses, includes = [], []
    for m in re.finditer(r"EXEC\s+SQL\s+(.*?)END-EXEC", src.text, re.S):
        body = " ".join(m.group(1).split())
        line = src.line_of(m.start())
        inc = re.match(r"INCLUDE\s+([A-Z0-9-]+)", body)
        if inc:
            includes.append(inc.group(1))
            continue
        table = r"(?:[A-Z0-9_]+\.)?([A-Z][A-Z0-9_]+)"
        for t in re.findall(rf"\bFROM\s+{table}", body):
            uses.append(("READS" if not body.startswith("DELETE") else "WRITES", t, line))
        for t in re.findall(rf"\b(?:INSERT\s+INTO|UPDATE)\s+{table}", body):
            uses.append(("WRITES", t, line))
    return uses, includes


DLI_READS = {"GU", "GN", "GNP", "GHU", "GHN", "GHNP"}
DLI_WRITES = {"ISRT", "REPL", "DLET"}


def dli_segments(src: Source) -> list[tuple[str, str, int]]:
    """IMS segments used in EXEC DLI blocks, e.g. EXEC DLI GU ... SEGMENT (PAUTSUM0)."""
    uses = []
    for m in re.finditer(r"EXEC\s+DLI\s+([A-Z]+)(.*?)END-EXEC", src.text, re.S):
        call = m.group(1)
        if call not in DLI_READS | DLI_WRITES:
            continue
        edge = "READS" if call in DLI_READS else "WRITES"
        for seg in re.findall(r"SEGMENT\s*\(\s*([A-Z0-9-]+)\s*\)", m.group(2)):
            uses.append((edge, seg, src.line_of(m.start())))
    return uses


def mq_queues(src: Source) -> list[tuple[str, str, int]]:
    """MQ queues named by a literal, e.g. MOVE 'CARD.DEMO.ERROR' TO ERROR-QUEUE-NAME.

    Queues a program reads usually come from the MQ trigger message (MQTM-QNAME), so
    only the literal queues, which these programs put replies and errors on, are known.
    """
    pattern = r"\bMOVE\s+'([A-Z0-9.]+\.[A-Z0-9.]+)'\s+TO\s+[A-Z0-9-]*(?:QUEUE|QNAME)[A-Z0-9-]*"
    if not re.search(r"CALL\s+'MQ(?:PUT|PUT1)'", src.text):
        return []
    return [("WRITES", m.group(1), src.line_of(m.start())) for m in re.finditer(pattern, src.text)]


def paragraphs(src: Source) -> list[Paragraph]:
    proc = next((i for i, c in enumerate(src.code) if "PROCEDURE DIVISION" in c), None)
    if proc is None:
        return []
    found = []
    for i in range(proc + 1, len(src.code)):
        line = src.code[i]
        m = re.match(r"([A-Z0-9][A-Z0-9-]*)(\s+SECTION)?\.\s*$", line)
        if m and line[:1] != " " and m.group(1) not in VERBS:
            found.append((m.group(1), i + 1))
    paras = []
    for n, (name, start) in enumerate(found):
        end = found[n + 1][1] - 1 if n + 1 < len(found) else len(src.code)
        paras.append(Paragraph(name, start, end))
    names = {p.name for p in paras}
    for para in paras:
        body = "\n".join(src.code[para.start : para.end])
        for m in re.finditer(r"\bPERFORM\s+([A-Z0-9][A-Z0-9-]*)(?:\s+THRU\s+([A-Z0-9-]+))?", body):
            for target in filter(None, m.groups()):
                if target in names:
                    para.performs.append((target, para.start + body.count("\n", 0, m.start()) + 1))
    return paras


def file_usage(text: str) -> tuple[dict[str, str], dict[str, set[str]]]:
    selects = {
        m.group(1): m.group(2)
        for m in re.finditer(r"\bSELECT\s+([A-Z0-9-]+)\s+ASSIGN\s+TO\s+([A-Z0-9-]+)", text)
    }
    opens: dict[str, set[str]] = {}
    words = text.split()
    for i, word in enumerate(words):
        if word != "OPEN":
            continue
        mode = None
        for w in (w.rstrip(".") for w in words[i + 1 :]):  # OPEN INPUT A B OUTPUT C
            if w in ("INPUT", "OUTPUT", "I-O", "EXTEND"):
                mode = w
            elif w in selects and mode:
                use = opens.setdefault(w, set())
                if mode in ("INPUT", "I-O"):
                    use.add("READS")
                if mode in ("OUTPUT", "EXTEND", "I-O"):
                    use.add("WRITES")
            else:
                break
    return selects, opens


def business_rules(src: Source, paras: list[Paragraph]) -> list[dict]:
    """Reason-code assignments and COMPUTE statements, each tied to its paragraph."""
    rules = []

    def para_at(line: int) -> str | None:
        return next((p.name for p in paras if p.start <= line <= p.end), None)

    text = src.text
    reason = r"MOVE\s+(\d+)\s+TO\s+([A-Z0-9-]*REASON[A-Z0-9-]*)\s+MOVE\s+'([^']+)'"
    for m in re.finditer(reason, text):
        line = src.line_of(m.start())
        rules.append(
            {
                "kind": "reason_code",
                "code": m.group(1),
                "field": m.group(2),
                "text": f"Reason {m.group(1)}: {m.group(3).strip()}",
                "line": line,
                "paragraph": para_at(line),
            }
        )
    for m in re.finditer(r"\bCOMPUTE\s+(.+?)(?=\n\s*(?:[A-Z][A-Z-]*\s)|\.\s*\n)", text, re.S):
        line = src.line_of(m.start())
        stmt = " ".join(m.group(1).split())
        if "=" in stmt and para_at(line):
            rules.append(
                {
                    "kind": "computation",
                    "text": f"COMPUTE {stmt}",
                    "line": line,
                    "paragraph": para_at(line),
                }
            )
    return rules


def parse_program(path: Path) -> Program | None:
    src = Source.read(path)
    text = src.text
    m = re.search(r"PROGRAM-ID\.\s+([A-Z0-9-]+)", text)
    if not m:
        return None
    paras = paragraphs(src)
    selects, opens = file_usage(text)
    calls = [
        (c.group(1), src.line_of(c.start())) for c in re.finditer(r"\bCALL\s+'([A-Z0-9-]+)'", text)
    ]
    sql, sql_includes = sql_tables(src)
    copies = list(dict.fromkeys(re.findall(COPY_RE, text) + sql_includes))
    return Program(
        name=m.group(1),
        path=path,
        kind="online" if "EXEC CICS" in " ".join(text.split()) else "batch",
        summary=header_summary(src),
        end_line=len(src.code),
        paragraphs=paras,
        copies=copies,
        calls=calls,
        cics=cics_blocks(src),
        selects=selects,
        opens=opens,
        values=value_literals(text),
        moves=moves_into(text),
        rules=business_rules(src, paras),
        sql=sql,
        dli=dli_segments(src),
        mq=mq_queues(src),
    )


def moves_into(text: str) -> dict[str, list[str]]:
    moves: dict[str, list[str]] = {}
    for m in re.finditer(
        r"\bMOVE\s+('[^']*'|[A-Z0-9][A-Z0-9-]*)\s+TO\s+([A-Z0-9][A-Z0-9-]*)", text
    ):
        moves.setdefault(m.group(2), []).append(m.group(1))
    return moves


def resolve_all(
    value: str | None, values: dict[str, str], moves: dict[str, list[str]]
) -> list[str]:
    """Every literal a CICS option can hold: a 'LITERAL', a VALUE, or literals MOVEd into it."""
    if not value:
        return []
    direct = resolve(value, values)
    if direct:
        return [direct]
    found = []
    for src in moves.get(value, []):
        lit = resolve(src, values)
        if lit and lit not in found:
            found.append(lit)
    return found


def resolve(value: str | None, values: dict[str, str]) -> str | None:
    """A CICS option is a 'LITERAL' or a variable whose VALUE we may know."""
    if not value:
        return None
    if value.startswith("'"):
        return value.strip("'").strip()
    return values.get(value)


def copybook_values(path: Path) -> dict[str, str]:
    return value_literals(Source.read(path).text)


def copybook_copies(path: Path) -> list[str]:
    return re.findall(COPY_RE, Source.read(path).text)


def copybook_literals(path: Path) -> list[str]:
    """Every VALUE literal in a copybook, used to find data-driven XCTL targets."""
    return re.findall(r"VALUE\s+'([A-Z0-9]+)\s*'", Source.read(path).text)
