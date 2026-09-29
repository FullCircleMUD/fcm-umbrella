---
name: feedback-follow-evennia-conventions
description: "Before naming hooks or inventing a pattern, check what Evennia's standard is and follow it — hooks are at_, never on_."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1501f45f-3477-4930-a432-9af4a1a14a76
  modified: 2026-09-28T13:53:15.111Z
---

Before building anything with a naming scheme or pattern, check what Evennia (or the framework in play) already does, and follow it. Evennia core names every hook `at_`; it has no `on_` hooks.

**Why:** `evennia-effects-conditions` shipped its spec hooks as `on_apply`/`on_remove`/`on_tick` without asking what the standard was — a reinvented wheel Tim now has to standardise later. See [[effects-conditions-on-hooks-pending-rename]].

**How to apply:** when a design introduces hooks, callbacks or a naming pattern, look up the framework's convention first and name it in the proposal. Don't rationalise a divergence after the fact.
