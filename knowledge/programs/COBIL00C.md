---
type: program
title: COBIL00C
description: Bill Payment - Pay account balance in full and a tractionsaction for
  the online bill payment.
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COBIL00C.cbl
---

# COBIL00C

Bill Payment - Pay account balance in full and a tractionsaction for the online bill payment.

Source: [app/cbl/COBIL00C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COBIL00C.cbl) lines 1-572

## Relationships

- Includes: [COBIL00](../copybooks/COBIL00.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [TRANSACT](../datasets/TRANSACT.md)
- Started by transaction: [CB00](../transactions/CB00.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COBIL00](../screens/COBIL00.md)
- Writes: [ACCTDATA](../datasets/ACCTDATA.md), [TRANSACT](../datasets/TRANSACT.md)

## Business rules

- `PROCESS-ENTER-KEY` line 234: COMPUTE ACCT-CURR-BAL = ACCT-CURR-BAL - TRAN-AMT

## Paragraphs (16)

- `MAIN-PARA` (line 99)
- `PROCESS-ENTER-KEY` (line 154)
- `GET-CURRENT-TIMESTAMP` (line 249)
- `RETURN-TO-PREV-SCREEN` (line 273)
- `SEND-BILLPAY-SCREEN` (line 289)
- `RECEIVE-BILLPAY-SCREEN` (line 306)
- `POPULATE-HEADER-INFO` (line 319)
- `READ-ACCTDAT-FILE` (line 343)
- `UPDATE-ACCTDAT-FILE` (line 377)
- `READ-CXACAIX-FILE` (line 408)
- `STARTBR-TRANSACT-FILE` (line 441)
- `READPREV-TRANSACT-FILE` (line 472)
- `ENDBR-TRANSACT-FILE` (line 501)
- `WRITE-TRANSACT-FILE` (line 510)
- `CLEAR-CURRENT-SCREEN` (line 552)
- `INITIALIZE-ALL-FIELDS` (line 560)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Bill Payment Feature](../../corpus/docs/confluence/2006-bill-payment-feature.md) (`CONFLUENCE:2006`)
- [CARD-104: Duplicate transaction IDs from concurrent bill payments](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-104`)
- [CARD-109: Allow partial bill payments](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-109`)

Documents can be out of date. When they disagree with the code, the code wins.
