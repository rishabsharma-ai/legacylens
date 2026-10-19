---
type: program
title: COPAUS0C
description: Summary View of Authoriation Messages
tags:
- ims-db2-mq-authorization
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl
---

# COPAUS0C

Summary View of Authoriation Messages

Source: [app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS0C.cbl) lines 1-1032

## Relationships

- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COPAU00](../copybooks/COPAU00.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), `DFHAID`, `DFHBMSCA`
- Reached by XCTL from: [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md), [PAUTDTL1](../datasets/PAUTDTL1.md), [PAUTSUM0](../datasets/PAUTSUM0.md)
- Transfers control to (XCTL): [COMEN01C](../programs/COMEN01C.md), [COPAUS0C](../programs/COPAUS0C.md), [COPAUS1C](../programs/COPAUS1C.md), [COSGN00C](../programs/COSGN00C.md)
- Uses screen: [COPAU00](../screens/COPAU00.md)

## Business rules

- `PROCESS-PF7-KEY` line 366: COMPUTE CDEMO-CPVS-PAGE-NUM = CDEMO-CPVS-PAGE-NUM - 1
- `PROCESS-PAGE-FORWARD` line 432: COMPUTE WS-IDX = WS-IDX + 1
- `PROCESS-PAGE-FORWARD` line 437: COMPUTE CDEMO-CPVS-PAGE-NUM =

## Paragraphs (20)

- `MAIN-PARA` (line 178)
- `PROCESS-ENTER-KEY` (line 261)
- `GATHER-DETAILS` (line 342)
- `PROCESS-PF7-KEY` (line 362)
- `PROCESS-PF8-KEY` (line 388)
- `PROCESS-PAGE-FORWARD` (line 415)
- `GET-AUTHORIZATIONS` (line 458)
- `REPOSITION-AUTHORIZATIONS` (line 488)
- `POPULATE-AUTH-LIST` (line 522)
- `INITIALIZE-AUTH-DATA` (line 608)
- `RETURN-TO-PREV-SCREEN` (line 665)
- `SEND-PAULST-SCREEN` (line 681)
- `RECEIVE-PAULST-SCREEN` (line 712)
- `POPULATE-HEADER-INFO` (line 726)
- `GATHER-ACCOUNT-DETAILS` (line 750)
- `GETCARDXREF-BYACCT` (line 812)
- `GETACCTDATA-BYACCT` (line 865)
- `GETCUSTDATA-BYCUST` (line 915)
- `GET-AUTH-SUMMARY` (line 966)
- `SCHEDULE-PSB` (line 1001)
