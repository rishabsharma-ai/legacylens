---
type: program
title: COTRN01C
description: View a Transaction from TRANSACT file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN01C.cbl
---

# COTRN01C

View a Transaction from TRANSACT file

Source: [app/cbl/COTRN01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN01C.cbl) lines 1-330

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTRN01](../copybooks/COTRN01.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md), [COTRN00C](../programs/COTRN00C.md)
- Reads: [TRANSACT](../datasets/TRANSACT.md)
- Started by transaction: [CT01](../transactions/CT01.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md)
- Uses screen: [COTRN01](../screens/COTRN01.md)

## Paragraphs (9)

- `MAIN-PARA` (line 86)
- `PROCESS-ENTER-KEY` (line 144)
- `RETURN-TO-PREV-SCREEN` (line 197)
- `SEND-TRNVIEW-SCREEN` (line 213)
- `RECEIVE-TRNVIEW-SCREEN` (line 230)
- `POPULATE-HEADER-INFO` (line 243)
- `READ-TRANSACT-FILE` (line 267)
- `CLEAR-CURRENT-SCREEN` (line 301)
- `INITIALIZE-ALL-FIELDS` (line 309)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
