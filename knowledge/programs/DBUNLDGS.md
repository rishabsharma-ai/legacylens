---
type: program
title: DBUNLDGS
description: Program DBUNLDGS.
tags:
- batch
- ims-db2-mq-authorization
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL
---

# DBUNLDGS

Program DBUNLDGS.

Source: [app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/DBUNLDGS.CBL) lines 1-366

## Relationships

- Calls: `CBLTDLI`
- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), [IMSFUNCS](../copybooks/IMSFUNCS.md), [PADFLPCB](../copybooks/PADFLPCB.md), [PASFLPCB](../copybooks/PASFLPCB.md), [PAUTBPCB](../copybooks/PAUTBPCB.md)

## Paragraphs (15)

- `MAIN-PARA` (line 164)
- `1000-INITIALIZE` (line 182)
- `1000-EXIT` (line 212)
- `2000-FIND-NEXT-AUTH-SUMMARY` (line 216)
- `2000-EXIT` (line 258)
- `3000-FIND-NEXT-AUTH-DTL` (line 263)
- `3000-EXIT` (line 296)
- `3100-INSERT-PARENT-SEG-GSAM` (line 300)
- `3100-EXIT` (line 316)
- `3200-INSERT-CHILD-SEG-GSAM` (line 319)
- `3200-EXIT` (line 335)
- `4000-FILE-CLOSE` (line 338)
- `4000-EXIT` (line 354)
- `9999-ABEND` (line 357)
- `9999-EXIT` (line 365)
