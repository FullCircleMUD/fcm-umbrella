---
name: feedback_no_troubleshooting_relics
description: "Only the code that solved the problem ships — no spikes, debug logging or failed attempts left behind"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4afd8299-0aa5-4091-8c8e-e5fd1dee1126
  modified: 2026-09-01T23:51:24.749Z
---

When something is finally solved, the codebase gets **only the code that solved it**. Spike files,
debug logging, instrumentation and abandoned approaches are removed, not left in place.

**Why:** a relic from a failed attempt is indistinguishable from working code to whoever reads it next.
It looks load-bearing, nobody dares delete it, and it accumulates. Worse, when several half-approaches
sit side by side, a later failure can't be attributed — you can't tell which one caused it.

**How to apply:** revert to a clean tree between troubleshooting attempts rather than layering a second
spike on top of a first. When the answer is found, the committed diff should contain the working
solution and nothing else. What the failed attempts *taught* belongs in the commit message or a design
doc — the code itself goes.

Related: [[feedback_terse_written_records]].
