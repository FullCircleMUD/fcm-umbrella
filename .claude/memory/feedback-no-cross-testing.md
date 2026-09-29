---
name: feedback-no-cross-testing
description: "A typeclass's tests assert composition only — the mixin is on the chain, and any re-declaration; what a component does is tested once, in that component"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 329ea1b4-1469-4c2c-aa46-12816f64fcef
  modified: 2026-09-25T21:09:19.077Z
---

A typeclass's tests check **composition**: the component's mixin is in the MRO, and whatever the
typeclass itself re-declares (an actor's `unseen_name`, say). They never test the component's
behaviour — its data shape, what its functions return.

**Why:** `typeclasses/base` and `typeclasses/items` tested perception's behaviour (per-sense fields,
`perceive` returning text). Perception moved on, its own tests moved with it, and the typeclass copies
rotted unnoticed until a later refactor turned them up. Cross-testing means one change has to be made
in several suites, and the ones nobody remembers go stale.

**How to apply:** when writing or reviewing a typeclass test, keep it to "is it composed" and "is its
own override right". If a case exercises what the mixin does, it belongs in the component's plan.
Related: [[feedback-cases-need-a-real-trigger]].
