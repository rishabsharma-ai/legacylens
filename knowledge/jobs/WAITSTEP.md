---
type: job
title: WAITSTEP
description: Batch job that runs COBSWAIT.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/WAITSTEP.jcl
---

# WAITSTEP

Batch job that runs COBSWAIT.

Source: [app/jcl/WAITSTEP.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/WAITSTEP.jcl)

## Relationships

- Runs: [COBSWAIT](../programs/COBSWAIT.md)

## Steps

- `WAIT` runs [COBSWAIT](../programs/COBSWAIT.md)
