---
type: job
title: UNLDGSAM
description: Batch job that runs DFSRRC00.
tags:
- ims-db2-mq-authorization
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL
---

# UNLDGSAM

Batch job that runs DFSRRC00.

Source: [app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/UNLDGSAM.JCL)

## Relationships

- Reads: [OEM.IMS.IMSP.DBDLIB](../datasets/OEM.IMS.IMSP.DBDLIB.md), [OEM.IMS.IMSP.PAUTHDB](../datasets/OEM.IMS.IMSP.PAUTHDB.md), [OEM.IMS.IMSP.PAUTHDBX](../datasets/OEM.IMS.IMSP.PAUTHDBX.md), [OEM.IMS.IMSP.PSBLIB](../datasets/OEM.IMS.IMSP.PSBLIB.md), [OEMA.IMS.IMSP.SDFSRESL](../datasets/OEMA.IMS.IMSP.SDFSRESL.md), [OEMA.IMS.IMSP.SDFSRESL.V151](../datasets/OEMA.IMS.IMSP.SDFSRESL.V151.md), [OEMPP.IMS.V15R01MB.PROCLIB](../datasets/OEMPP.IMS.V15R01MB.PROCLIB.md), [PAUTDB.CHILD.GSAM](../datasets/PAUTDB.CHILD.GSAM.md), [PAUTDB.ROOT.GSAM](../datasets/PAUTDB.ROOT.GSAM.md)
- Runs: `DFSRRC00`

## Steps

- `STEP01` runs `DFSRRC00`
