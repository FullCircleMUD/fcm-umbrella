---
name: directions-are-strings-not-an-enum
description: components/directions holds directions as plain strings; a Direction enum was considered and declined
metadata: 
  node_type: memory
  type: project
  originSessionId: 77c60e22-fecc-4304-9a08-4142e2110df3
  modified: 2026-09-25T02:30:24.167Z
---

`components/directions` holds the ten directions as plain strings. A `Direction` enum was weighed
against [[enums-are-plain-enums]] on 2026-09-24 and declined.

**Why:** a direction is the word the player types — it arrives as a string from YAML and from input,
registers as an Evennia alias, and prints as display text. A member would be `.value`'d at every
boundary and held nowhere. `Position` and `DamageType` earn enums because code compares those in
logic; nothing compares a direction. `resolve()` is the single string→canonical gate and an enum
would be a second way in that skips it.

**How to apply:** don't re-propose the enum. If it is ever revisited, the refactor is cheap and not
urgent — no stored-data migration (pre-alpha, fresh DB), and YAML stays `direction: north` either
way, so only the call sites in `src/router` change.
