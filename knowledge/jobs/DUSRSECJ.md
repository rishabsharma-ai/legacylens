---
type: job
title: DUSRSECJ
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/DUSRSECJ.jcl
---

# DUSRSECJ

Batch job (utilities only).

Source: [app/jcl/DUSRSECJ.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/DUSRSECJ.jcl)

## Relationships

- Reads: [USRSEC](../datasets/USRSEC.md)
- Writes: [USRSEC](../datasets/USRSEC.md)

Utility steps (IDCAMS, SORT and so on): PREDEL, STEP01, STEP02, STEP03
