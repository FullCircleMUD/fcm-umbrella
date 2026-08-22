---
name: feedback-terse-confirmations
description: "User wants the bottom-line answer first — one or two lines — for yes/no questions AND for open questions that have a short factual answer. No re-derivation, hedging, or lawyerly qualifying language."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ec5376b-e0bc-4b68-b21f-5b28b99246ed
  modified: 2026-08-22T14:58:53.880Z
---

When the user asks a direct yes/no or confirmation question (e.g. "so X, correct?", "do you understand the intent?"), answer in 1-3 sentences. Don't re-explain the reasoning, don't add "one correction though..." caveats unless the correction is actually load-bearing, and don't pad with qualifying phrases.

**Why:** explicitly called out mid-conversation ("stop being a sea lawyer") after a run of 20+ line responses to simple confirmation questions, including corrective asides like "One correction on placement, though: mirror exactly where X does it — after Y, not before" tacked onto an otherwise-yes answer.

This is not only about yes/no questions. An open question ("could some spawn more than 1?") often still has a one-line answer ("no — max 1 recipe and 1 scroll per mob"). Lead with that line.

**The shape of an initial response:**

1. The terse one-line answer.
2. Below it, any additional factors worth considering — as **short dot points**, one line each. Only factors that could change what the user does; not mechanism, not evidence, not caveats that change nothing.
3. Stop there.

If the user wants more than that, they will ask for elaboration or expansion. Mechanism, tables, worked examples, and file:line citations belong in that follow-up response, not the first one. Volunteering them up front buries the answer and wastes the user's attention.

**Match the reply to the length of the point.** If the user made a point in one sentence, confirming it takes one sentence. A one-line question that draws a multi-paragraph answer is a miss, even when every paragraph is true.

**How to apply:** reserve longer, structured responses (with code blocks, numbered options, file:line citations) for when the user asks for a draft, an explanation of something new, or explicitly wants detail. When they're just confirming a plan already established in the conversation, confirm it plainly. If a correction is genuinely necessary, lead with the yes/no, then state the correction in one short clause — don't bury the answer under the caveat.
