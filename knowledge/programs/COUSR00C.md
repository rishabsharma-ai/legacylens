---
type: program
title: COUSR00C
description: List all users from USRSEC file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR00C.cbl
---

# COUSR00C

List all users from USRSEC file

Source: [app/cbl/COUSR00C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR00C.cbl) lines 1-695

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [COUSR00](../copybooks/COUSR00.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md)
- Reads: [USRSEC](../datasets/USRSEC.md)
- Started by transaction: [CU00](../transactions/CU00.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COSGN00C](../programs/COSGN00C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)
- Uses screen: [COUSR00](../screens/COUSR00.md)

## Business rules

- `PROCESS-PAGE-FORWARD` line 304: COMPUTE WS-IDX = WS-IDX + 1
- `PROCESS-PAGE-FORWARD` line 309: COMPUTE CDEMO-CU00-PAGE-NUM = CDEMO-CU00-PAGE-NUM + 1
- `PROCESS-PAGE-FORWARD` line 320: COMPUTE CDEMO-CU00-PAGE-NUM = CDEMO-CU00-PAGE-NUM + 1
- `PROCESS-PAGE-BACKWARD` line 358: COMPUTE WS-IDX = WS-IDX - 1

## Paragraphs (16)

- `MAIN-PARA` (line 98)
- `PROCESS-ENTER-KEY` (line 149)
- `PROCESS-PF7-KEY` (line 237)
- `PROCESS-PF8-KEY` (line 260)
- `PROCESS-PAGE-FORWARD` (line 282)
- `PROCESS-PAGE-BACKWARD` (line 336)
- `POPULATE-USER-DATA` (line 384)
- `INITIALIZE-USER-DATA` (line 446)
- `RETURN-TO-PREV-SCREEN` (line 506)
- `SEND-USRLST-SCREEN` (line 522)
- `RECEIVE-USRLST-SCREEN` (line 549)
- `POPULATE-HEADER-INFO` (line 562)
- `STARTBR-USER-SEC-FILE` (line 586)
- `READNEXT-USER-SEC-FILE` (line 619)
- `READPREV-USER-SEC-FILE` (line 653)
- `ENDBR-USER-SEC-FILE` (line 687)

## Documents that mention it

- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)

Documents can be out of date. When they disagree with the code, the code wins.
