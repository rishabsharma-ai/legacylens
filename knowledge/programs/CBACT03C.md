---
type: program
title: CBACT03C
description: Read and print account cross reference data file.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT03C.cbl
---

# CBACT03C

Read and print account cross reference data file.

Source: [app/cbl/CBACT03C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT03C.cbl) lines 1-178

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT03Y](../copybooks/CVACT03Y.md)
- Reads: [CARDXREF](../datasets/CARDXREF.md)
- Run by job: [READXREF](../jobs/READXREF.md)

## Paragraphs (5)

- `1000-XREFFILE-GET-NEXT` (line 92)
- `0000-XREFFILE-OPEN` (line 118)
- `9000-XREFFILE-CLOSE` (line 136)
- `9999-ABEND-PROGRAM` (line 154)
- `9910-DISPLAY-IO-STATUS` (line 161)
