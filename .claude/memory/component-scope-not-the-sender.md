---
name: component-scope-not-the-sender
description: "A component is complete when it processes its signal correctly; \"nothing sends it yet\" is not a caveat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a6b21d09-a348-4d4d-a385-0d485ff6a71c
  modified: 2026-09-22T18:54:10.937Z
---

Working on a component, its business is that an arriving signal gets processed correctly. Who sends
it is out of scope. Never qualify a finished component with "but nothing sends this yet" or "the loop
isn't closed end-to-end" — that is the decoupling working as designed, not an incompleteness.

**Why:** Tim has had to correct this in session after session. It reframes a complete piece of work
as partial, and drags the conversation to a scope he did not ask about.

**How to apply:** Report the component against its own contract. If a sender is genuinely the next
task, that is a separate item raised on its own, not a footnote on "is this done?".

Related: [[feedback-build-for-the-intended-game]], [[feedback-dont-second-guess-agreed-scope]],
[[confirm-before-crossing-repos]].
