---
name: feedback-dont-overinvest-tangents
description: "Don't spend multiple tool calls chasing precise answers to side questions that don't affect the actual task outcome — give a best-effort answer from what's already found and move on."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ec5376b-e0bc-4b68-b21f-5b28b99246ed
  modified: 2026-08-08T01:30:42.752Z
---

When a question is tangential to the real work (e.g. "was this a recent Evennia change?" during a bug-fix session), don't chain multiple searches/API calls trying to pin down an exact, fully-confirmed answer. Give the best-effort answer from whatever's already been found, flag the uncertainty briefly if any, and move on.

**Why:** called out directly after a multi-step WebSearch → GitHub API commit search → tag comparison chain to pin down exactly which Evennia release included a one-line signature change, for a question that had zero bearing on the fix itself.

**How to apply:** one lookup is usually enough for a side question. If it's inconclusive, say so and give the closest available data point (a date, a nearby commit) rather than escalating to more tool calls. Save the multi-step research chains for things the task actually depends on. Related to [[feedback_terse_confirmations]] — same instinct, applied to tool-call effort instead of response length.
