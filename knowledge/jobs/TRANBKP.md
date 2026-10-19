---
type: job
title: TRANBKP
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANBKP.jcl
---

# TRANBKP

Batch job (utilities only).

Source: [app/jcl/TRANBKP.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANBKP.jcl)

## Relationships

- Reads: [TRANSACT](../datasets/TRANSACT.md)
- Writes: [TRANSACT.BKUP](../datasets/TRANSACT.BKUP.md)

Utility steps (IDCAMS, SORT and so on): STEP05, STEP10

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)

Documents can be out of date. When they disagree with the code, the code wins.
