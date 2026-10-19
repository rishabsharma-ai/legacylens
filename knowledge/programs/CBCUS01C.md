---
type: program
title: CBCUS01C
description: Read and print customer data file.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBCUS01C.cbl
---

# CBCUS01C

Read and print customer data file.

Source: [app/cbl/CBCUS01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBCUS01C.cbl) lines 1-178

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVCUS01Y](../copybooks/CVCUS01Y.md)
- Reads: [CUSTDATA](../datasets/CUSTDATA.md)
- Run by job: [READCUST](../jobs/READCUST.md)

## Paragraphs (5)

- `1000-CUSTFILE-GET-NEXT` (line 92)
- `0000-CUSTFILE-OPEN` (line 118)
- `9000-CUSTFILE-CLOSE` (line 136)
- `Z-ABEND-PROGRAM` (line 154)
- `Z-DISPLAY-IO-STATUS` (line 161)
