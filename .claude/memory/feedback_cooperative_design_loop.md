---
name: feedback_cooperative_design_loop
description: "Library/feature work runs as a human-in-the-loop cycle — discuss architecture, plan, write cases for one named unit, get approval, then write tests."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4564f16a-cfb5-4642-a69f-991804917e1f
  modified: 2026-09-08T15:29:51.998Z
---

The order is: discuss the architecture → plan it → write test cases **for a particular unit** → Tim
reviews and approves them → then write the tests. Never run the whole loop unattended.

**Why:** Tim's value is the thinking — understanding the problem, weighing options, choosing. Code
written ahead of that approval is autopilot output he then has to audit rather than direct. Bulk-
producing a full test plan across every surface skips his review of every one of them.

**How to apply:** scaffolding a repo means the structure, not the content — `docs/test-plan.md` gets
the fixtures table and at most the first surface's cases (per the bootstrap checklist in
`design/library-standards.md`), not a plan for ten surfaces. When a task's checklist item and the
conversation disagree about scope, the conversation wins; ask.

Related: [[feedback_stop_on_each_problem]], [[feedback_question_is_not_instruction]],
[[feedback_reason_dont_just_gather]].
