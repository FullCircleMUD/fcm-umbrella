---
name: npc_placement_world_vs_mob_spawner
description: "Which repo an NPC/mob goes in is decided by whether it can be killed — fcm-world for unkillable, fcm-mobs for anything that needs to respawn"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5000a25b-c39d-4f57-8a34-0180fc6bdd24
  modified: 2026-08-15T15:16:54.523Z
---

Explained 2026-08-15. An NPC belongs in one of two repos, and the deciding
question is **can it be killed?**

- **`fcm-world`** (`npc_*.yaml`, static placement) — only for NPCs that
  cannot die. In practice that means they stand in a room where combat is
  off, so nothing can ever remove them. There is no respawn mechanism
  here: once gone, gone. Rowan is the example — he is in The Harvest Moon,
  a `RoomInn` subclass, and `RoomInn` forces `allow_combat`, `allow_pvp`
  and `allow_death` to False.
- **`fcm-mobs`** (spawn rules, `rules:` with `rule_id`) — for anything
  killable, i.e. anything standing in a room that allows combat. The spawn
  rule's `respawn_seconds` is what brings it back, which is the entire
  reason it cannot live in `fcm-world`.

**How to apply:** before placing a new NPC, check the `allow_combat` of the
room it will stand in (`RoomBase` defaults to True; `RoomInn` and its
subclasses force False). Combat on → it needs a spawn rule in `fcm-mobs`,
not a `npc_*.yaml` in `fcm-world`. A killable NPC placed statically in
`fcm-world` is a defect: the first player to kill it removes it permanently.

The spawn rule's `area_tag` is what sets the mob's `mob_area` tag — do not
hardcode it in the typeclass. The matching tag goes on each room the mob may
wander into; see [[mob_area_tag_controls_wandering]].

Old spawn JSON under `src/game/world/spawns/*.json` is superseded — spawn
rules live in `fcm-mobs`.
