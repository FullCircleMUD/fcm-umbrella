---
name: feedback_stop_on_each_problem
description: "When auditing/reviewing, surface one problem at a time and stop for the user's decision before fixing or moving on"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3bba4c6-d5c8-403d-8943-4b214af2df80
---

When I identify a problem (a broken link, a convention breach, a bug, anything an
audit surfaces), **stop and let the user decide whether it needs fixing** before I
edit anything or go looking for the next problem. One finding → pause → user
adjudicates (fix / leave / defer) → only then proceed.

**Why:** rushing ahead to fix automatically, or to enumerate the next ten problems,
leaves far too much room to miss things — and it takes the fix/no-fix decision away
from the user. Deliberate, one-at-a-time adjudication keeps coverage tight and keeps
the user in control of what actually changes. (Confirmed 2026-06-19, after I batch-
identified broken links and then auto-applied edits without waiting.)

**How to apply:** present a single finding clearly, then wait. Do not Edit/fix on
the strength of an ambiguous "and the other one?" — treat that as "explain/propose,"
not "go fix it." Propose the fix, stop, and let the user say yes. Relates to
[[feedback_cheap_tests_over_theory]].
