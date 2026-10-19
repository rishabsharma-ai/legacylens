---
type: job
title: DEFGDGD
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/DEFGDGD.jcl
---

# DEFGDGD

Batch job (utilities only).

Source: [app/jcl/DEFGDGD.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/DEFGDGD.jcl)

## Relationships

- Reads: [DISCGRP](../datasets/DISCGRP.md), [TRANCATG](../datasets/TRANCATG.md), [TRANTYPE](../datasets/TRANTYPE.md)
- Writes: [DISCGRP.BKUP](../datasets/DISCGRP.BKUP.md), [TRANCATG.PS.BKUP](../datasets/TRANCATG.PS.BKUP.md), [TRANTYPE.BKUP](../datasets/TRANTYPE.BKUP.md)

Utility steps (IDCAMS, SORT and so on): STEP10, STEP20, STEP30, STEP40, STEP50, STEP60
