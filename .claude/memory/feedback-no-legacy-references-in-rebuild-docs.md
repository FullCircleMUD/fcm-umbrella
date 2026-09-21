---
name: feedback-no-legacy-references-in-rebuild-docs
description: "The rebuild's own documentation carries no comparison to src_old — no \"legacy did X\", no deviation notes, no relationship to it at all."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 491a24e1-2aaa-47a1-8002-8d79e40c4e55
  modified: 2026-09-20T14:22:34.390Z
---

Documentation written in `src/` (test plans, READMEs, docstrings, comments) says what the thing is.
It never says what `src_old/` did, how this differs, that a choice is a deviation, or what was
considered and rejected along the way.

**This is about documentation only, not conversation.** Discussing legacy while working is normal and
expected — reading it for reference, taking ideas from it, porting a chunk and reworking it. That is
how the work gets done. What must not happen is any of that process reaching the docs.

**Why:** documentation describes the artefact, not the journey to it. `src/` is a standalone build;
once a piece exists here the relationship to its source is over, and a doc carrying it forward is
describing something that is not this codebase.

**How to apply:** describe the component on its own terms, in its current form, full stop. No
archaeology, no process notes, no alternatives-considered. A design reason stands on its own merits —
"alignment is a score that moves with what a character does, so a race-level constraint has nothing
to enforce" — with no sentence about what it used to be. Same for "Named deviations" sections: don't
write one. Related: [[no-bulk-carry-over-from-src-old]], [[feedback-name-the-deviation-and-its-benefits]]
(that one is about not silently substituting a design in conversation, not about writing it into the
docs).
