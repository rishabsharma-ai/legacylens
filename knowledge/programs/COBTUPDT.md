---
type: program
title: COBTUPDT
description: Update Transaction type based on user input
tags:
- batch
- db2-transaction-type
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/cbl/COBTUPDT.cbl
---

# COBTUPDT

Update Transaction type based on user input

Source: [app/app-transaction-type-db2/cbl/COBTUPDT.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/cbl/COBTUPDT.cbl) lines 1-237

## Relationships

- Includes: [DCLTRTYP](../copybooks/DCLTRTYP.md), `SQLCA`
- Writes: [TRANSACTION_TYPE](../datasets/TRANSACTION_TYPE.md)

## Paragraphs (9)

- `0001-OPEN-FILES` (line 82)
- `1001-READ-NEXT-RECORDS` (line 91)
- `1002-READ-RECORDS` (line 100)
- `1003-TREAT-RECORD` (line 109)
- `10031-INSERT-DB` (line 132)
- `10032-UPDATE-DB` (line 166)
- `10033-DELETE-DB` (line 196)
- `9999-ABEND` (line 230)
- `2001-CLOSE-STOP` (line 234)
