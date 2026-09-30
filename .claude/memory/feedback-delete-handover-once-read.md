---
name: feedback-delete-handover-once-read
description: A handover in ops/scratch is deleted as soon as it has been read back after compaction
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1501f45f-3477-4930-a432-9af4a1a14a76
  modified: 2026-09-29T13:43:28.360Z
---

Delete a handover file (e.g. `ops/scratch/<topic>-handover.md`) as soon as it has been read at the start of the continued session.

**Why:** stale handovers otherwise pile up in `ops/scratch/`.

**How to apply:** read it, then delete it in the same turn; carry what matters in the conversation.
