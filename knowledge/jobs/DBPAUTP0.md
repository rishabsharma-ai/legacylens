---
type: job
title: DBPAUTP0
description: Batch job that runs DFSRRC00.
tags:
- ims-db2-mq-authorization
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl
---

# DBPAUTP0

Batch job that runs DFSRRC00.

Source: [app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/jcl/DBPAUTP0.jcl)

## Relationships

- Reads: [IMSDATA.DBPAUTP0](../datasets/IMSDATA.DBPAUTP0.md), [OEM.IMS.IMSP.DBDLIB](../datasets/OEM.IMS.IMSP.DBDLIB.md), [OEM.IMS.IMSP.PAUTHDB](../datasets/OEM.IMS.IMSP.PAUTHDB.md), [OEM.IMS.IMSP.PAUTHDBX](../datasets/OEM.IMS.IMSP.PAUTHDBX.md), [OEM.IMS.IMSP.PSBLIB](../datasets/OEM.IMS.IMSP.PSBLIB.md), [OEM.IMS.IMSP.RECON1](../datasets/OEM.IMS.IMSP.RECON1.md), [OEM.IMS.IMSP.RECON2](../datasets/OEM.IMS.IMSP.RECON2.md), [OEM.IMS.IMSP.RECON3](../datasets/OEM.IMS.IMSP.RECON3.md), [OEMA.IMS.IMSP.SDFSRESL](../datasets/OEMA.IMS.IMSP.SDFSRESL.md), [OEMPP.IMS.V15R01MB.PROCLIB](../datasets/OEMPP.IMS.V15R01MB.PROCLIB.md)
- Runs: `DFSRRC00`
- Writes: [IMSDATA.DBPAUTP0](../datasets/IMSDATA.DBPAUTP0.md)

## Steps

- `UNLOAD` runs `DFSRRC00`

Utility steps (IDCAMS, SORT and so on): STEPDEL
