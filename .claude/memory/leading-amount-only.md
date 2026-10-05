---
name: leading-amount-only
description: "Current practice: a quantity of a thing in a command leads (`deposit 50 gold`); menu value-setting like point buy takes either order. Open to change"
metadata:
  node_type: memory
  type: project
  originSessionId: 1e98abbb-3f82-411c-b647-c88fa87d7bd7
  modified: 2026-09-25T20:14:05.919Z
---

The current approach: a quantity of an in-game thing in a command's arguments leads the target — `deposit 50 gold`, `take 20 wheat` — read with evennia-targeting's `parse_quantity`. Ported commands have dropped legacy's trailing form (`gold 50`) so far.

Menu input that sets a value is outside it: chargen point buy currently takes `14 str` and `str 14` (2026-10-03).

**Why:** one grammar for quantities, read by one shared parser (Tim, 2026-09-25, porting the bank).

**How to apply:** use it as the default when porting a command. It is what we are doing now, not a constraint — if a better way turns up, raise it rather than citing this. Related: [[feedback-standardisation-is-the-gain]].
