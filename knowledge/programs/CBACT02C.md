---
type: program
title: CBACT02C
description: Read and print card data file.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT02C.cbl
---

# CBACT02C

Read and print card data file.

Source: [app/cbl/CBACT02C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT02C.cbl) lines 1-178

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT02Y](../copybooks/CVACT02Y.md)
- Reads: [CARDDATA](../datasets/CARDDATA.md)
- Run by job: [READCARD](../jobs/READCARD.md)

## Paragraphs (5)

- `1000-CARDFILE-GET-NEXT` (line 92)
- `0000-CARDFILE-OPEN` (line 118)
- `9000-CARDFILE-CLOSE` (line 136)
- `9999-ABEND-PROGRAM` (line 154)
- `9910-DISPLAY-IO-STATUS` (line 161)
