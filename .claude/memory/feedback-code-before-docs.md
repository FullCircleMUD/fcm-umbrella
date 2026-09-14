---
name: feedback-code-before-docs
description: "Finish all code changes before the documentation pass; docs written mid-stream bake in \"not yet done\" and go stale immediately."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 56c3cd45-3227-4854-bc36-a2ce121d7e28
  modified: 2026-09-13T00:24:20.570Z
---

When a body of work has both code changes and documentation, do **all** the code first and the
documentation last, in one pass at the end.

**Why:** Claude documents the state in front of it. Docs written while code work is outstanding fill
up with "this is yet to be done" statements that are wrong as soon as the next commit lands, forcing
a second documentation pass. Telling Claude "we'll fix these after, so write it as if done" does not
work reliably — it documents what it sees.

**How to apply:** Sequence phases so every code item is closed before any doc is touched. When
proposing an order of work, put doc-only items last even when one of them clears a linter *error* and
the code items are only warnings. Applies to `docs/`, `CLAUDE.md`, `README.md` and progress entries
alike; in-code comments explaining a decision travel with the code change that needs them.

Related: [[feedback_docs_short_and_plain]], [[feedback_terse_written_records]].
