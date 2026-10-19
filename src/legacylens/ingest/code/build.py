"""Turn the parsed CardDemo source into graph nodes and edges."""

from pathlib import Path

from legacylens.ingest.code import cics, cobol, jcl
from legacylens.ingest.code.model import Graph, NodeRow, dataset_name, node_id

ROOT = Path(__file__).resolve().parents[4]
CORPUS = ROOT / "corpus" / "carddemo" / "app"
SUBAPPS = {
    "app-transaction-type-db2": "db2-transaction-type",
    "app-authorization-ims-db2-mq": "ims-db2-mq-authorization",
    "app-vsam-mq": "vsam-mq",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT / "corpus" / "carddemo"))


def source_files(root: Path, folder: str, *exts: str) -> list[Path]:
    """Files in the base app folder and in each optional sub-application."""
    dirs = [root / folder] + [root / sub / folder for sub in SUBAPPS]
    found = []
    for d in dirs:
        if d.is_dir():
            found += sorted(p for p in d.iterdir() if p.suffix.lower() in exts)
    return found


def app_of(path: Path) -> str:
    for part in path.parts:
        if part in SUBAPPS:
            return SUBAPPS[part]
    return "base"


def build_graph(root: Path = CORPUS) -> Graph:
    g = Graph()

    # CICS definitions first: they map CICS file names to datasets.
    cics_files: dict[str, str] = {}
    for csd in source_files(root, "csd", ".csd"):
        defs = cics.parse_csd(csd)
        cics_files.update(defs["files"])
        for tran, program in defs["transactions"].items():
            g.add_node(NodeRow("Transaction", tran, rel(csd), props={"app": app_of(csd)}))
            g.ensure_node(node_id("Program", program))
            g.add_edge(node_id("Transaction", tran), "STARTS", node_id("Program", program))

    for bms in source_files(root, "bms", ".bms"):
        for mapset, line in cics.parse_bms(bms):
            g.add_node(NodeRow("Screen", mapset, rel(bms), line, props={"app": app_of(bms)}))

    copybook_paths: dict[str, Path] = {}
    for cpy in (
        source_files(root, "cpy", ".cpy")
        + source_files(root, "cpy-bms", ".cpy")
        + source_files(root, "dcl", ".dcl", ".cpy")
    ):
        name = cpy.stem.upper()
        copybook_paths[name] = cpy
        kind = "bms_symbolic_map" if cpy.parent.name == "cpy-bms" else "record_layout"
        g.add_node(NodeRow("Copybook", name, rel(cpy), 1, props={"kind": kind, "app": app_of(cpy)}))
    for name, cpy in copybook_paths.items():
        for inner in cobol.copybook_copies(cpy):
            g.ensure_node(node_id("Copybook", inner), system=inner.startswith("DFH"))
            g.add_edge(node_id("Copybook", name), "INCLUDES", node_id("Copybook", inner))

    programs: dict[str, cobol.Program] = {}
    for path in source_files(root, "cbl", ".cbl"):
        prog = cobol.parse_program(path)
        if prog:
            programs[prog.name] = prog

    for prog in programs.values():
        pid = node_id("Program", prog.name)
        g.add_node(
            NodeRow(
                "Program",
                prog.name,
                rel(prog.path),
                1,
                prog.end_line,
                prog.summary,
                props={
                    "kind": prog.kind,
                    "app": app_of(prog.path),
                    "dd_names": sorted(prog.selects.values()),
                },
            )
        )
        seen = set()
        for para in prog.paragraphs:
            if para.name in seen:  # some programs repeat a label; keep the first
                continue
            seen.add(para.name)
            para_id = node_id("Paragraph", f"{prog.name}.{para.name}")
            g.add_node(
                NodeRow(
                    "Paragraph",
                    f"{prog.name}.{para.name}",
                    rel(prog.path),
                    para.start,
                    para.end,
                    props={"program": prog.name},
                )
            )
            g.add_edge(pid, "HAS_PARAGRAPH", para_id)
        for para in prog.paragraphs:
            for target, line in para.performs:
                g.add_edge(
                    node_id("Paragraph", f"{prog.name}.{para.name}"),
                    "PERFORMS",
                    node_id("Paragraph", f"{prog.name}.{target}"),
                    lines=line,
                )

        # Values from the program and from the copybooks it includes.
        values = dict(prog.values)
        for cpy in prog.copies:
            if cpy in copybook_paths:
                values = cobol.copybook_values(copybook_paths[cpy]) | values
        for cpy in prog.copies:
            g.ensure_node(node_id("Copybook", cpy), system=cpy.startswith("DFH"))
            g.add_edge(pid, "INCLUDES", node_id("Copybook", cpy))
        for callee, line in prog.calls:
            g.ensure_node(node_id("Program", callee), external=True)
            g.add_edge(pid, "CALLS", node_id("Program", callee), lines=line)

        unresolved = []
        for block in prog.cics:
            cmd = block["command"]
            if cmd in ("XCTL", "LINK"):
                targets = cobol.resolve_all(block.get("program"), values, prog.moves)
                targets = [t for t in targets if t in programs]
                if not targets:
                    unresolved.append(
                        {"command": cmd, "line": block["line"], "operand": block.get("program")}
                    )
                for t in targets:
                    g.add_edge(pid, cmd, node_id("Program", t), lines=block["line"])
            elif cmd.split()[0] in cobol.CICS_READS | cobol.CICS_WRITES:
                file_opt = block.get("dataset") or block.get("file")
                for name in cobol.resolve_all(file_opt, values, prog.moves):
                    dsn = cics_files.get(name)
                    if not dsn:
                        continue
                    ds = dataset_name(dsn)
                    g.add_node(NodeRow("Dataset", ds, props={"dsn": base_dsn(dsn)}))
                    edge = "READS" if cmd.split()[0] in cobol.CICS_READS else "WRITES"
                    g.add_edge(
                        pid, edge, node_id("Dataset", ds), lines=block["line"], cics_file=name
                    )
            elif cmd.startswith(("SEND MAP", "RECEIVE MAP")):
                for mapset in cobol.resolve_all(block.get("mapset"), values, prog.moves):
                    if node_id("Screen", mapset) in g.nodes:
                        g.add_edge(pid, "USES_SCREEN", node_id("Screen", mapset))
        if unresolved:
            g.nodes[pid].props["unresolved_transfers"] = unresolved
        for edge, table, line in prog.sql:
            if table == "SQLCA":
                continue
            g.add_node(NodeRow("Dataset", table, props={"kind": "db2_table"}))
            g.add_edge(pid, edge, node_id("Dataset", table), lines=line)

        for n, rule in enumerate(prog.rules):
            name = f"{prog.name}.{rule['paragraph']}.{rule['kind'].upper()}-{n}"
            if rule["kind"] == "reason_code":
                name = f"{prog.name}.REASON-{rule['code']}"
            g.add_node(
                NodeRow(
                    "BusinessRule",
                    name,
                    rel(prog.path),
                    rule["line"],
                    rule["line"],
                    rule["text"],
                    props={"kind": rule["kind"], "program": prog.name},
                )
            )
            g.add_edge(
                node_id("Paragraph", f"{prog.name}.{rule['paragraph']}"),
                "DEFINES_RULE",
                node_id("BusinessRule", name),
            )

    data_driven_transfers(g, programs, copybook_paths)

    for path in source_files(root, "jcl", ".jcl"):
        job = jcl.parse_job(path)
        if not job:
            continue
        jid = node_id("Job", job.name)
        utility_steps = [s.name for s in job.steps if s.program in jcl.UTILITIES]
        g.add_node(
            NodeRow(
                "Job",
                job.name,
                rel(path),
                1,
                props={
                    "app": app_of(path),
                    "utility_steps": utility_steps,
                    "procs": sorted({s.proc for s in job.steps if s.proc}),
                },
            )
        )
        for step in job.steps:
            dd_map = {}
            for dd in step.dds:
                if dd.name in ("STEPLIB", "JOBLIB") or dd.dsn.endswith("LOADLIB"):
                    continue
                ds = dataset_name(dd.dsn)
                g.add_node(
                    NodeRow("Dataset", ds, props={"dsn": base_dsn(dd.dsn), "gdg": "(" in dd.dsn})
                )
                edge = "WRITES" if dd.disp in ("NEW", "MOD") else "READS"
                g.add_edge(jid, edge, node_id("Dataset", ds), steps=step.name)
                dd_map[dd.name] = (ds, edge)
            prog = programs.get(step.program or "")
            if step.program and step.program not in jcl.UTILITIES:
                g.ensure_node(node_id("Program", step.program), external=True)
                g.add_edge(jid, "RUNS", node_id("Program", step.program), steps=step.name)
            if prog:  # join the program's SELECT ... ASSIGN TO dd with this step's DDs
                for cobol_file, dd in prog.selects.items():
                    if dd not in dd_map:
                        continue
                    ds, disp_edge = dd_map[dd]
                    for edge in sorted(prog.opens.get(cobol_file, {disp_edge})):
                        g.add_edge(
                            node_id("Program", prog.name),
                            edge,
                            node_id("Dataset", ds),
                            dd=dd,
                            steps=f"{job.name}.{step.name}",
                        )

    for edge in list(g.edges.values()):
        g.ensure_node(edge.src_id)
        g.ensure_node(edge.dst_id)
    return g


def base_dsn(dsn: str) -> str:
    return dsn.split("(")[0]


def data_driven_transfers(g: Graph, programs: dict, copybook_paths: dict) -> None:
    """XCTL targets read from a data table, like the main menu's options in COMEN02Y.

    When a program's XCTL operand can't be resolved, look for program names held as
    VALUE literals in the copybooks it includes. These edges are marked so readers know
    they come from data, not from a literal in the code.
    """
    for prog in programs.values():
        pid = node_id("Program", prog.name)
        if not g.nodes[pid].props.get("unresolved_transfers"):
            continue
        for cpy in prog.copies:
            path = copybook_paths.get(cpy)
            if not path:
                continue
            targets = [
                t
                for t in dict.fromkeys(cobol.copybook_literals(path))
                if t in programs and t != prog.name
            ]
            if len(targets) >= 2:  # a table of programs, not a single constant
                for t in targets:
                    g.add_edge(pid, "XCTL", node_id("Program", t), via=cpy, method="data_table")
