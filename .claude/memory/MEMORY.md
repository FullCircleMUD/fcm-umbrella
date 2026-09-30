# Project Memory

## Security Rules
- **NEVER** run `git diff` on `secret_settings.local`/`secret_settings.py` or any git-crypt encrypted file before committing — it exposes plaintext secrets. Stage and commit without viewing the diff.
- [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md) — `secret_settings.local` is git-crypt encrypted; a fresh clone is locked until `git-crypt unlock <keyfile>`.

## Compliance — non-negotiable
- [FCM is not a play-to-earn game](not_play_to_earn.md) — "play" and "earn" never share a sentence or paragraph. No token sales, no redemption. Say "we make no representation that you can or will make money", never "you cannot".
- [Free in pre-alpha, monthly subscription later](fcm_subscription_after_pre_alpha.md) — future tense; no price set.

## Working Policies
- **Always ask about existing work first** — before creating from scratch, ask whether artifacts, implementations, accounts or servers already exist (confirmed 2026-04-23)

## Existing Assets
- **Discord server already exists** for FullCircleMUD — do not create a new one

## Project Structure
- Work happens in the **FCM umbrella** (`/Users/timbaird/Documents/FCM-umbrella/`), which gitignores the nested repos. Repo manifest + layout: `design/new-machine-setup.md`.
- [Libraries commit straight to main](libraries_commit_straight_to_main.md) — no branches in `libraries/` repos until production.
- [Work on dev, merge up to main](feedback_work_on_dev_branch.md) — `dev` is the working branch in `src/game`.

## World content
- [NPC placement: fcm-world vs fcm-mobs](npc_placement_world_vs_mob_spawner.md) — killable NPCs need a spawn rule in `fcm-mobs`; only unkillable ones go statically in `fcm-world`.
- [mob_area tag controls wandering](mob_area_tag_controls_wandering.md) — mobs only enter rooms sharing their `mob_area` tag.
- [fcm-world test-branch strategy](fcm_world_test_branch_strategy.md) — `main` is live content; test world on `test`, merged main → test only; `WORLDBUILDER_REF` points at it.

## Archive & recovery
- [Archive exists for playtest continuity](archive_enables_playtest_continuity.md) — `evennia.db3` disposable; `archive.db3`, `xrpl.db3`, `subscriptions.db3` permanent from alpha. Never wipe evennia+archive while keeping xrpl.

## Upcoming Work
- [Log levels: INFO vs WARN](feedback_log_levels_info_vs_warn.md) — INFO = working as intended; WARN/ERROR only when something is or may be wrong.
- [logging-extension loses settings-window writes in twistd children](logging-extension-settings-window-loss.md) — raise with the extension, not a consumer bug.
- [fcm-telemetry-spawn parked pending fcm-xrpl](telemetry-spawn-parked-pending-xrpl.md) — waits on the XRPL library's shape.
- [fcm-telemetry-spawn is unlicensed](library-unlicensed-fcm-telemetry-spawn.md) — sanctioned; the 3 licence findings are expected.
- [evennia-targeting does not log](library-no-logging-evennia-targeting.md) — accepted; `log_shim_unused` is expected.

## Documentation
- **Document what IS, not what WAS** — see [CLAUDE.md](../../CLAUDE.md). No "used to be"/"migrated from"/"renamed from".
- [No legacy references in rebuild docs](feedback-no-legacy-references-in-rebuild-docs.md) — `src/` docs never compare themselves to `src_old/`.
- [Docs short and plain](feedback_docs_short_and_plain.md) — what it is, how it works, how to use it; no hedging or archaeology. Cut drafts to a third.
- [No tuned values in prose](feedback-no-tuned-values-in-prose.md) — say what an attribute means, never what it is set to.
- [Code before docs](feedback-code-before-docs.md) — finish the code before the documentation pass.
- [Config is never asserted in tests](feedback-config-never-asserted-in-tests.md) — tests pin mechanics; read or patch the config value.
- [Component plan docs are deleted](component-plan-docs-are-deleted.md) — a finished component keeps README, test-plan, tests and `__init__` only.


## Code conventions
- [Enums are plain Enum](enums-are-plain-enums.md) — cross into strings with `.value`; no `str, Enum` or `IntEnum`.
- [Leading amount only](leading-amount-only.md) — `50 gold`, never `gold 50`; the game-wide command grammar, parsed by targeting's `parse_quantity`.
- [Directions are strings, not an enum](directions-are-strings-not-an-enum.md) — a direction is the word the player types.
- [Typeclasses live in typeclasses/ — a principle, not a rule](typeclass-location-principle.md) — a component that instantiates its own objects holds those classes.
- [Components talk by signal](event-driven-components.md) — a component prefer not to import another to make something happen.
- [Properties are written by assignment](property-writes-by-assignment.md) — never in-place mutation; `at_set` only runs on assignment.
- [In-memory first](feedback-in-memory-first.md) — lazy-load from the DB once, serve from memory; writes update both.
- [Decimal for fractional values](decimal-for-fractional-values.md) — no floats in game code; convert library/Evennia floats at the edge.

## Do not use
- [No evennia-stateful-text library — use Evennia native](evennia-stateful-text.md) — don't propose, reference or fetch it.

## YAML porting conventions
- [Mobs are spawn-script driven, not YAML entities](feedback_mobs_vs_npcs_yaml.md) — NPCs in `npc_*.yaml`; mobs get only a `mob_area` room tag.

## Libraries and the rebuild
- [Vertical positioning is deprecated](vertical-positioning-deprecated.md) — no heights in the rebuild; drop anything height-related from legacy comparisons.
- [Live test in a demo gamedir, not the unit suite](library-live-test-in-demo-gamedir.md) — real puppet/unpuppet and ticks wait for a demo environment.
- [Editable installs until beta](libraries-installed-editable-until-beta.md) — clone and editable-install; publishing waits for production.
- [Library-declared content lives in the game's libraries folder](game-libraries-content-folder.md) — `src/router/libraries/<library-name>/`.
- [Build for the intended game, not today's state](feedback-build-for-the-intended-game.md) — inert until its consumer exists still goes in.
- [Rebuild, not retrofit](rebuild-not-retrofit.md) — libraries never go into the running game; the rebuilt game is the consumer.
- [Never change an inherited hook's signature](never-change-inherited-hook-signatures.md) — override with the base signature verbatim.
- ["Legacy production", not "production"](feedback-legacy-production-not-production.md) — always qualify `src_old/`.
- [Never bulk-carry anything from src_old to src](no-bulk-carry-over-from-src-old.md) — every element re-decided one at a time.
- [No in-room height in the rebuild](no-in-room-height-in-rebuild.md) — legacy `max_height`/`max_depth` are not ported.
- [Weigh a variation against downstream port cost](rebuild-weigh-variation-by-downstream-port-cost.md) — port legacy straight; vary only by agreement.
- [Follow Evennia's conventions](feedback-follow-evennia-conventions.md) — check the framework standard before naming; hooks are `at_`, never `on_`.
- [effects-conditions on_ hooks pending rename](effects-conditions-on-hooks-pending-rename.md) — kept `on_` for now; rename to `at_` later.

## Instance-to-instance messaging
- [Shards superseded by scaling](shards-superseded-by-scaling.md) — the rebuild targets `evennia-scaling`; don't design for shards.
- [Shards v2 — independent instances, not shared Postgres](shards-v2-independent-instances.md) — archive+xrpl move the character, the bus coordinates.
- [evennia-message-bus library](evennia-message-bus-library.md) — round trip proven between demo instances; no consumer yet.
- [Enemies are derived from targets](enemies-derived-from-targets.md) — no sides list in rebuild combat; AoE enemy logic is per-spell, later.
- [Groups are per-server](groups-are-per-server.md) — members always on one server; no off-server `None` guard.
- [Shard first boot runs in isolation](scaling-shard-first-boot-in-isolation.md) — plain `evennia start` first, shut down, then `server_start`.

## Multi-shard dev setup
- [Shards view gamedirs — fix at symlink layer, not settings](feedback_shards_view_gamedirs.md) — Unix view gamedirs symlink back to `../game/`.

## Working approach
- [Confirm before crossing repos](confirm-before-crossing-repos.md) — ask before writing in another repo; reading is fine.
- [Test-instance credentials are root / p](feedback_test_instance_credentials.md) — local test gamedirs only.
- [Cheap tests beat confident theory](feedback_cheap_tests_over_theory.md) — verify before asserting; unverified means ask.
- [Reason, don't reflexively gather](feedback_reason_dont_just_gather.md) — before a check, ask what result would change the recommendation.
- [Green means green except tripwires](green-means-green-except-tripwires.md) — documented placeholders aren't findings.
- [Router tests use settings_router.py](router-tests-use-settings-router.md) — `--settings settings_router.py`; `settings.py` is stock and breaks on Account.
- [One file while iterating, sweep at the end](feedback_targeted_tests_during_dev.md) — run only the module just edited; full suite end-of-day.
- [No troubleshooting relics](feedback_no_troubleshooting_relics.md) — only the code that solved it ships.
- [Cooperative design loop](feedback_cooperative_design_loop.md) — discuss, plan, cases for one unit, approval, *then* tests. Scaffolding means structure, not content.
- [One issue per reply](feedback_stop_on_each_problem.md) — one decision, stop, then the next. Never close with "two more things".
- [No legacy-data concerns, ever](feedback_no_legacy_data_concerns.md) — fresh DB every deploy; never propose a backfill.
- [Fail loud until production](fail-loud-until-production.md) — raise, never swallow.
- [No hardening language](feedback_no_hardening_language.md) — the *current* plan, never settled; external constraints excepted.
- [Think twice before a TBD](feedback-no-tbd-for-undiscussed-values.md) — only for a meaningful open issue; a resolved TBD disappears.
- [Terse written records too](feedback_terse_written_records.md) — one line per fact in memory and notes.
- [Bottom line first](feedback_terse_confirmations.md) — one-line answer, then short dot points; stop.
- [Don't second-guess agreed scope](feedback-dont-second-guess-agreed-scope.md) — scope stated means execute.
- [A question is not an instruction](feedback_question_is_not_instruction.md) — answer and stop; wait for an imperative.
- [Never invent detail](feedback_never_invent_detail.md) — no invented timespans, counts or severities.
- [Consumers don't live in what they consume](feedback-consumers-dont-live-in-what-they-consume.md) — a command using messaging isn't a messaging command; ask placement as its own question.
- [Trust the owning component](feedback-trust-the-owning-component.md) — hand `tell_room` the lines and subject and stop; never test who is blind or deaf from a consumer.
- [A component's scope stops at the signal](component-scope-not-the-sender.md) — complete when an arriving signal is processed correctly.
- [Delete a handover once read](feedback-delete-handover-once-read.md) — `ops/scratch` handovers go as soon as they're read back.
- [Other sessions' uncommitted work is not yours](other-sessions-uncommitted-work.md) — stage only your paths; never `git add -A`.
- [Never refactor a dependency unasked](feedback-never-refactor-dependencies-unasked.md) — ask and wait; `git diff --stat` is the check.
- [Use the standard tooling](feedback-use-library-tooling.md) — check `design/parser-filter-inventory.md` first; nothing fits → raise a common helper, never hand-roll.
- [Standardisation is the gain](feedback-standardisation-is-the-gain.md) — moving onto the one standard implementation is worth it alone.
- [Name the deviation and its benefits](feedback-name-the-deviation-and-its-benefits.md) — say so and list what it buys; empty list means don't.
- [Patch the boundary first](feedback-patch-the-boundary-first.md) — a test broken by outside code: say "patch it" up front.
- [No cross-testing](feedback-no-cross-testing.md) — a typeclass's tests assert composition only (mixin on the chain, its own re-declarations); component behaviour is tested once, in the component.
- [Cases need a real trigger](feedback-cases-need-a-real-trigger.md) — a bug that happened or a plausible refactor into one.
- [No manufactured objections](feedback_no_manufactured_objections.md) — only concerns that bind here; zero means say so.
- [Answer the concept, not the literal wording](feedback_answer_the_concept_not_the_literal.md) — judge the idea before objecting.
- [Lead with the no](feedback_lead_with_the_no.md) — "no" in the first sentence.
- [Next step, not "settles it"](feedback_next_step_not_settles_it.md) — a diagnostic is the next step.
- [No alarming phrasing](feedback_no_alarming_phrasing.md) — state refinements plainly.
- [Frame findings as solvable work items](feedback_frame_findings_as_solvable.md) — options and a recommendation, never "this blocks everything".
- [Don't overinvest in tangents](feedback_dont_overinvest_tangents.md) — no tool-call chains on side questions.
- [Always include the imports](feedback_always_include_imports.md) — every in-game `py` snippet self-contained.
- [Show code as links, not dumps](feedback_code_links_not_dumps.md) — file link + line number.
- [Pushing no longer deploys](feedback_commit_includes_push.md) — deploys are manual; commit only what's approved.
- [Ask in prose, not option dialogues](feedback_ask_in_prose_not_dialogues.md) — no multiple-choice dialogues.
