---
page_id: "2002"
space: CARD
title: Nightly Batch Runbook
author: Marcus Lee
created: 2022-05-02
updated: 2025-01-20
labels: [batch, runbook, operations]
synthetic: true
---

# Nightly Batch Runbook

The nightly batch runs in this order. Do not start a job until the one before it
has ended with return code 0.

| Order | Job      | What it does                                   |
|-------|----------|------------------------------------------------|
| 1     | CLOSEFIL | Closes the VSAM files in CICS                  |
| 2     | POSTTRAN | Posts the daily transaction file               |
| 3     | INTCALC  | Calculates monthly interest                    |
| 4     | COMBTRAN | Merges system-generated and daily transactions |
| 5     | CREASTMT | Produces customer statements                   |
| 6     | OPENFIL  | Reopens the VSAM files in CICS                 |

## The posting job

The posting job reads the daily transaction file (DALYTRAN) and writes every
transaction it cannot post to the daily rejects file, DALYREJS. DALYREJS is a GDG, so
each run creates a new generation. If the rejects count is above zero the job ends
with return code 4. That is a warning, not a failure, so continue to the interest job.

## The interest job

The interest job takes a run date as its PARM, for example PARM='2022071800'.
Change the PARM before a rerun for a past date.

## Restarting

All jobs can be rerun from the top. The posting job is not idempotent: rerunning it
for the same DALYTRAN input posts the transactions twice. Restore TRANSACT from the
TRANBKP backup first.
