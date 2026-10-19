---
type: program
title: COTRN00C
description: List Transactions from TRANSACT file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN00C.cbl
---

# COTRN00C

List Transactions from TRANSACT file

Source: [app/cbl/COTRN00C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN00C.cbl) lines 1-699

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTRN00](../copybooks/COTRN00.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md), [COTRN01C](../programs/COTRN01C.md)
- Reads: [TRANSACT](../datasets/TRANSACT.md)
- Started by transaction: [CT00](../transactions/CT00.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN01C](../programs/COTRN01C.md)
- Uses screen: [COTRN00](../screens/COTRN00.md)

## Business rules

- `PROCESS-PAGE-FORWARD` line 301: COMPUTE WS-IDX = WS-IDX + 1
- `PROCESS-PAGE-FORWARD` line 306: COMPUTE CDEMO-CT00-PAGE-NUM = CDEMO-CT00-PAGE-NUM + 1
- `PROCESS-PAGE-FORWARD` line 317: COMPUTE CDEMO-CT00-PAGE-NUM = CDEMO-CT00-PAGE-NUM + 1
- `PROCESS-PAGE-BACKWARD` line 355: COMPUTE WS-IDX = WS-IDX - 1

## Paragraphs (16)

- `MAIN-PARA` (line 95)
- `PROCESS-ENTER-KEY` (line 146)
- `PROCESS-PF7-KEY` (line 234)
- `PROCESS-PF8-KEY` (line 257)
- `PROCESS-PAGE-FORWARD` (line 279)
- `PROCESS-PAGE-BACKWARD` (line 333)
- `POPULATE-TRAN-DATA` (line 381)
- `INITIALIZE-TRAN-DATA` (line 450)
- `RETURN-TO-PREV-SCREEN` (line 510)
- `SEND-TRNLST-SCREEN` (line 527)
- `RECEIVE-TRNLST-SCREEN` (line 554)
- `POPULATE-HEADER-INFO` (line 567)
- `STARTBR-TRANSACT-FILE` (line 591)
- `READNEXT-TRANSACT-FILE` (line 624)
- `READPREV-TRANSACT-FILE` (line 658)
- `ENDBR-TRANSACT-FILE` (line 692)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
