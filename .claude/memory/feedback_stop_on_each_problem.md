---
name: feedback_stop_on_each_problem
description: "One issue per reply, then stop — never a reply carrying several things that each need a decision"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b3bba4c6-d5c8-403d-8943-4b214af2df80
  modified: 2026-09-18T21:39:36.017Z
---

**One issue per reply.** Surface it, stop, let Tim address it, then give the next
one. This applies to anything needing his decision — audit findings, open design
calls, flagged caveats, things I chose that he might want changed — not just
reviews.

**Why:** a reply carrying ten items gets one of them discussed. The discussion
scrolls the other nine off the screen and they are never addressed. Recovering them
means Tim scrolling back through pages of output, which is my failure to manage, not
his to fix. (Confirmed 2026-09-16. Originally 2026-06-19, narrower — auto-fixing
batch-identified problems instead of waiting.)

**Silence on a point is not agreement.** When a reply did carry several items and Tim
answers one, the rest are *unanswered*, not approved. Never build on them, never
write them up later as "considered and agreed", and never treat a "that's fine" aimed
at the top item as covering the ones below it. Go back and ask, one at a time.

**Why:** an unflagged assumption compounds. A design point buried under an answered
question gets carried into the code, then into the next unit, and surfaces turns later
as work already built on a decision Tim never made. Found 2026-09-18: a change to when
archiving fires was shown inside a multi-point reply, the top point was answered, and
the rest was treated as settled for two units of work.

**How to apply:** pick the single most important open item and give only that.
Everything else waits for its turn. Never close a reply with a list of further
concerns, "two more things", or a table of open decisions. Do not Edit/fix on the
strength of an ambiguous "and the other one?" — treat that as "explain/propose," not
"go fix it." Relates to [[feedback_cheap_tests_over_theory]],
[[feedback_terse_confirmations]], [[feedback_never_invent_detail]].
