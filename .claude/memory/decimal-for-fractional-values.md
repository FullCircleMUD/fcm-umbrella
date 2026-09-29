---
name: decimal-for-fractional-values
description: "The game's own fractional values are Decimal, not float; floats from libraries/Evennia are converted at the edge"
metadata:
  node_type: memory
  type: project
  originSessionId: a47828bd-d081-46a7-ad12-675db4f26360
  modified: 2026-09-28T02:27:17.186Z
---

Current practice (2026-09-27): every fractional value the game stores or computes is a `Decimal`. Where it meets a float from a library or Evennia (evennia-equipment's `WeightProperty`, `delay()` seconds), convert explicitly at that line.

**Why:** Tim wants one numeric type — less variation to troubleshoot, and one fix reaches every instance instead of hunting the same bug in several places. Money is already `Decimal` in fcm-xrpl.

**How to apply:** new fractional properties use `DecimalProperty` (custom_properties); don't introduce floats. Tim may later refactor evennia-equipment's weight to Decimal — his call, not a side-quest. See [[feedback-standardisation-is-the-gain]].
