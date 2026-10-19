---
type: program
title: CORPT00C
description: Print Transaction reports by submitting batch job from online using extra
  partition TDQ.
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CORPT00C.cbl
---

# CORPT00C

Print Transaction reports by submitting batch job from online using extra partition TDQ.

Source: [app/cbl/CORPT00C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CORPT00C.cbl) lines 1-649

## Relationships

- Calls: [CSUTLDTC](../programs/CSUTLDTC.md)
- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [CORPT00](../copybooks/CORPT00.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md)
- Started by transaction: [CR00](../transactions/CR00.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [CORPT00](../screens/CORPT00.md)

## Business rules

- `PROCESS-ENTER-KEY` line 229: COMPUTE WS-CURDATE-N = FUNCTION DATE-OF-INTEGER(
- `PROCESS-ENTER-KEY` line 305: COMPUTE WS-NUM-99 = FUNCTION NUMVAL-C (SDTMMI OF CORPT0AI)
- `PROCESS-ENTER-KEY` line 309: COMPUTE WS-NUM-99 = FUNCTION NUMVAL-C (SDTDDI OF CORPT0AI)
- `PROCESS-ENTER-KEY` line 313: COMPUTE WS-NUM-9999 = FUNCTION NUMVAL-C (SDTYYYYI OF CORPT0AI)
- `PROCESS-ENTER-KEY` line 317: COMPUTE WS-NUM-99 = FUNCTION NUMVAL-C (EDTMMI OF CORPT0AI)
- `PROCESS-ENTER-KEY` line 321: COMPUTE WS-NUM-99 = FUNCTION NUMVAL-C (EDTDDI OF CORPT0AI)
- `PROCESS-ENTER-KEY` line 325: COMPUTE WS-NUM-9999 = FUNCTION NUMVAL-C (EDTYYYYI OF CORPT0AI)

## Paragraphs (10)

- `MAIN-PARA` (line 163)
- `PROCESS-ENTER-KEY` (line 208)
- `SUBMIT-JOB-TO-INTRDR` (line 462)
- `WIRTE-JOBSUB-TDQ` (line 515)
- `RETURN-TO-PREV-SCREEN` (line 540)
- `SEND-TRNRPT-SCREEN` (line 556)
- `RETURN-TO-CICS` (line 585)
- `RECEIVE-TRNRPT-SCREEN` (line 596)
- `POPULATE-HEADER-INFO` (line 609)
- `INITIALIZE-ALL-FIELDS` (line 633)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [CARD-110: Transaction report request from the online menu](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-110`)

Documents can be out of date. When they disagree with the code, the code wins.
