---
name: feedback-terse-confirmations
description: "User wants short, direct answers to yes/no or confirmation questions — no re-derivation, hedging, or lawyerly qualifying language."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9ec5376b-e0bc-4b68-b21f-5b28b99246ed
  modified: 2026-08-08T00:59:28.466Z
---

When the user asks a direct yes/no or confirmation question (e.g. "so X, correct?", "do you understand the intent?"), answer in 1-3 sentences. Don't re-explain the reasoning, don't add "one correction though..." caveats unless the correction is actually load-bearing, and don't pad with qualifying phrases.

**Why:** explicitly called out mid-conversation ("stop being a sea lawyer") after a run of 20+ line responses to simple confirmation questions, including corrective asides like "One correction on placement, though: mirror exactly where X does it — after Y, not before" tacked onto an otherwise-yes answer.

**How to apply:** reserve longer, structured responses (with code blocks, numbered options, file:line citations) for when the user asks for a draft, an explanation of something new, or explicitly wants detail. When they're just confirming a plan already established in the conversation, confirm it plainly. If a correction is genuinely necessary, lead with the yes/no, then state the correction in one short clause — don't bury the answer under the caveat.
