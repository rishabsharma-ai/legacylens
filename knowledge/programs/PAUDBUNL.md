---
type: program
title: PAUDBUNL
description: Program PAUDBUNL.
tags:
- batch
- ims-db2-mq-authorization
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL
---

# PAUDBUNL

Program PAUDBUNL.

Source: [app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/PAUDBUNL.CBL) lines 1-317

## Relationships

- Calls: `CBLTDLI`
- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), [IMSFUNCS](../copybooks/IMSFUNCS.md), [PAUTBPCB](../copybooks/PAUTBPCB.md)

## Paragraphs (11)

- `MAIN-PARA` (line 157)
- `1000-INITIALIZE` (line 173)
- `1000-EXIT` (line 203)
- `2000-FIND-NEXT-AUTH-SUMMARY` (line 207)
- `2000-EXIT` (line 248)
- `3000-FIND-NEXT-AUTH-DTL` (line 253)
- `3000-EXIT` (line 285)
- `4000-FILE-CLOSE` (line 289)
- `4000-EXIT` (line 305)
- `9999-ABEND` (line 308)
- `9999-EXIT` (line 316)
