---
name: kit-classes-naming
description: "The rebuild's class system is \"kit_classes\"; KitClass is the enum and KitClassRecord the record — not character classes, not a Base suffix."
metadata: 
  node_type: memory
  type: project
  originSessionId: 06081ecf-7499-4f21-bb5f-cd9ce025673e
  modified: 2026-09-20T14:20:20.342Z
---

The rebuild's class component is `kit_classes`. Three names, and which gets the short one is
deliberate:

| Thing | Name |
|---|---|
| Enum of class keys | `KitClass` |
| The record (frozen dataclass, one per class) | `KitClassRecord` |
| The registry instance | `kit_classes` |

- **The enum gets the short name** because it is referenced constantly and the record rarely.
- **A kit class is not a character class.** Any actor able to learn can hold one, including
  intelligent NPCs and mobs. Most actors hold none — a rabbit is just a rabbit.
- **"kit"** keeps the game concept readable next to a Python class in an import line.
- **No `Base` suffix.** Nothing subclasses the record; each class is an instance of it.

**Why:** the names carry meaning that a shorter or more obvious choice would lose.

**How to apply:** say "kit class" in prose. Relates to [[rebuild-not-retrofit]].
