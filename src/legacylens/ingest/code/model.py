"""Rows for the Node and Edge tables, plus the naming rules for node IDs."""

import json
import re
from dataclasses import dataclass, field

NODE_TYPES = {
    "Program",
    "Paragraph",
    "Copybook",
    "Dataset",
    "Job",
    "Transaction",
    "Screen",
    "BusinessRule",
    "Chunk",
}
EDGE_TYPES = {
    "HAS_PARAGRAPH",
    "PERFORMS",
    "INCLUDES",
    "CALLS",
    "XCTL",
    "LINK",
    "READS",
    "WRITES",
    "RUNS",
    "STARTS",
    "USES_SCREEN",
    "DEFINES_RULE",
    "MENTIONS",
}
# A dataset is named by the distinctive part of its DSN.
_DSN_PREFIX = "AWS.M2.CARDDEMO."
_DSN_SUFFIXES = {"VSAM", "KSDS", "ESDS", "RRDS", "AIX", "PATH", "PS", "DATA", "INDEX"}


def node_id(node_type: str, name: str) -> str:
    return f"{node_type.upper()}:{name.upper()}"


def dataset_name(dsn: str) -> str:
    """AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS -> ACCTDATA; ...DALYREJS(+1) -> DALYREJS."""
    name = re.sub(r"\(.*\)$", "", dsn.strip().upper())
    name = name.removeprefix(_DSN_PREFIX)
    parts = name.split(".")
    while len(parts) > 1 and parts[-1] in _DSN_SUFFIXES:
        parts.pop()
    return ".".join(parts)


@dataclass
class NodeRow:
    node_type: str
    name: str
    source_path: str | None = None
    start_line: int | None = None
    end_line: int | None = None
    summary: str | None = None
    props: dict = field(default_factory=dict)

    @property
    def node_id(self) -> str:
        return node_id(self.node_type, self.name)

    def row(self) -> tuple:
        return (
            self.node_id,
            self.node_type,
            self.name,
            self.source_path,
            self.start_line,
            self.end_line,
            self.summary,
            json.dumps(self.props, sort_keys=True),
        )


NODE_COLUMNS = (
    "node_id",
    "node_type",
    "name",
    "source_path",
    "start_line",
    "end_line",
    "summary",
    "props",
)


@dataclass
class EdgeRow:
    src_id: str
    edge_type: str
    dst_id: str
    props: dict = field(default_factory=dict)

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.src_id, self.edge_type, self.dst_id)

    def row(self) -> tuple:
        return (self.src_id, self.edge_type, self.dst_id, json.dumps(self.props, sort_keys=True))


EDGE_COLUMNS = ("src_id", "edge_type", "dst_id", "props")


class Graph:
    """Collects nodes and edges, merging duplicates."""

    def __init__(self) -> None:
        self.nodes: dict[str, NodeRow] = {}
        self.edges: dict[tuple[str, str, str], EdgeRow] = {}

    def add_node(self, node: NodeRow) -> NodeRow:
        if node.node_type not in NODE_TYPES:
            raise ValueError(f"unknown node type {node.node_type}")
        existing = self.nodes.get(node.node_id)
        if existing is None or existing.props.get("unresolved"):
            self.nodes[node.node_id] = node
            return node
        existing.props.update({k: v for k, v in node.props.items() if k not in existing.props})
        return existing

    def add_edge(self, src: str, edge_type: str, dst: str, **props) -> EdgeRow:
        if edge_type not in EDGE_TYPES:
            raise ValueError(f"unknown edge type {edge_type}")
        edge = self.edges.get((src, edge_type, dst))
        if edge is None:
            edge = self.edges[(src, edge_type, dst)] = EdgeRow(src, edge_type, dst, {})
        for k, v in props.items():
            if k in ("steps", "lines"):  # list-valued props accumulate
                merged = edge.props.setdefault(k, [])
                for item in v if isinstance(v, list) else [v]:
                    if item not in merged:
                        merged.append(item)
            else:
                edge.props.setdefault(k, v)
        return edge

    def ensure_node(self, nid: str, **props) -> None:
        """Make sure an edge target exists; unknown targets become placeholders."""
        if nid not in self.nodes:
            node_type, name = nid.split(":", 1)
            node_type = next(t for t in NODE_TYPES if t.upper() == node_type)
            self.nodes[nid] = NodeRow(node_type, name, props={"unresolved": True, **props})
