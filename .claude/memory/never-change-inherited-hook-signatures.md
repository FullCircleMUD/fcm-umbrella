---
name: never-change-inherited-hook-signatures
description: Never alter the signature of a hook the library did not define — override it with the base signature verbatim
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6eb6c38a-f048-4ca6-902c-bb200ac5f366
  modified: 2026-09-15T22:03:04.900Z
---

A library overriding a hook defined by Evennia, the game, or another library keeps that hook's
signature exactly as the base declares it.

**Why:** the hook is a contract shared by every other consumer of it. Changing the signature breaks
any other library's mixin in the same MRO, and any game-side override, silently — the caller still
passes the old arguments.

**How to apply:** check the base class's real signature before writing an override. Anything the
library needs that the hook does not give it is derived inside the body, not added as a parameter.
Whether to call `super()` is a separate decision, made per hook — usually yes, not always.
Related: [[game-libraries-content-folder]], [[rebuild-not-retrofit]].
