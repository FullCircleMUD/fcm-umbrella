---
name: no-bulk-carry-over-from-src-old
description: "Never bulk-copy, bulk-port or bulk-rewrite anything from src_old/ into src/ — every element of the rebuild is re-decided one at a time."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec8709eb-feba-4e03-9ef4-988743d934bf
  modified: 2026-09-14T19:43:34.882Z
---

Never run a bulk operation that moves anything from `src_old/` to `src/`. No `cp -r`, no `sed` across
files, no "port this module across", no find-and-replace sweep over the docs. Applies to code,
settings, content, tests and documentation references alike.

**Why:** the rebuild exists so every element gets re-evaluated on its merits. A bulk operation carries
the old design across without anyone looking at it, and brings the reasons it was wrong with it.

**How to apply:** one thing at a time, with a stated reason for keeping it. `src_old/` is reference
material to read and learn from, never a source to copy from. See [[rebuild-not-retrofit]] and the
always-on rule in [CLAUDE.md](../../CLAUDE.md).
