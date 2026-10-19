---
type: job
title: TRANFILE
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANFILE.jcl
---

# TRANFILE

Batch job (utilities only).

Source: [app/jcl/TRANFILE.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/TRANFILE.jcl)

## Relationships

- Reads: [DALYTRAN.PS.INIT](../datasets/DALYTRAN.PS.INIT.md), [TRANSACT](../datasets/TRANSACT.md)

Utility steps (IDCAMS, SORT and so on): CLCIFIL, STEP05, STEP10, STEP15, STEP20, STEP25, STEP30, OPCIFIL
