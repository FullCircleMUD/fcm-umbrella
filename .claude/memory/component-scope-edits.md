---
name: component-scope-edits
description: "Working on a src/router component, edit anything inside it freely; anything outside it is left to last and discussed separately"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 87975c6a-e3c2-47a8-adef-84e747015d9d
  modified: 2026-10-01T14:19:47.457Z
---

When the work is on one component in `src/router/components/`, anything inside that component may be updated as the work needs. Anything outside it — another component, even in the same repo — is left to last and raised as its own discussion.

**Why:** stated 2026-10-01 during the crafting recipe-tier refactor (a field rename reached `telemetry_spawn`'s saturation service).

**How to apply:** list the outside reaches when scoping a change, do the in-component work, then raise the outside ones separately. The component-level version of [[confirm-before-crossing-repos]].
