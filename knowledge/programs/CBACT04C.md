---
type: program
title: CBACT04C
description: This is a interest calculator program.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT04C.cbl
---

# CBACT04C

This is a interest calculator program.

Source: [app/cbl/CBACT04C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT04C.cbl) lines 1-652

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVTRA01Y](../copybooks/CVTRA01Y.md), [CVTRA02Y](../copybooks/CVTRA02Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [DISCGRP](../datasets/DISCGRP.md), [TCATBALF](../datasets/TCATBALF.md)
- Run by job: [INTCALC](../jobs/INTCALC.md)
- Writes: [ACCTDATA](../datasets/ACCTDATA.md), [SYSTRAN](../datasets/SYSTRAN.md)

## Business rules

- `1300-COMPUTE-INTEREST` line 464: COMPUTE WS-MONTHLY-INT = ( TRAN-CAT-BAL * DIS-INT-RATE) / 1200

## Paragraphs (22)

- `0000-TCATBALF-OPEN` (line 234)
- `0100-XREFFILE-OPEN` (line 252)
- `0200-DISCGRP-OPEN` (line 270)
- `0300-ACCTFILE-OPEN` (line 289)
- `0400-TRANFILE-OPEN` (line 307)
- `1000-TCATBALF-GET-NEXT` (line 325)
- `1050-UPDATE-ACCOUNT` (line 350)
- `1100-GET-ACCT-DATA` (line 372)
- `1110-GET-XREF-DATA` (line 393)
- `1200-GET-INTEREST-RATE` (line 415)
- `1200-A-GET-DEFAULT-INT-RATE` (line 443)
- `1300-COMPUTE-INTEREST` (line 462)
- `1300-B-WRITE-TX` (line 473)
- `1400-COMPUTE-FEES` (line 518)
- `9000-TCATBALF-CLOSE` (line 522)
- `9100-XREFFILE-CLOSE` (line 541)
- `9200-DISCGRP-CLOSE` (line 559)
- `9300-ACCTFILE-CLOSE` (line 577)
- `9400-TRANFILE-CLOSE` (line 595)
- `Z-GET-DB2-FORMAT-TIMESTAMP` (line 613)
- `9999-ABEND-PROGRAM` (line 628)
- `9910-DISPLAY-IO-STATUS` (line 635)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [Transaction Posting Rules](../../corpus/docs/confluence/2003-transaction-posting-rules.md) (`CONFLUENCE:2003`)
- [Interest Calculation Design](../../corpus/docs/confluence/2004-interest-calculation-design.md) (`CONFLUENCE:2004`)
- [CARD-102: Implement fee computation in the interest job](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-102`)
- [CARD-106: Accounts with a missing disclosure group silently get the DEFAULT rate](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-106`)
- [CARD-112: Document the interest formula for auditors](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-112`)

Documents can be out of date. When they disagree with the code, the code wins.
