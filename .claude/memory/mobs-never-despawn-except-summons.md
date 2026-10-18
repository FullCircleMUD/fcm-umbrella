---
name: mobs-never-despawn-except-summons
description: "General mobs stay in the game until killed; only summoned creatures (familiar, raised skeleton, elemental) despawn, at the end of their summon's duration."
metadata:
  node_type: memory
  type: project
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T15:02:46.651Z
---

Current plan: a general mob is only ever removed by being killed. The only despawn is a summoned creature — a familiar, a raised skeleton, an elemental — whose summon has a duration and which despawns when it runs out. (Tim, 2026-10-17.)

**How to apply:** anything that must happen when a mob leaves the game (closing an open encounter, storing memory) can hang off the death announcement for general mobs; summons' timed despawn is the one other exit to cover. Related: [[enemies-derived-from-targets]].
