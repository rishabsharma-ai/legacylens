# ADK dev UI entry point

`make adk` runs `adk web adk`, which lists each folder here as an agent. `lens/` just
re-exports `root_agent` from `src/legacylens/agents/agentic_agent.py`. The folder is
not called `legacylens`, because ADK puts this directory on the import path and the
name would hide the real package.
