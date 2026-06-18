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
- Work happens in the **FCM umbrella** (`/Users/timbaird/Documents/FCM-umbrella/`) — the dev workspace that gitignores the nested repos. Full repo manifest + layout live in `docs/new-machine-setup.md`; design docs now live in the umbrella `docs/` (migrated from the former `design` repo, which is being retired).
- `src/game` uses git-crypt — see [git-crypt setup for src/game secrets](gitcrypt_game_secrets.md).
- `src/game` branches: `main` (default), `dev`, and the active working branch `shards-rework`.

## Upcoming Work
- [Upcoming FCM world build in YAML](upcoming_fcm_world_build.md) — starting 2026-05-08, rebuilding FCM world content via the `evennia-world-builder` library; real-world content expected to surface edge cases the synthetic fixtures didn't reach

## Documentation
- [Design docs live in the umbrella docs/](design-docs-in-umbrella.md) — FCM system design now lives in `FCM-umbrella/docs/` (kebab-case); the standalone `design` repo is superseded/deprecated (archived, not deleted). Libraries self-document in their own `docs/`. Edit design docs in the umbrella, not the design repo.

## Dropped / Deprecated
- [evennia-stateful-text dropped](project_evennia_stateful_text_dropped.md) — Evennia provides the functionality natively; GitHub repo deleted (2026-05-14)

## YAML porting conventions
- [Mobs are spawn-script driven, not YAML entities](feedback_mobs_vs_npcs_yaml.md) — NPCs go in `npc_*.yaml`; mobs (incl. named bosses) get only a `mob_area` room tag and are spawned dynamically

## Multi-shard dev setup
- [Shards view gamedirs — fix at symlink layer, not settings](feedback_shards_view_gamedirs.md) — Windows runs all roles from `src/game/`; Unix needs view gamedirs (`game-router/`, `game-shard1/`) with symlinks back to `../game/`. Solve path errors with symlinks, not settings edits.

## Working approach
- [Cheap tests beat confident theory](feedback_cheap_tests_over_theory.md) — when user experience contradicts my model, propose a `--plan`/dry-run/read-only check before re-asserting. Two wrong calls in one session were both avoidable with a cheap test.
