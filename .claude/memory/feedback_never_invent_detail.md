---
name: feedback_never_invent_detail
description: "Never invent factual detail for colour — state only what was observed, and check a claim before repeating it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f3eca7d4-0ea6-4155-a517-e23818c873f8
  modified: 2026-09-11T18:09:19.640Z
---

Never invent factual detail. Not a timespan, not a count, not a frequency, not a severity — nothing
added to make a point land harder.

The case that prompted this. `ops/scratch/logging-conversion-process-2026-09-10.md` carried:

> The calendar's original mocked cases passed for months while no line ever landed

When checked, the first commit on `evennia-calendar` was three days old. "For months" was invented.
Nothing was measured, nothing was observed, and the library had not existed long enough for it to be
possible.

The facts on their own were the whole point: **tests mocked the shim, so they asserted a call was
made and never that a line reached disk.** That says everything the reader needs. "For months" adds
no information — it is dramatisation.

Repeating an invented detail from a note is the same offence as inventing it. A claim that carries a
number, a duration or a severity gets checked before it is restated, or it gets dropped.

**Why:** an invented detail is indistinguishable from a measured one once it is written down. It gets
quoted back as evidence, it shapes decisions, and the cost of finding out it was never real is far
higher than the nothing it added.

**How to apply:**
- State what was observed. If it was not observed, it does not go in.
- Drop intensifiers that carry no information — "for months", "repeatedly", "silently for ages",
  "dozens of".
- Before repeating a factual claim from a note, a doc or an earlier message, verify it. If it cannot
  be verified cheaply, drop the detail and keep the mechanism.
- If a point only lands with the embellishment, the point is weak — say the weak version.

Related: [[feedback_no_alarming_phrasing]], [[feedback_no_manufactured_objections]],
[[feedback_cheap_tests_over_theory]], [[feedback_terse_written_records]].
