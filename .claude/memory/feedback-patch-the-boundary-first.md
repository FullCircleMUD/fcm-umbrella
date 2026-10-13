---
name: feedback-patch-the-boundary-first
description: "When a test breaks because code outside the unit runs, say \"patch it at the boundary\" first — not a tour of why."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2476726b-6b4a-4e2e-91fb-281a5061310c
  modified: 2026-10-09T22:13:23.545Z
---

When a test fails because something outside the unit under test runs (a signal's receiver, another component's method), lead with the fix: patch the thing at the boundary — e.g. `mock.patch.object(module, "the_signal")` and assert on `.send`.

**Why:** Tim spent many turns (2026-09-26, the inn's `quit` tests vs death's new receiver) getting to "patch the signal" while I explained signals, fixtures and alternatives. He wanted "this call raises outside our control — let's patch it" up front.

**Isolate by default, not only when it breaks** (Tim, 2026-10-09, said repeatedly — do it unasked): a component's tests never send or receive real inter-component signal traffic. Call a receiver directly for its behaviour; prove the wiring by emptying the signal's `receivers` and freshly importing the package (mob_ai TK-09, OD-03), or narrowing `receivers` to the component's own. **Adding a `.send` to a component means patching it in that component's existing tests in the same change** — combat patches its outgoing signals module-wide via `setUpModule`. Never ask whether to.

**How to apply:** one line naming the outside call and the patch; explanation only if asked. Related: [[component-scope-not-the-sender]], [[feedback-no-cross-testing]].
