---
type: program
title: COCRDLIC
description: List Credit Cards a) All cards if no context passed and admin user b)
  Only the ones associated with ACCT in COMMAREA if user is not admin
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDLIC.cbl
---

# COCRDLIC

List Credit Cards a) All cards if no context passed and admin user b) Only the ones associated with ACCT in COMMAREA if user is not admin

Source: [app/cbl/COCRDLIC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDLIC.cbl) lines 1-1459

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COCRDLI](../copybooks/COCRDLI.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COCRDLIC](../programs/COCRDLIC.md), [COMEN01C](../programs/COMEN01C.md)
- Reads: [CARDDATA](../datasets/CARDDATA.md)
- Started by transaction: [CCLI](../transactions/CCLI.md)
- Transfers control to (XCTL): [COCRDLIC](../programs/COCRDLIC.md), [COCRDSLC](../programs/COCRDSLC.md), [COCRDUPC](../programs/COCRDUPC.md), [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COCRDLI](../screens/COCRDLI.md)

## Business rules

- `9100-READ-BACKWARDS` line 1284: COMPUTE WS-SCRN-COUNTER =

## Paragraphs (39)

- `0000-MAIN` (line 298)
- `COMMON-RETURN` (line 604)
- `0000-MAIN-EXIT` (line 621)
- `1000-SEND-MAP` (line 624)
- `1000-SEND-MAP-EXIT` (line 639)
- `1100-SCREEN-INIT` (line 642)
- `1100-SCREEN-INIT-EXIT` (line 674)
- `1200-SCREEN-ARRAY-INIT` (line 678)
- `1200-SCREEN-ARRAY-INIT-EXIT` (line 745)
- `1250-SETUP-ARRAY-ATTRIBS` (line 748)
- `1250-SETUP-ARRAY-ATTRIBS-EXIT` (line 834)
- `1300-SETUP-SCREEN-ATTRS` (line 837)
- `1300-SETUP-SCREEN-ATTRS-EXIT` (line 890)
- `1400-SETUP-MESSAGE` (line 895)
- `1400-SETUP-MESSAGE-EXIT` (line 933)
- `1500-SEND-SCREEN` (line 938)
- `1500-SEND-SCREEN-EXIT` (line 948)
- `2000-RECEIVE-MAP` (line 951)
- `2000-RECEIVE-MAP-EXIT` (line 959)
- `2100-RECEIVE-SCREEN` (line 962)
- `2100-RECEIVE-SCREEN-EXIT` (line 981)
- `2200-EDIT-INPUTS` (line 985)
- `2200-EDIT-INPUTS-EXIT` (line 999)
- `2210-EDIT-ACCOUNT` (line 1003)
- `2210-EDIT-ACCOUNT-EXIT` (line 1032)
- `2220-EDIT-CARD` (line 1036)
- `2220-EDIT-CARD-EXIT` (line 1069)
- `2250-EDIT-ARRAY` (line 1073)
- `2250-EDIT-ARRAY-EXIT` (line 1119)
- `9000-READ-FORWARD` (line 1123)
- `9000-READ-FORWARD-EXIT` (line 1261)
- `9100-READ-BACKWARDS` (line 1264)
- `9100-READ-BACKWARDS-EXIT` (line 1374)
- `9500-FILTER-RECORDS` (line 1382)
- `9500-FILTER-RECORDS-EXIT` (line 1409)
- `SEND-PLAIN-TEXT` (line 1422)
- `SEND-PLAIN-TEXT-EXIT` (line 1433)
- `SEND-LONG-TEXT` (line 1441)
- `SEND-LONG-TEXT-EXIT` (line 1452)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
