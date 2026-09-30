---
name: feedback-config-never-asserted-in-tests
description: "Tests assert behaviour and mechanics, never a configured value or a list's contents"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1501f45f-3477-4930-a432-9af4a1a14a76
  modified: 2026-09-30T02:06:15.766Z
---

Configuration is never built into or asserted in tests — no case pins a constant's value or what a config list/table contains. Tests assert the mechanism against whatever the config holds: read `config.X` at run time, or patch it to a figure of the test's own.

**Why:** config gets tuned in playtesting; a test pinning it breaks on every tweak and tests nothing about the machine.

**How to apply:** when writing or touching a suite, express expectations relative to the config value (`cap + 25` stores above the cap, answers `cap`); retire any case whose only job is to pin a number. Related: [[feedback-no-tuned-values-in-prose]].
