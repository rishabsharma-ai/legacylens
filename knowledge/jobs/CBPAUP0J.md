---
type: job
title: CBPAUP0J
description: Batch job that runs DFSRRC00.
tags:
- ims-db2-mq-authorization
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/CBPAUP0J.jcl
---

# CBPAUP0J

Batch job that runs DFSRRC00.

Source: [app/app-authorization-ims-db2-mq/jcl/CBPAUP0J.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/CBPAUP0J.jcl)

## Relationships

- Reads: [IMS.DBDLIB](../datasets/IMS.DBDLIB.md), [IMS.PROCLIB](../datasets/IMS.PROCLIB.md), [IMS.PSBLIB](../datasets/IMS.PSBLIB.md), [IMS.SDFSRESL](../datasets/IMS.SDFSRESL.md)
- Runs: `DFSRRC00`

## Steps

- `STEP01` runs `DFSRRC00`
