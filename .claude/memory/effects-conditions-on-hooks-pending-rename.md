---
name: effects-conditions-on-hooks-pending-rename
description: "evennia-effects-conditions spec hooks use on_ (on_apply, on_remove, on_tick, on_pre_apply_new); renaming to at_ is deferred."
metadata:
  node_type: memory
  type: project
  originSessionId: 1501f45f-3477-4930-a432-9af4a1a14a76
  modified: 2026-09-28T13:53:17.862Z
---

`evennia-effects-conditions` `EffectSpec` hooks are `on_`-prefixed, against Evennia's `at_` convention. Tim chose (2026-09-28) to keep `on_` for now, including the new `on_pre_apply_new`, and standardise later.

Size when sized: ~86 references across 13 files — library src/tests/docs plus `src/router` catalogue entries.

Related: [[feedback-follow-evennia-conventions]].
