---
type: job
title: CUSTFILE
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CUSTFILE.jcl
---

# CUSTFILE

Batch job (utilities only).

Source: [app/jcl/CUSTFILE.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CUSTFILE.jcl)

## Relationships

- Reads: [CUSTDATA](../datasets/CUSTDATA.md)

Utility steps (IDCAMS, SORT and so on): CLCIFIL, STEP05, STEP10, STEP15, OPCIFIL
