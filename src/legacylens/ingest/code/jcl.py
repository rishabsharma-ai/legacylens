"""Extract jobs, steps and the datasets each step touches from JCL."""

import re
from dataclasses import dataclass, field
from pathlib import Path

UTILITIES = {
    "IDCAMS",
    "SORT",
    "IEFBR14",
    "IEBGENER",
    "IEBCOPY",
    "ICETOOL",
    "DFSORT",
    "IKJEFT01",
    "IKJEFT1B",
    "FTP",
    "TXT2PDF",
    "SDSF",
}


@dataclass
class DD:
    name: str
    dsn: str
    disp: str  # first DISP value: SHR, OLD, NEW, MOD
    line: int


@dataclass
class Step:
    name: str
    program: str | None
    proc: str | None
    line: int
    dds: list[DD] = field(default_factory=list)


@dataclass
class Job:
    name: str
    path: Path
    kind: str  # job | proc
    steps: list[Step]


def statements(path: Path) -> list[tuple[int, str, str, str]]:
    """(line, name, operation, operands) with continuation lines joined."""
    out: list[list] = []
    for n, raw in enumerate(path.read_text(errors="replace").splitlines(), start=1):
        line = raw[:72].rstrip()
        if not line.startswith("//") or line.startswith("//*"):
            continue
        body = line[2:]
        cont = out and out[-1][3].rstrip().endswith(",") and body[:1] == " "
        if cont:
            out[-1][3] += body.strip()
            continue
        m = re.match(r"(\S*)\s+(\S+)\s*(.*)", body)
        if m:
            out.append([n, m.group(1), m.group(2), m.group(3).strip()])
    # operands stop at the first space (the rest is a comment)
    return [(n, name, op, operands.split(" ")[0]) for n, name, op, operands in out]


def parse_job(path: Path) -> Job | None:
    stmts = statements(path)
    if not stmts:
        return None
    first = stmts[0]
    kind = "proc" if first[2] == "PROC" else "job"
    job = Job(first[1] or path.stem.upper(), path, kind, [])
    for line, name, op, operands in stmts:
        if op == "EXEC":
            pgm = re.search(r"PGM=([A-Z0-9#@$]+)", operands)
            proc = re.search(r"PROC=([A-Z0-9#@$]+)", operands)
            if not pgm and not proc:
                bare = re.match(r"([A-Z0-9#@$]+)(,|$)", operands)
                proc = bare
            job.steps.append(Step(name, pgm and pgm.group(1), proc and proc.group(1), line))
        elif op == "DD" and job.steps:
            dsn = re.search(r"DSN(?:AME)?=([A-Z0-9.#@$&]+(?:\([+-]?\w+\))?)", operands)
            if not dsn or dsn.group(1).startswith("&") or dsn.group(1) == "NULLFILE":
                continue
            disp = re.search(r"DISP=\(?([A-Z]+)", operands)
            job.steps[-1].dds.append(DD(name, dsn.group(1), disp.group(1) if disp else "SHR", line))
    return job
