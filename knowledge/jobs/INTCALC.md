---
type: job
title: INTCALC
description: Batch job that runs CBACT04C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/INTCALC.jcl
---

# INTCALC

Batch job that runs CBACT04C.

Source: [app/jcl/INTCALC.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/INTCALC.jcl)

## Relationships

- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [DISCGRP](../datasets/DISCGRP.md), [TCATBALF](../datasets/TCATBALF.md)
- Runs: [CBACT04C](../programs/CBACT04C.md)
- Writes: [SYSTRAN](../datasets/SYSTRAN.md)

## Steps

- `STEP15` runs [CBACT04C](../programs/CBACT04C.md)

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [Transaction Posting Rules](../../corpus/docs/confluence/2003-transaction-posting-rules.md) (`CONFLUENCE:2003`)
- [Interest Calculation Design](../../corpus/docs/confluence/2004-interest-calculation-design.md) (`CONFLUENCE:2004`)
- [CARD-102: Implement fee computation in the interest job](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-102`)
- [CARD-106: Accounts with a missing disclosure group silently get the DEFAULT rate](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-106`)

Documents can be out of date. When they disagree with the code, the code wins.
