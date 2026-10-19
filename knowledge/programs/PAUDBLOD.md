---
type: program
title: PAUDBLOD
description: Program PAUDBLOD.
tags:
- batch
- ims-db2-mq-authorization
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL
---

# PAUDBLOD

Program PAUDBLOD.

Source: [app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/app-authorization-ims-db2-mq/cbl/PAUDBLOD.CBL) lines 1-369

## Relationships

- Calls: `CBLTDLI`
- Includes: [CIPAUDTY](../copybooks/CIPAUDTY.md), [CIPAUSMY](../copybooks/CIPAUSMY.md), [IMSFUNCS](../copybooks/IMSFUNCS.md), [PAUTBPCB](../copybooks/PAUTBPCB.md)

## Paragraphs (17)

- `MAIN-PARA` (line 169)
- `1000-INITIALIZE` (line 190)
- `1000-EXIT` (line 218)
- `2000-READ-ROOT-SEG-FILE` (line 222)
- `2000-EXIT` (line 239)
- `2100-INSERT-ROOT-SEG` (line 242)
- `2100-EXIT` (line 264)
- `3000-READ-CHILD-SEG-FILE` (line 269)
- `3000-EXIT` (line 290)
- `3100-INSERT-CHILD-SEG` (line 292)
- `3100-EXIT` (line 315)
- `3200-INSERT-IMS-CALL` (line 318)
- `3200-EXIT` (line 338)
- `4000-FILE-CLOSE` (line 341)
- `4000-EXIT` (line 357)
- `9999-ABEND` (line 360)
- `9999-EXIT` (line 368)
