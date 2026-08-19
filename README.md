# fcm-umbrella

> *The development workspace for FullCircleMUD — the game, its libraries, and its infrastructure.*

The **umbrella repository** for FullCircleMUD (FCM) development. FCM is a text-based MUD with real
**on-chain item ownership** on the XRP Ledger and an **LLM-driven AI layer** for its NPCs. This repo is
the coordination layer that ties the many independent FCM repositories together under one roof —
carrying the shared Claude Code tooling (`.claude/`, `CLAUDE.md`, rules, portable memory) and the local
multi-shard dev setup — while each working repo stays version-controlled by its own remote. System
design lives in the `design` repo. (Marketing and operational material is secondary and lives in
private repos such as `ops/`.)

> The umbrella **gitignores** the nested working repos: cloning this repo does not bring them down.
> See **[design/new-machine-setup.md](design/new-machine-setup.md)** for the re-clone manifest.

## Layout

```
fcm-umbrella/
├── .claude/              shared tooling: settings, rules, agents, hooks, memory
├── CLAUDE.md             always-loaded project context + working rules
├── design/               the technical / knowledge wiki (own repo; start at design/INDEX.md)
├── libraries/            Evennia support libraries (each its own repo; see libraries/README.md)
├── src/
│   ├── game/             the Evennia game (git-crypt'd secrets; own repo)
│   ├── game-router/      Unix view gamedir (symlinks → ../game) — tracked here
│   └── game-shard1/      Unix view gamedir (symlinks → ../game) — tracked here
└── <top-level repos>     cosigner, fcm-mobs, fcm-world, fullcirclemud, llm-test-harness,
                          lore, nft_api, ops, transparency, xrpl-tools (each its own repo)
```

## Getting started

1. **New machine?** Follow [design/new-machine-setup.md](design/new-machine-setup.md) — prerequisites, the
   nested-repo re-clone manifest (some repos are private), portable-memory first launch, and git-crypt
   unlock for the game secrets.
2. **Always launch Claude from the umbrella root** — that's what makes the shared `.claude/` layer
   authoritative while each sub-repo's own context loads on demand.
3. Read [design/INDEX.md](design/INDEX.md) for the documentation map and
   [design/doco-structure.md](design/doco-structure.md) for what belongs in which surface.

## Status

In active development. The `design` repo is the **source of truth for FCM design documentation**.
