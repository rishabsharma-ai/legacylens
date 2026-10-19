"""Named, parameterised GQL queries over LegacyGraph.

The agent calls these instead of writing GQL itself, so it can't invent a label or
a relationship that doesn't exist. Each function returns plain dicts.
"""

from google.cloud.spanner_v1 import param_types

from legacylens.store.spanner import database


def run(sql: str, params: dict | None = None, db=None) -> list[dict]:
    db = db or database()
    types = {k: param_types.STRING for k in (params or {})}
    with db.snapshot() as snap:
        result = snap.execute_sql(sql, params=params, param_types=types)
        rows = list(result)
        names = [f.name for f in result.fields]
    return [dict(zip(names, row, strict=True)) for row in rows]


def graph(match: str, order: str, params: dict | None = None, db=None) -> list[dict]:
    """Run a MATCH ... RETURN over LegacyGraph inside SQL, so ORDER BY is applied."""
    return run(f"SELECT * FROM GRAPH_TABLE(LegacyGraph {match}) ORDER BY {order}", params, db)


def node(node_id: str, db=None) -> dict | None:
    rows = run(
        "SELECT node_id, node_type, name, source_path, start_line, end_line, summary, "
        "TO_JSON_STRING(props) AS props FROM Node WHERE node_id = @id",
        {"id": node_id},
        db,
    )
    return rows[0] if rows else None


def jobs_running(program: str, db=None) -> list[dict]:
    match = """
        MATCH (j:Job)-[r:RUNS]->(p:Program {name: @name})
        RETURN j.name AS job, TO_JSON_STRING(r.steps) AS steps, j.source_path AS source"""
    return graph(match, "job", {"name": program}, db)


def files_of(program: str, db=None) -> list[dict]:
    match = """
        MATCH (p:Program {name: @name})-[r:READS|WRITES]->(d:Dataset)
        RETURN d.name AS dataset, r.edge_type AS access"""
    return graph(match, "dataset, access", {"name": program}, db)


def callers_of(program: str, db=None) -> list[dict]:
    match = """
        MATCH (c)-[r:CALLS|XCTL|LINK|RUNS|STARTS]->(p:Program {name: @name})
        RETURN c.node_id AS caller, r.edge_type AS how"""
    return graph(match, "caller", {"name": program}, db)


def callees_of(program: str, db=None) -> list[dict]:
    match = """
        MATCH (p:Program {name: @name})-[r:CALLS|XCTL|LINK]->(c:Program)
        RETURN c.name AS callee, r.edge_type AS how, JSON_VALUE(r.props, '$.method') AS method"""
    return graph(match, "callee", {"name": program}, db)


def programs_including(copybook: str, db=None) -> list[dict]:
    match = """
        MATCH (p:Program)-[:INCLUDES]->(c:Copybook {name: @name})
        RETURN p.name AS program, JSON_VALUE(p.props, '$.app') AS app"""
    return graph(match, "program", {"name": copybook}, db)


def programs_using_dataset(dataset: str, db=None) -> list[dict]:
    match = """
        MATCH (p:Program)-[r:READS|WRITES]->(d:Dataset {name: @name})
        RETURN p.name AS program, r.edge_type AS access"""
    return graph(match, "program, access", {"name": dataset}, db)


def rules_of(program: str, db=None) -> list[dict]:
    match = """
        MATCH (p:Program {name: @name})-[:HAS_PARAGRAPH]->(para:Paragraph)
              -[:DEFINES_RULE]->(r:BusinessRule)
        RETURN para.name AS paragraph, r.summary AS rule, r.start_line AS line"""
    return graph(match, "line", {"name": program}, db)


def neighbourhood(node_id: str, db=None) -> list[dict]:
    """Every edge in or out of a node, skipping the many paragraph-level edges."""
    match = """
        MATCH (a {node_id: @id})-[r]-(b)
        WHERE r.edge_type NOT IN ('HAS_PARAGRAPH', 'PERFORMS', 'MENTIONS')
        RETURN r.src_id AS src, r.edge_type AS edge, r.dst_id AS dst"""
    return graph(match, "edge, src, dst", {"id": node_id}, db)


TEMPLATES = {
    "jobs_running": jobs_running,
    "files_of": files_of,
    "callers_of": callers_of,
    "callees_of": callees_of,
    "programs_including": programs_including,
    "programs_using_dataset": programs_using_dataset,
    "rules_of": rules_of,
}
