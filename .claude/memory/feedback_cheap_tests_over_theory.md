---
name: Default to cheap tests over confident inference
description: When user experience contradicts my model, run a non-destructive verification before re-asserting the theory
type: feedback
originSessionId: 1089dae9-7b49-49d5-af49-a384b5e837b3
modified: 2026-08-10T02:34:36.477Z
---
When I have a hypothesis about what's wrong and there's a low-risk way to verify it (a dry-run flag like `--plan`, a read-only query, a `git log` check, a `gh repo view`, an inode check), DO THAT before asserting strong claims — especially before pushing back on the user's lived experience.

**Why:** twice in the same session (2026-06-05) I made confident wrong inferences from incomplete evidence. (1) Read a GitHub "Repository not found" 404 as "the repo doesn't exist" and told the user their repos were gone, when in fact GitHub returns the same response for "private repo your active token can't see" — the four repos existed fine and the user proved it with a screenshot. (2) Confidently asserted "you must have run `evennia migrate --settings settings_shard0` on the other machine, you just don't remember" when the user said they hadn't, instead of just suggesting the dry-run `--plan` upfront. The user said afterwards: "a cheap test is always a good idea."

The same failure again on 2026-08-09, in a form worth naming separately: **asserting what code does without finishing reading it.** I found that `enter_combat()`'s counter-attack branch is guarded on `is_alive` (mob-only), concluded a busy player therefore "cannot fight back", and wrote that into a player-facing message, a code comment and a design doc. The `else` branch queueing `auto_attack_first_enemy()` for every non-initiator sat ten lines below where I had stopped reading. A live test appeared to confirm the wrong model by coincidence of tick timing. The user's response: "fucking assumptions."

**How to apply:**
- If the user contradicts my model from their own experience, treat that as a real signal my model may be wrong, not as a memory lapse on their part. Propose a cheap verification and run it before re-asserting.
- Before stating what a function does, read it to the end. A partial read plus inference is the same error as a confident guess, and it propagates into code comments and docs where it is expensive to undo.
- When a discovery raises an obvious follow-up question ("if that path is guarded off, how does this ever work?"), chase it. That question is the cheap test.
- For ambiguous API/CLI responses (HTTP 404s, "permission denied", empty results), enumerate at least two plausible causes before picking one. Pick the cheapest test that distinguishes between them.
- Prefer non-destructive flags wherever they exist: `--plan`, `--dry-run`, `--check`, read-only queries, listing commands. Reach for these before any state-changing command.
- When my analysis disagrees with what the user just told me, the right response is "let's check" — not a longer explanation of why I'm right.
