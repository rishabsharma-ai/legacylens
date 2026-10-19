---
type: program
title: CBIMPORT
description: Import Customer Data from Branch Migration Export Reads multi-record
  export file and splits it into separate normalized target files (CUSTOMER, ACCOUN
  CARD-XREF, TRANSACTION) with validation
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBIMPORT.cbl
---

# CBIMPORT

Import Customer Data from Branch Migration Export Reads multi-record export file and splits it into separate normalized target files (CUSTOMER, ACCOUN CARD-XREF, TRANSACTION) with validation

Source: [app/cbl/CBIMPORT.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBIMPORT.cbl) lines 1-487

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), [CVEXPORT](../copybooks/CVEXPORT.md), [CVTRA05Y](../copybooks/CVTRA05Y.md)
- Reads: [EXPORT](../datasets/EXPORT.md)
- Run by job: [CBIMPORT](../jobs/CBIMPORT.md)
- Writes: [ACCTDATA.IMPORT](../datasets/ACCTDATA.IMPORT.md), [CARDXREF.IMPORT](../datasets/CARDXREF.IMPORT.md), [CUSTDATA.IMPORT](../datasets/CUSTDATA.IMPORT.md), [IMPORT.ERRORS](../datasets/IMPORT.ERRORS.md), [TRANSACT.IMPORT](../datasets/TRANSACT.IMPORT.md)

## Paragraphs (16)

- `0000-MAIN-PROCESSING` (line 165)
- `1000-INITIALIZE` (line 174)
- `1100-OPEN-FILES` (line 196)
- `2000-PROCESS-EXPORT-FILE` (line 248)
- `2100-READ-EXPORT-RECORD` (line 259)
- `2200-PROCESS-RECORD-BY-TYPE` (line 270)
- `2300-PROCESS-CUSTOMER-RECORD` (line 288)
- `2400-PROCESS-ACCOUNT-RECORD` (line 323)
- `2500-PROCESS-XREF-RECORD` (line 352)
- `2600-PROCESS-TRAN-RECORD` (line 372)
- `2650-PROCESS-CARD-RECORD` (line 402)
- `2700-PROCESS-UNKNOWN-RECORD` (line 425)
- `2750-WRITE-ERROR` (line 437)
- `3000-VALIDATE-IMPORT` (line 449)
- `4000-FINALIZE` (line 455)
- `9999-ABEND-PROGRAM` (line 481)
