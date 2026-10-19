---
type: program
title: COADM01C
description: Admin Menu for Admin users
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COADM01C.cbl
---

# COADM01C

Admin Menu for Admin users

Source: [app/cbl/COADM01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COADM01C.cbl) lines 1-288

## Relationships

- Includes: [COADM01](../copybooks/COADM01.md), [COADM02Y](../copybooks/COADM02Y.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COSGN00C](../programs/COSGN00C.md), [COTRTLIC](../programs/COTRTLIC.md), [COTRTUPC](../programs/COTRTUPC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)
- Started by transaction: [CA00](../transactions/CA00.md)
- Transfers control to (XCTL): [COSGN00C](../programs/COSGN00C.md), [COTRTLIC](../programs/COTRTLIC.md), [COTRTUPC](../programs/COTRTUPC.md), [COUSR00C](../programs/COUSR00C.md), [COUSR01C](../programs/COUSR01C.md), [COUSR02C](../programs/COUSR02C.md), [COUSR03C](../programs/COUSR03C.md)
- Uses screen: [COADM01](../screens/COADM01.md)

## Paragraphs (8)

- `MAIN-PARA` (line 75)
- `PROCESS-ENTER-KEY` (line 119)
- `RETURN-TO-SIGNON-SCREEN` (line 163)
- `SEND-MENU-SCREEN` (line 175)
- `RECEIVE-MENU-SCREEN` (line 192)
- `POPULATE-HEADER-INFO` (line 205)
- `BUILD-MENU-OPTIONS` (line 229)
- `PGMIDERR-ERR-PARA` (line 270)

## Transfers the parser could not resolve

- XCTL at line 145, operand `CDEMO-ADMIN-OPT-PGMNAME(WS-OPTION)`

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)

Documents can be out of date. When they disagree with the code, the code wins.
