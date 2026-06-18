# libraries — nested working repos

The Evennia support libraries for FCM. Each is an **independent git repository** with its own
remote, so the umbrella **gitignores** them (see the umbrella root `.gitignore`) — only this README
is tracked here, to keep the folder and document what belongs in it.

> On a fresh machine, cloning the umbrella does **not** bring these down. Re-clone them with the
> commands below. (For the full umbrella-wide re-clone recipe across all sub-repos, see `docs/`.)

## Repos

| Repo | Branch | Clone |
|---|---|---|
| evennia-mob-spawner | main | `git clone https://github.com/FullCircleMUD/evennia-mob-spawner.git` |
| evennia-mob-spawner-test-world | main | `git clone https://github.com/FullCircleMUD/evennia-mob-spawner-test-world.git` |
| evennia-mob-spawner-test-yaml | main | `git clone https://github.com/FullCircleMUD/evennia-mob-spawner-test-yaml.git` |
| evennia-shards | main | `git clone https://github.com/FullCircleMUD/evennia-shards.git` |
| evennia-targeting | main | `git clone https://github.com/FullCircleMUD/evennia-targeting.git` |
| evennia-world-builder | main | `git clone https://github.com/FullCircleMUD/evennia-world-builder.git` |
| evennia-world-builder-test-yaml | main | `git clone https://github.com/FullCircleMUD/evennia-world-builder-test-yaml.git` |
| evennia-yaml-reader | main | `git clone https://github.com/FullCircleMUD/evennia-yaml-reader.git` |

Run these from inside `libraries/`. Folder names must match the `.gitignore` entries exactly.
