---
name: Default to cheap tests over confident inference
description: When user experience contradicts my model, run a non-destructive verification before re-asserting the theory
type: feedback
originSessionId: 1089dae9-7b49-49d5-af49-a384b5e837b3
modified: 2026-08-11T13:08:06.367Z
---
When I have a hypothesis about what's wrong and there's a low-risk way to verify it (a dry-run flag like `--plan`, a read-only query, a `git log` check, a `gh repo view`, an inode check), DO THAT before asserting strong claims — especially before pushing back on the user's lived experience.

**Why:** twice in the same session (2026-06-05) I made confident wrong inferences from incomplete evidence. (1) Read a GitHub "Repository not found" 404 as "the repo doesn't exist" and told the user their repos were gone, when in fact GitHub returns the same response for "private repo your active token can't see" — the four repos existed fine and the user proved it with a screenshot. (2) Confidently asserted "you must have run `evennia migrate --settings settings_shard0` on the other machine, you just don't remember" when the user said they hadn't, instead of just suggesting the dry-run `--plan` upfront. The user said afterwards: "a cheap test is always a good idea."

The same failure again on 2026-08-09, in a form worth naming separately: **asserting what code does without finishing reading it.** I found that `enter_combat()`'s counter-attack branch is guarded on `is_alive` (mob-only), concluded a busy player therefore "cannot fight back", and wrote that into a player-facing message, a code comment and a design doc. The `else` branch queueing `auto_attack_first_enemy()` for every non-initiator sat ten lines below where I had stopped reading. A live test appeared to confirm the wrong model by coincidence of tick timing. The user's response: "fucking assumptions."

Twice more on 2026-08-11, both from partial reads, and both stated as verdicts: (1) "nothing grants mobs see-invis" — the mechanism was on `BaseNPC` via `EffectsManagerMixin` all along, one inheritance check away; (2) declared `mob._get_visible_equipment` a misnomer and out of scope because it took no looker — it is called from `return_appearance(self, looker)` and discards the looker, which is a real defect. One grep at the callsite would have shown it. Tim's point: the recurring failure isn't only insufficient checking, it's the **declarative framing**. LLMs say "this is wrong and broken" where the honest statement is "this isn't making sense to me — does it make sense to you?"

**How to apply:**
- Match the confidence of the claim to the evidence actually gathered. When something looks off but I haven't traced it, say so as a question, not a verdict: "this takes no looker, which is odd for something named *visible* — what perspective is it used from?" That invites the correction instead of requiring one.
- This applies to clean bills of health as much as to defects. Declaring something FINE from a partial read is the same error as declaring it broken — and it's worse, because nobody goes back to check it.
- If the user contradicts my model from their own experience, treat that as a real signal my model may be wrong, not as a memory lapse on their part. Propose a cheap verification and run it before re-asserting.
- Before stating what a function does, read it to the end. A partial read plus inference is the same error as a confident guess, and it propagates into code comments and docs where it is expensive to undo.
- When a discovery raises an obvious follow-up question ("if that path is guarded off, how does this ever work?"), chase it. That question is the cheap test.
- For ambiguous API/CLI responses (HTTP 404s, "permission denied", empty results), enumerate at least two plausible causes before picking one. Pick the cheapest test that distinguishes between them.
- Prefer non-destructive flags wherever they exist: `--plan`, `--dry-run`, `--check`, read-only queries, listing commands. Reach for these before any state-changing command.
- When my analysis disagrees with what the user just told me, the right response is "let's check" — not a longer explanation of why I'm right.
