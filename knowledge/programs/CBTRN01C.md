---
type: program
title: CBTRN01C
description: Post the records from daily transaction file.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN01C.cbl
---

# CBTRN01C

Post the records from daily transaction file.

Source: [app/cbl/CBTRN01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBTRN01C.cbl) lines 1-494

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), [CVTRA05Y](../copybooks/CVTRA05Y.md), [CVTRA06Y](../copybooks/CVTRA06Y.md)

## Paragraphs (18)

- `MAIN-PARA` (line 155)
- `1000-DALYTRAN-GET-NEXT` (line 202)
- `2000-LOOKUP-XREF` (line 227)
- `3000-READ-ACCOUNT` (line 241)
- `0000-DALYTRAN-OPEN` (line 252)
- `0100-CUSTFILE-OPEN` (line 271)
- `0200-XREFFILE-OPEN` (line 289)
- `0300-CARDFILE-OPEN` (line 307)
- `0400-ACCTFILE-OPEN` (line 325)
- `0500-TRANFILE-OPEN` (line 343)
- `9000-DALYTRAN-CLOSE` (line 361)
- `9100-CUSTFILE-CLOSE` (line 379)
- `9200-XREFFILE-CLOSE` (line 397)
- `9300-CARDFILE-CLOSE` (line 415)
- `9400-ACCTFILE-CLOSE` (line 433)
- `9500-TRANFILE-CLOSE` (line 451)
- `Z-ABEND-PROGRAM` (line 469)
- `Z-DISPLAY-IO-STATUS` (line 476)
