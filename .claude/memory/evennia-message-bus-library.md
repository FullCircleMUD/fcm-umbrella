---
name: evennia-message-bus-library
description: "evennia-message-bus lets separate Evennia instances message each other through a shared bus database; built for [[shards-v2-independent-instances]]"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1afdbdce-9713-480c-b097-28942dcaa04b
  modified: 2026-08-31T02:40:09.099Z
---

`libraries/evennia-message-bus` — messaging between independent Evennia instances over a shared bus
database. Working, round trip proven between the two demo gamedirs in `examples/`. No consumer game
yet, and untried on PostgreSQL.

Design and install docs live in the repo (`docs/design.md`, `docs/messagebus-settings.md`). Not
repeated here.

**Why:** built ahead of its consumer, which is [[shards-v2-independent-instances]].

**How to apply:** scope is messaging between instances, full stop — not how it integrates with other
libraries or the main game. Behavioural change starts in `docs/test-plan.md`, then a test, then code.
