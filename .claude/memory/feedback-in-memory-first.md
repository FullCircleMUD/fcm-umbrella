---
name: feedback-in-memory-first
description: "Game state is loaded lazily from the DB once, then served from memory; every write updates DB and memory together"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9f68f648-93bc-4223-bd69-b580a76ab08e
  modified: 2026-09-27T14:59:18.748Z
---

Keep as much game state in memory as possible. Anything that must come from the database is loaded lazily, once, on first read, and served from memory after that; every write updates the row and the in-memory copy in the same call.

**Why:** Tim does not want hot or repeated paths "smashing the database" — a DB read per check is the thing to avoid.

**How to apply:** For a new cached collection, follow the groups pattern (`member_instances`, `request_instances`, the `_group` slot): lazy-built on first read, writers update it alongside the rows, no per-read query. Don't argue "it's only a typed command, one query is fine" as a reason to skip the in-memory copy. Related: [[property-writes-by-assignment]].
