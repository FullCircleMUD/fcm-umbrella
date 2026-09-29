---
name: enemies-derived-from-targets
description: "Rebuild combat has no sides list; \"enemies\" is worked out from who targets whom, per spell, when needed"
metadata:
  node_type: memory
  type: project
  originSessionId: 9d4e2fae-1aeb-449d-b9d8-c5bedffd5adb
  modified: 2026-09-29T00:34:12.572Z
---

The rebuild's combat has no combat object holding sides. Each actor has one target (`ndb.combat_target`); switching with `kill` leaves the old target still attacking you.

Current thinking on "enemies", when something needs them: anyone targeting you, anyone you target, and, in a group, anyone targeting or targeted by a group member. Aggressive mobs may target any party member.

AoE secondaries come from the *target's* room, not the caster's (a ranged AoE lands through one exit).

**Why:** legacy `get_room_enemies` read `get_sides()` from a CombatHandler that the rebuild does not have.
**How to apply:** this belongs to individual spell mechanics, worked out when those spells are built — not to the spells machinery. Related: combat's `circle-combat-algorithm.md`.
