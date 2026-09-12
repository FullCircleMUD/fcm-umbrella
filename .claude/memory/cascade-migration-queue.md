---
name: cascade-migration-queue
description: "The linter's hand_rolled_router / hand_rolled_resolution errors are the cascade-migration queue, not defects — don't migrate a library unless asked."
metadata: 
  node_type: memory
  type: project
  originSessionId: d87a8dde-3ada-482e-89f5-046b0612bf88
  modified: 2026-09-11T15:16:10.705Z
---

The standard (2026-09-11) requires libraries owning alias tables to declare a `db_spec` to
`evennia-database-cascade` — no own router, no resolution code. Still to migrate:
evennia-ai-memory and fcm-xrpl, which error on `hand_rolled_router` / `hand_rolled_resolution`;
evennia-shards warns on `models_without_spec`.

**`evennia-scaling`'s `models_without_spec` warn is not queue work.** Its ticket table belongs in the
consumer's game database deliberately — one instance writes and reads it seconds apart, and after a
wipe no handoff is in flight — which is the standard's own game-database case. `TK-05` pins it and
the library's CLAUDE.md records it as a sanctioned divergence. Don't "fix" it into a spec.

**Why:** same pattern as [[logging-migration-pass-pending]] — the errors are the work queue.

**How to apply:** don't migrate a library to the cascade unless asked. `evennia-archive` migrated
2026-09-11 (first real consumer, proven live: boot, round trip, cascade_migrate) — copy from it.
`evennia-message-bus` followed. `evennia-scaling` 2026-09-12 as a *consumer* rather than an alias
owner: its test settings and its three demo gamedirs call `configure()`, and it declares no spec.

**`configure()` is called from the settings file `DJANGO_SETTINGS_MODULE` names, last, after its
imports** — never from a shared settings module the per-instance files import. From there it re-enters
Django's settings loading and the boot dies on an `AttributeError` for a setting that is set. Recorded
in the cascade's own `docs/installing.md` § 4.
