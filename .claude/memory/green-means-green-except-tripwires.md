---
name: green-means-green-except-tripwires
description: "\"All tests green\" means green apart from known tripwires for functionality not yet built — documented placeholders are not findings and do not block a commit"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25438ffb-5927-4494-bbfa-cce458e38867
  modified: 2026-09-24T12:24:35.980Z
---

A suite reporting failures is still "green" when those failures are known tripwires for functionality
that has not been built — a property raising `NotImplementedError`, a case asserting a sum nothing can
compute yet. They are not regressions, not findings, and not a reason to hold a commit.

**Why:** the rebuild is full of deliberate placeholders that raise rather than return a plausible
wrong answer. Treating each run's red as a problem means re-diagnosing the same expected failures
every session and reporting them as though something broke.

**How to apply:**
- Before calling a failure a finding, check whether it is documented as expected — a component's
  README or test plan usually says so outright, and `git show HEAD:<file>` tells you whether the raise
  predates your change.
- Report it in one clause — "N fail, all documented tripwires" — not a paragraph of diagnosis.
- A failure in code your change touched is still yours. This covers documented placeholders, not
  anything that merely fails.

Related: [[fail-loud-until-production]] is why the placeholders raise in the first place, and
[[other-sessions-uncommitted-work]] is why an unfamiliar failure is often not yours at all.
