# ADR-0008: Python 3.12, uv, ruff, pytest, and a Claude Code project setup

- Status: accepted
- Date: 2026-10-19

## Context

The stack must suit Google ADK (Python-first), be quick to set up on a laptop, and
work well when Claude Code does much of the building.

## Decision

- Python 3.12 or newer, one package `legacylens` in a `src/` layout, managed with uv.
- ruff for lint and format, pytest for tests. Tests that need the emulator are marked
  `emulator` and skip when it isn't running.
- A Makefile carries the everyday commands, so humans and agents run the same thing.
- GitHub Actions runs lint and all tests, with the emulator as a service container.
- Claude Code setup:
  - `CLAUDE.md`: short and factual, with commands, layout, rules, and pointers to
    `docs/`. It stays under about 100 lines because it loads into every session.
  - `.claude/settings.json`: allows the everyday commands without prompts, blocks
    reading `.env`, and runs a hook that formats Python files after each edit.
  - `.claude/skills/`: repeatable workflows (`new-adr`, `explain`) that load only when
    used.
  - Decisions live in `docs/adr/`, so a new session can learn why things are the way
    they are without re-asking.

## Alternatives considered

- **Poetry or pip-tools**: work, but uv is faster and handles the Python version too.
- **A long CLAUDE.md with everything**: wastes context in every session. Detail
  belongs in `docs/`, loaded when needed.

## Consequences

- `make setup && make emulator && make test` is the whole onboarding.
- The format hook needs uv installed on the machine running Claude Code.
