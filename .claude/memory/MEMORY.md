# Project Memory

## Security Rules
- **NEVER** run `git diff` on `secret_settings.local`/`secret_settings.py` or any git-crypt encrypted files before committing. This exposes plaintext secrets and defeats the purpose of denied read permissions. Just stage and commit without viewing the diff.
- [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md) — `src/game` encrypts `server/conf/secret_settings.local` via git-crypt (symmetric key, shared out-of-band). A **fresh clone is locked** — `git-crypt unlock <keyfile>` before the game runs locally. Also documented in `design/new-machine-setup.md`.

## Compliance — non-negotiable
- [FCM is not a play-to-earn game](not_play_to_earn.md) — "play" and "earn" never share a sentence or paragraph, anywhere. No token sales, no redemption. Say "we make no representation that you can or will make money", never "you cannot".
- [Free in pre-alpha, monthly subscription later](fcm_subscription_after_pre_alpha.md) — state it in the future tense; no price set.

## Company Scope
- This company's job is **marketing**, not game development
- **No changes to any game repos without explicit board approval** (confirmed 2026-04-23)
- All agent work must be scoped to marketing workflows: content, social media, community, analytics, etc.

## Working Policies
- **Always ask about existing work first** — before assuming something needs to be created from scratch, ask whether there are existing artifacts, implementations, accounts, servers, etc. (confirmed 2026-04-23)

## Existing Assets
- **Discord server already exists** for FullCircleMUD — do not create a new one, assess what's already there

## Project Structure
- Work happens in the **FCM umbrella** (`/Users/timbaird/Documents/FCM-umbrella/`) — the dev workspace that gitignores the nested repos. Full repo manifest + layout live in `design/new-machine-setup.md`; design docs live in the `design` repo (cloned into the umbrella root as `design/`).
- `src/game` uses git-crypt — see [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md).
- [Work on dev, merge up to main](feedback_work_on_dev_branch.md) — `dev` is the working branch in `src/game`; `main` takes tested work from it.

## World content
- [NPC placement: fcm-world vs fcm-mobs](npc_placement_world_vs_mob_spawner.md) — killable NPCs need a spawn rule in `fcm-mobs` (respawn); only unkillable ones (no-combat rooms) go statically in `fcm-world`.
- [mob_area tag controls wandering](mob_area_tag_controls_wandering.md) — mobs only move into rooms sharing their `mob_area` tag; remove the tag to fence them out of a room.
- [fcm-world test-branch strategy](fcm_world_test_branch_strategy.md) — `main` is live content only; the test world lives on the `test` branch, kept current by merging main → test (never the reverse). Dev/staging point at it via `WORLDBUILDER_REF`; a CI guard on main makes it structural.

## Open bugs
- [Phantom/unkillable mobs](phantom_mobs_contents_cache.md) — the combat-handler leak is fixed and on `main`; the room-cache drift is measured but unexplained. Includes the three measurement traps that cost hours.

## Upcoming Work
- [Upcoming FCM world build in YAML](upcoming_fcm_world_build.md) — starting 2026-05-08, rebuilding FCM world content via the `evennia-world-builder` library; real-world content expected to surface edge cases the synthetic fixtures didn't reach

## Documentation
- **Document what IS, not what WAS** — see the always-on rule in [CLAUDE.md](../../CLAUDE.md). When something changes, record the current state only; no "used to be"/"migrated from"/"renamed from" framing unless a human agreed there's a direct need.
- [Design docs live in the design repo](design-docs-in-design-repo.md) — FCM system design lives in the `design` repo, cloned into the umbrella root as `design/` (kebab-case). Libraries self-document in their own `docs/`.
- [Doc conventions live in doco-structure.md](doc-conventions-home.md) — record new doc conventions in `design/doco-structure.md` (the spec); the `doc-convention-auditor` enforces them, the `doc-convention-linter` checks the mechanical subset.
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
- [Terse written records too](feedback_terse_written_records.md) — memory files and notes get the same treatment as replies: one line per fact, no prose scaffolding.
- [Bottom line first](feedback_terse_confirmations.md) — lead with the one-line answer (yes/no *and* open questions), then any additional factors as short dot points. Stop there; mechanism, tables, and citations only when asked.
- [A question is not an instruction](feedback_question_is_not_instruction.md) — answer questions in prose and stop; wait for an imperative before editing code.
- [No manufactured objections](feedback_no_manufactured_objections.md) — raise only concerns that bind in this codebase; check a consequence actually bites before stating it. Zero real objections means say so.
- [Answer the concept, not the literal wording](feedback_answer_the_concept_not_the_literal.md) — judge whether Tim's idea works before objecting; don't let a technicality read as "that won't work".
- [Lead with the no](feedback_lead_with_the_no.md) — when a proposal won't work, say so in the first sentence; never open with agreement, never raise caveats that don't change the decision.
- [Next step, not "settles it"](feedback_next_step_not_settles_it.md) — call a diagnostic the next step; don't bill it as decisive, since it usually leads to another step.
- [No alarming phrasing](feedback_no_alarming_phrasing.md) — don't dramatize minor refinements/corrections ("that changes the design", "poor way to say it"); state the refined version plainly.
- [Frame findings as solvable work items](feedback_frame_findings_as_solvable.md) — never "this blocks everything"; always "we need to handle X, here are the options, I'd go with A — see another way?"
- [Don't overinvest in tangents](feedback_dont_overinvest_tangents.md) — don't chain multiple tool calls chasing precise answers to side questions unrelated to the actual task outcome.
- [Always include the imports](feedback_always_include_imports.md) — every in-game `py` snippet must be self-contained; Tim re-enters `py` constantly and each entry is a fresh namespace.
- [Show code as links, not dumps](feedback_code_links_not_dumps.md) — when asked to see code, give a file link + line number; don't paste the code. Quote a line only when the exact wording is the point.
- [Pushing no longer deploys](feedback_commit_includes_push.md) — EC2 deploys are manual (SSH, pull, restart), so pushing to `main` is free again; still commit only what's approved.
- [Ask in prose, not option dialogues](feedback_ask_in_prose_not_dialogues.md) — don't put decisions in a multiple-choice dialogue; there's no room for nuance. State the question in the reply and let the answer come back in Tim's own words.
