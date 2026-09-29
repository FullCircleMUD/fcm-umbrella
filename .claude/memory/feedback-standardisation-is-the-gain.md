---
name: feedback-standardisation-is-the-gain
description: Moving a working call site onto the one standard implementation is worth doing for the standard alone; never weigh it only by player-visible change
metadata:
  node_type: memory
  type: feedback
  originSessionId: 329ea1b4-1469-4c2c-aa46-12816f64fcef
  modified: 2026-09-29T10:47:58.157Z
---

Converging hand-rolled code onto one standard implementation (a targeting parser, an Evennia helper)
is a gain in itself, even when the old code works and a player would notice nothing.

**Why:** the legacy game had every command hand-rolling its own parsing and searching. Bugs came from
the inconsistency, there was no single place to check how a thing was done, and a bug found in one
command meant auditing and refactoring 20–30 others. Standardisation is what removes that cost.

**How to apply:** when weighing a conversion, count the standard as the benefit — one implementation,
one place to look, one fix that reaches every caller. Don't recommend leaving a working site
hand-rolled on the grounds that "it works and a player wouldn't notice". For parsers and filters,
the standard is recorded in `design/parser-filter-inventory.md`.
Related: [[feedback-name-the-deviation-and-its-benefits]].
