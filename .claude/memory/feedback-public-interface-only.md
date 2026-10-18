---
name: feedback-public-interface-only
description: No code reaches inside another component — import only what its package exports
metadata:
  node_type: memory
  type: feedback
  originSessionId: 621a7def-9e23-4757-956b-a3266405c919
  modified: 2026-10-17T19:54:18.501Z
---

No component or other code imports from inside another component's modules; only what the package exports (`__init__` / `__all__`) is used.

**Why:** Tim, 2026-10-17, on search importing `p_actor_visible_to` from `components.perception.targeting`. The exported surface is the interface; anything else is internal.

**How to apply:** Need an unexported name → export it from the owning component (its scaffold case too), then import from the package. Related: [[event-driven-components]], [[feedback-trust-the-owning-component]].
