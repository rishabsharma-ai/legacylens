---
type: job
title: MNTTRDB2
description: Batch job (utilities only).
tags:
- db2-transaction-type
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/jcl/MNTTRDB2.jcl
---

# MNTTRDB2

Batch job (utilities only).

Source: [app/app-transaction-type-db2/jcl/MNTTRDB2.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-transaction-type-db2/jcl/MNTTRDB2.jcl)

## Relationships

- Reads: [DBRMLIB](../datasets/DBRMLIB.md), [INPFILE](../datasets/INPFILE.md), [OEMA.DB2.VERSIONA.SDSNLOAD](../datasets/OEMA.DB2.VERSIONA.SDSNLOAD.md)

Utility steps (IDCAMS, SORT and so on): STEP1
