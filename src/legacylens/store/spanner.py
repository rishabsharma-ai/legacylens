"""Create the emulator instance and database, and apply schema.sql.

The emulator keeps everything in memory, so this runs on every fresh start.
Usage: uv run python -m legacylens.store.spanner
"""

import os
from pathlib import Path

from google.cloud import spanner
from google.cloud.spanner_admin_instance_v1.types import Instance
from google.cloud.spanner_v1 import database as _db  # noqa: F401

from legacylens.config import settings

SCHEMA = Path(__file__).with_name("schema.sql")


def ddl_statements() -> list[str]:
    """Split schema.sql on lines that hold only ';' and drop comment-only parts."""
    parts = SCHEMA.read_text().split("\n;\n")
    stmts = []
    for part in parts:
        lines = [ln for ln in part.splitlines() if not ln.strip().startswith("--")]
        stmt = "\n".join(lines).strip().rstrip(";").strip()
        if stmt:
            stmts.append(stmt)
    return stmts


def client() -> spanner.Client:
    os.environ.setdefault("SPANNER_EMULATOR_HOST", settings.emulator_host)
    return spanner.Client(project=settings.project)


def reset_database(name: str = settings.database) -> _db.Database:
    """Drop and recreate the database with the current schema."""
    c = client()
    instance = c.instance(settings.instance)
    if not instance.exists():
        config = f"projects/{settings.project}/instanceConfigs/emulator-config"
        c.instance_admin_api.create_instance(
            parent=f"projects/{settings.project}",
            instance_id=settings.instance,
            instance=Instance(config=config, display_name="LegacyLens", node_count=1),
        ).result(60)
    db = instance.database(name, ddl_statements=ddl_statements())
    if db.exists():
        db.drop()
    db.create().result(120)
    return db


if __name__ == "__main__":
    db = reset_database()
    print(f"Created {db.name} with {len(ddl_statements())} DDL statements")
