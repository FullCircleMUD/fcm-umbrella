---
name: rebuild-not-retrofit
description: Libraries are not installed into the existing FCM game — the game is rebuilt once the libraries are ready.
metadata: 
  node_type: memory
  type: project
  originSessionId: 85ba999f-0ab5-4052-bbe7-51b5aa43e6c9
  modified: 2026-09-12T17:57:16.391Z
---

Libraries under `libraries/` are **not** retrofitted into the running FCM game. When the libraries are
up to speed, FCM's game code is **rebuilt**, and the rebuilt game is what consumes them.

**Why:** confirmed 2026-09-12, correcting docs in `evennia-llm-service` that had stage one "complete
when FCM can delete its LLM service code, install the library, and the game still works".

**How to apply:** `src/game/` is *source material* for a library, never a destination. A library stage
is complete when the library stands on its own — covered, documented, behaving — not when a running
game has adopted it. Don't write "installed into FCM", "stays in FCM", or "FCM can delete X and
install this"; say the consumer game, or the rebuilt game.

Related: [[shards-superseded-by-scaling]] — the rebuild targets `evennia-scaling`.
