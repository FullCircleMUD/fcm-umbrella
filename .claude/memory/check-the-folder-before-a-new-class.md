---
name: check-the-folder-before-a-new-class
description: "Before proposing a new typeclass, mixin or module, list the folder it would live in — what exists may already do it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-25T16:24:02.954Z
---

Before proposing a new class, `ls` the folder it would go in and read what is there. Never take a README's class table as the inventory.

**Why:** 2026-10-25 — proposed `ConversationalAILootableSkilledActor` for the gate guards, MRO checked and cases drafted, when `MemoryAILootableSkilledActor` already did exactly that and the townspeople used it. The `typeclasses/actors` README table did not list it. Tim asked why it wasn't identified earlier.

**How to apply:** the check comes before the proposal, not before the build. See [[always-ask-about-existing-work-first]].
