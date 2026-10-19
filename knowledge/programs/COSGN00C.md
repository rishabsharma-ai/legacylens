---
type: program
title: COSGN00C
description: Signon Screen for the CardDemo Application
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COSGN00C.cbl
---

# COSGN00C

Signon Screen for the CardDemo Application

Source: [app/cbl/COSGN00C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COSGN00C.cbl) lines 1-260

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COSGN00](../copybooks/COSGN00.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md), [COBIL00C](../programs/COBIL00C.md), [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)
- Reads: [USRSEC](../datasets/USRSEC.md)
- Started by transaction: [CC00](../transactions/CC00.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COSGN00](../screens/COSGN00.md)

## Paragraphs (6)

- `MAIN-PARA` (line 73)
- `PROCESS-ENTER-KEY` (line 108)
- `SEND-SIGNON-SCREEN` (line 145)
- `SEND-PLAIN-TEXT` (line 162)
- `POPULATE-HEADER-INFO` (line 177)
- `READ-USER-SEC-FILE` (line 209)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)
- [CARD-103: Sign-on compares passwords in plain text](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-103`)
- [CARD-111: Nightly batch overran into the online window](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-111`)

Documents can be out of date. When they disagree with the code, the code wins.
