---
name: feedback_question_is_not_instruction
description: "A question is not an instruction — answer it and stop, don't start editing code"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 648ae4cd-3a40-432c-b50f-69caa28028ac
  modified: 2026-08-14T18:01:25.303Z
---

When Tim asks a question — "are these simple changes?", "would it be better to X?", "is scout
an existing command?" — **answer it and stop**. Do not begin editing code, even when the answer
makes the change look obvious and even when he seems likely to say yes.

He is still weighing the decision. Acting on it removes his chance to say "no, because…" and
means he is reviewing a diff instead of thinking.

**Why:** the whole value of the human-in-the-loop on this project is the context I cannot hold
(see the Development Approach section of `src/game/CLAUDE.md`). Pre-empting the decision spends
that value. It also creates work to undo.

**How to apply:** if the message ends in a question mark, the reply is prose. Wait for an
imperative — "do it", "go ahead", "make that change" — before touching a file. When the answer
implies an obvious edit, say what the edit would be and offer it; don't make it.

**The check-to-edit slide.** The most common way this goes wrong: I say "let me check what that
depends on", run the check, and continue straight into the edit in the same turn — so Tim never
gets told the result he was promised. Announcing a check is a commitment to report back and stop.
Run it, state what it found, wait. This applies during design discussion especially: exploring
options aloud is not agreement, and "agreed in principle" is mine to say, not a licence to act.

Related: [[feedback_lead_with_the_no]], [[feedback_ask_in_prose_not_dialogues]],
[[feedback_stop_on_each_problem]].
