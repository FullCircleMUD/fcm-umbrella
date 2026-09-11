---
name: feedback_test_instance_credentials
description: Local test/demo instances use root / p as the superuser username and password — never anything deployed.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4564f16a-cfb5-4642-a69f-991804917e1f
  modified: 2026-09-10T20:24:20.773Z
---

Superuser credentials for a **local testing instance** — a demo gamedir, an `examples/` gamedir, a
throwaway instance — are `root` / `p`.

**Why:** they get typed dozens of times a session. Anything longer is friction for no benefit on an
instance that holds nothing and is reachable from nowhere.

**How to apply:** create the superuser with those, and say so in that demo's README. **Local only** —
never for anything deployed, shared, or reachable off the machine. Related:
[[feedback_no_troubleshooting_relics]].
