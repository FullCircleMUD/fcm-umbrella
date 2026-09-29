---
name: feedback-consumers-dont-live-in-what-they-consume
description: "A command or feature that only consumes a component lives with its own concern, never inside the component it uses"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b32f101a-a951-409c-b6d3-05f6e39e8f0b
  modified: 2026-09-26T18:35:40.408Z
---

A component holds only what is about its own concern. Something that merely *uses* it — the `exits` command using messaging's `describe_contents_to` — lives with its own subject (e.g. `components/exit_types/…` or `commands/`), and the used component publishes what it needs.

**Why:** Tim, 2026-09-26: I put `CmdExits` in messaging to keep `describe_contents_to` unpublished. "It adds no value to messaging, it's not a messaging command." Also: I'd buried the placement choice in a long reply and took a side remark as agreement.

**How to apply:** placement of a new command/feature is its own one-line question with an explicit yes, not folded into a bigger reply. Publishing a function is the right cost; hiding it isn't a reason to misplace a consumer. See [[confirm-before-crossing-repos]], [[feedback_stop_on_each_problem]].
