---
type: program
title: CBPAUP0C
description: Delete Expired Pending Authoriation Messages
tags:
- batch
- ims-db2-mq-authorization
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl
---

# CBPAUP0C

Delete Expired Pending Authoriation Messages

Source: [app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl) lines 1-386

## Relationships

- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md)
- Reads: [PAUTDTL1](../datasets/PAUTDTL1.md), [PAUTSUM0](../datasets/PAUTSUM0.md)
- Writes: [PAUTDTL1](../datasets/PAUTDTL1.md), [PAUTSUM0](../datasets/PAUTSUM0.md)

## Business rules

- `4000-CHECK-IF-EXPIRED` line 280: COMPUTE WS-AUTH-DATE = 99999 - PA-AUTH-DATE-9C
- `4000-CHECK-IF-EXPIRED` line 282: COMPUTE WS-DAY-DIFF = CURRENT-YYDDD - WS-AUTH-DATE

## Paragraphs (17)

- `MAIN-PARA` (line 136)
- `1000-INITIALIZE` (line 183)
- `1000-EXIT` (line 212)
- `2000-FIND-NEXT-AUTH-SUMMARY` (line 216)
- `2000-EXIT` (line 243)
- `3000-FIND-NEXT-AUTH-DTL` (line 248)
- `3000-EXIT` (line 273)
- `4000-CHECK-IF-EXPIRED` (line 277)
- `4000-EXIT` (line 299)
- `5000-DELETE-AUTH-DTL` (line 303)
- `5000-EXIT` (line 324)
- `6000-DELETE-AUTH-SUMMARY` (line 328)
- `6000-EXIT` (line 348)
- `9000-TAKE-CHECKPOINT` (line 352)
- `9000-EXIT` (line 373)
- `9999-ABEND` (line 377)
- `9999-EXIT` (line 385)
