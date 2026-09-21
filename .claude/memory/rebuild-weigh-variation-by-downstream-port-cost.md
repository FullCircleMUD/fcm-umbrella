---
name: rebuild-weigh-variation-by-downstream-port-cost
description: A variation from the legacy shape is a trade-off — what it buys against how much harder it makes the later port of everything that depends on it.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cade497a-9bbb-44da-8a18-f318935326b3
  modified: 2026-09-16T17:02:18.844Z
---

The base assumption is that the legacy system works. Port it straight; vary only for a discussed and
agreed reason. A variation is weighed as a trade-off between two things:

- **What it buys** — better performance, more efficient or clearer code, a class of problem removed.
- **What it costs** — how much harder it makes the later port of the consumers that depend on this
  piece.

**Why:** the rebuild ports one chunk at a time, so a component always lands before its consumers. The
benefit is visible immediately and the cost is deferred — paid later, once per consumer, by whoever is
porting them. Naming both sides is what stops the deferred half going unweighed.

**How to apply:** a big enough benefit justifies a real downstream cost; a marginal one does not.
Cheapest case is a variation whose call sites keep working verbatim — consumer code ports as a straight
copy and any tidy-up is optional. `DamageType` becoming a `StrEnum` was that case: it removes the
hand-managed member↔string translation at every boundary, and the legacy `.value`,
`hasattr(x, "value")` and `isinstance(x, str)` patterns all still return the same results, so the
translation code becomes redundant rather than wrong. Phase the work: straight port first, "should we
tweak it" second, as a separate conversation per change.

Related: [[no-bulk-carry-over-from-src-old]], [[feedback-name-the-deviation-and-its-benefits]],
[[rebuild-not-retrofit]].
