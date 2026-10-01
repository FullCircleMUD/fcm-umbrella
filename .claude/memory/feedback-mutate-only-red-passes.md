---
name: feedback-mutate-only-red-passes
description: "Mutate only the cases that passed on the red run, not every new case; keep test time proportionate"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a47828bd-d081-46a7-ad12-675db4f26360
  modified: 2026-09-30T23:21:20.051Z
---

Mutate only the cases that passed on the red run — CLAUDE.md step 5 — not every case whose red failure came from the placeholder. Run targeted classes while iterating and the full suite once at the end.

**Why:** Tim, 2026-09-30, after long mutation runs on inset: "There is a limit to how much testing makes sense." Mutating every new case roughly doubled the test time for little gain.

**How to apply:** after the red run, list the cases that passed and mutate those alone. See [[feedback_targeted_tests_during_dev]].
