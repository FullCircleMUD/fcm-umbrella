---
name: feedback_docs_short_and_plain
description: "Documentation is short, plain and current-state only — no hedging, no alternatives considered, no history of what was tried."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4afd8299-0aa5-4091-8c8e-e5fd1dee1126
  modified: 2026-09-02T12:02:04.248Z
---

Write docs short and plain: what the thing is, how it works, how to use it. Nothing else. No hedging,
no options weighed and discarded, no record of what was tried first, no restating what it is *not*.

**Why:** a human should not need an LLM to interpret documentation an LLM wrote. Tim has raised this
across many sessions and it keeps reappearing — LLM verbosity is the default failure, not an occasional
slip.

**How to apply:** after drafting, cut to a third. Delete every sentence that says what the thing isn't,
what was tried, or what might change. If a paragraph can be a sentence, make it a sentence. Recorded in
`design/doco-structure.md`; see also [[feedback_terse_written_records]] and
[[feedback_no_hardening_language]].
