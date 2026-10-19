import os
import socket

import pytest


def _emulator_up() -> bool:
    host, port = os.getenv("SPANNER_EMULATOR_HOST", "localhost:9010").split(":")
    try:
        socket.create_connection((host, int(port)), timeout=1).close()
        return True
    except OSError:
        return False


def pytest_collection_modifyitems(config, items):
    if _emulator_up():
        return
    skip = pytest.mark.skip(reason="Spanner emulator not running (make emulator)")
    for item in items:
        if "emulator" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def knowledge_db():
    """A database with the full code graph and documents, used as the default database.

    The agents, the chat UI and the OKF generator call the default database, so this
    points graph_queries.database() at a fresh test copy for the whole session.
    """
    from legacylens.ingest.code.build import build_graph
    from legacylens.ingest.code.load import load_graph
    from legacylens.ingest.docs.load import load_docs
    from legacylens.retrieval import graph_queries, search
    from legacylens.store.spanner import reset_database

    db = reset_database("test_knowledge")
    load_graph(db, build_graph())
    load_docs(db)
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(graph_queries, "database", lambda: db)
        search._matchers.clear()
        yield db
