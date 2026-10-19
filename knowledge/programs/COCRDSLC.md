---
type: program
title: COCRDSLC
description: Accept and process credit card detail request
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDSLC.cbl
---

# COCRDSLC

Accept and process credit card detail request

Source: [app/cbl/COCRDSLC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDSLC.cbl) lines 1-887

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COCRDSL](../copybooks/COCRDSL.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COCRDLIC](../programs/COCRDLIC.md), [COMEN01C](../programs/COMEN01C.md)
- Reads: [CARDDATA](../datasets/CARDDATA.md)
- Started by transaction: [CCDL](../transactions/CCDL.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COCRDSL](../screens/COCRDSL.md)

## Paragraphs (34)

- `0000-MAIN` (line 248)
- `COMMON-RETURN` (line 394)
- `0000-MAIN-EXIT` (line 408)
- `1000-SEND-MAP` (line 412)
- `1000-SEND-MAP-EXIT` (line 423)
- `1100-SCREEN-INIT` (line 427)
- `1100-SCREEN-INIT-EXIT` (line 453)
- `1200-SETUP-SCREEN-VARS` (line 457)
- `1200-SETUP-SCREEN-VARS-EXIT` (line 499)
- `1300-SETUP-SCREEN-ATTRS` (line 502)
- `1300-SETUP-SCREEN-ATTRS-EXIT` (line 559)
- `1400-SEND-SCREEN` (line 563)
- `1400-SEND-SCREEN-EXIT` (line 578)
- `2000-PROCESS-INPUTS` (line 582)
- `2000-PROCESS-INPUTS-EXIT` (line 593)
- `2100-RECEIVE-MAP` (line 596)
- `2100-RECEIVE-MAP-EXIT` (line 605)
- `2200-EDIT-MAP-INPUTS` (line 608)
- `2200-EDIT-MAP-INPUTS-EXIT` (line 643)
- `2210-EDIT-ACCOUNT` (line 647)
- `2210-EDIT-ACCOUNT-EXIT` (line 681)
- `2220-EDIT-CARD` (line 685)
- `2220-EDIT-CARD-EXIT` (line 722)
- `9000-READ-DATA` (line 726)
- `9000-READ-DATA-EXIT` (line 732)
- `9100-GETCARD-BYACCTCARD` (line 736)
- `9100-GETCARD-BYACCTCARD-EXIT` (line 775)
- `9150-GETCARD-BYACCT` (line 779)
- `9150-GETCARD-BYACCT-EXIT` (line 810)
- `SEND-LONG-TEXT` (line 820)
- `SEND-LONG-TEXT-EXIT` (line 831)
- `SEND-PLAIN-TEXT` (line 838)
- `SEND-PLAIN-TEXT-EXIT` (line 849)
- `ABEND-ROUTINE` (line 857)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
