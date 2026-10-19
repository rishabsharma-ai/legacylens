---
type: program
title: COACTVWC
description: Accept and process Account View request
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COACTVWC.cbl
---

# COACTVWC

Accept and process Account View request

Source: [app/cbl/COACTVWC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COACTVWC.cbl) lines 1-941

## Relationships

- Includes: [COACTVW](../copybooks/COACTVW.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md)
- Started by transaction: [CAVW](../transactions/CAVW.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COACTVW](../screens/COACTVW.md)

## Paragraphs (34)

- `0000-MAIN` (line 262)
- `COMMON-RETURN` (line 394)
- `0000-MAIN-EXIT` (line 408)
- `1000-SEND-MAP` (line 416)
- `1000-SEND-MAP-EXIT` (line 427)
- `1100-SCREEN-INIT` (line 431)
- `1100-SCREEN-INIT-EXIT` (line 457)
- `1200-SETUP-SCREEN-VARS` (line 460)
- `1200-SETUP-SCREEN-VARS-EXIT` (line 537)
- `1300-SETUP-SCREEN-ATTRS` (line 541)
- `1300-SETUP-SCREEN-ATTRS-EXIT` (line 574)
- `1400-SEND-SCREEN` (line 577)
- `1400-SEND-SCREEN-EXIT` (line 592)
- `2000-PROCESS-INPUTS` (line 596)
- `2000-PROCESS-INPUTS-EXIT` (line 607)
- `2100-RECEIVE-MAP` (line 610)
- `2100-RECEIVE-MAP-EXIT` (line 619)
- `2200-EDIT-MAP-INPUTS` (line 622)
- `2200-EDIT-MAP-INPUTS-EXIT` (line 645)
- `2210-EDIT-ACCOUNT` (line 649)
- `2210-EDIT-ACCOUNT-EXIT` (line 683)
- `9000-READ-ACCT` (line 687)
- `9000-READ-ACCT-EXIT` (line 720)
- `9200-GETCARDXREF-BYACCT` (line 723)
- `9200-GETCARDXREF-BYACCT-EXIT` (line 771)
- `9300-GETACCTDATA-BYACCT` (line 774)
- `9300-GETACCTDATA-BYACCT-EXIT` (line 821)
- `9400-GETCUSTDATA-BYCUST` (line 825)
- `9400-GETCUSTDATA-BYCUST-EXIT` (line 870)
- `SEND-PLAIN-TEXT` (line 877)
- `SEND-PLAIN-TEXT-EXIT` (line 888)
- `SEND-LONG-TEXT` (line 896)
- `SEND-LONG-TEXT-EXIT` (line 907)
- `ABEND-ROUTINE` (line 916)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
