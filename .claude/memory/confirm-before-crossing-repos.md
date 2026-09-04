---
name: confirm-before-crossing-repos
description: "When tasked in one repo, confirm before making changes in another"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59e09c63-3179-49d1-b4b3-3788d7782f28
  modified: 2026-09-01T18:14:57.216Z
---

When the work has been scoped to one repository, **confirm explicitly before changing anything in
another one**. Reading across repos is always fine; writing is not.

**Why:** the umbrella holds many repos and sessions are often assigned one each. Two sessions editing
the same file collide, and a change made outside the assigned repo lands where nobody is expecting it.

**How to apply:** if a task in repo A implies an edit in repo B — a reciprocal doc section, a
dependency the other side must add, a method the other library should expose — **specify it and hand
it over** rather than making it. Name the method, signature, return and the case that needs it, and
let the user route it.

Live instance: the `fcm-xrpl` / `fcm-telemetry-spawn` extraction is split across two concurrent
sessions, one per library. See [[telemetry-spawn-parked-pending-xrpl]].
