---
name: phantom-mobs-contents-cache
description: Phantom/unkillable mobs — handler leak fixed and deployed; room-cache drift still unexplained; null shard_id found
metadata: 
  node_type: memory
  type: project
  originSessionId: 5c171053-81dc-40eb-a35d-b8d83ca4cc34
  modified: 2026-08-18T23:48:03.680Z
---

Investigated 2026-08-18.

**Fixed, on `main`.** Mobs leaving a fight kept their `combat_handler`, so
`initiate_attack` no-opped and `ai_wander` returned early — mob passive, stuck,
unkillable. Fixed in `retreat_to_spawn`; plus a guard so delayed attacks check
both parties still exist. Other flee paths checked, not leaky.

**Upstream Evennia bug, not the cause.** `at_idmapper_flush` clears foreign-key
caches by the pre-Django-2.0 name `_<field>_cache`; they live in
`_state.fields_cache`. Reproduced in `test_flush_premise.py`. Overriding it
changed nothing live. Worth reporting upstream.

**Null `shard_id`** — `evennia-shards` only stamps it if a current tenant is set
([tenancy.py:236](../../libraries/evennia-shards/src/evennia_shards/tenancy.py#L236)).
Script ticks and `at_object_creation` have none, so rows save NULL and become
invisible to every ORM query — cannot be found, moved or deleted, and their
holder cannot be deleted either (FK violation). On Tim's backlog. May also explain
the drift, since `filter(db_location=room)` is tenant-filtered. Unconfirmed.

**Unsolved.** Room caches disagree with the database, dozens of rooms, only for
mobs that move. Ruled out: add/remove pairing, each verified on return; `init`
rebuilds; duplicate room objects; write failures; tenancy on shard ids; a
single-threaded race.

**Measurement traps.** Reading `obj.contents_cache` *builds* one — use
`obj.__dict__["contents_cache"]`. Two separate `py` commands see different worlds.
The router drifts by design; check `evennia_shards.get_role()` first.

**Tooling** on branch `mob-ghost-debug` (probes, tests, `PHANTOM_MOB_HUNT.md`).
Never on `main`.
