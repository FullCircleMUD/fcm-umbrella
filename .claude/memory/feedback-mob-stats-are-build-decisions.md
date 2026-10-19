---
name: feedback-mob-stats-are-build-decisions
description: "A mob's race is a label; its stats, gear and conditions are chosen by the builder, never derived from the player race's chargen bonuses"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 66e431a4-180f-4afc-93fd-e9a26d5cd9cf
  modified: 2026-10-19T17:44:05.854Z
---

Race bonuses exist to give players a choice at character creation. A mob's stats, equipment and conditions are world-building decisions set directly; calling it an elf doesn't mean adding up elf bonuses or running `apply_race`.

**Why:** Tim, 2026-10-19 — I framed a raceless attribute write as "missing" the race's grants and framed copying them as drift. Wrong frame.

**How to apply:** configure mobs by setting the values wanted (spawn rule `attrs` or typeclass defaults); `race` is just set. Don't propose chargen machinery (`apply_race`, race-derived numbers) for mobs. Related: [[mobs-share-the-character-command-set]].
