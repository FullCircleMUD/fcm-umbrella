---
name: feedback-defer-anything-that-could-block
description: "Current thinking — defer DB queries and other blocking calls off the reactor wherever viable, however small. Open to revision."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38ea812b-f540-4a39-a308-bc27292b05c6
  modified: 2026-10-05T14:34:22.123Z
---

The current thinking on best practice: anything that could block the reactor goes through `defer_to_db_thread` (from `evennia_database_cascade`) where that is viable, even a single cheap indexed query. Not a rule — where something else suits a case better, that is Tim's call, and the practice changes when things change.

**Why:** big jobs get broken up separately; what then limits how far one instance can be pushed is the sum of many small blockers at once. Invisible at low player counts, matters at scale.

**How to apply:** lean towards deferring rather than keeping a query in-line because it is small. Shopkeeper is a worked example (dispatch in `commands.py`, tests patch the helper to `defer.maybeDeferred`). Sits beside [[feedback-in-memory-first]], which doesn't fit data another instance can write — that is read fresh.
