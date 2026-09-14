---
name: shards-superseded-by-scaling
description: evennia-shards is being deprecated; evennia-scaling is the standard and the rebuild targets it
metadata: 
  node_type: memory
  type: project
  originSessionId: f7d8cab1-b454-46a6-b725-7b76d2d34e2c
  modified: 2026-09-13T01:02:28.866Z
---

`evennia-shards` is on its way out; `evennia-scaling` (feature complete, needs the logging refactor) is the new standard, and the FCM rebuild will build on scaling, not shards. Stated 2026-09-10.

The end state is **retired from service and yanked from PyPI, not deleted**, once scaling is implemented. Confirmed 2026-09-11.

**Why:** shards has the fuller docs and CLAUDE.md, so a session would otherwise treat it as the more current of the two.

**How to apply:** don't consider shards in new library development or design decisions; don't propose features or integrations for it. Its `security=True` log divergence died with this — see [[library-no-logging-evennia-targeting]] for the shape of such rulings.

**`evennia-mob-spawner` carries a real shards integration and needs converting** — the shard-scoped command gates, the `shard`-first level mandate, the `owning_shard` stamp and `docs/shards-compatibility.md`. That is a piece of work in its own right, unscheduled as at 2026-09-12, and the open question inside it is `ms_spawn_report`: its whole-world census has no unscoped process to run on once each instance holds its own database. Tracked in that library's `docs/interoperability.md` § evennia-scaling.
