---
page_id: "2001"
space: CARD
title: CardDemo System Overview
author: Priya Nair
created: 2022-03-14
updated: 2024-11-02
labels: [overview, architecture]
synthetic: true
---

# CardDemo System Overview

CardDemo is our credit card management system. It has two halves: an online part that
runs under CICS, and a nightly batch part that runs as JCL jobs.

## Online (CICS)

Users start at the sign-on screen (transaction CC00, program COSGN00C). After a
successful sign-on, regular users land on the main menu (COMEN01C) and admins land on
the admin menu (COADM01C).

From the main menu a user can:

- view or update an account (COACTVWC, COACTUPC)
- list, view or update credit cards (COCRDLIC, COCRDSLC, COCRDUPC)
- list, view or add transactions (COTRN00C, COTRN01C, COTRN02C)
- request a transaction report (CORPT00C)
- pay a bill (COBIL00C)

Programs pass control to each other with EXEC CICS XCTL and share state through the
CARDDEMO-COMMAREA defined in copybook COCOM01Y.

## Batch

The nightly batch posts the day's card transactions, calculates interest and
produces statements. See the Nightly Batch Runbook for the job order.

## Data

All master data lives in VSAM KSDS files: accounts (ACCTDATA), cards (CARDDATA),
customers (CUSTDATA), the card-to-account cross reference (CARDXREF), transactions
(TRANSACT) and user security (USRSEC).
