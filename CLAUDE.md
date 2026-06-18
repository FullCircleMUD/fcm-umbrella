# CLAUDE.md — FCM umbrella

The always-loaded operating context for the FullCircleMUD (FCM) project. You work from the **umbrella
repo** — always launch from here so this layer is authoritative; each sub-repo's own `CLAUDE.md` and
skills load on demand.

## What this project is

**FullCircleMUD (FCM)** is a text-based multiplayer online game (a MUD) distinguished by two layers:
real **on-chain item and currency ownership** on the XRP Ledger, and an **LLM-driven AI layer** that
gives NPCs memory and emergent behaviour. This **umbrella repo is the development workspace** for the
game, its supporting libraries, and its infrastructure — the coordination layer over the many
independent repositories that build and run FCM. It carries the shared Claude tooling and the
system-design documentation; each working repo stays version-controlled by its own remote.

**How it fits together:** the game runs on **Evennia** (Python/Django) in `src/game`; reusable,
FCM-agnostic Evennia extensions live in `libraries/` (world-builder, mob-spawner, targeting, shards,
yaml-reader); blockchain/XRPL integration spans `xrpl-tools`, `nft_api`, `cosigner`, and
`transparency`. System design lives in `docs/`. Marketing and operational material is secondary and
kept in private repos (e.g. `ops/`).

**Deliberately not:** a financial product — no redemption, peg, or backing. Blockchain is FCM's
*database* for genuine ownership, not an investment; XRPL tokens are how the game implements items and
currency.

**Project status** is not tracked here (it would go stale) — see `docs/` and `MEMORY` for current state.

## Read first
- **[docs/INDEX.md](docs/INDEX.md) — read this every session** (the docs catalogue; not auto-loaded
  like `MEMORY`), and load the relevant doc before related work.
- **MEMORY** (`.claude/memory/MEMORY.md`) — auto-loaded durable decisions/agreements; the index points
  to topic files pulled in on demand.
- [README.md](README.md) — what this is and its layout.
- [docs/new-machine-setup.md](docs/new-machine-setup.md) — re-clone manifest + git-crypt unlock.
- [docs/doco-structure.md](docs/doco-structure.md) — what belongs in which doc surface.

## Sub-repo context

Each nested repo can carry its own `CLAUDE.md`, **auto-loaded (lazily) when Claude reads a file in
that repo** — repo-specific context arrives only when relevant. The loading is automatic (these are
orientation links, not the trigger). Sub-repos with their own context today:

- [src/game](src/game/CLAUDE.md) — the Evennia game module
- [ops](ops/CLAUDE.md) — operations workspace (development, marketing, loose material)
- [libraries/evennia-mob-spawner](libraries/evennia-mob-spawner/CLAUDE.md)
- [libraries/evennia-shards](libraries/evennia-shards/CLAUDE.md)
- [libraries/evennia-targeting](libraries/evennia-targeting/CLAUDE.md)
- [libraries/evennia-world-builder](libraries/evennia-world-builder/CLAUDE.md)
- [libraries/evennia-yaml-reader](libraries/evennia-yaml-reader/CLAUDE.md)

The **full** set of nested repos (including those without their own `CLAUDE.md` yet) is listed in
[docs/new-machine-setup.md](docs/new-machine-setup.md).

> These are **plain markdown links, not `@imports`** — plain links keep each sub-repo's `CLAUDE.md`
> lazy; an `@import` would load them all eagerly on every session.

## Project scope — game-repo changes need board approval

**No changes to any game repos without explicit board approval.** Development, analysis, and local
work are fine, but committing/pushing changes to the game repositories requires board sign-off for that
specific change. When unsure whether a repo counts, ask before changing it.

## Working discipline — assumptions & documentation

Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
explicitly approved. Flag anything not yet agreed with `[TBD — needs discussion: <what is open>]`
rather than writing it as settled.

- Capture only what was discussed and agreed; don't extrapolate a principle into unraised specifics.
- Flag open questions explicitly with `[TBD — …]` so a later session picks them up deliberately.
- Distinguish archived/historical material from in-conversation decisions.
- Smaller is better — three faithfully-captured points beat ten padded ones.
- Self-correct — if you catch yourself writing beyond what was discussed, remove it or mark it `[TBD]`.
- Docs describe the **current state only**; what-was lives in git history, not in prose.

## Git safety — destructive operations require explicit approval

Never run a destructive git operation without explicit, in-conversation approval for that specific
action — regardless of any settings allowlist or prior approval. Destructive includes: force push,
hard reset, discarding uncommitted changes, `git clean -f`, force-deleting branches, history rewrites
(`rebase`, `amend` on pushed commits, `filter-branch`/`filter-repo`), dropping stashes, deleting tags,
and any `--no-verify` / `--no-gpg-sign` bypass. Force-pushing a protected branch (`main`/`master`/
`release/*`) must be refused outright. When unsure whether something can lose work or rewrite history,
treat it as destructive and ask.

