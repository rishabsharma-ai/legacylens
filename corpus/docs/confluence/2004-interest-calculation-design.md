---
page_id: "2004"
space: CARD
title: Interest Calculation Design
author: Daniel Okafor
created: 2021-11-03
updated: 2023-02-07
labels: [business-rules, batch, interest]
synthetic: true
---

# Interest Calculation Design

The interest job (INTCALC, program CBACT04C) runs after posting. It walks the
transaction category balance file, TCATBALF, one account at a time.

## Finding the rate

Each account belongs to a disclosure group. The rate for a group and transaction
category comes from the disclosure group file, DISCGRP. If an account's group has no
row, the program looks up the group called DEFAULT instead.

## The formula

Monthly interest = category balance x annual rate / 1200.

The rate is stored as a percentage, for example 18.00, so dividing by 1200 turns an
annual percentage into a monthly fraction.

## Fees

Late fees and over-limit fees are calculated in the same pass by paragraph
1400-COMPUTE-FEES and posted as separate transactions.

## Output

Interest is written as new transactions to the SYSTRAN file, which COMBTRAN later
merges into TRANSACT.
