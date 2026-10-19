---
page_id: "2006"
space: CARD
title: Bill Payment Feature
author: Sofia Alvarez
created: 2023-03-01
updated: 2024-09-12
labels: [online, payments]
synthetic: true
---

# Bill Payment Feature

Online bill payment (transaction CB00) lets a customer pay their card balance.

## Behaviour

- The customer enters the account ID and sees the current balance.
- If the balance is zero or negative the screen shows "You have nothing to pay...".
- The customer confirms with Y. The payment always clears the full balance; partial
  payments are not supported.

## What gets written

The program writes one transaction to TRANSACT with type code 02, category 2 and the
description "BILL PAYMENT - ONLINE", then subtracts the amount from the account's
current balance in ACCTDATA.

The new transaction ID is the highest existing transaction ID plus one.
