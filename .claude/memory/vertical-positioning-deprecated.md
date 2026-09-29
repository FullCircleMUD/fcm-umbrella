---
name: vertical-positioning-deprecated
description: "Legacy vertical positioning (heights, depths, height-gated exits) is deprecated and absent from the rebuild — never a consideration"
metadata:
  node_type: memory
  type: project
  originSessionId: b32f101a-a951-409c-b6d3-05f6e39e8f0b
  modified: 2026-09-26T12:27:38.573Z
---

Vertical positioning is not implemented in the rebuild and won't be. Heights, depths, `ExitVerticalAware`, height-gated exits, `p_same_height` — all legacy-only.

**Why:** Tim, 2026-09-26, after I listed height filtering as a legacy-vs-rebuild difference.

**How to apply:** when comparing against `src_old/`, drop anything height-related silently; don't list it as a gap or ask about it. See [[no-bulk-carry-over-from-src-old]].
