---
type: job
title: READCARD
description: Batch job that runs CBACT02C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READCARD.jcl
---

# READCARD

Batch job that runs CBACT02C.

Source: [app/jcl/READCARD.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READCARD.jcl)

## Relationships

- Reads: [CARDDATA](../datasets/CARDDATA.md)
- Runs: [CBACT02C](../programs/CBACT02C.md)

## Steps

- `STEP05` runs [CBACT02C](../programs/CBACT02C.md)
