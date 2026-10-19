---
type: job
title: POSTTRAN
description: Batch job that runs CBTRN02C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/POSTTRAN.jcl
---

# POSTTRAN

Batch job that runs CBTRN02C.

Source: [app/jcl/POSTTRAN.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/POSTTRAN.jcl)

## Relationships

- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [DALYTRAN](../datasets/DALYTRAN.md), [TCATBALF](../datasets/TCATBALF.md), [TRANSACT](../datasets/TRANSACT.md)
- Runs: [CBTRN02C](../programs/CBTRN02C.md)
- Writes: [DALYREJS](../datasets/DALYREJS.md)

## Steps

- `STEP15` runs [CBTRN02C](../programs/CBTRN02C.md)

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [CARD-101: Spike in overlimit rejects after credit limit migration](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-101`)
- [CARD-111: Nightly batch overran into the online window](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-111`)

Documents can be out of date. When they disagree with the code, the code wins.
