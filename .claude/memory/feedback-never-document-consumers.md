---
name: feedback-never-document-consumers
description: A component or library documents its interface and what it depends on — never who consumes it
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9d4e2fae-1aeb-449d-b9d8-c5bedffd5adb
  modified: 2026-09-30T01:23:58.301Z
---

A component presents its interface; anyone may consume it without the component knowing or recording it. So no README, docstring, comment or test-plan note in a component names who calls it, composes it, or what a consumer does with it ("goes on SkilledActor", "what remort is for", "class SpellScrollNFTItem(...)").

What a component does declare is what **it** consumes: its `DEPENDS_ON`, and the signals, libraries and other components it reads.

**Stay in the lane.** While working on one component, touch and document only that component. Don't describe other components in its docs, and don't offer to clean up theirs — that is their own work, done when working on them.

**Why:** consumers change without the component changing; recording them couples the component to its users and goes stale.
**How to apply:** before writing any doc line, ask "is this about my interface or my dependencies?" — if it names a caller, cut it. Related: [[feedback-consumers-dont-live-in-what-they-consume]], [[feedback_docs_short_and_plain]].
