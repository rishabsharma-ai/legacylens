---
type: program
title: CBTRN02C
description: Post the records from daily transaction file.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN02C.cbl
---

# CBTRN02C

Post the records from daily transaction file.

Source: [app/cbl/CBTRN02C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN02C.cbl) lines 1-731

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVTRA01Y](../copybooks/CVTRA01Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), [CVTRA06Y](../copybooks/CVTRA06Y.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [DALYTRAN](../datasets/DALYTRAN.md), [TCATBALF](../datasets/TCATBALF.md)
- Run by job: [POSTTRAN](../jobs/POSTTRAN.md)
- Writes: [ACCTDATA](../datasets/ACCTDATA.md), [DALYREJS](../datasets/DALYREJS.md), [TCATBALF](../datasets/TCATBALF.md), [TRANSACT](../datasets/TRANSACT.md)

## Business rules

- `1500-A-LOOKUP-XREF` line 385: Reason 100: INVALID CARD NUMBER FOUND
- `1500-B-LOOKUP-ACCT` line 397: Reason 101: ACCOUNT RECORD NOT FOUND
- `1500-B-LOOKUP-ACCT` line 403: COMPUTE WS-TEMP-BAL = ACCT-CURR-CYC-CREDIT - ACCT-CURR-CYC-DEBIT + DALYTRAN-AMT
- `1500-B-LOOKUP-ACCT` line 410: Reason 102: OVERLIMIT TRANSACTION
- `1500-B-LOOKUP-ACCT` line 417: Reason 103: TRANSACTION RECEIVED AFTER ACCT EXPIRATION
- `2800-UPDATE-ACCOUNT-REC` line 556: Reason 109: ACCOUNT RECORD NOT FOUND

## Paragraphs (26)

- `0000-DALYTRAN-OPEN` (line 236)
- `0100-TRANFILE-OPEN` (line 254)
- `0200-XREFFILE-OPEN` (line 273)
- `0300-DALYREJS-OPEN` (line 291)
- `0400-ACCTFILE-OPEN` (line 309)
- `0500-TCATBALF-OPEN` (line 327)
- `1000-DALYTRAN-GET-NEXT` (line 345)
- `1500-VALIDATE-TRAN` (line 370)
- `1500-A-LOOKUP-XREF` (line 380)
- `1500-B-LOOKUP-ACCT` (line 393)
- `2000-POST-TRANSACTION` (line 424)
- `2500-WRITE-REJECT-REC` (line 446)
- `2700-UPDATE-TCATBAL` (line 467)
- `2700-A-CREATE-TCATBAL-REC` (line 503)
- `2700-B-UPDATE-TCATBAL-REC` (line 526)
- `2800-UPDATE-ACCOUNT-REC` (line 545)
- `2900-WRITE-TRANSACTION-FILE` (line 562)
- `9000-DALYTRAN-CLOSE` (line 582)
- `9100-TRANFILE-CLOSE` (line 600)
- `9200-XREFFILE-CLOSE` (line 619)
- `9300-DALYREJS-CLOSE` (line 637)
- `9400-ACCTFILE-CLOSE` (line 655)
- `9500-TCATBALF-CLOSE` (line 674)
- `Z-GET-DB2-FORMAT-TIMESTAMP` (line 692)
- `9999-ABEND-PROGRAM` (line 707)
- `9910-DISPLAY-IO-STATUS` (line 714)

## Documents that mention it

- [Nightly Batch Runbook](../../corpus/docs/confluence/2002-nightly-batch-runbook.md) (`CONFLUENCE:2002`)
- [Transaction Posting Rules](../../corpus/docs/confluence/2003-transaction-posting-rules.md) (`CONFLUENCE:2003`)
- [Interest Calculation Design](../../corpus/docs/confluence/2004-interest-calculation-design.md) (`CONFLUENCE:2004`)
- [CARD-101: Spike in overlimit rejects after credit limit migration](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-101`)
- [CARD-105: Field name typo ACCT-EXPIRAION-DATE](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-105`)
- [CARD-111: Nightly batch overran into the online window](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-111`)

Documents can be out of date. When they disagree with the code, the code wins.
