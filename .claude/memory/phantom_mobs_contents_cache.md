---
name: phantom-mobs-contents-cache
description: Phantom/unkillable mobs — handler leak fixed and deployed; null shard_id now blocked by a guard; room-cache drift still unexplained
metadata: 
  node_type: memory
  type: project
  originSessionId: 5c171053-81dc-40eb-a35d-b8d83ca4cc34
  modified: 2026-08-19T02:07:24.095Z
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

**Null `shard_id` — now impossible to create.** `evennia-shards` 0.1.3 refuses any
`ObjectDB` INSERT that would land unstamped, on both `save()` and `bulk_create()`,
and logs it at ERROR to `shards.log` before raising. Deliberate unstamped inserts
opt in via `allow_unstamped_insert()` — the library's chargen, and FCM's account
bank in `at_post_login`. See
[tenancy.md](../../libraries/evennia-shards/docs/tenancy.md#the-unstamped-insert-guard).

Whether NULL rows explain the cache drift is still **unconfirmed** — a NULL row is
invisible to every tenant-filtered query, so `filter(db_location=room)` would miss
it. The original intermittent case did not reproduce during the 2026-08-18 play
test; it will now announce itself in `shards.log` if it recurs.

**Unsolved.** Room caches disagree with the database, dozens of rooms, only for
mobs that move. Ruled out: add/remove pairing, each verified on return; `init`
rebuilds; duplicate room objects; write failures; tenancy on shard ids; a
single-threaded race.

**Measurement traps.** Reading `obj.contents_cache` *builds* one — use
`obj.__dict__["contents_cache"]`. Two separate `py` commands see different worlds.
The router drifts by design; check `evennia_shards.get_role()` first.

**Tooling** on branch `mob-ghost-debug` (probes, tests, `PHANTOM_MOB_HUNT.md`).
Never on `main`.
