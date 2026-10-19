---
type: program
title: CBSTM03A
description: Print Account Statements from Transaction data
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBSTM03A.CBL
---

# CBSTM03A

Print Account Statements from Transaction data

Source: [app/cbl/CBSTM03A.CBL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBSTM03A.CBL) lines 1-924

## Relationships

- Calls: [CBSTM03B](../programs/CBSTM03B.md), `CEE3ABD`
- Includes: [COSTM01](../copybooks/COSTM01.md), [CUSTREC](../copybooks/CUSTREC.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md)
- Run by job: [CREASTMT](../jobs/CREASTMT.md)
- Writes: [STATEMNT.HTML](../datasets/STATEMNT.HTML.md)

## Business rules

- `2000-CUSTFILE-GET` line 374: COMPUTE WS-M03B-KEY-LN = LENGTH OF XREF-CUST-ID
- `3000-ACCTFILE-GET` line 398: COMPUTE WS-M03B-KEY-LN = LENGTH OF XREF-ACCT-ID

## Paragraphs (25)

- `0000-START` (line 296)
- `1000-MAINLINE` (line 316)
- `9999-GOBACK` (line 341)
- `1000-XREFFILE-GET-NEXT` (line 345)
- `2000-CUSTFILE-GET` (line 368)
- `3000-ACCTFILE-GET` (line 392)
- `4000-TRNXFILE-GET` (line 416)
- `5000-CREATE-STATEMENT` (line 458)
- `5100-WRITE-HTML-HEADER` (line 506)
- `5100-EXIT` (line 554)
- `5200-WRITE-HTML-NMADBS` (line 558)
- `5200-EXIT` (line 671)
- `6000-WRITE-TRANS` (line 675)
- `8100-FILE-OPEN` (line 726)
- `8100-TRNXFILE-OPEN` (line 730)
- `8200-XREFFILE-OPEN` (line 765)
- `8300-CUSTFILE-OPEN` (line 783)
- `8400-ACCTFILE-OPEN` (line 801)
- `8500-READTRNX-READ` (line 818)
- `8599-EXIT` (line 849)
- `9100-TRNXFILE-CLOSE` (line 856)
- `9200-XREFFILE-CLOSE` (line 873)
- `9300-CUSTFILE-CLOSE` (line 889)
- `9400-ACCTFILE-CLOSE` (line 905)
- `9999-ABEND-PROGRAM` (line 921)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [CARD-107: Add a Statements option to the main menu](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-107`)
- [CARD-108: CREASTMT abended S0C7 in statement step](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-108`)

Documents can be out of date. When they disagree with the code, the code wins.
