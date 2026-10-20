---
name: feedback-mob-stats-are-build-decisions
description: "A mob's race and class are assigned; stats, gear, conditions and levels are chosen by the builder, never derived from chargen bonuses or run through character progression"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 66e431a4-180f-4afc-93fd-e9a26d5cd9cf
  modified: 2026-10-19T19:30:47.393Z
---

Race bonuses exist to give players a choice at character creation. A mob's stats, equipment and conditions are world-building decisions set directly; calling it an elf doesn't mean adding up elf bonuses or running `apply_race`.

**Why:** Tim, 2026-10-19 — I framed a raceless attribute write as "missing" the race's grants and framed copying them as drift. Wrong frame.

The same holds for classes: a mob's class and level are assigned, never reached by running a character's progression (`take_class` plus a `spend_level` per level — a level-17 thief would be 17 calls). What a mob does need is the class's command set.

**How to apply:** configure mobs by setting the values wanted (spawn rule `attrs` or typeclass defaults); `race` and class levels are just set. Don't propose chargen or progression machinery (`apply_race`, `take_class`, `spend_level`) for mobs. Related: [[mobs-share-the-character-command-set]].
