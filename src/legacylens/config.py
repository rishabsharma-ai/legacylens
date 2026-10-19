"""Settings read from the environment (see .env.example)."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    project: str = os.getenv("SPANNER_PROJECT", "legacylens-local")
    instance: str = os.getenv("SPANNER_INSTANCE", "legacylens")
    database: str = os.getenv("SPANNER_DATABASE", "knowledge")
    emulator_host: str = os.getenv("SPANNER_EMULATOR_HOST", "localhost:9010")


settings = Settings()
