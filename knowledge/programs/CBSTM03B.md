---
type: program
title: CBSTM03B
description: Does file processing related to Transact Report
tags:
- base
- batch
- program
resource: https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBSTM03B.CBL
---

# CBSTM03B

Does file processing related to Transact Report

Source: [app/cbl/CBSTM03B.CBL](https://github.com/aws-samples/aws-mainframe-modernization-carddemo/blob/59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e/app/cbl/CBSTM03B.CBL) lines 1-230

## Relationships

- Called by: [CBSTM03A](../programs/CBSTM03A.md)

## Paragraphs (14)

- `0000-START` (line 116)
- `9999-GOBACK` (line 130)
- `1000-TRNXFILE-PROC` (line 133)
- `1900-EXIT` (line 151)
- `1999-EXIT` (line 154)
- `2000-XREFFILE-PROC` (line 157)
- `2900-EXIT` (line 175)
- `2999-EXIT` (line 178)
- `3000-CUSTFILE-PROC` (line 181)
- `3900-EXIT` (line 200)
- `3999-EXIT` (line 203)
- `4000-ACCTFILE-PROC` (line 206)
- `4900-EXIT` (line 225)
- `4999-EXIT` (line 228)
