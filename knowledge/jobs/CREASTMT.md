---
type: job
title: CREASTMT
description: Batch job that runs CBSTM03A.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CREASTMT.JCL
---

# CREASTMT

Batch job that runs CBSTM03A.

Source: [app/jcl/CREASTMT.JCL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CREASTMT.JCL)

## Relationships

- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md), [TRANSACT](../datasets/TRANSACT.md), [TRXFL](../datasets/TRXFL.md), [TRXFL.SEQ](../datasets/TRXFL.SEQ.md)
- Runs: [CBSTM03A](../programs/CBSTM03A.md)
- Writes: [STATEMNT](../datasets/STATEMNT.md), [STATEMNT.HTML](../datasets/STATEMNT.HTML.md), [TRXFL.SEQ](../datasets/TRXFL.SEQ.md)

## Steps

- `STEP040` runs [CBSTM03A](../programs/CBSTM03A.md)

Utility steps (IDCAMS, SORT and so on): DELDEF01, STEP010, STEP020, STEP030

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [CARD-108: CREASTMT abended S0C7 in statement step](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-108`)

Documents can be out of date. When they disagree with the code, the code wins.
