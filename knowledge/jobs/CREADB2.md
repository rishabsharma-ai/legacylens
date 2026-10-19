---
type: job
title: CREADB2
description: Batch job (utilities only).
tags:
- db2-transaction-type
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/jcl/CREADB21.jcl
---

# CREADB2

Batch job (utilities only).

Source: [app/app-transaction-type-db2/jcl/CREADB21.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/jcl/CREADB21.jcl)

## Relationships

- Reads: [OEMA.DB2.VERSIONA.SDSNLOAD](../datasets/OEMA.DB2.VERSIONA.SDSNLOAD.md)

Utility steps (IDCAMS, SORT and so on): FREEPLN, CRCRDDB, LDTTYPE, RUNTEP2, LDTCCAT
