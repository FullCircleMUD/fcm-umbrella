---
name: always-router-plus-multiple-shards
description: "FCM only ever runs in the evennia-scaling environment — a router and several shards, never one server"
metadata:
  node_type: memory
  type: project
  originSessionId: a89f8303-18d6-48fc-86a1-0c7484893460
  modified: 2026-10-19T20:10:16.293Z
---

The game only ever runs under evennia-scaling with a router and multiple shards; it is never run on a single server. Stated by Tim 2026-10-19.

**Why:** a single-server path would be design and test surface for a deployment that never happens.

**How to apply:** design and review cross-instance work (spawn, telemetry, `who`, presence) for router + several shards; don't propose single-server fallbacks or monolith modes. Related: [[shards-superseded-by-scaling]].
