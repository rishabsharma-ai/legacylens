---
type: job
title: READXREF
description: Batch job that runs CBACT03C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READXREF.jcl
---

# READXREF

Batch job that runs CBACT03C.

Source: [app/jcl/READXREF.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READXREF.jcl)

## Relationships

- Reads: [CARDXREF](../datasets/CARDXREF.md)
- Runs: [CBACT03C](../programs/CBACT03C.md)

## Steps

- `STEP05` runs [CBACT03C](../programs/CBACT03C.md)
