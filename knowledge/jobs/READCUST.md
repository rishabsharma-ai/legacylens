---
type: job
title: READCUST
description: Batch job that runs CBCUS01C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READCUST.jcl
---

# READCUST

Batch job that runs CBCUS01C.

Source: [app/jcl/READCUST.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READCUST.jcl)

## Relationships

- Reads: [CUSTDATA](../datasets/CUSTDATA.md)
- Runs: [CBCUS01C](../programs/CBCUS01C.md)

## Steps

- `STEP05` runs [CBCUS01C](../programs/CBCUS01C.md)
