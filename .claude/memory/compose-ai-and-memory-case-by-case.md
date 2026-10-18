---
name: compose-ai-and-memory-case-by-case
description: "Current practice — AI (AIActorMixin) and encounter memory (EncounterMemoryActorMixin) are composed onto each typeclass as it needs them; no pre-combined mixin, no inheritance lines for \"AI mob with memory\"."
metadata:
  node_type: memory
  type: project
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T16:53:00.408Z
---

`AIActorMixin` and `EncounterMemoryActorMixin` are independent capabilities. Each typeclass composes whichever it needs — a base combat actor with AI and memory, a base actor that only converses, a skilled actor with memory — case by case. There is no combined "AI with memory" mixin and no inheritance chain encoding the combination. (Tim, 2026-10-17.)

**Why:** the combinations cut across BaseActor / BaseCombatActor / SkilledActor, so no clean inheritance line exists; a pre-combined mixin would only save one line per typeclass.

**How to apply:** when a mob needs memory, add `EncounterMemoryActorMixin` to its typeclass; `memory_id` lives there, not on `AIActorMixin`. Related: [[typeclass-location-principle]], [[base-actor-is-for-static-npcs]].
