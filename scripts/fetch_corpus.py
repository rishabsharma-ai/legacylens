"""Download the pinned CardDemo commit into corpus/carddemo (git-ignored).

We fetch instead of committing the source so the repo stays small and the
corpus version is explicit. Usage: uv run python scripts/fetch_corpus.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "corpus" / "carddemo.lock"
DEST = ROOT / "corpus" / "carddemo"


def main() -> None:
    lock = dict(line.split("=", 1) for line in LOCK.read_text().splitlines() if "=" in line)
    if not DEST.exists():
        subprocess.run(["git", "init", "-q", str(DEST)], check=True)
        subprocess.run(
            ["git", "-C", str(DEST), "remote", "add", "origin", lock["repo"]], check=True
        )
    subprocess.run(
        ["git", "-C", str(DEST), "fetch", "-q", "--depth", "1", "origin", lock["commit"]],
        check=True,
    )
    subprocess.run(["git", "-C", str(DEST), "checkout", "-q", "FETCH_HEAD"], check=True)
    count = sum(1 for _ in (DEST / "app").rglob("*") if _.is_file())
    print(f"CardDemo {lock['commit'][:8]} ready in {DEST} ({count} files under app/)")


if __name__ == "__main__":
    main()
