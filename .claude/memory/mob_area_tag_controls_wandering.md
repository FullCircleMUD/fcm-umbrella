---
name: mob_area_tag_controls_wandering
description: A mob only moves into rooms sharing its mob_area tag — removing the tag from a room fences mobs out of it entirely
metadata: 
  node_type: memory
  type: project
  originSessionId: 5000a25b-c39d-4f57-8a34-0180fc6bdd24
  modified: 2026-08-15T15:17:04.990Z
---

`AIHandler.get_area_exits()` (`src/game/typeclasses/actors/ai_handler.py`)
narrows a mob's usable exits to those whose destination room carries the
mob's own `mob_area` tag. A mob with no area tag is unrestricted.

Every movement decision routes through it — wander, flee, cornered checks,
wounded retreats — so the tag is a complete fence, not just a wander hint.
The spawn system also counts population by the same tag, so an untagged
room cannot be spawned into either.

**How to apply:**
- To let a mob roam a set of rooms, put the same `mob_area` tag on each of
  them and set `area_tag` on the spawn rule in `fcm-mobs`. The spawn rule
  sets the mob's tag — do not hardcode it in the typeclass.
- To keep mobs *out* of one room, remove its `mob_area` tag. This is how
  the Trapper's Hut keeps wolves out: it is `allow_combat: false`, so
  wolves that wandered in just stood there unable to attack.
- Watch for shared YAML tag anchors — several rooms often share one
  `&anchor`, so editing it changes all of them. Give the odd room out its
  own tag list and move the anchor to the next room that uses it.

Related: [[npc_placement_world_vs_mob_spawner]].
