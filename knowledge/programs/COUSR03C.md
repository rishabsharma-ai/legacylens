---
type: program
title: COUSR03C
description: Delete a user from USRSEC file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR03C.cbl
---

# COUSR03C

Delete a user from USRSEC file

Source: [app/cbl/COUSR03C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR03C.cbl) lines 1-359

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [COUSR03](../copybooks/COUSR03.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md), [COUSR00C](../programs/COUSR00C.md)
- Reads: [USRSEC](../datasets/USRSEC.md)
- Started by transaction: [CU03](../transactions/CU03.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COUSR03](../screens/COUSR03.md)
- Writes: [USRSEC](../datasets/USRSEC.md)

## Paragraphs (11)

- `MAIN-PARA` (line 82)
- `PROCESS-ENTER-KEY` (line 142)
- `DELETE-USER-INFO` (line 174)
- `RETURN-TO-PREV-SCREEN` (line 197)
- `SEND-USRDEL-SCREEN` (line 213)
- `RECEIVE-USRDEL-SCREEN` (line 230)
- `POPULATE-HEADER-INFO` (line 243)
- `READ-USER-SEC-FILE` (line 267)
- `DELETE-USER-SEC-FILE` (line 305)
- `CLEAR-CURRENT-SCREEN` (line 341)
- `INITIALIZE-ALL-FIELDS` (line 349)

## Documents that mention it

- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)

Documents can be out of date. When they disagree with the code, the code wins.
