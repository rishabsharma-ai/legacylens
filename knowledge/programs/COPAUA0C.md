---
type: program
title: COPAUA0C
description: Card Authorization Decision Program
tags:
- ims-db2-mq-authorization
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl
---

# COPAUA0C

Card Authorization Decision Program

Source: [app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl) lines 1-1026

## Relationships

- Calls: `MQCLOSE`, `MQGET`, `MQOPEN`, `MQPUT1`
- Includes: [CCPAUERY](../copybooks/CCPAUERY.md), [CCPAURLY](../copybooks/CCPAURLY.md), [CCPAURQY](../copybooks/CCPAURQY.md), [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), `CMQGMOV`, `CMQMDV`, `CMQODV`, `CMQPMOV`, `CMQTML`, `CMQV`, [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md), [PAUTSUM0](../datasets/PAUTSUM0.md)
- Writes: [PAUTDTL1](../datasets/PAUTDTL1.md), [PAUTSUM0](../datasets/PAUTSUM0.md)

## Business rules

- `1100-OPEN-REQUEST-QUEUE` line 260: COMPUTE WS-OPTIONS = MQOO-INPUT-SHARED
- `2100-EXTRACT-REQUEST-MSG` line 376: COMPUTE PA-RQ-TRANSACTION-AMT =
- `3100-READ-REQUEST-MQ` line 389: COMPUTE MQGMO-OPTIONS = MQGMO-NO-SYNCPOINT + MQGMO-WAIT + MQGMO-CONVERT + MQGMO-FAIL-IF-QUIESCING
- `6000-MAKE-DECISION` line 666: COMPUTE WS-AVAILABLE-AMT = PA-CREDIT-LIMIT - PA-CREDIT-BALANCE
- `6000-MAKE-DECISION` line 674: COMPUTE WS-AVAILABLE-AMT = ACCT-CREDIT-LIMIT - ACCT-CURR-BAL
- `7100-SEND-RESPONSE` line 753: COMPUTE MQPMO-OPTIONS = MQPMO-NO-SYNCPOINT +
- `8500-INSERT-AUTH` line 871: COMPUTE WS-TIME-WITH-MS = (WS-CUR-TIME-N6 * 1000) +
- `8500-INSERT-AUTH` line 874: COMPUTE PA-AUTH-DATE-9C = 99999 - WS-YYDDD
- `8500-INSERT-AUTH` line 875: COMPUTE PA-AUTH-TIME-9C = 999999999 - WS-TIME-WITH-MS

## Paragraphs (43)

- `MAIN-PARA` (line 220)
- `1000-INITIALIZE` (line 230)
- `1000-EXIT` (line 249)
- `1100-OPEN-REQUEST-QUEUE` (line 255)
- `1100-EXIT` (line 286)
- `1200-SCHEDULE-PSB` (line 292)
- `1200-EXIT` (line 319)
- `2000-MAIN-PROCESS` (line 323)
- `2000-EXIT` (line 347)
- `2100-EXTRACT-REQUEST-MSG` (line 351)
- `2100-EXIT` (line 382)
- `3100-READ-REQUEST-MQ` (line 386)
- `3100-EXIT` (line 434)
- `5000-PROCESS-AUTH` (line 438)
- `5000-EXIT` (line 468)
- `5100-READ-XREF-RECORD` (line 472)
- `5100-EXIT` (line 516)
- `5200-READ-ACCT-RECORD` (line 520)
- `5200-EXIT` (line 564)
- `5300-READ-CUST-RECORD` (line 568)
- `5300-EXIT` (line 612)
- `5500-READ-AUTH-SUMMRY` (line 616)
- `5500-EXIT` (line 643)
- `5600-READ-PROFILE-DATA` (line 647)
- `5600-EXIT` (line 653)
- `6000-MAKE-DECISION` (line 657)
- `6000-EXIT` (line 734)
- `7100-SEND-RESPONSE` (line 738)
- `7100-EXIT` (line 782)
- `8000-WRITE-AUTH-TO-DB` (line 786)
- `8000-EXIT` (line 794)
- `8400-UPDATE-SUMMARY` (line 798)
- `8400-EXIT` (line 850)
- `8500-INSERT-AUTH` (line 854)
- `8500-EXIT` (line 935)
- `9000-TERMINATE` (line 940)
- `9000-EXIT` (line 950)
- `9100-CLOSE-REQUEST-QUEUE` (line 953)
- `9100-EXIT` (line 979)
- `9500-LOG-ERROR` (line 983)
- `9500-EXIT` (line 1012)
- `9990-END-ROUTINE` (line 1016)
- `9990-EXIT` (line 1024)
