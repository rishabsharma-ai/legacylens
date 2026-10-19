---
type: job
title: COMBTRAN
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/COMBTRAN.jcl
---

# COMBTRAN

Batch job (utilities only).

Source: [app/jcl/COMBTRAN.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/COMBTRAN.jcl)

## Relationships

- Reads: [SYSTRAN](../datasets/SYSTRAN.md), [TRANSACT](../datasets/TRANSACT.md), [TRANSACT.BKUP](../datasets/TRANSACT.BKUP.md), [TRANSACT.COMBINED](../datasets/TRANSACT.COMBINED.md)
- Writes: [TRANSACT.COMBINED](../datasets/TRANSACT.COMBINED.md)

Utility steps (IDCAMS, SORT and so on): STEP05R, STEP10

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [Interest Calculation Design](../../corpus/docs/confluence/2004-interest-calculation-design.md) (`CONFLUENCE:2004`)

Documents can be out of date. When they disagree with the code, the code wins.
