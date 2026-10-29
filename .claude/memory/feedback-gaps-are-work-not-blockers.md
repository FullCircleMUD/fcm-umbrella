---
name: feedback-gaps-are-work-not-blockers
description: "When existing machinery doesn't support what a design needs, frame it as work to make it support it — not as \"it won't work because\"."
metadata:
  node_type: memory
  type: feedback
  originSessionId: d490f46b-233e-43ea-b29a-28fa1e662221
  modified: 2026-10-20T19:38:46.728Z
---

A mechanism gap in the way of a design is part of the work, not a reason the design fails. Say "this needs X so it works", never "X won't work because Y".

**Why:** Tim corrected me (2026-10-18) when I said a wand's `key` wouldn't survive a token restore — the answer is to make it survive.

Same for a missing piece the architecture expects to grow: a new strategy component, criterion, handler. Writing one is the normal step — never call it "the catch", a cost, or a constraint, and never steer toward bending an existing one to avoid it (2026-10-20, placeholder AI strategies).

**How to apply:** when checking a design against current code, list the gap as a requirement in the scope. Related: [[feedback-never-contradict-flippantly]].
