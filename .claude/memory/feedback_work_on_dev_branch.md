---
name: feedback_work_on_dev_branch
description: src/game work happens on dev; main takes tested work by merge from dev
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed97c619-f494-4326-9ba3-080961ada760
  modified: 2026-08-23T23:53:27.797Z
---

`dev` is the working branch in `src/game` as a general rule. `main` receives tested work merged
up from `dev`.

**Why:** agreed 2026-08-23 after clearing the stale branches — one working branch beats a new
short-lived branch per task.

**How to apply:** default to `dev` for new work in `src/game`. Merge `dev` → `main` only once Tim
says the work is tested. Feature branches are still fine when a piece of work warrants isolation;
they come back to `dev`.

Related: [[gitcrypt_game_secrets]], [[feedback_commit_includes_push]].
