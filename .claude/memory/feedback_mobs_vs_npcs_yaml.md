---
name: Mobs are spawn-script driven, not YAML entities
description: For evennia-world-builder YAML porting, NPCs go in npc_*.yaml files but mobs do NOT — they are spawned dynamically by scripts using mob_area tags on rooms.
type: feedback
originSessionId: 31a4e48c-5a55-4ada-b632-1d108e3c0214
---
When porting FCM world content to YAML via the evennia-world-builder library:

- **NPCs** (shopkeepers, trainers, guildmasters, librarian, named characters
  like Bron / Tindel / Mara) → go in their own `npc_*.yaml` files alongside
  the room they live in.
- **Mobs** (named bosses like The Magpie, plus regular hostile creatures like
  rooftops_footpads) → DO NOT go in YAML. They are spawned dynamically by
  spawn scripts, which read `mob_area` tags on rooms (e.g.
  `rooftops_boss`, `rooftops_footpads`, `city_watch_patrol`,
  `south_gate_guards`).

What the YAML's job is for mobs:
- Tag the rooms with the appropriate `mob_area` category. The spawn script
  uses that tag to pick spawn locations.
- That's it. No mob entity, no creature stats, no HP, no AI config in YAML.

**Why:** Mob populations are dynamic — they respawn, scale, and rotate
based on player activity, telemetry, and saturation rules. Pinning them
into world YAML would make them static fixtures that fight the spawn
system. Loot, keys (e.g. `magpie_stash` key for Magpie's chest), and
behaviour are all owned by the spawn / mob systems, not the world build.

**How to apply:** When porting a zone, treat anything in source that's
created by `spawn_*.py`, registered to `mob_area` tags, or that the source
documents as "spawned" → leave it out of YAML and just make sure the
relevant `mob_area` tag is on the room. NPCs (created via `create_object`
in the room build, with NPC typeclass) DO go in YAML.
