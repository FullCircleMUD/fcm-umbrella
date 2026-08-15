# Project Memory

## Security Rules
- **NEVER** run `git diff` on `secret_settings.local`/`secret_settings.py` or any git-crypt encrypted files before committing. This exposes plaintext secrets and defeats the purpose of denied read permissions. Just stage and commit without viewing the diff.
- [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md) — `src/game` encrypts `server/conf/secret_settings.local` via git-crypt (symmetric key, shared out-of-band). A **fresh clone is locked** — `git-crypt unlock <keyfile>` before the game runs locally. Also documented in `docs/` new-machine setup.

## Company Scope
- This company's job is **marketing**, not game development
- **No changes to any game repos without explicit board approval** (confirmed 2026-04-23)
- All agent work must be scoped to marketing workflows: content, social media, community, analytics, etc.

## Working Policies
- **Always ask about existing work first** — before assuming something needs to be created from scratch, ask whether there are existing artifacts, implementations, accounts, servers, etc. (confirmed 2026-04-23)

## Existing Assets
- **Discord server already exists** for FullCircleMUD — do not create a new one, assess what's already there

## Project Structure
- Work happens in the **FCM umbrella** (`/Users/timbaird/Documents/FCM-umbrella/`) — the dev workspace that gitignores the nested repos. Full repo manifest + layout live in `docs/new-machine-setup.md`; design docs live in the umbrella `docs/` (edit them there, not in the deprecated standalone `design` repo).
- `src/game` uses git-crypt — see [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md).
- `src/game` branches: `main` (default), `dev`, and the active working branch `shards-rework`.

## World content
- [NPC placement: fcm-world vs fcm-mobs](npc_placement_world_vs_mob_spawner.md) — killable NPCs need a spawn rule in `fcm-mobs` (respawn); only unkillable ones (no-combat rooms) go statically in `fcm-world`.
- [mob_area tag controls wandering](mob_area_tag_controls_wandering.md) — mobs only move into rooms sharing their `mob_area` tag; remove the tag to fence them out of a room.
- [fcm-world test-branch strategy](fcm_world_test_branch_strategy.md) — `main` is live content only; the test world lives on the `test` branch, kept current by merging main → test (never the reverse). Dev/staging point at it via `WORLDBUILDER_REF`; a CI guard on main makes it structural.

## Upcoming Work
- [Upcoming FCM world build in YAML](upcoming_fcm_world_build.md) — starting 2026-05-08, rebuilding FCM world content via the `evennia-world-builder` library; real-world content expected to surface edge cases the synthetic fixtures didn't reach

## Documentation
- **Document what IS, not what WAS** — see the always-on rule in [CLAUDE.md](../../CLAUDE.md). When something changes, record the current state only; no "used to be"/"migrated from"/"renamed from" framing unless a human agreed there's a direct need.
- [Design docs live in the umbrella docs/](design-docs-in-umbrella.md) — FCM system design lives in `FCM-umbrella/docs/` (kebab-case); edit design docs there, not the deprecated `design` repo. Libraries self-document in their own `docs/`.
- [Doc conventions live in doco-structure.md](doc-conventions-home.md) — record new doc conventions in `docs/doco-structure.md` (the spec); the `doc-convention-auditor` enforces them, the `doc-convention-linter` checks the mechanical subset.
- [Doc/library audit toolchain + consistency campaign](doc-audit-toolchain-and-campaign.md) — the spec→linter→auditor pairs (all read-only) and the in-flight code-vs-doc consistency sweep (shards + world-builder done; mob-spawner, yaml-reader, src/game next; targeting deferred).

## Do not use
- [No evennia-stateful-text library — use Evennia native](evennia-stateful-text.md) — Evennia provides stateful-text natively; don't propose, reference, or try to fetch an `evennia-stateful-text` repo.

## YAML porting conventions
- [Mobs are spawn-script driven, not YAML entities](feedback_mobs_vs_npcs_yaml.md) — NPCs go in `npc_*.yaml`; mobs (incl. named bosses) get only a `mob_area` room tag and are spawned dynamically

## Multi-shard dev setup
- [Shards view gamedirs — fix at symlink layer, not settings](feedback_shards_view_gamedirs.md) — Windows runs all roles from `src/game/`; Unix needs view gamedirs (`game-router/`, `game-shard1/`) with symlinks back to `../game/`. Solve path errors with symlinks, not settings edits.

## Working approach
- [Cheap tests beat confident theory](feedback_cheap_tests_over_theory.md) — verify before asserting; and when I haven't verified, ask ("does this make sense to you?") rather than declaring it broken — or fine.
- [Reason, don't reflexively gather](feedback_reason_dont_just_gather.md) — senior-dev role: before running a check, ask what result would change the recommendation. "Changes behaviour" ≠ "risky".
- [Targeted tests during dev, full suite at end of day](feedback_targeted_tests_during_dev.md) — the full `src/game` suite runs ~2 hours and holds the test DBs, blocking all other test runs. Name the specific suites while working.
- [Stop on each problem](feedback_stop_on_each_problem.md) — when auditing, surface one finding, stop, and let the user decide fix/leave/defer before editing or hunting the next one. Don't auto-fix or batch-enumerate.
- [No legacy-data concerns during shards work](feedback_no_legacy_data_concerns.md) — pre-alpha, fresh DB every deploy, live deploy replaces the current one wholesale. Don't weigh existing-database impact until a sharded deployment is live and working.
- [Terse confirmations](feedback_terse_confirmations.md) — answer yes/no or confirmation questions in 1-3 sentences, no re-derivation or hedging caveats.
- [A question is not an instruction](feedback_question_is_not_instruction.md) — answer questions in prose and stop; wait for an imperative before editing code.
- [No manufactured objections](feedback_no_manufactured_objections.md) — raise only concerns that bind in this codebase; check a consequence actually bites before stating it. Zero real objections means say so.
- [Lead with the no](feedback_lead_with_the_no.md) — when a proposal won't work, say so in the first sentence; never open with agreement, never raise caveats that don't change the decision.
- [No alarming phrasing](feedback_no_alarming_phrasing.md) — don't dramatize minor refinements/corrections ("that changes the design", "poor way to say it"); state the refined version plainly.
- [Don't overinvest in tangents](feedback_dont_overinvest_tangents.md) — don't chain multiple tool calls chasing precise answers to side questions unrelated to the actual task outcome.
- [Show code as links, not dumps](feedback_code_links_not_dumps.md) — when asked to see code, give a file link + line number; don't paste the code. Quote a line only when the exact wording is the point.
- [Commit approval includes push](feedback_commit_includes_push.md) — when a commit is approved, push it in the same step; don't stop for a second confirmation.
- [Ask in prose, not option dialogues](feedback_ask_in_prose_not_dialogues.md) — don't put decisions in a multiple-choice dialogue; there's no room for nuance. State the question in the reply and let the answer come back in Tim's own words.
