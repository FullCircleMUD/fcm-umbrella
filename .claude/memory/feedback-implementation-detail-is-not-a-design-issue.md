---
name: feedback-implementation-detail-is-not-a-design-issue
description: "When Tim's described design is buildable, say so; an implementation detail that changes nothing for him gets one line, not a discussion"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 87975c6a-e3c2-47a8-adef-84e747015d9d
  modified: 2026-10-01T16:06:40.482Z
---

If the design Tim describes can be built as described, the answer is "yes, buildable" — and any wiring detail that doesn't change behaviour or need his decision gets at most one line, then move on.

**Why:** 2026-10-01, crafting tier selection via EvMenu. I turned "the menu's answer arrives in a callback" into several replies of options and code shapes; Tim had to ask whether there was any blocker at all. There wasn't. It cost him time and read as spinning wheels.

**How to apply:** before raising a technical point, ask whether it needs his decision or changes what the player sees. If neither, handle it in the build and mention it once. Related: [[feedback_no_manufactured_objections]], [[feedback_answer_the_concept_not_the_literal]], [[feedback_dont_overinvest_tangents]].
