---
name: feedback-use-library-tooling
description: "Check design/parser-filter-helper-inventory.md before writing any helper; use the standard one, and if none fits raise a common one — never hand-roll"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b32f101a-a951-409c-b6d3-05f6e39e8f0b
  modified: 2026-09-29T10:54:28.288Z
---

When a library already has the tool, use it. Room/inventory filtering is `walk_contents` with predicates (`p_not_exit`, `f_excluding(caller)`, a perception predicate); name matching is `match_named`. Exits come from `room.exits`, as targeting itself says.

**Why:** Tim, 2026-09-26, on `open`: I wrote `if obj is not caller` instead of `f_excluding(caller)`. "Write it with the tooling provided rather than reinventing your own."

Player-typed names against a list of names — recipes, skills, keywords — go through `parse_match`, so every command matches the same way. Deviate only for a specific, real reason (Tim, 2026-09-29: the player experience should be as common as possible across the game).

**How to apply:** before writing a parser, filter, matcher or any other helper, check `design/parser-filter-helper-inventory.md`. If nothing fits, raise a common helper with Tim rather than hand-rolling one; once built, it goes in the inventory. See [[feedback-standardisation-is-the-gain]].
