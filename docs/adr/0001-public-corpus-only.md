# ADR-0001: Use only public code and synthetic documents

- Status: accepted
- Date: 2026-10-19

## Context

LegacyLens mirrors a system built at work, but it is a personal project. No employer
code, data, documents or prompts may enter this repository, its history, or any LLM
call made from it. We still need a corpus realistic enough to exercise CICS, batch
JCL, VSAM files and copybooks.

## Decision

- Code corpus: AWS CardDemo (`aws-samples/aws-mainframe-modernization-carddemo`,
  Apache-2.0), pinned to one commit in `corpus/carddemo.lock`. It is fetched, not
  committed, into the git-ignored `corpus/carddemo/`.
- Document corpus: Confluence and Jira style documents written for this project in
  `corpus/docs/`, each marked `synthetic: true`. Every fact in them was checked
  against the CardDemo source, except where a document is deliberately wrong (see
  page 2004), which is noted in the eval set.
- Start with the base app (`app/cbl`, `app/cpy`, `app/jcl`, `app/bms`, `app/csd`).
  The optional Db2, IMS and MQ extensions come in once the base graph is solid.

## Alternatives considered

- **Other public COBOL samples** (IBM Z samples, GnuCOBOL tests): smaller or not one
  coherent business application, so cross-program questions would be thin.
- **Committing the CardDemo source**: adds about 6,700 files to the repo and makes the
  pinned version less obvious.

## Consequences

- Anyone can rebuild the corpus with one command, and the eval set stays valid
  because the commit is pinned.
- The documents are small and clean compared with a real wiki. Thread 3 can add noise
  (duplicates, long pages, tables) once the basic pipeline works.
