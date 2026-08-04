---
name: feedback-no-legacy-data-concerns
description: "Don't raise legacy/existing-database concerns when weighing shards-era changes — pre-alpha, fresh DB every deploy, until a sharded deployment is live and working"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c41cb4a-335c-4edf-8beb-92321dc36d13
  modified: 2026-08-04T02:49:40.634Z
---

While the sharded implementation is being built, **do not raise existing-database or
legacy-data impact** as a consideration for a change — stale rows, orphaned records,
"is there a live DB still carrying X", data that a removed cleanup mechanism might
strand. Confirmed emphatically 2026-08-03.

**Why:** FCM is pre-alpha. Local testing always begins by redeploying a fresh database.
The live sharded deployment will delete the current non-sharded implementation in its
entirety. There is no legacy data to preserve, so raising it adds friction to every
deletion decision without informing it.

**How to apply:** when judging whether to delete a mechanism, weigh only its current and
future correctness — not what it may have left behind. This is scoped: it holds **until
there is a live, working sharded deployment**, after which existing-data impact becomes
a real consideration again. Distinct from [[feedback_stop_on_each_problem]], which is
about surfacing findings one at a time — this one is about which findings are worth
surfacing at all right now.
