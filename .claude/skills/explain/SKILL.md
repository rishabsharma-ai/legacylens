---
name: explain
description: Explain how a part of LegacyLens works end to end, for learning. Use when asked "how does X work", "walk me through X" or "why is X like this".
---

The owner is building this project to learn context engineering, graph databases,
RAG and agents. When explaining:

1. Start with what the part does for the user, in one or two sentences.
2. Trace one concrete example through the real code, such as the question "Why would
   a transaction be rejected during posting?", naming files and functions with
   `path:line`.
3. Show the actual data at each step: a GQL query and its rows, or a chunk and its
   MENTIONS edges. Run it against the emulator if it is up.
4. Name the general technique (for example Reciprocal Rank Fusion) and link the ADR
   or learning note that covers it.
5. End with one thing worth trying next, such as an experiment or a change to see
   what breaks.
