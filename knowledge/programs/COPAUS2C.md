---
type: program
title: COPAUS2C
description: Mark Authorization Message Fraud
tags:
- ims-db2-mq-authorization
- online
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl
---

# COPAUS2C

Mark Authorization Message Fraud

Source: [app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/COPAUS2C.cbl) lines 1-244

## Relationships

- Includes: [AUTHFRDS](../copybooks/AUTHFRDS.md), [CIPAUDTY](../copybooks/CIPAUDTY.md), `SQLCA`
- Linked from: [COPAUS1C](../programs/COPAUS1C.md)
- Writes: [AUTHFRDS](../datasets/AUTHFRDS.md)

## Business rules

- `MAIN-PARA` line 107: COMPUTE WS-AUTH-TIME = 999999999 - PA-AUTH-TIME-9C

## Paragraphs (2)

- `MAIN-PARA` (line 89)
- `FRAUD-UPDATE` (line 221)
