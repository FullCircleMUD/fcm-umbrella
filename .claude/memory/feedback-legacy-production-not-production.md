---
name: feedback-legacy-production-not-production
description: "Call src_old/ code \"legacy production\", never \"production\" — it was production, it isn't now."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 906ab2a1-b57c-42e0-8ad5-7c4ae9cd03cf
  modified: 2026-09-16T13:32:09.113Z
---

Code in `src_old/` is **legacy production**. Never call it "production" unqualified.

**Why:** it *was* production; it isn't now. "Production" unqualified reads as currently-running
and blurs the line the rebuild depends on — see [[rebuild-not-retrofit]] and
[[no-bulk-carry-over-from-src-old]].

**How to apply:** "legacy production code", "the legacy implementation", "legacy production
non-test code" when distinguishing it from `src_old/game/tests/`. The rebuild in `src/` is the
thing that becomes production.
