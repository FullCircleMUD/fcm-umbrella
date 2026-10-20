---
name: mob-xp-level-squared
description: "Current practice — a mob's kill XP is its level equivalent squared × 10; levelling pace is balanced on the XP-per-level table, not on mob XP"
metadata:
  node_type: memory
  type: project
  originSessionId: 66e431a4-180f-4afc-93fd-e9a26d5cd9cf
  modified: 2026-10-19T23:58:37.040Z
---

Current practice (2026-10-19, Tim calls it a test mechanism): a spawn rule sets `experience_points_value` to level² × 10 for the mob's level equivalent. Mob XP is not tuned per mob; how fast characters level is balanced by changing the XP each level needs.

**Why:** a fixed curve on the mob side keeps high-level kills worth thousands (a level-40 greater dragon pays 16,000), so the level table is the one place to rebalance.

**How to apply:** every new spawn rule gets `experience_points_value` from its level equivalent by the formula; raise pace problems against the experience level table, not mob values. Related: [[feedback-mob-stats-are-build-decisions]].
