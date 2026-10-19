.PHONY: setup emulator emulator-stop corpus db test lint format

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

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .
