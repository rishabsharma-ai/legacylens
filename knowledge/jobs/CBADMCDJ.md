---
type: job
title: CBADMCDJ
description: Batch job that runs DFHCSDUP.
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBADMCDJ.jcl
---

# CBADMCDJ

Batch job that runs DFHCSDUP.

Source: [app/jcl/CBADMCDJ.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/CBADMCDJ.jcl)

## Relationships

- Reads: [OEM.CICSTS.DFHCSD](../datasets/OEM.CICSTS.DFHCSD.md)
- Runs: `DFHCSDUP`

## Steps

- `STEP1` runs `DFHCSDUP`
