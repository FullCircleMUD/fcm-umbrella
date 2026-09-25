---
name: design-repo-not-maintained-for-rebuild
description: "The design/ repo documents the legacy game and is not maintained for the rebuild. Read it as reference; never cite it as what the rebuilt game does, and never update it as rebuild work lands."
metadata: 
  node_type: memory
  type: project
  originSessionId: 94844aa8-37e3-42ff-b0c2-897acafa218a
  modified: 2026-09-23T17:37:16.119Z
---

The `design/` repo documents the **legacy** game. It is not maintained for the rebuild and is not
updated as rebuild work lands. Rebuild documentation is written **once**, after the game reaches a
stable state and the design concepts are settled — a single concise pass, not a running record.

**Why:** maintained progressively through the legacy build, it became an unwinnable fight against
bloat — archaeology of decisions, superseded detail, material serving neither a developer nor a
player. A running design doc through the rebuild would reproduce exactly that. Confirmed 2026-09-23.

**How to apply:**
- Never propose or perform an update to a `design/` doc because rebuild work changed something.
- Never cite a `design/` doc as describing what the rebuilt game does — it describes the legacy game.
  Read the code in `src/` for that.
- A `design/` doc contradicting `src/` is expected, not drift, and not a finding.
- Where the docs live and how the repo is laid out is still current: [[design-docs-live-in-the-design-repo]].
- The rebuild's own rules on what documentation may say: [[feedback-no-legacy-references-in-rebuild-docs]],
  [[feedback_docs_short_and_plain]].
