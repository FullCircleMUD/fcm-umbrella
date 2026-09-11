---
name: feedback-log-levels-info-vs-warn
description: "INFO = game working as intended, recorded for lookup; WARN/ERROR only when something is actually or potentially wrong"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5d3d8e3e-8550-444d-90cf-195969271193
  modified: 2026-09-11T13:02:46.211Z
---

INFO is for the game working as intended — a line so a player's question can be looked up later. WARN and ERROR are reserved for something actually or potentially wrong with the game.

**Why:** logs are for diagnosing bugs; a WARN on expected behaviour buries the real ones. Settled during the evennia-equipment logging pass (2026-09-11): slot reconciliation and restore refusals are INFO (state changed underneath a working mechanism); an identity-less worn item at record time is WARN (the game's identifying system is broken).

**How to apply:** when adding a log line, ask "is the game broken or potentially broken here?" — no → INFO, yes → WARN/ERROR. See [[logging-migration-pass-pending]].
