---
name: telemetry-spawn-parked-pending-xrpl
description: fcm-telemetry-spawn is scaffolded and parked until the fcm-xrpl extraction firms up
metadata: 
  node_type: memory
  type: project
  originSessionId: 59e09c63-3179-49d1-b4b3-3788d7782f28
  modified: 2026-08-31T14:38:25.692Z
---

`libraries/fcm-telemetry-spawn` is scaffolded (2026-08-31) and deliberately parked. Resume only after
`fcm-xrpl`'s extraction has a firmer shape.

**Why:** the telemetry and saturation services read the XRPL currency and NFT models directly, so this
library's input shape can't be settled first. A hard dependency on `fcm-xrpl` is a live possibility, to
be inspected then — not decided now.

**How to apply:** don't start the extraction unprompted. Scope, surface, table ownership and the XRPL
coupling are all open, listed under *Open decisions* in the library's `docs/test-plan.md`.

Stage-one intent: replicate `src/game/blockchain/xrpl/services/` (telemetry, saturation, item/resource
spawn — **not** mobs) closely enough to swap out. See [[library-unlicensed-fcm-telemetry-spawn]].
