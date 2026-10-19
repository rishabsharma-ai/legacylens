---
type: program
title: CBACT01C
description: Program CBACT01C.
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT01C.cbl
---

# CBACT01C

Program CBACT01C.

Source: [app/cbl/CBACT01C.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBACT01C.cbl) lines 1-430

## Relationships

- Calls: `CEE3ABD`, `COBDATFT`
- Includes: [CODATECN](../copybooks/CODATECN.md), [CVACT01Y](../copybooks/CVACT01Y.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md)
- Run by job: [READACCT](../jobs/READACCT.md)
- Writes: [ACCTDATA.ARRYPS](../datasets/ACCTDATA.ARRYPS.md), [ACCTDATA.PSCOMP](../datasets/ACCTDATA.PSCOMP.md), [ACCTDATA.VBPS](../datasets/ACCTDATA.VBPS.md)

## Paragraphs (16)

- `1000-ACCTFILE-GET-NEXT` (line 165)
- `1100-DISPLAY-ACCT-RECORD` (line 200)
- `1300-POPUL-ACCT-RECORD` (line 215)
- `1350-WRITE-ACCT-RECORD` (line 242)
- `1400-POPUL-ARRAY-RECORD` (line 253)
- `1450-WRITE-ARRY-RECORD` (line 263)
- `1500-POPUL-VBRC-RECORD` (line 276)
- `1550-WRITE-VB1-RECORD` (line 287)
- `1575-WRITE-VB2-RECORD` (line 302)
- `0000-ACCTFILE-OPEN` (line 317)
- `2000-OUTFILE-OPEN` (line 334)
- `3000-ARRFILE-OPEN` (line 352)
- `4000-VBRFILE-OPEN` (line 370)
- `9000-ACCTFILE-CLOSE` (line 388)
- `9999-ABEND-PROGRAM` (line 406)
- `9910-DISPLAY-IO-STATUS` (line 413)
