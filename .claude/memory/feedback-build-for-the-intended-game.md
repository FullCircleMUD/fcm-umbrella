---
name: feedback-build-for-the-intended-game
description: "Design against the finished game, not the half-built state of the rebuild"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 83a659ae-32e1-4229-8e13-0cd424cda811
  modified: 2026-09-18T20:52:24.294Z
---

Build each piece for the game as it will be once the rebuild is done, not for what exists in
`src/router` today. A thing that is inert right now because its consumer has not been built yet
still goes in.

**Why:** the rebuild is assembled a component at a time, so almost every piece arrives before the
system that uses it. Judging each one against the current half-built state would strip out exactly
the parts that make the next piece possible — and they then have to be rediscovered and re-added.
`levels_to_spend` is the worked example: meaningless until character classes exist, and impossible
to build classes without.

**How to apply:** don't flag state as questionable merely because nothing reads it yet. Ask what the
finished system needs. Raise it only if it is wrong *for the target design*, not if it is
unreferenced today. Relates to [[rebuild-not-retrofit]] and
[[rebuild-weigh-variation-by-downstream-port-cost]].
