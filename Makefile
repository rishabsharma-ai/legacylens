.PHONY: setup emulator emulator-stop corpus db load-code load test lint format

include $(wildcard .env)
export

setup:
	uv sync

emulator:
	docker compose up -d spanner

emulator-stop:
	docker compose down

corpus:
	uv run python scripts/fetch_corpus.py

db:
	uv run python -m legacylens.store.spanner

load-code:
	uv run python -m legacylens.ingest.code.load

load: db load-code

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .
