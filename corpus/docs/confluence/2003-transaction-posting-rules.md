---
page_id: "2003"
space: CARD
title: Transaction Posting Rules
author: Priya Nair
created: 2022-06-10
updated: 2024-08-15
labels: [business-rules, batch, posting]
synthetic: true
---

# Transaction Posting Rules

The daily posting program, CBTRN02C, validates each transaction before posting it.
A transaction that fails a check goes to the rejects file with a reason code.

## Reject reason codes

| Code | Meaning                                      | Check                                                    |
|------|----------------------------------------------|----------------------------------------------------------|
| 100  | Invalid card number                          | The card number is not in the CARDXREF cross reference.  |
| 101  | Account record not found                     | The account linked to the card is not in ACCTDATA.       |
| 102  | Overlimit transaction                        | Cycle credit minus cycle debit plus the amount is above the credit limit. |
| 103  | Transaction received after account expiration | The transaction date is after the account expiry date.  |

Codes 102 and 103 are checked together, and if both fail the record carries 103.

## What posting updates

For each valid transaction the program:

1. writes the transaction to TRANSACT,
2. updates the account's current balance and cycle credit or debit in ACCTDATA,
3. adds the amount to the category balance in TCATBALF.

The category balance file is what the interest job reads the next step.
