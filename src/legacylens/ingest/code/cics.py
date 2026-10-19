"""CICS resource definitions (CSD) and BMS screen maps."""

import re
from pathlib import Path


def parse_csd(path: Path) -> dict:
    """Transactions (tran id -> program) and files (CICS file name -> DSN)."""
    text = path.read_text(errors="replace")
    blocks = re.split(r"\n(?= DEFINE )", "\n" + text)
    transactions, files = {}, {}
    for block in blocks:
        m = re.match(r"\s*DEFINE\s+(TRANSACTION|FILE)\((\w+)\)", block)
        if not m:
            continue
        if m.group(1) == "TRANSACTION":
            pgm = re.search(r"\bPROGRAM\((\w+)\)", block)
            if pgm:
                transactions[m.group(2)] = pgm.group(1)
        else:
            dsn = re.search(r"\bDSNAME\(([\w.]+)\)", block)
            if dsn:
                files[m.group(2)] = dsn.group(1)
    return {"transactions": transactions, "files": files}


def parse_bms(path: Path) -> list[tuple[str, int]]:
    """Mapset names from DFHMSD macros, with their line numbers."""
    found = []
    for n, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
        m = re.match(r"([A-Z0-9#@$]+)\s+DFHMSD\b", line)
        if m:
            found.append((m.group(1), n))
    return found
