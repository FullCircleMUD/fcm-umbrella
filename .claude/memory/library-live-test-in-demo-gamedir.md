---
name: library-live-test-in-demo-gamedir
description: "A library's live end-to-end verification happens in a demo gamedir once the library is complete, not in its unit suite"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6eb6c38a-f048-4ca6-902c-bb200ac5f366
  modified: 2026-09-15T22:29:27.991Z
---

Unit tests call a library's hooks and methods directly. Driving the real engine — puppeting a
character, running a server tick — waits for a demo environment stood up after the library is
finished, where it is exercised live.

**Why:** a unit suite that drives Evennia's session machinery is mostly testing Evennia, and the
fixtures cost more than they prove.

**How to apply:** in a library suite, compose the mixin onto a test typeclass and call the hook.
Don't build login, session or server-start fixtures to reach it. Related:
[[feedback_test_instance_credentials]], [[libraries-installed-editable-until-beta]].
