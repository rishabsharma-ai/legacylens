---
type: program
title: COTRN02C
description: Add a new Transaction to TRANSACT file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN02C.cbl
---

# COTRN02C

Add a new Transaction to TRANSACT file

Source: [app/cbl/COTRN02C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COTRN02C.cbl) lines 1-783

## Relationships

- Calls: [CSUTLDTC](../programs/CSUTLDTC.md)
- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTRN02](../copybooks/COTRN02.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md)
- Reads: [CARDXREF](../datasets/CARDXREF.md), [TRANSACT](../datasets/TRANSACT.md)
- Started by transaction: [CT02](../transactions/CT02.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COTRN02](../screens/COTRN02.md)
- Writes: [TRANSACT](../datasets/TRANSACT.md)

## Business rules

- `VALIDATE-INPUT-KEY-FIELDS` line 204: COMPUTE WS-ACCT-ID-N = FUNCTION NUMVAL(ACTIDINI OF COTRN2AI)
- `VALIDATE-INPUT-KEY-FIELDS` line 218: COMPUTE WS-CARD-NUM-N = FUNCTION NUMVAL(CARDNINI OF COTRN2AI)
- `VALIDATE-INPUT-DATA-FIELDS` line 383: COMPUTE WS-TRAN-AMT-N = FUNCTION NUMVAL-C(TRNAMTI OF COTRN2AI)
- `ADD-TRANSACTION` line 456: COMPUTE WS-TRAN-AMT-N = FUNCTION NUMVAL-C(TRNAMTI OF COTRN2AI)

## Paragraphs (18)

- `MAIN-PARA` (line 107)
- `PROCESS-ENTER-KEY` (line 164)
- `VALIDATE-INPUT-KEY-FIELDS` (line 193)
- `VALIDATE-INPUT-DATA-FIELDS` (line 235)
- `ADD-TRANSACTION` (line 442)
- `COPY-LAST-TRAN-DATA` (line 471)
- `RETURN-TO-PREV-SCREEN` (line 500)
- `SEND-TRNADD-SCREEN` (line 516)
- `RECEIVE-TRNADD-SCREEN` (line 539)
- `POPULATE-HEADER-INFO` (line 552)
- `READ-CXACAIX-FILE` (line 576)
- `READ-CCXREF-FILE` (line 609)
- `STARTBR-TRANSACT-FILE` (line 642)
- `READPREV-TRANSACT-FILE` (line 673)
- `ENDBR-TRANSACT-FILE` (line 702)
- `WRITE-TRANSACT-FILE` (line 711)
- `CLEAR-CURRENT-SCREEN` (line 754)
- `INITIALIZE-ALL-FIELDS` (line 762)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
