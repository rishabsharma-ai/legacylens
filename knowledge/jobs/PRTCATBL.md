---
type: job
title: PRTCATBL
description: Batch job (utilities only).
tags:
- base
- job
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/PRTCATBL.jcl
---

# PRTCATBL

Batch job (utilities only).

Source: [app/jcl/PRTCATBL.jcl](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/jcl/PRTCATBL.jcl)

## Relationships

- Reads: [TCATBALF](../datasets/TCATBALF.md), [TCATBALF.BKUP](../datasets/TCATBALF.BKUP.md)
- Writes: [TCATBALF.BKUP](../datasets/TCATBALF.BKUP.md), [TCATBALF.REPT](../datasets/TCATBALF.REPT.md)

Utility steps (IDCAMS, SORT and so on): DELDEF, STEP10R
