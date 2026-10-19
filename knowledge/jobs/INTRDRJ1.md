---
type: job
title: INTRDRJ1
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/INTRDRJ1.JCL
---

# INTRDRJ1

Batch job (utilities only).

Source: [app/jcl/INTRDRJ1.JCL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/INTRDRJ1.JCL)

## Relationships

- Reads: [AWS.M2.CARDEMO.FTP.TEST](../datasets/AWS.M2.CARDEMO.FTP.TEST.md), [AWS.M2.CARDEMO.FTP.TEST.BKUP](../datasets/AWS.M2.CARDEMO.FTP.TEST.BKUP.md), [JCL](../datasets/JCL.md)

Utility steps (IDCAMS, SORT and so on): IDCAMS, STEP01
