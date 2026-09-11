---
name: cascade-migration-queue
description: "The linter's hand_rolled_router / hand_rolled_resolution errors are the cascade-migration queue, not defects — don't migrate a library unless asked."
metadata: 
  node_type: memory
  type: project
  originSessionId: d87a8dde-3ada-482e-89f5-046b0612bf88
  modified: 2026-09-11T13:46:28.854Z
---

The standard (2026-09-11) requires libraries owning alias tables to declare a `db_spec` to
`evennia-database-cascade` — no own router, no resolution code. Four libraries pre-date it:
evennia-ai-memory, evennia-archive, evennia-message-bus, fcm-xrpl error on `hand_rolled_router` /
`hand_rolled_resolution`; evennia-scaling and evennia-shards warn on `models_without_spec`.

**Why:** same pattern as [[logging-migration-pass-pending]] — the errors are the work queue.

**How to apply:** don't migrate a library to the cascade unless asked. The cascade has no real
consumer yet; the first migration proves it live.
