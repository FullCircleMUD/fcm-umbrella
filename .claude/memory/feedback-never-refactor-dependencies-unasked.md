---
name: feedback-never-refactor-dependencies-unasked
description: Never refactor existing code that other code depends on without asking first — not as a side effect of building something new.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d20119e7-abb1-4931-81f9-967ef2e8f37d
  modified: 2026-09-21T02:13:55.501Z
---

Never refactor, restructure or "extract" existing working code without asking first. Not as a
side effect of adding something new, not to remove duplication, not when the reasoning is sound.
Ask, and wait.

**Why:** building `EnumListProperty` I also rewrote `EnumProperty`'s internals so the two could
share a helper — unasked, unflagged, and without checking the five components that declare one. The
verification came out clean, but that was luck. It turned a session about the item-restrictions
mixin into an unplanned refactor-and-regression-hunt, and it cost trust, which is worse: "how can I
trust you to work with you when you do things like this".

**How to apply:** the stated scope is the file list. Anything outside it gets a question, not an
edit. `git diff --stat` is the check — if a file is in there that was not in the ask, I overstepped.
Duplication in code that does not exist yet beats churn in code that works. See
[[feedback-name-the-deviation-and-its-benefits]] — this is the harder form of it: for a dependency
of other code, naming the deviation is not enough, it needs agreement before the edit.
