---
type: program
title: CBTRN03C
description: Print the transaction detail report.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN03C.cbl
---

# CBTRN03C

Print the transaction detail report.

Source: [app/cbl/CBTRN03C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN03C.cbl) lines 1-649

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT03Y](../copybooks/CVACT03Y.md), [CVTRA03Y](../copybooks/CVTRA03Y.md), [CVTRA04Y](../copybooks/CVTRA04Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), [CVTRA07Y](../copybooks/CVTRA07Y.md)
- Reads: [CARDXREF](../datasets/CARDXREF.md), [DATEPARM](../datasets/DATEPARM.md), [TRANCATG](../datasets/TRANCATG.md), [TRANSACT.DALY](../datasets/TRANSACT.DALY.md), [TRANTYPE](../datasets/TRANTYPE.md)
- Run by job: [TRANREPT](../jobs/TRANREPT.md)
- Writes: [TRANREPT](../datasets/TRANREPT.md)

## Paragraphs (26)

- `0550-DATEPARM-READ` (line 220)
- `1000-TRANFILE-GET-NEXT` (line 248)
- `1100-WRITE-TRANSACTION-REPORT` (line 274)
- `1110-WRITE-PAGE-TOTALS` (line 293)
- `1120-WRITE-ACCOUNT-TOTALS` (line 306)
- `1110-WRITE-GRAND-TOTALS` (line 318)
- `1120-WRITE-HEADERS` (line 324)
- `1111-WRITE-REPORT-REC` (line 343)
- `1120-WRITE-DETAIL` (line 361)
- `0000-TRANFILE-OPEN` (line 376)
- `0100-REPTFILE-OPEN` (line 394)
- `0200-CARDXREF-OPEN` (line 412)
- `0300-TRANTYPE-OPEN` (line 430)
- `0400-TRANCATG-OPEN` (line 448)
- `0500-DATEPARM-OPEN` (line 466)
- `1500-A-LOOKUP-XREF` (line 484)
- `1500-B-LOOKUP-TRANTYPE` (line 494)
- `1500-C-LOOKUP-TRANCATG` (line 504)
- `9000-TRANFILE-CLOSE` (line 514)
- `9100-REPTFILE-CLOSE` (line 532)
- `9200-CARDXREF-CLOSE` (line 551)
- `9300-TRANTYPE-CLOSE` (line 569)
- `9400-TRANCATG-CLOSE` (line 587)
- `9500-DATEPARM-CLOSE` (line 605)
- `9999-ABEND-PROGRAM` (line 626)
- `9910-DISPLAY-IO-STATUS` (line 633)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [CARD-110: Transaction report request from the online menu](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-110`)

Documents can be out of date. When they disagree with the code, the code wins.
