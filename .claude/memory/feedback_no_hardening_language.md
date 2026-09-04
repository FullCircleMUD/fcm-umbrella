---
name: feedback_no_hardening_language
description: "Never write decisions up as settled/locked in/immutable/final — record them as the current plan, always open to revision"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4afd8299-0aa5-4091-8c8e-e5fd1dee1126
  modified: 2026-09-01T18:39:47.030Z
---

It is the framing that matters, not the vocabulary. "The current working convention", "current
thinking", even "the current decision" are all fine. What is not fine is framing any of them as
*settled*, *locked in*, *firm*, *immutable* or *final*.

**Why:** Tim brainstorms laterally, and a note that hardened "this is probably the best way forward"
into "this is settled" gets quoted back at him by a later session as a reason not to explore. He then
spends half the conversation arguing an LLM out of a constraint that was never a constraint. The
hardening cuts off possibilities that were never closed.

**How to apply:** everything stays open to review and refactor if a better way emerges or a necessity
forces it. Applies to memory files, design docs and replies alike.

**Two kinds of thing are not ours to soften.** A constraint imposed from outside — how a third-party
API behaves, what a protocol permits, what a dependency will and will not do — is a fact about the
world rather than a decision, and gets recorded plainly as a hard external constraint. Regulatory and
compliance rules are deliberately absolute; see the umbrella `CLAUDE.md`.

The test is who holds the power: anything **we** can decide is open, always. Anything outside our
control is recorded as what it is.

Related: [[feedback_terse_written_records]], [[feedback_no_manufactured_objections]].
