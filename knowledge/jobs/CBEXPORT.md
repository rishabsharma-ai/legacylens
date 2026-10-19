---
type: job
title: CBEXPORT
description: Batch job that runs CBEXPORT.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBEXPORT.jcl
---

# CBEXPORT

Batch job that runs CBEXPORT.

Source: [app/jcl/CBEXPORT.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBEXPORT.jcl)

## Relationships

- Reads: [ACCTDATA](../datasets/ACCTDATA.md), [CARDDATA](../datasets/CARDDATA.md), [CARDXREF](../datasets/CARDXREF.md), [CUSTDATA](../datasets/CUSTDATA.md), [EXPORT](../datasets/EXPORT.md), [TRANSACT](../datasets/TRANSACT.md)
- Runs: [CBEXPORT](../programs/CBEXPORT.md)

## Steps

- `STEP02` runs [CBEXPORT](../programs/CBEXPORT.md)

Utility steps (IDCAMS, SORT and so on): STEP01
