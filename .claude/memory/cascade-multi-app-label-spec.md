---
name: cascade-multi-app-label-spec
description: "AliasSpec grows multiple app labels (app_labels tuple) so fcm-xrpl's seed app can be pinned; agreed 2026-09-12, cascade work in its own session"
metadata: 
  node_type: memory
  type: project
  originSessionId: abdee214-f244-40df-90bc-44186d0e890c
  modified: 2026-09-12T20:49:09.748Z
---

Agreed 2026-09-12, current plan:

- `AliasSpec.app_label` becomes `app_labels` (tuple, any length); the cascade router pins **every** listed label to the alias — yes on the alias, `False` elsewhere. Rename sweeps the three existing consumers (archive, ai-memory, message-bus) + cascade tests/docs.
- Why: fcm-xrpl's consumer seed app (`xrpl_seed`, data migrations writing to fcm_xrpl tables) is invisible to the one-label router — all routers abstain on other DBs and Django's fallback runs seed migrations against default (crash on split deploys, double-seed on shared).
- `XRPL_SEED_APPS` setting disappears; the seed-app name is fixed as part of fcm-xrpl's contract (its settings helper already creates `xrpl_seed`).
- The cascade is library-facing: specs are authored by libraries, so labels fixed at library-authoring time is the design, not a loss.
- The fcm-xrpl standards conversion ([[xrpl-conversion-phases]]) waits on this cascade change.
- Idea noted, NOT part of the conversion: a game command that runs seed migrations live (data-only migrations can run while the game is up; SQLite file-lock caveat). [TBD — needs discussion: that whole feature.]
