---
name: event-driven-components
description: "FCM's own components talk to each other by signal wherever practical, including request-shaped signals, so no component imports another to make something happen."
metadata: 
  node_type: memory
  type: project
  originSessionId: 06081ecf-7499-4f21-bb5f-cd9ce025673e
  modified: 2026-09-20T23:52:11.838Z
---

The FCM layer — `components/` and the game's typeclasses, not Evennia's core — is built to be as
event-driven as practical. One component never imports another to make something happen.

- Signals are declared in `components/signals`, a leaf that imports nothing, so both sender and
  receiver import *down* into it and neither imports the other.
- **Request-shaped signals are accepted**, not only notifications. `languages_granted(actor,
  languages)` means "add these", sent by anything that grants a language. The alternative is the
  granting component exposing a function that every sender imports, which is the dependency being
  avoided.
- A signal carries **no data a receiver could derive from what it already has**. Two copies of a
  grant is how one gets applied twice.
- A shared signal beats one per source. `languages` has a single receiver however many systems
  grant languages.

**Why:** complete decoupling. A component can be rewritten or replaced without any other component
changing, because nothing holds a reference to it.

**How to apply:** when one component's work has to land in another's state, reach for a signal before
an import or a shared attribute. Expect refactoring toward this in components built before the
direction was set. Relates to [[kit-classes-naming]].
