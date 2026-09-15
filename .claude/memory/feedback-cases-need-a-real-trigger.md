---
name: feedback-cases-need-a-real-trigger
description: A test case earns its place only from a real bug or a plausible refactor — not from a pattern seen in reference code
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f01b092e-2f6b-4378-8e0d-8e478bcd879c
  modified: 2026-09-15T15:24:29.359Z
---

A test case needs a trigger that exists in *this* library: a bug that actually happened, or a
plausible way someone refactors into one by misreading the code. A pattern noticed in `src_old/` or
another codebase is neither.

**Why:** stated 2026-09-15 on `fcm-xrpl` TQ-03, written to guard an `or Decimal(0)` idiom read in the
substrate. `fcm-xrpl` contained no `aggregate()` or `Sum()` at all, so there was nothing to guard —
and the swap it feared was unobservable anyway. Guarding an absent pattern is the rebuild rule failing
without a line being copied: the old design still shaped what got written.

**How to apply:** before writing a case, name the trigger. No trigger, no case. Applies to defensive
code and raised concerns the same way. See [[no-bulk-carry-over-from-src-old]],
[[feedback_no_manufactured_objections]].
