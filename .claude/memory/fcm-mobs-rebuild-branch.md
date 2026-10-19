---
name: fcm-mobs-rebuild-branch
description: "fcm-mobs rules are rebuilt on the `rebuild` branch from an empty scaffold; content/fcm-mobs-legacy is a local reference copy of the old rules"
metadata:
  node_type: memory
  type: project
  originSessionId: 66e431a4-180f-4afc-93fd-e9a26d5cd9cf
  modified: 2026-10-19T15:01:48.059Z
---

Since 2026-10-19, `content/fcm-mobs` spawn rules are rebuilt area by area on the `rebuild` branch, which started as the scaffold only (definitions, indexes, README). `content/fcm-mobs-legacy` is a plain local copy of the old rules (no `.git`, umbrella-ignored), reference only — same pattern as `fcm-world-legacy`.

**Why:** the spawner was rebuilt (calendar tick, `pack`, `condition`, unknown fields refused), and the old rules named legacy typeclasses and retired fields.

**How to apply:** new rules go on `rebuild`, written against `evennia-mob-spawner` main; a rule only `ms_load`s once its mob typeclass exists in `src/router`. Read the legacy copy for reference, never copy across. Related: [[fcm_world_test_branch_strategy]], [[npc_placement_world_vs_mob_spawner]].
