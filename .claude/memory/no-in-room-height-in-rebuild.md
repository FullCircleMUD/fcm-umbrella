---
name: no-in-room-height-in-rebuild
description: The rebuild has no height/depth within a room — legacy max_height/max_depth are not carried over
metadata:
  node_type: memory
  type: project
  originSessionId: daadc4c1-4f29-4bd6-a536-2ae44c0874aa
  modified: 2026-09-26T11:05:16.726Z
---

The rebuild currently has no concept of height or depth within a single room. Legacy `max_height` / `max_depth` room attributes (and anything keyed off them) are not ported.

**Why:** Tim, 2026-09-26, while surveying the legacy inn room.
**How to apply:** when surveying or porting any legacy room type, drop height/depth settings without raising them as a scoping item. See [[no-bulk-carry-over-from-src-old]].
