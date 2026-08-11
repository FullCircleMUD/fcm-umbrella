---
name: feedback_targeted_tests_during_dev
description: "Run targeted test suites during dev work; the full suite is an end-of-day job, not a mid-task one"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0d698307-7faf-451e-ba74-bd5adfbc796e
  modified: 2026-08-10T20:29:02.784Z
---

Run only the **targeted** test suites relevant to the change while developing. The full
`evennia test --settings settings tests` run takes close to two hours in `src/game`.

**Why:** a full run holds the test databases for its whole duration, so any other `evennia test`
collides and dev work stalls behind it. It also tests the tree as it was when Python imported the
modules at start, so results go stale the moment editing continues — the run has to be repeated
anyway.

**How to apply:** name the specific suites (`tests.typeclass_tests.test_exit_door`,
`tests.utils_tests.test_movement_messages`, …) — several can be passed in one command. Save the
full suite for end of day, or when Tim asks for it. Always `tee` multi-package runs to a file, per
[[../../ops/DEVELOPMENT/TESTING.md]]. Related: [[feedback_cheap_tests_over_theory]].
