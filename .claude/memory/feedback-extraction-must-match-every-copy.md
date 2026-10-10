---
name: feedback-extraction-must-match-every-copy
description: "Before proposing to extract or move a helper, check its output matches every copy it replaces; if not, it is a behaviour change — say so and list consumer edits"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 60bcbd38-f6c8-4635-851c-f6adbf81bc39
  modified: 2026-10-09T17:06:46.408Z
---

An extraction is only "moving the helper" when the new function returns exactly what each copy it replaces returned. If the shape, labels or types differ in any way, it is a behaviour change: say so up front and list every consumer line that must change, before Tim approves.

**Why:** 2026-10-09 — `_held_names` existed in death (string labels) and bank (`TargetKind`). I proposed `get_held_fungible_names` on the fcm-xrpl mixin as a swap, built it with a new `FungibleKind` label, and only discovered at the death refactor that every label comparison in both consumers had to change. Tim approved a move and got a redesign.

**How to apply:** trace each copy's return value into its callers (what compares or passes it on) before writing the proposal. Present the result as either "identical — import swap only" or "differs in X — these N places change". Related: [[feedback-ask-before-a-structural-change]], [[feedback-never-refactor-dependencies-unasked]].
