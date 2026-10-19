---
type: program
title: COCRDUPC
description: Accept and process credit card detail request
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDUPC.cbl
---

# COCRDUPC

Accept and process credit card detail request

Source: [app/cbl/COCRDUPC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COCRDUPC.cbl) lines 1-1560

## Relationships

- Includes: [COCOM01Y](../copybooks/COCOM01Y.md), [COCRDUP](../copybooks/COCRDUP.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COCRDLIC](../programs/COCRDLIC.md), [COMEN01C](../programs/COMEN01C.md)
- Reads: [CARDDATA](../datasets/CARDDATA.md)
- Started by transaction: [CCUP](../transactions/CCUP.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COCRDUP](../screens/COCRDUP.md)
- Writes: [CARDDATA](../datasets/CARDDATA.md)

## Paragraphs (45)

- `0000-MAIN` (line 367)
- `COMMON-RETURN` (line 546)
- `0000-MAIN-EXIT` (line 560)
- `1000-PROCESS-INPUTS` (line 564)
- `1000-PROCESS-INPUTS-EXIT` (line 575)
- `1100-RECEIVE-MAP` (line 578)
- `1100-RECEIVE-MAP-EXIT` (line 638)
- `1200-EDIT-MAP-INPUTS` (line 641)
- `1200-EDIT-MAP-INPUTS-EXIT` (line 717)
- `1210-EDIT-ACCOUNT` (line 721)
- `1210-EDIT-ACCOUNT-EXIT` (line 758)
- `1220-EDIT-CARD` (line 762)
- `1220-EDIT-CARD-EXIT` (line 802)
- `1230-EDIT-NAME` (line 806)
- `1230-EDIT-NAME-EXIT` (line 841)
- `1240-EDIT-CARDSTATUS` (line 845)
- `1240-EDIT-CARDSTATUS-EXIT` (line 874)
- `1250-EDIT-EXPIRY-MON` (line 877)
- `1250-EDIT-EXPIRY-MON-EXIT` (line 910)
- `1260-EDIT-EXPIRY-YEAR` (line 913)
- `1260-EDIT-EXPIRY-YEAR-EXIT` (line 945)
- `2000-DECIDE-ACTION` (line 948)
- `2000-DECIDE-ACTION-EXIT` (line 1029)
- `3000-SEND-MAP` (line 1035)
- `3000-SEND-MAP-EXIT` (line 1048)
- `3100-SCREEN-INIT` (line 1052)
- `3100-SCREEN-INIT-EXIT` (line 1078)
- `3200-SETUP-SCREEN-VARS` (line 1082)
- `3200-SETUP-SCREEN-VARS-EXIT` (line 1135)
- `3250-SETUP-INFOMSG` (line 1138)
- `3250-SETUP-INFOMSG-EXIT` (line 1165)
- `3300-SETUP-SCREEN-ATTRS` (line 1168)
- `3300-SETUP-SCREEN-ATTRS-EXIT` (line 1319)
- `3400-SEND-SCREEN` (line 1324)
- `3400-SEND-SCREEN-EXIT` (line 1338)
- `9000-READ-DATA` (line 1343)
- `9000-READ-DATA-EXIT` (line 1372)
- `9100-GETCARD-BYACCTCARD` (line 1376)
- `9100-GETCARD-BYACCTCARD-EXIT` (line 1415)
- `9200-WRITE-PROCESSING` (line 1420)
- `9200-WRITE-PROCESSING-EXIT` (line 1494)
- `9300-CHECK-CHANGE-IN-REC` (line 1498)
- `9300-CHECK-CHANGE-IN-REC-EXIT` (line 1521)
- `ABEND-ROUTINE` (line 1531)
- `ABEND-ROUTINE-EXIT` (line 1554)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
