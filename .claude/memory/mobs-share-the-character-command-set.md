---
name: mobs-share-the-character-command-set
description: Current practice — mobs carry (very nearly) the same commands as characters; one combat and command system for every actor
metadata:
  node_type: memory
  type: feedback
  originSessionId: 071e0a5b-fd32-48ca-8856-a2955ffd0e7c
  modified: 2026-10-10T12:00:57.470Z
---

Every command that can viably be exposed to mobs is; mobs and characters go through one combat and command system, not two. A mob's AI issues the same commands a player types, waits the same turns, and passes the same gates. A mob given a class gets that class's commands, as a character would.

**Why:** Tim (2026-10-09): "there is not two separate systems" — anything a character can do in a fight, a mob should be able to do once its AI chooses to.

**How to apply:** a command given to all characters goes in `CharacterCmdSet` (it reaches all `DefaultCharacter` subclasses, so `BaseActor` and every mob). A command given by class or other group membership goes in that class's or group's command set. Don't propose a character-only home for a command a mob could use. See [[base-actor-is-for-static-npcs]].
