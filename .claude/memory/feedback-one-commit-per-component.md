---
name: feedback-one-commit-per-component
description: "Each component (and each typeclass surface) gets its own commit, even when one change spans several."
metadata:
  node_type: memory
  type: feedback
  originSessionId: e0b7b070-51ba-45ce-93f8-ae5978d10125
  modified: 2026-09-29T12:43:47.415Z
---

A change that touches several components is committed one component at a time — the component's files in one commit, the typeclass surface that composes it in another.

**Why:** Tim stated it (2026-09-29): "each of these is a separate component, it needs to be committed and pushed separately."

**How to apply:** when a unit of work spans `components/<x>` and `typeclasses/<y>`, stage and commit each path set on its own, then push. Still needs Tim's approval per commit. See [[other-sessions-uncommitted-work]].
