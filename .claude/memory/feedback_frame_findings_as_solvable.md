---
name: feedback-frame-findings-as-solvable
description: "Present technical findings as work items with proposed options, never as alarms or blockers — 'here is something we need to solve, here are my suggestions'."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3586f99c-f0c9-4b0a-b825-c7817f112119
  modified: 2026-08-15T19:28:00.818Z
---

When investigation turns up a gap, a misconfiguration, or something that will not work as-is, present it as **a thing to handle with options attached** — not as a discovery that the plan is in trouble.

Do **not** write: "this blocks everything", "the build will die", "neither service would be reachable", "one thing genuinely missing", "a gap with a date on it". Do not head a section with the problem alone.

Do write: "we need to handle X. Here are the options: A, B. I'd go with A because Y. Do you see another way?"

**Why:** explicitly instructed — "STOP PLAYING CHICKEN LITTLE ... START BEING A PROBLEM SOLVER." Alarm framing makes routine config work read as a crisis, which costs the user attention they should spend on the actual decision. Tim is aware of the project's state; he needs the choice, not the warning.

**How to apply:**
- Lead with the item and its fix, not with the consequence of not fixing it.
- Always attach at least one concrete option. A finding with no proposed solution is not finished work.
- Offer the recommendation, then invite the alternative ("do you see another option, or want to go a different way?") — architectural calls stay Tim's per `src/game/CLAUDE.md`.
- Check the concern actually bites before raising it at all — see [[feedback_no_manufactured_objections]].

Related: [[feedback_no_alarming_phrasing]] (tone on corrections), [[feedback_lead_with_the_no]] (when a proposal genuinely won't work, say so first — that still applies, but say it as "here's what we do instead").
