---
type: program
title: COUSR02C
description: Update a user in USRSEC file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR02C.cbl
---

# COUSR02C

Update a user in USRSEC file

Source: [app/cbl/COUSR02C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR02C.cbl) lines 1-414

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [COUSR02](../copybooks/COUSR02.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md), [COUSR00C](../programs/COUSR00C.md)
- Reads: [USRSEC](../datasets/USRSEC.md)
- Started by transaction: [CU02](../transactions/CU02.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COUSR02](../screens/COUSR02.md)
- Writes: [USRSEC](../datasets/USRSEC.md)

## Paragraphs (11)

- `MAIN-PARA` (line 82)
- `PROCESS-ENTER-KEY` (line 143)
- `UPDATE-USER-INFO` (line 177)
- `RETURN-TO-PREV-SCREEN` (line 250)
- `SEND-USRUPD-SCREEN` (line 266)
- `RECEIVE-USRUPD-SCREEN` (line 283)
- `POPULATE-HEADER-INFO` (line 296)
- `READ-USER-SEC-FILE` (line 320)
- `UPDATE-USER-SEC-FILE` (line 358)
- `CLEAR-CURRENT-SCREEN` (line 395)
- `INITIALIZE-ALL-FIELDS` (line 403)

## Documents that mention it

- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)
- [CARD-103: Sign-on compares passwords in plain text](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-103`)

Documents can be out of date. When they disagree with the code, the code wins.
