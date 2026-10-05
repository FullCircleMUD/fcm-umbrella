---
name: base-actor-is-for-static-npcs
description: "BaseActor is for stationary, unkillable NPCs (guildmasters, shopkeepers in no-combat areas); anything that moves with players or fights goes on BaseCombatActor"
metadata:
  node_type: memory
  type: project
  originSessionId: a18aa240-91f7-4bba-b1b7-71678e69ed7f
  modified: 2026-10-03T20:40:13.932Z
---

`BaseActor` is for NPCs that stay put in areas that never change and cannot be killed — a guildmaster in a no-combat guild, shopkeepers. Players, pets, retainers and mobs sit on `BaseCombatActor`.

**Why:** Tim placed the follow mixin on `BaseCombatActor` for this reason (2026-10-03).

**How to apply:** a mechanic for actors that move with players or fight goes on `BaseCombatActor`, not `BaseActor`.
