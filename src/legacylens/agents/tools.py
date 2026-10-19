"""Function tools for the agentic ADK agent.

ADK turns each function into a tool the model can call: the name, the type hints and
the docstring become the tool's description, so the docstrings are written for the
model. Every result carries node IDs with source paths, or chunk IDs with document
titles, so the model can cite them.
"""

import json

from legacylens.retrieval import graph_queries as gq
from legacylens.retrieval import search


def find_entities(question: str) -> dict:
    """Find the CardDemo code entities (programs, jobs, datasets, copybooks, paragraphs,
    transactions, screens) that a question names, by exact name, business alias such as
    "posting job", or a near-miss spelling. Call this first.

    Args:
        question: the user's question, unchanged.

    Returns:
        {"entities": [{"node_id": "PROGRAM:CBTRN02C", "method": "exact_name", ...}]}
        An empty list means the question names no code entity; search the documents.
    """
    return {"entities": search.resolve_entities(question)}


def describe_entity(node_id: str) -> dict:
    """Get one code entity's graph facts: summary, source file and lines, every direct
    relationship (jobs that run it, files it reads and writes, programs it calls or
    transfers to, copybooks), its business rules, and for a paragraph its COBOL code.

    Args:
        node_id: an ID from find_entities, such as "PROGRAM:CBTRN02C" or "JOB:POSTTRAN".
    """
    facts = search.graph_facts([node_id])
    if not facts:
        return {"error": f"No entity {node_id}. Use find_entities to get a valid ID."}
    fact = facts[0]
    if isinstance(fact.get("props"), str):
        fact["props"] = json.loads(fact["props"])
    return fact


def query_graph(template: str, name: str) -> dict:
    """Run a named graph query over the code graph.

    Args:
        template: one of jobs_running, files_of, callers_of, callees_of (take a program
            name), programs_including (a copybook name), programs_using_dataset (a
            dataset name), rules_of (a program name).
        name: the entity's bare name, such as "CBTRN02C", not the node ID.
    """
    fn = gq.TEMPLATES.get(template)
    if not fn:
        return {"error": f"Unknown template. Use one of: {', '.join(gq.TEMPLATES)}"}
    return {"template": template, "name": name, "rows": fn(name.upper())}


def linked_documents(node_ids: list[str], question: str) -> dict:
    """Get the Confluence and Jira chunks linked to code entities, best first. Use it
    for the "why" and "what does the business say" part of a question.

    Args:
        node_ids: IDs from find_entities.
        question: the user's question, used to rank the chunks.
    """
    hits = search.linked_chunks(node_ids, question, k=5)
    return {"chunks": [_hit(h) for h in hits]}


def search_documents(query: str) -> dict:
    """Search the Confluence and Jira chunks by meaning and keywords (hybrid search).
    Use it when the question names no code entity, or the linked documents are thin.

    Args:
        query: what to look for, in plain words.
    """
    return {"chunks": [_hit(h) for h in search.hybrid_search(query, k=5)]}


def _hit(h: search.Hit) -> dict:
    return {
        "chunk_id": h.chunk_id,
        "doc_id": h.doc_id,
        "title": h.title,
        "heading": h.heading,
        "text": h.text,
        "linked_to": h.linked_to,
    }


def read_concept(path: str = "index.md") -> dict:
    """Read a page of the OKF knowledge bundle: a generated Markdown page per program,
    job, dataset, copybook or screen, with links to related pages. Start at "index.md"
    and follow links such as "programs/CBTRN02C.md".

    Args:
        path: a path inside the bundle, such as "jobs/POSTTRAN.md".
    """
    from legacylens.okf.generate import read_page

    return read_page(path)


TOOLS = [
    find_entities,
    describe_entity,
    query_graph,
    linked_documents,
    search_documents,
    read_concept,
]
