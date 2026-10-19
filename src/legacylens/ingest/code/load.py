"""Load the CardDemo code graph into Spanner.

Usage: uv run python -m legacylens.ingest.code.load
"""

from collections import Counter

from legacylens.ingest.code.build import build_graph
from legacylens.ingest.code.model import EDGE_COLUMNS, NODE_COLUMNS, Graph
from legacylens.store.spanner import database

BATCH = 500


def write_rows(db, table: str, columns: tuple, rows: list[tuple]) -> None:
    for i in range(0, len(rows), BATCH):
        with db.batch() as b:
            b.insert_or_update(table, columns, rows[i : i + BATCH])


def load_graph(db, graph: Graph) -> None:
    """Nodes first, then edges, because edges have foreign keys to nodes."""
    write_rows(db, "Node", NODE_COLUMNS, [n.row() for n in graph.nodes.values()])
    write_rows(db, "Edge", EDGE_COLUMNS, [e.row() for e in graph.edges.values()])


def main() -> None:
    graph = build_graph()
    load_graph(database(), graph)
    nodes = Counter(n.node_type for n in graph.nodes.values())
    edges = Counter(e.edge_type for e in graph.edges.values())
    print("Loaded nodes:", dict(sorted(nodes.items())))
    print("Loaded edges:", dict(sorted(edges.items())))


if __name__ == "__main__":
    main()
