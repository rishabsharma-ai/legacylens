---
type: program
title: COACTUPC
description: Accept and process ACCOUNT UPDATE
tags:
- base
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COACTUPC.cbl
---

# COACTUPC

Accept and process ACCOUNT UPDATE

Source: [app/cbl/COACTUPC.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/COACTUPC.cbl) lines 1-4236

## Relationships

- Includes: [COACTUP](../copybooks/COACTUP.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSLKPCDY](../copybooks/CSLKPCDY.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), [CSSETATY](../copybooks/CSSETATY.md), [CSSTRPFY](../copybooks/CSSTRPFY.md), [CSUSR01Y](../copybooks/CSUSR01Y.md), [CSUTLDPY](../copybooks/CSUTLDPY.md), [CSUTLDWY](../copybooks/CSUTLDWY.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCRD01Y](../copybooks/CVCRD01Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md)
- Started by transaction: [CAUP](../transactions/CAUP.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md)
- Uses screen: [COACTUP](../screens/COACTUP.md)
- Writes: [ACCTDATA](../datasets/ACCTDATA.md), [CUSTDATA](../datasets/CUSTDATA.md)

## Business rules

- `1100-RECEIVE-MAP` line 1079: COMPUTE ACUP-NEW-CREDIT-LIMIT-N =
- `1100-RECEIVE-MAP` line 1093: COMPUTE ACUP-NEW-CASH-CREDIT-LIMIT-N =
- `1100-RECEIVE-MAP` line 1107: COMPUTE ACUP-NEW-CURR-BAL-N =
- `1100-RECEIVE-MAP` line 1121: COMPUTE ACUP-NEW-CURR-CYC-CREDIT-N =
- `1100-RECEIVE-MAP` line 1135: COMPUTE ACUP-NEW-CURR-CYC-DEBIT-N =

## Paragraphs (85)

- `0000-MAIN` (line 859)
- `COMMON-RETURN` (line 1007)
- `0000-MAIN-EXIT` (line 1021)
- `1000-PROCESS-INPUTS` (line 1025)
- `1000-PROCESS-INPUTS-EXIT` (line 1036)
- `1100-RECEIVE-MAP` (line 1039)
- `1100-RECEIVE-MAP-EXIT` (line 1426)
- `1200-EDIT-MAP-INPUTS` (line 1429)
- `1200-EDIT-MAP-INPUTS-EXIT` (line 1678)
- `1205-COMPARE-OLD-NEW` (line 1681)
- `1205-COMPARE-OLD-NEW-EXIT` (line 1777)
- `1210-EDIT-ACCOUNT` (line 1783)
- `1210-EDIT-ACCOUNT-EXIT` (line 1820)
- `1215-EDIT-MANDATORY` (line 1824)
- `1215-EDIT-MANDATORY-EXIT` (line 1852)
- `1220-EDIT-YESNO` (line 1856)
- `1220-EDIT-YESNO-EXIT` (line 1894)
- `1225-EDIT-ALPHA-REQD` (line 1898)
- `1225-EDIT-ALPHA-REQD-EXIT` (line 1951)
- `1230-EDIT-ALPHANUM-REQD` (line 1955)
- `1230-EDIT-ALPHANUM-REQD-EXIT` (line 2009)
- `1235-EDIT-ALPHA-OPT` (line 2012)
- `1235-EDIT-ALPHA-OPT-EXIT` (line 2057)
- `1240-EDIT-ALPHANUM-OPT` (line 2061)
- `1240-EDIT-ALPHANUM-OPT-EXIT` (line 2105)
- `1245-EDIT-NUM-REQD` (line 2109)
- `1245-EDIT-NUM-REQD-EXIT` (line 2176)
- `1250-EDIT-SIGNED-9V2` (line 2180)
- `1250-EDIT-SIGNED-9V2-EXIT` (line 2221)
- `1260-EDIT-US-PHONE-NUM` (line 2225)
- `EDIT-AREA-CODE` (line 2246)
- `EDIT-US-PHONE-PREFIX` (line 2316)
- `EDIT-US-PHONE-LINENUM` (line 2370)
- `EDIT-US-PHONE-EXIT` (line 2424)
- `1260-EDIT-US-PHONE-NUM-EXIT` (line 2427)
- `1265-EDIT-US-SSN` (line 2431)
- `1265-EDIT-US-SSN-EXIT` (line 2489)
- `1270-EDIT-US-STATE-CD` (line 2493)
- `1270-EDIT-US-STATE-CD-EXIT` (line 2511)
- `1275-EDIT-FICO-SCORE` (line 2514)
- `1275-EDIT-FICO-SCORE-EXIT` (line 2531)
- `1280-EDIT-US-STATE-ZIP-CD` (line 2536)
- `1280-EDIT-US-STATE-ZIP-CD-EXIT` (line 2558)
- `2000-DECIDE-ACTION` (line 2562)
- `2000-DECIDE-ACTION-EXIT` (line 2643)
- `3000-SEND-MAP` (line 2649)
- `3000-SEND-MAP-EXIT` (line 2664)
- `3100-SCREEN-INIT` (line 2668)
- `3100-SCREEN-INIT-EXIT` (line 2694)
- `3200-SETUP-SCREEN-VARS` (line 2698)
- `3200-SETUP-SCREEN-VARS-EXIT` (line 2727)
- `3201-SHOW-INITIAL-VALUES` (line 2731)
- `3201-SHOW-INITIAL-VALUES-EXIT` (line 2783)
- `3202-SHOW-ORIGINAL-VALUES` (line 2787)
- `3202-SHOW-ORIGINAL-VALUES-EXIT` (line 2867)
- `3203-SHOW-UPDATED-VALUES` (line 2870)
- `3203-SHOW-UPDATED-VALUES-EXIT` (line 2951)
- `3250-SETUP-INFOMSG` (line 2955)
- `3250-SETUP-INFOMSG-EXIT` (line 2983)
- `3300-SETUP-SCREEN-ATTRS` (line 2986)
- `3300-SETUP-SCREEN-ATTRS-EXIT` (line 3437)
- `3310-PROTECT-ALL-ATTRS` (line 3441)
- `3310-PROTECT-ALL-ATTRS-EXIT` (line 3496)
- `3320-UNPROTECT-FEW-ATTRS` (line 3500)
- `3320-UNPROTECT-FEW-ATTRS-EXIT` (line 3562)
- `3390-SETUP-INFOMSG-ATTRS` (line 3566)
- `3390-SETUP-INFOMSG-ATTRS-EXIT` (line 3584)
- `3400-SEND-SCREEN` (line 3589)
- `3400-SEND-SCREEN-EXIT` (line 3603)
- `9000-READ-ACCT` (line 3608)
- `9000-READ-ACCT-EXIT` (line 3647)
- `9200-GETCARDXREF-BYACCT` (line 3650)
- `9200-GETCARDXREF-BYACCT-EXIT` (line 3698)
- `9300-GETACCTDATA-BYACCT` (line 3701)
- `9300-GETACCTDATA-BYACCT-EXIT` (line 3748)
- `9400-GETCUSTDATA-BYCUST` (line 3752)
- `9400-GETCUSTDATA-BYCUST-EXIT` (line 3797)
- `9500-STORE-FETCHED-DATA` (line 3801)
- `9500-STORE-FETCHED-DATA-EXIT` (line 3885)
- `9600-WRITE-PROCESSING` (line 3888)
- `9600-WRITE-PROCESSING-EXIT` (line 4105)
- `9700-CHECK-CHANGE-IN-REC` (line 4109)
- `9700-CHECK-CHANGE-IN-REC-EXIT` (line 4193)
- `ABEND-ROUTINE` (line 4203)
- `ABEND-ROUTINE-EXIT` (line 4226)

## Documents that mention it

- [CardDemo System Overview](../../corpus/docs/confluence/2001-carddemo-system-overview.md) (`CONFLUENCE:2001`)

Documents can be out of date. When they disagree with the code, the code wins.
