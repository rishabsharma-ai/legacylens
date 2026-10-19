#!/usr/bin/env bash
# After Claude edits a Python file, format it and apply safe lint fixes.
# Receives the tool call as JSON on stdin.
file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
[[ "$file" == *.py ]] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
uv run --quiet ruff format "$file" >/dev/null 2>&1
uv run --quiet ruff check --fix --quiet "$file" >/dev/null 2>&1
exit 0
