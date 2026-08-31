---
name: shards-v2-independent-instances
description: "Shards v2 drops the shared Postgres — independent Evennia instances, with archive+xrpl moving characters and the message bus coordinating"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1afdbdce-9713-480c-b097-28942dcaa04b
  modified: 2026-08-31T02:40:02.021Z
---

Shards v2 abandons the shared-Postgres model. Instances become standalone vanilla Evennia servers,
each with its own database.

- A character leaving instance A is archived with its possessions (`evennia-archive`), deleted from A's
  game database, and reconstructed on B's.
- Ownership travels through the XRPL data, which becomes a library as the extraction finishes.
- [[evennia-message-bus-library]] carries the coordination — "this character is arriving, here is its
  archive identifier".
- Net effect is a sharded deployment without a truly sharded environment: no single Postgres, none of
  its bug surface.

**Why:** the complication and bug risk of running many instances over one Postgres is the thing being
designed out.

**How to apply:** when Tim says "non-shards", he means *not shards as it exists today* — not that
shards is irrelevant. Do not evaluate proposals against current shards' shape; that repo is being
refactored. Game DB is per-instance and private; bus, archive and ownership DBs are shared.
