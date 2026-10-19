---
type: job
title: TRANREPT
description: Batch job that runs CBTRN03C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANREPT.jcl
---

# TRANREPT

Batch job that runs CBTRN03C.

Source: [app/jcl/TRANREPT.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANREPT.jcl)

## Relationships

- Reads: [CARDXREF](../datasets/CARDXREF.md), [DATEPARM](../datasets/DATEPARM.md), [TRANCATG](../datasets/TRANCATG.md), [TRANSACT](../datasets/TRANSACT.md), [TRANSACT.BKUP](../datasets/TRANSACT.BKUP.md), [TRANSACT.DALY](../datasets/TRANSACT.DALY.md), [TRANTYPE](../datasets/TRANTYPE.md)
- Runs: [CBTRN03C](../programs/CBTRN03C.md)
- Writes: [TRANREPT](../datasets/TRANREPT.md), [TRANSACT.BKUP](../datasets/TRANSACT.BKUP.md), [TRANSACT.DALY](../datasets/TRANSACT.DALY.md)

## Steps

- `STEP10R` runs [CBTRN03C](../programs/CBTRN03C.md)

Utility steps (IDCAMS, SORT and so on): STEP05R

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [CARD-110: Transaction report request from the online menu](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-110`)

Documents can be out of date. When they disagree with the code, the code wins.
