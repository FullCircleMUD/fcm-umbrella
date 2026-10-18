---
name: interface-base-for-swappable-subsystems
description: "Current practice for new subsystems that could be reimplemented (AI engines, encounter memory) — declare an interface base class first, implementation behind it; not applied retroactively."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T15:29:34.570Z
---

For a new subsystem whose implementation could change — a different technology, a different store (a local DB today, DynamoDB tomorrow) — declare an interface base class first (methods raising `NotImplementedError`, not an ABC), and put the implementation behind it as a subclass. Even with only one implementation, it keeps the black box swappable. Done for `AIEngine`; being done for `encounter_memory`.

**Why:** Tim, 2026-10-17: "it may be that we only ever have the one implementation, but … we've got the flexibility to build different memory systems by just extending the one interface base." He wishes it had been done throughout but does not want existing components reworked for it.

**Each implementation gets its own test plan and tests** — beside it, not in the component's plan — so one can be worked on and tested in isolation from the others. The component's plan covers the interface and what is shared. Applies to every encounter memory implementation and every AI engine (Tim, 2026-10-17).

**How to apply:** raise it when scoping a new subsystem of that kind; never propose retrofitting existing components unless asked. Related: [[feedback-simplest-way-no-redundant-knobs]], [[event-driven-components]].
