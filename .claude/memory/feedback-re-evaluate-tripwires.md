---
name: feedback-re-evaluate-tripwires
description: "On meeting a NotImplementedError tripwire, check whether what it waits for now exists — if so remove it and build that part; if not, add it to the gap checklist"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a18aa240-91f7-4bba-b1b7-71678e69ed7f
  modified: 2026-10-03T23:59:50.749Z
---

Whenever a `NotImplementedError` tripwire turns up (a test run, a traceback, reading code), re-evaluate it: has the thing it was set to wait for been built since?

- **Built** → propose removing the tripwire and building that part out.
- **Not built** → add it to `ops/scratch/rebuild-gap-checklist.md` if it isn't there.

**Why:** Tim, 2026-10-03, on the encumbrance gate's messaging tripwire. Tripwires go stale silently once their dependency lands.

**How to apply:** don't just report a tripwire as pre-existing and move on. Related: [[green-means-green-except-tripwires]].
