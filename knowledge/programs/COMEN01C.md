---
type: program
title: COMEN01C
description: Main Menu for the Regular users
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COMEN01C.cbl
---

# COMEN01C

Main Menu for the Regular users

Source: [app/cbl/COMEN01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COMEN01C.cbl) lines 1-308

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COMEN01](../copybooks/COMEN01.md), [COMEN02Y](../copybooks/COMEN02Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md)
- Started by transaction: [CM00](../transactions/CM00.md)
- Transfers control to (XCTL): [COACTUPC](../programs/COACTUPC.md), [COACTVWC](../programs/COACTVWC.md), [COBIL00C](../programs/COBIL00C.md), [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COPAUS0C](../programs/COPAUS0C.md), [CORPT00C](../programs/CORPT00C.md), [COSGN00C](../programs/COSGN00C.md), [COTRN00C](../programs/COTRN00C.md), [COTRN01C](../programs/COTRN01C.md), [COTRN02C](../programs/COTRN02C.md)
- Uses screen: [COMEN01](../screens/COMEN01.md)

## Paragraphs (7)

- `MAIN-PARA` (line 75)
- `PROCESS-ENTER-KEY` (line 115)
- `RETURN-TO-SIGNON-SCREEN` (line 196)
- `SEND-MENU-SCREEN` (line 208)
- `RECEIVE-MENU-SCREEN` (line 225)
- `POPULATE-HEADER-INFO` (line 238)
- `BUILD-MENU-OPTIONS` (line 262)

## Transfers the parser could not resolve

- XCTL at line 156, operand `CDEMO-MENU-OPT-PGMNAME(WS-OPTION)`
- XCTL at line 184, operand `CDEMO-MENU-OPT-PGMNAME(WS-OPTION)`

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)
- [Online Sign-on and Security](../../corpus/docs/confluence/2005-online-signon-and-security.md) (`CONFLUENCE:2005`)
- [CARD-107: Add a Statements option to the main menu](../../corpus/docs/jira/tickets.jsonl) (`JIRA:CARD-107`)

Documents can be out of date. When they disagree with the code, the code wins.
