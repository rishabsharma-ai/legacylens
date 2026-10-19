---
type: program
title: COTRTLIC
description: List Transaction Type for updates and deletes
tags:
- db2-transaction-type
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/cbl/COTRTLIC.cbl
---

# COTRTLIC

List Transaction Type for updates and deletes

Source: [app/app-transaction-type-db2/cbl/COTRTLIC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/cbl/COTRTLIC.cbl) lines 1-2098

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COTRTLI](../copybooks/COTRTLI.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSDB2RPY](../copybooks/CSDB2RPY.md), [CSDB2RWY](../copybooks/CSDB2RWY.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), [DCLTRTYP](../copybooks/DCLTRTYP.md), `DFHAID`, `DFHBMSCA`, `SQLCA`
- Reached by XCTL from: [COADM01C](../programs/COADM01C.md)
- Reads: [TRANSACTION_TYPE](../datasets/TRANSACTION_TYPE.md)
- Transfers control to (XCTL): [COADM01C](../programs/COADM01C.md), [COTRTUPC](../programs/COTRTUPC.md)
- Uses screen: [COTRTLI](../screens/COTRTLI.md)
- Writes: [TRANSACTION_TYPE](../datasets/TRANSACTION_TYPE.md)

## Business rules

- `1210-EDIT-ARRAY` line 1003: COMPUTE WS-ACTIONS-REQUESTED = WS-MAX-SCREEN-LINES - WS-NO-ACTIONS-SELECTED
- `1210-EDIT-ARRAY` line 1006: COMPUTE COMPUTE WS-VALID-ACTIONS-SELECTED =
- `2500-SETUP-MESSAGE` line 1562: COMPUTE WS-STRING-LEN =
- `2500-SETUP-MESSAGE` line 1566: COMPUTE WS-STRING-MID = (FUNCTION LENGTH(WS-INFO-MSG) - WS-STRING-LEN) / 2 + 1
- `8100-READ-BACKWARDS` line 1735: COMPUTE WS-ROW-NUMBER =
- `9200-UPDATE-RECORD` line 1843: COMPUTE DCL-TR-DESCRIPTION-LEN = FUNCTION LENGTH(WS-ROW-TR-DESC-IN (I-SELECTED))

## Paragraphs (56)

- `0000-MAIN` (line 498)
- `COMMON-RETURN` (line 899)
- `0000-MAIN-EXIT` (line 916)
- `1000-RECEIVE-MAP` (line 919)
- `1000-RECEIVE-MAP-EXIT` (line 926)
- `1100-RECEIVE-SCREEN` (line 930)
- `1100-RECEIVE-SCREEN-EXIT` (line 956)
- `1200-EDIT-INPUTS` (line 960)
- `1200-EDIT-INPUTS-EXIT` (line 978)
- `1210-EDIT-ARRAY` (line 982)
- `1210-EDIT-ARRAY-EXIT` (line 1055)
- `1211-EDIT-ARRAY-DESC` (line 1060)
- `1211-EDIT-ARRAY-DESC-EXIT` (line 1092)
- `1220-EDIT-TYPECD` (line 1096)
- `1220-EDIT-TYPECD-EXIT` (line 1125)
- `1230-EDIT-DESC` (line 1142)
- `1230-EDIT-DESC-EXIT` (line 1165)
- `1240-EDIT-ALPHANUM-REQD` (line 1181)
- `1240-EDIT-ALPHANUM-REQD-EXIT` (line 1235)
- `1290-CROSS-EDITS` (line 1239)
- `1290-CROSS-EDITS-EXIT` (line 1269)
- `2000-SEND-MAP-EXIT` (line 1290)
- `2100-SCREEN-INIT` (line 1293)
- `2100-SCREEN-INIT-EXIT` (line 1325)
- `2200-SETUP-ARRAY-ATTRIBS` (line 1329)
- `2200-SETUP-ARRAY-ATTRIBS-EXIT` (line 1377)
- `2300-SCREEN-ARRAY-INIT` (line 1383)
- `2300-SCREEN-ARRAY-INIT-EXIT` (line 1433)
- `2400-SETUP-SCREEN-ATTRS` (line 1438)
- `2400-SETUP-SCREEN-ATTRS-EXIT` (line 1499)
- `2500-SETUP-MESSAGE` (line 1504)
- `2500-SETUP-MESSAGE-EXIT` (line 1582)
- `2600-SEND-SCREEN` (line 1587)
- `2600-SEND-SCREEN-EXIT` (line 1597)
- `8000-READ-FORWARD` (line 1603)
- `8000-READ-FORWARD-EXIT` (line 1724)
- `8100-READ-BACKWARDS` (line 1727)
- `8100-READ-BACKWARDS-EXIT` (line 1794)
- `9100-CHECK-FILTERS` (line 1801)
- `9100-CHECK-FILTERS-EXIT` (line 1834)
- `9200-UPDATE-RECORD` (line 1837)
- `9200-UPDATE-RECORD-EXIT` (line 1892)
- `9300-DELETE-RECORD` (line 1896)
- `9300-DELETE-RECORD-EXIT` (line 1938)
- `9400-OPEN-FORWARD-CURSOR` (line 1942)
- `9400-OPEN-FORWARD-CURSOR-EXIT` (line 1965)
- `9450-CLOSE-FORWARD-CURSOR` (line 1970)
- `9450-CLOSE-FORWARD-CURSOR-EXIT` (line 1993)
- `9500-OPEN-BACKWARD-CURSOR` (line 1997)
- `9500-OPEN-BACKWARD-CURSOR-EXIT` (line 2021)
- `9550-CLOSE-BACK-CURSOR` (line 2026)
- `9550-CLOSE-BACK-CURSOR-EXIT` (line 2049)
- `SEND-PLAIN-TEXT` (line 2066)
- `SEND-PLAIN-TEXT-EXIT` (line 2077)
- `SEND-LONG-TEXT` (line 2085)
- `SEND-LONG-TEXT-EXIT` (line 2096)
