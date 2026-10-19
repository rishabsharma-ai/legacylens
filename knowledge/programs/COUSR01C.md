---
type: program
title: COUSR01C
description: Add a new Regular/Admin user to USRSEC file
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR01C.cbl
---

# COUSR01C

Add a new Regular/Admin user to USRSEC file

Source: [app/cbl/COUSR01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COUSR01C.cbl) lines 1-299

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [COUSR01](../copybooks/COUSR01.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md)
- Started by transaction: [CU01](../transactions/CU01.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COUSR01](../screens/COUSR01.md)
- Writes: [USRSEC](../datasets/USRSEC.md)

## Paragraphs (9)

- `MAIN-PARA` (line 71)
- `PROCESS-ENTER-KEY` (line 115)
- `RETURN-TO-PREV-SCREEN` (line 165)
- `SEND-USRADD-SCREEN` (line 184)
- `RECEIVE-USRADD-SCREEN` (line 201)
- `POPULATE-HEADER-INFO` (line 214)
- `WRITE-USER-SEC-FILE` (line 238)
- `CLEAR-CURRENT-SCREEN` (line 279)
- `INITIALIZE-ALL-FIELDS` (line 287)

## Documents that mention it

- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)
- [CARD-103: Sign-on compares passwords in plain text](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-103`)

Documents can be out of date. When they disagree with the code, the code wins.
