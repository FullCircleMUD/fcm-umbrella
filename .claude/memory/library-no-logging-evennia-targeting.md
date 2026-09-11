---
name: library-no-logging-evennia-targeting
description: "evennia-targeting ships the log shim but never calls it — an accepted divergence, not a gap to fix"
metadata: 
  node_type: memory
  type: project
  originSessionId: f7fd84e0-ba3b-4018-8e54-2beb3fb1d6fe
  modified: 2026-09-11T13:11:18.492Z
---

`evennia-targeting` has no logging and needs none. Its `log.py` carries the standard
`evennia-logging-extension` binding (`targeting_log`, migrated 2026-09-11); nothing calls it. The
`library-standards-linter` warns `log_shim_unused` — expected here.

**Why:** predicates are pure (no side effects, no logging, no messaging) and the two helpers are
silent, so no operation warrants a log line. The only refusals are `ValueError` at composition, which
raises. Confirmed with Tim 2026-09-07.

**How to apply:** do not add call sites to clear the warning — that would break the purity principle.
Recorded in the library's own `CLAUDE.md` § Out of scope. Same shape as
[[library-unlicensed-fcm-telemetry-spawn]].
