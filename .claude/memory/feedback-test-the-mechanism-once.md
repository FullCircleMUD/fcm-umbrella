---
name: feedback-test-the-mechanism-once
description: "A test proves a mechanism once; don't extend it for each new instance that rides the same mechanism"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c8b68d75-546f-40ec-938a-71d67627c3a3
  modified: 2026-09-30T13:46:13.184Z
---

A test pins the mechanism, not every outcome it produces. Once a case proves the mechanism (e.g. CF-04: boot problems arrive grouped, not one at a time), a new setting riding that mechanism doesn't need adding to the case.

**Why:** 2026-09-30 — I offered to extend CF-04 with the new payload setting. Tim: tests written to specific outcomes rather than the mechanism are the problem; if two errors arrive grouped, the architecture groups them all.

**How to apply:** before proposing to extend a test for a new instance, ask whether it tests a mechanism already proven. If so, leave it. Related: [[feedback-no-cross-testing]], [[feedback-cases-need-a-real-trigger]].
