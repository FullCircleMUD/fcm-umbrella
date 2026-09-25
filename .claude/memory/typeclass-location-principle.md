---
name: typeclass-location-principle
description: "Typeclasses live in typeclasses/ — a principle to try for, with a permitted exception when a component instantiates its own objects"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2476726b-6b4a-4e2e-91fb-281a5061310c
  modified: 2026-09-24T15:21:14.782Z
---

Typeclasses instantiated into the game live in the `typeclasses/` folder. Try for this.

**This is a principle, not a canonical rule.** Where applying it is untenable, going around it is
permitted. Do not quote it back at Tim as the reason something cannot be done.

**The named exception:** a typeclass instantiated into the game may live in a component, when that
component needs to instantiate its own objects into the game. The component then imports the game's
`Object` base, which the exception carries with it.

**Why:** a person looking for what a thing *is* should find it beside every other instantiable thing.
But a component that creates its own objects cannot name a class it is not allowed to import, and
every way around that — a registry, a settings path, passing the class in on a signal — costs more
than the exception does.

**How to apply:** default to `typeclasses/`. When a component creates the object itself, the class
goes in the component. `components/death` holding `Corpse` is the standing example.

Related: [[event-driven-components]], [[confirm-before-crossing-repos]].
