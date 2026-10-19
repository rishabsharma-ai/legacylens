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
