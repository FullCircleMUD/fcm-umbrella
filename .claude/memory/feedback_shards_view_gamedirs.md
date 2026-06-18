---
name: Shards view gamedirs — fix at the symlink layer, not in settings
description: For multi-shard local dev on macOS/Linux, don't propose settings.py changes — solve view-gamedir issues with filesystem symlinks (including .db3 files)
type: feedback
originSessionId: 1089dae9-7b49-49d5-af49-a384b5e837b3
---
When wiring up `game-router/` and `game-shard1/` as Unix view gamedirs alongside `src/game/` (the canonical shard0 dir), DO NOT propose changes to `settings.py` or `settings_common_shard_config.py` to make paths work. Solve every layout problem with filesystem symlinks.

**Why:** the settings files are validated and working on the user's Windows dev machine (Windows runs all roles directly from `src/game/`, no view dirs needed). Adding Unix-only branches to settings would diverge that working baseline. The view-gamedir pattern is a *local filesystem* concern, not a code concern. The `libraries/evennia-shards/examples/` demo on Unix uses a settings override for its single SQLite db, but that approach is not appropriate for FCM — FCM has 4 SQLite dbs and a Windows dev baseline to preserve.

**How to apply:** when an `evennia <cmd> --settings settings_router` (or similar) fails from a view gamedir with a path-related error (db missing, module missing, etc.), the fix is a new symlink in the view gamedir back to `../game/` or `../../game/server/`. Specifically:
- Top-level Python packages → symlink each from `../game/<pkg>`
- `server/conf`, `server/.static`, `server/main_menu`, `server/walletwebclient.py` → symlink from `../../game/server/<name>`
- `server/*.db3` (all four: evennia, xrpl, ai_memory, subscriptions) → symlink from `../../game/server/<name>` so SQLite follows them to the canonical db and creates journal/WAL files alongside the real files
- `server/__init__.py`, `server/logs/` → real per-instance (empty file and empty dir)
