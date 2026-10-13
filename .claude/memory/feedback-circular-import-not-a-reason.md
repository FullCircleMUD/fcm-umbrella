---
name: feedback-circular-import-not-a-reason
description: A circular import is never an argument against a design — the codebase resolves them with lazy imports routinely.
metadata:
  node_type: memory
  type: feedback
  originSessionId: e22219b7-f51d-408c-97ba-54252b909d4c
  modified: 2026-10-05T23:08:25.406Z
---

Never weigh a design option down because it would create a circular import. The codebase resolves
those with a deferred import inside the function (e.g. `PreferencesCharacterMixin.at_object_creation`,
`BankRoomMixin`), and has many times.

**Why:** 2026-10-05, I argued `fights_for` over an `isinstance` check partly on import-cycle risk; Tim:
"a circular import is not a reason to not do something."

**How to apply:** judge options on design merit. If one needs an import that would cycle, note "lazy
import" as the wiring in one line, not as a cost. Related: [[feedback-implementation-detail-is-not-a-design-issue]].
