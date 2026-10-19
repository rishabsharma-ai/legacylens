---
page_id: "2005"
space: CARD
title: Online Sign-on and Security
author: Marcus Lee
created: 2022-01-19
updated: 2024-04-30
labels: [online, security]
synthetic: true
---

# Online Sign-on and Security

The sign-on program reads the user's record from the USRSEC file using the user ID
typed on the screen. The record layout is in copybook CSUSR01Y.

If the password matches, the program saves the user ID and user type in the
COMMAREA and transfers control:

- user type A (admin) goes to the admin menu, COADM01C
- any other type goes to the main menu, COMEN01C

A wrong password shows "Wrong Password. Try again ..." and keeps the user on the
sign-on screen. There is no lockout after repeated failures.

Users are maintained by admins with the user programs COUSR00C (list), COUSR01C
(add), COUSR02C (update) and COUSR03C (delete).
