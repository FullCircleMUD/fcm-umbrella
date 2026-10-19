---
name: feedback-library-docs-are-the-convention
description: "Read the owning library's docs before designing against it; never re-document a library's convention in a consumer."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3490b4dc-5abb-479a-b0a7-1fa9de845af4
  modified: 2026-10-19T12:22:24.169Z
---

Before designing world YAML (or anything) against a library, read that library's docs and follow what it already prescribes. Never copy its convention into a consumer's README or notes.

**Why:** I designed Millholm's cross-file doorways ("block owns both directions") without reading evennia-world-builder's `incoming_exits:` / `links:` convention, then offered to re-document the convention in fcm-world. Tim: re-documenting it in each consumer is how sessions end up needing reminding again.

**How to apply:** the library's docs are the single source; consult them first. Related: [[feedback-follow-evennia-conventions]].
