---
name: leading-amount-only
description: "Amounts in player commands are leading only (`50 gold`, `all wheat`); no trailing-amount form anywhere in the game"
metadata:
  node_type: memory
  type: project
  originSessionId: 1e98abbb-3f82-411c-b647-c88fa87d7bd7
  modified: 2026-09-25T20:14:05.919Z
---

The current game-wide standard: an amount leads the target (`deposit 50 gold`, `all wheat`), parsed by evennia-targeting's `parse_quantity`. No trailing form (`gold 50`) in any command, even where legacy accepted one.

**Why:** one grammar across every command, parsed by the one shared parser; stated by Tim 2026-09-25 while porting the bank.

**How to apply:** when porting a command whose legacy syntax took a trailing amount, drop that form rather than hand-rolling it. Related: [[feedback-standardisation-is-the-gain]].
