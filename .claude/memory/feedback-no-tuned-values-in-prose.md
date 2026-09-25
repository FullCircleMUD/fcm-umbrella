---
name: feedback-no-tuned-values-in-prose
description: "Never restate a balance-tunable value in a docstring, comment or doc — say what the attribute means, not what it is set to"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 335d0645-d79b-40b1-95bc-8c1e52c2ff46
  modified: 2026-09-23T08:17:01.347Z
---

A docstring says what an attribute *is*. It never restates the value, or anything derived from it.

- Wrong: "Thirty real minutes of fuel — 180 ticks at ten seconds each."
- Right: "Capacity, in burn ticks. A tick is `BURN_TICK_SECONDS` of real time."

**Why:** a tuned number is tuned again. Every prose copy of it goes stale the moment someone
rebalances, and the declaration right below already states it. It also tells a developer nothing
they wanted — they came to find out what `max_fuel` does, not what this one class sets it to.

**How to apply:** durations, damage, weights, costs, capacities, DCs, level thresholds. Put the
value in the declaration and the meaning in the comment. Same rule in READMEs, test plans and tree
diagrams — `LanternNFTItem  burns, refuelled`, never `180 ticks, refuelled`. Where a test needs the
figures, a single table drives both the fixture and the assertion so there is one copy.

Raised 2026-09-23 on the lantern and torch docstrings. Related:
[[feedback_docs_short_and_plain]], [[feedback_terse_written_records]].
