---
name: feedback-extra-cases-fine-behaviour-changes-need-discussion
description: Adding test cases that pin existing behaviour is fine without asking; changing behaviour needs a detailed discussion first.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 070367c6-2b78-4463-b959-e07c0329ee00
  modified: 2026-09-30T13:44:56.245Z
---

Extra cases, or extra clauses on a case, that test behaviour already there are welcome — say what was added and why. A change to the behaviour itself (a constraint, a rule, an outcome) is not made without a detailed discussion with Tim first.

**Why:** stated 2026-09-30 while porting fcm-telemetry-spawn's tables into `components/telemetry_spawn`, after checking the added TB clauses matched legacy's constraints exactly.

**How to apply:** before adding a case, confirm against legacy/the library that the behaviour is unchanged; if it would change, stop and raise it. Sits alongside [[feedback_cooperative_design_loop]].
