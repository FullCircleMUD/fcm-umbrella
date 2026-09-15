---
name: feedback-name-the-deviation-and-its-benefits
description: Deviating from a reference implementation means saying so up front and listing concrete benefits — not substituting quietly
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f01b092e-2f6b-4378-8e0d-8e478bcd879c
  modified: 2026-09-15T16:05:18.860Z
---

When writing something that already exists elsewhere (the substrate, a legacy helper, a sibling
library), say plainly that the new version differs and itemise what the change buys: faster query,
easier return format to process, more intuitive for the consumer, fewer call sites. If the list
cannot be filled with concrete items, don't make the change.

**Why:** stated 2026-09-15 on `fcm-xrpl`'s `sum_or_zero`. A reshaped helper was presented as *the*
helper rather than as a deviation, and only surfaced because Tim asked what the new signature bought.
The answer was three lines of boilerplate. The objection is to the silent substitution, not to
changing things — a justified change is fine, an unannounced one is not.

**How to apply:** lead with "this differs from X, here is what it buys: 1, 2, 3". Tim decides. An
empty benefit list is the answer, not a prompt to argue. Do not over-correct into reverting
everything either — the ask is disclosure, not conservatism. See
[[feedback-cases-need-a-real-trigger]], [[no-bulk-carry-over-from-src-old]].
