---
type: job
title: READACCT
description: Batch job that runs CBACT01C.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READACCT.jcl
---

# READACCT

Batch job that runs CBACT01C.

Source: [app/jcl/READACCT.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/READACCT.jcl)

## Relationships

- Reads: [ACCTDATA](../datasets/ACCTDATA.md)
- Runs: [CBACT01C](../programs/CBACT01C.md)
- Writes: [ACCTDATA.ARRYPS](../datasets/ACCTDATA.ARRYPS.md), [ACCTDATA.PSCOMP](../datasets/ACCTDATA.PSCOMP.md), [ACCTDATA.VBPS](../datasets/ACCTDATA.VBPS.md)

## Steps

- `STEP05` runs [CBACT01C](../programs/CBACT01C.md)

Utility steps (IDCAMS, SORT and so on): PREDEL
