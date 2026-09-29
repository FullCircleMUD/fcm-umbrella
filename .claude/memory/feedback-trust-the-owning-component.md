---
name: feedback-trust-the-owning-component
description: "A component hands off to perception/messaging and trusts them — its tests check the call, never who is blind or deaf"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b32f101a-a951-409c-b6d3-05f6e39e8f0b
  modified: 2026-09-25T18:25:47.874Z
---

A component that sends a room line hands `tell_room` the room, the lines and the subject, and stops. Who perceives what is `components/perception` and `components/messaging`'s job; their suites cover it.

**Why:** Tim, 2026-09-25, on the doors auto-close cases — per-observer blind/deaf cases re-tested another component's rules through this one.

**How to apply:** test the handoff (patch `tell_room`, assert the call), not the outcome for each sense profile. Same boundary as [[component-scope-not-the-sender]] and [[event-driven-components]].
