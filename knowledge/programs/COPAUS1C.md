---
type: program
title: COPAUS1C
description: Detail View of Authorization Message
tags:
- ims-db2-mq-authorization
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl
---

# COPAUS1C

Detail View of Authorization Message

Source: [app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl) lines 1-604

## Relationships

- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), [COCOM01Y](../copybooks/COCOM01Y.md), [COPAU01](../copybooks/COPAU01.md), [COTTL01Y](../copybooks/COTTL01Y.md), [CSDAT01Y](../copybooks/CSDAT01Y.md), [CSMSG01Y](../copybooks/CSMSG01Y.md), [CSMSG02Y](../copybooks/CSMSG02Y.md), `DFHAID`, `DFHBMSCA`
- Links to: [COPAUS2C](../programs/COPAUS2C.md)
- Reached by XCTL from: [COPAUS0C](../programs/COPAUS0C.md)
- Reads: [PAUTDTL1](../datasets/PAUTDTL1.md), [PAUTSUM0](../datasets/PAUTSUM0.md)
- Transfers control to (XCTL): [COPAUS0C](../programs/COPAUS0C.md)
- Uses screen: [COPAU01](../screens/COPAU01.md)
- Writes: [PAUTDTL1](../datasets/PAUTDTL1.md)

## Paragraphs (15)

- `MAIN-PARA` (line 157)
- `PROCESS-ENTER-KEY` (line 208)
- `MARK-AUTH-FRAUD` (line 230)
- `PROCESS-PF8-KEY` (line 268)
- `POPULATE-AUTH-DETAILS` (line 291)
- `RETURN-TO-PREV-SCREEN` (line 360)
- `SEND-AUTHVIEW-SCREEN` (line 373)
- `RECEIVE-AUTHVIEW-SCREEN` (line 398)
- `POPULATE-HEADER-INFO` (line 409)
- `READ-AUTH-RECORD` (line 431)
- `READ-NEXT-AUTH-RECORD` (line 493)
- `UPDATE-AUTH-DETAILS` (line 520)
- `TAKE-SYNCPOINT` (line 557)
- `ROLL-BACK` (line 565)
- `SCHEDULE-PSB` (line 574)
