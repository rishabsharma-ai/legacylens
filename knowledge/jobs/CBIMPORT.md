---
type: job
title: CBIMPORT
description: Batch job that runs CBIMPORT.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBIMPORT.jcl
---

# CBIMPORT

Batch job that runs CBIMPORT.

Source: [app/jcl/CBIMPORT.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBIMPORT.jcl)

## Relationships

- Reads: [EXPORT](../datasets/EXPORT.md)
- Runs: [CBIMPORT](../programs/CBIMPORT.md)
- Writes: [ACCTDATA.IMPORT](../datasets/ACCTDATA.IMPORT.md), [CARDXREF.IMPORT](../datasets/CARDXREF.IMPORT.md), [CUSTDATA.IMPORT](../datasets/CUSTDATA.IMPORT.md), [IMPORT.ERRORS](../datasets/IMPORT.ERRORS.md), [TRANSACT.IMPORT](../datasets/TRANSACT.IMPORT.md)

## Steps

- `STEP01` runs [CBIMPORT](../programs/CBIMPORT.md)
