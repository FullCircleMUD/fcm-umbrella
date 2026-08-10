---
name: fcm_world_test_branch_strategy
description: "fcm-world keeps test content on a `test` branch; main is live game content only, guarded by CI"
metadata: 
  node_type: memory
  type: project
  originSessionId: 056f5d90-423a-4e31-9679-c99a1d4c1d36
  modified: 2026-08-10T14:45:49.649Z
---

Agreed 2026-08-10. `fcm-world` uses a two-branch split:

- **`main`** — live game content only. Never contains test content.
- **`test`** — everything on main, plus `shard0/test-world/`. Kept current by merging
  **main → test only**; never merge test → main.

Local dev and (later) staging point at the test branch via `WORLDBUILDER_REF=test`;
production stays on `main`. Both `WORLDBUILDER_REPO` and `WORLDBUILDER_REF` are env vars read in
`src/game/server/conf/settings.py`, so this is a settings change, not a code change. `ref` accepts a
branch, tag, or commit SHA. There is no per-invocation override — `wb_build` resolves the reader from
settings, so changing branch needs a restart.

**Why:** the test world can then never reach production by accident, while still tracking the live
world as it evolves. The test content lives in its own directory tree, so main → test merges only
conflict on the one line each adds to `shard0/index.yaml`.

**How to apply:** a CI workflow on main fails if `shard0/test-world/` exists. It is **advisory, not
blocking** — required status checks need branch protection or rulesets, and both are gated behind
GitHub Pro for private repos. That is accepted for now: the real control is that Claude commits and
pushes nothing without Tim's approval, and merges nothing without explicit approval. Revisit the Pro
plan if anyone else starts working on the repo.

**fcm-world stays private permanently** — it is the full map of what is where in the game, so public
visibility would let players cheat. Making it public is not an option for unlocking branch
protection, or for anything else.

Because the approval gate covers intent rather than placement, state the target branch and the exact
staged paths before every commit in this repo — an approved commit can still land on the wrong
branch. Untracked files follow across branch switches, so a `git add -A` on main while
`shard0/test-world/` is untracked would commit the whole test world there.

The world-builder `wb-validate` step is intended to join that workflow once the library ships to
PyPI; until then `wb_build` pre-validates the whole repo at build time
(`repo-ci-pre-validation: false`).

Cross-branch references (e.g. the test hub's exits into millholm's Harvest Moon) are authored
entirely in test-branch files, including the return leg — a top-level exit entity with a `location:`
cross-ref into the main-branch room. That keeps main free of test-only lines. The cost: rebuilding
that millholm file alone cascade-deletes both exits until the hub file is rebuilt, because the
library's fix (`incoming_exits:`) would require editing a main-branch file.
