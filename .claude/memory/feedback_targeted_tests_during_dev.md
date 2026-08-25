---
name: feedback_targeted_tests_during_dev
description: "While iterating run only the file(s) just touched; save the broad multi-suite sweep for the end of a body of work, and the full suite for end of day"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0d698307-7faf-451e-ba74-bd5adfbc796e
  modified: 2026-08-25T20:24:39.954Z
---

Three tiers, and pick the smallest one that answers the question:

1. **While iterating** — run only the test file just edited. Seconds.
2. **At the end of a body of work** — the broad sweep across the related suites. Minutes.
3. **End of day, or when Tim asks** — the full `evennia test --settings settings tests` run. Close
   to two hours.

**Why:** a ~15-suite sweep costs about four minutes. Running one after every small change means Tim
sits watching a progress bar repeatedly for no new information — confirmed with visible irritation
2026-08-25 ("how long are we gonna wait and sit and do nothing for every little single change?").
The full run is worse still: it holds the test databases for its whole duration, so any other
`evennia test` collides and dev work stalls behind it, and it tests the tree as it was at import
time, so results go stale the moment editing continues.

**How to apply:** after editing `tests/typeclass_tests/test_x.py`, run exactly that module. Only
widen when the body of work is finished or when a change plausibly reaches other suites. Always
`tee` multi-package runs to a file, per [[../../ops/DEVELOPMENT/TESTING.md]]. Related:
[[feedback_cheap_tests_over_theory]], [[feedback_dont_overinvest_tangents]].
