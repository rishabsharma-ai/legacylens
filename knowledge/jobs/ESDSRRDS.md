---
type: job
title: ESDSRRDS
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/ESDSRRDS.jcl
---

# ESDSRRDS

Batch job (utilities only).

Source: [app/jcl/ESDSRRDS.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/ESDSRRDS.jcl)

## Relationships

- Reads: [ESDSRRDS](../datasets/ESDSRRDS.md), [USRSEC](../datasets/USRSEC.md)
- Writes: [ESDSRRDS](../datasets/ESDSRRDS.md)

Utility steps (IDCAMS, SORT and so on): PREDEL, STEP01, STEP02, STEP03, STEP04, STEP05
