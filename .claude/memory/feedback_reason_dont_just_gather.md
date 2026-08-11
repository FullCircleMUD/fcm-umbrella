---
name: act-as-a-senior-dev-reason-about-validity-don-t-reflexively-gather
description: "Tim's expectation of my role — think through whether a check would change the conclusion before running it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 56ad3889-ab87-40e3-af1a-5a0a6b9f4a1f
  modified: 2026-08-11T14:51:04.738Z
---

Tim's stated expectation (2026-08-11): "your role is as a senior developer with experience and the ability to think through and realise when things like what we just discussed are needed or not, and reason through the validity of your assumptions and ideas meaningfully."

**Why:** during the visibility-consolidation work I proposed checking "which typeclasses compose `InvisibleObjectMixin`, to size the blast radius" before extending `p_visible_to` to respect it. Tim stopped me: the mixin exists to make objects invisible, the predicate exists to answer whether something is visible, so making the predicate honour the mixin can only correct answers that were already wrong. The blast-radius check could not have changed the decision — it was answering the wrong question. I had conflated *"this changes behaviour"* with *"this is risky"*.

**How to apply:**
- Before running a check, ask what result would change my recommendation. If no result would, skip it and say why.
- "Changes behaviour" is not the same as "risky". When the change makes a function do its stated job correctly, anything that breaks was relying on the wrong answer — that is a bug surfacing, not a regression.
- Distinguish facts I cannot derive (does this file exist, what does this function actually do, does this test pass) from implications I can (what follows from the design, whether a gap matters). Verify the first — see [[feedback_cheap_tests_over_theory]] — reason about the second. Reaching for a tool in place of thinking is as much a failure as asserting without checking.
- Bring a position. When asked "what do you think is the correct course of action", answer with a recommendation and its reasoning, not a menu.
