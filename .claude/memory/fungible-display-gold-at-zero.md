---
name: fungible-display-gold-at-zero
description: "Tim wants get_fungible_display() to always show gold, even at 0 — a small fcm-xrpl refactor, deferred"
metadata:
  node_type: memory
  type: project
  originSessionId: 80acec2b-ec61-4894-bc9b-a497be0449f4
  modified: 2026-09-29T17:54:18.238Z
---

Tim's preference (2026-09-29): a holder's fungibles display always shows a gold line, `0` included, even with no resources. `fcm-xrpl`'s `XRPLFungibleInventoryMixin.get_fungible_display()` currently omits gold at 0 and returns `Nothing.` when nothing is held.

**Why:** deferred as a small refactor in the method itself; the `inventory` command in `src/router/commands/equipment/` just calls the method and shows whatever it returns.

**How to apply:** callers call the method and show what it returns — no conditional logic around it. Any change to what shows (hiding it when empty, gold at 0) goes in the method. When touching `get_fungible_display()`, raise it. Check its other callers first — a corpse or container showing `Gold: 0` may not be wanted.
