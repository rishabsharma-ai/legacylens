---
type: program
title: CBEXPORT
description: Export Customer Data for Branch Migration Reads normalized CardDemo files
  and creates multi-record export file for data migration
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBEXPORT.cbl
---

# CBEXPORT

Export Customer Data for Branch Migration Reads normalized CardDemo files and creates multi-record export file for data migration

Source: [app/cbl/CBEXPORT.cbl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBEXPORT.cbl) lines 1-582

## Relationships

- Calls: `CEE3ABD`
- Includes: [CVACT01Y](../copybooks/CVACT01Y.md), [CVACT02Y](../copybooks/CVACT02Y.md), [CVACT03Y](../copybooks/CVACT03Y.md), [CVCUS01Y](../copybooks/CVCUS01Y.md), [CVEXPORT](../copybooks/CVEXPORT.md), [CVTRA05Y](../copybooks/CVTRA05Y.md)
- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDDATA](../datasets/CARDDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md), [TRANSACT](../datasets/TRANSACT.md)
- Run by job: [CBEXPORT](../jobs/CBEXPORT.md)
- Writes: [EXPORT](../datasets/EXPORT.md)

## Paragraphs (21)

- `0000-MAIN-PROCESSING` (line 149)
- `1000-INITIALIZE` (line 161)
- `1050-GENERATE-TIMESTAMP` (line 172)
- `1100-OPEN-FILES` (line 198)
- `2000-EXPORT-CUSTOMERS` (line 243)
- `2100-READ-CUSTOMER-RECORD` (line 258)
- `2200-CREATE-CUSTOMER-EXP-REC` (line 269)
- `3000-EXPORT-ACCOUNTS` (line 312)
- `3100-READ-ACCOUNT-RECORD` (line 327)
- `3200-CREATE-ACCOUNT-EXP-REC` (line 338)
- `4000-EXPORT-XREFS` (line 376)
- `4100-READ-XREF-RECORD` (line 391)
- `4200-CREATE-XREF-EXPORT-RECORD` (line 402)
- `5000-EXPORT-TRANSACTIONS` (line 431)
- `5100-READ-TRANSACTION-RECORD` (line 446)
- `5200-CREATE-TRAN-EXP-REC` (line 457)
- `5500-EXPORT-CARDS` (line 496)
- `5600-READ-CARD-RECORD` (line 511)
- `5700-CREATE-CARD-EXPORT-RECORD` (line 522)
- `6000-FINALIZE` (line 554)
- `9999-ABEND-PROGRAM` (line 576)
