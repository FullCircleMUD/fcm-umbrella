---
name: feedback-scope-in-the-components-own-terms
description: "When scoping or discussing one component, talk only in that component's terms — never pull its consumers (what will use it) into the scope, even to say they are untouched."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T16:24:05.670Z
---

While building a component, describe its scope only in its own terms: what it holds, what it offers, what it calls. Do not bring in the components that will consume it — not to change them, and not to say they are left alone.

**Why:** scoping `encounter_memory` (2026-10-17), I kept naming `converse` and `develop_strategy` ("converse keeps its direct call…"). Tim: "converse is not part of encounter memory … we're losing our separation of concerns." Mentioning consumers drags their design questions into the unit and the discussion sprawls; the consumers become much clearer once the component exists.

**How to apply:** the one exception is the agreed switch-over point — name only *that a caller changes to call the component*, in one line. Related: [[feedback-never-document-consumers]], [[feedback-consumers-dont-live-in-what-they-consume]], [[component-scope-edits]], [[feedback_dont_overinvest_tangents]].
