---
name: test-fixture-typeclass-names-unique
description: A typeclass defined in a test module needs a name unique across every suite; Tim is happy for fixtures to be changed as needed to make tests work
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-29T15:37:30.150Z
---

Name a test-module typeclass for its suite (`SelfSummaryWearable`, `AIOptionsPotion`), never a bare `Wearable` or `Potion`. Evennia registers every typeclass as a Django model under `objects`, so two suites defining the same class name cannot load in one run — `RuntimeError: Conflicting 'wearable' models`.

Tim is happy for test fixtures to be changed as needed to make tests work (2026-10-29) — no ask needed for a fixture rename or reshape. Commits still need his approval.

**Why:** two of mine collided with `commands.equipment.tests.Wearable` and stopped a multi-suite run before any test ran.

**How to apply:** when a run of several suites dies at import with a conflicting-model error, rename the fixture; and pick suite-specific names from the start. See [[feedback_targeted_tests_during_dev]].
