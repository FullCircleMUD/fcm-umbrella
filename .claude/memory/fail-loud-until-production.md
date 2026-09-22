---
name: fail-loud-until-production
description: "Everything raises loudly through pre-alpha and staging; quietening exceptions is a pre-production decision, not a design default"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cb464e13-b17e-4aa0-9c1d-fc3bd6686928
  modified: 2026-09-22T16:24:50.307Z
---

Raise loudly, never swallow. Through local playtesting, staging and pre-alpha, a bad state stops the
game rather than being logged and stepped over.

**Why:** the plan is to playtest hard locally, then hard again in staging with real players, and get
the game to a bug-free state before production. A swallowed exception is a bug that survives that
process. Loud raises get found and fixed while people are actively looking.

**How to apply:** no bare `except`, no silent fallback, no "log it and carry on" for a state that
should not occur. A refusal that a caller can act on is different — that is a return value, not a
swallowed error. Quietening exceptions before production is a decision for another day and must not
be pre-empted by designing for it now.

**The one sanctioned exception: a batch pass over many subjects catches per subject**, logs the
traceback at ERROR and carries on. One bad item must not stop every character behind it in the queue.
The test is blast radius — a silent gap for one subject is smaller than a silent gap for everyone
after it. `evennia-survival` catches per holder; durability's decay pass catches per item. Anywhere
else, raise.

Related: [[feedback_no_hardening_language]], [[feedback_log_levels_info_vs_warn]].
