---
name: feedback-commit-at-the-agreed-point
description: "A commit approval given alongside a stated plan applies at the point the plan named, not immediately"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c8b68d75-546f-40ec-938a-71d67627c3a3
  modified: 2026-10-04T15:57:51.242Z
---

When Tim approves a commit in the same breath as a plan ("do X, then commit"), the approval is for the commit at that point in the plan — not now.

**Why:** 2026-09-30 — Tim said commit after the boot check; a later "yes, you can commit to main" answered a stacked question and was read as "commit now". The commit landed a unit early.

**How to apply:** when replies answer several stacked questions at once, map each answer to its question before acting; if an approval could mean "now" or "at the agreed point", take the agreed point. Better still, don't stack a commit question with design questions. See [[feedback_stop_on_each_problem]].

**Offer a commit once, then drop it.** 2026-10-04 — Tim: "I'll tell you when I want it committed." Asking again in every reply is noise; uncommitted work waits for him to raise it.
