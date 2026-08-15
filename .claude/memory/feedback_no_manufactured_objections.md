---
name: feedback_no_manufactured_objections
description: Raise only objections that bind in this world; never pad a list to strengthen a position
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 56ad3889-ab87-40e3-af1a-5a0a6b9f4a1f
  modified: 2026-08-15T00:31:28.178Z
---

Never manufacture objections. Raise a concern only when it has a live consequence in *this*
codebase, and check that it binds before stating it. One real objection beats three, and zero real
objections means say "no, there's no reason" and move on.

**Why:** listing every theoretical difference (what a class change would cost, what a mixin
provides) reads as building an argument to win rather than giving feedback. It wastes Tim's time
adjudicating points that were never live, and it erodes trust in the objections that *are* real —
he can no longer tell which ones to take seriously.

**How to apply:** before stating a consequence, find the fact that makes it bite. Worked example —
"moving Friar Pluck off the mob line makes him immortal and removes his combat" was empty twice
over: his room is a `RoomInn`, which sets `allow_combat`/`allow_death` to False, and he never
wanders out of it. He was already unkillable. The check was ten lines into a file already open in
that conversation. Enumerating inheritance diffs is not analysis; tracing whether one changes
observable behaviour is.

**The recurring form: an inconsistency reported as a defect.** Finding that three call sites pass
different `getattr` defaults, or that two flags seem to cover one job, is *not* a finding. Before
saying anything, work out what the code would do if it were made uniform. Twice in one session the
odd one out turned out to be carrying the design: `combat_utils` defaults `is_alive` to False so a
player is never auto-attacked by the server on their own behalf, and `_dying` is the character-side
death latch, not dead weight beside the mob's `is_alive`. Both were stated as bugs, both had to be
retracted after Tim asked for a proper check. Being asked to verify and then reversing is worse than
saying nothing — it spends his attention and then tells him the spend was wasted.

Related: [[feedback_cheap_tests_over_theory]] (verify before asserting),
[[feedback_lead_with_the_no]] (when there *is* a real objection, it goes first),
[[feedback_reason_dont_just_gather]] (ask what result would change the recommendation).
