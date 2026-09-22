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
yaml-reader); game-content repos (fcm-world, fcm-mobs, lore, fullcirclemud, transparency) are grouped
under `content/`; supporting tools — including the blockchain/XRPL integration (`xrpl-tools`,
`nft_api`, `cosigner`) and `llm-test-harness` — are grouped under `utilities/`. System design lives in
`design/`. Marketing and operational material is secondary and kept in private repos (e.g. `ops/`).

**Deliberately not:** a financial product — no redemption, peg, or backing. Blockchain is FCM's
*database* for genuine ownership, not an investment; XRPL tokens are how the game implements items and
currency.

**Project status** is not tracked here (it would go stale) — see `design/` and `MEMORY` for current state.

## Read first
- **[design/INDEX.md](design/INDEX.md) — read this every session** (the docs catalogue; not auto-loaded
  like `MEMORY`), and load the relevant doc before related work.
- **MEMORY** (`.claude/memory/MEMORY.md`) — auto-loaded durable decisions/agreements; the index points
  to topic files pulled in on demand.
- [README.md](README.md) — what this is and its layout.
- [design/new-machine-setup.md](design/new-machine-setup.md) — re-clone manifest + git-crypt unlock.
- [design/doco-structure.md](design/doco-structure.md) — what belongs in which doc surface.

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
[design/new-machine-setup.md](design/new-machine-setup.md).

> These are **plain markdown links, not `@imports`** — plain links keep each sub-repo's `CLAUDE.md`
> lazy; an `@import` would load them all eagerly on every session.

## The rebuild — nothing carries over unexamined

**Never bulk-copy, bulk-port or bulk-rewrite anything from `src_old/` into `src/`.** No `cp -r`, no
`sed` across files, no "port this module across", no find-and-replace sweep over the docs. Not once,
not for the easy cases, not to save time.

The entire point of the rebuild is that every element gets re-evaluated on its merits and exists in
`src/` because it was decided to, not because it was there before. A bulk operation is the one move
that guarantees the opposite: it carries the old design across without anyone looking at it, and the
reasons it was wrong come with it.

So: one thing at a time, with a reason for keeping it. This covers code, settings, content, tests,
and documentation references alike. `src_old/` is reference material to read and learn from — never a
source to copy from.

## Project scope — game-repo changes need Tim's approval

**No changes to any game repos without Tim's explicit approval.** Development, analysis, and local
work are fine, but committing/pushing changes to the game repositories requires Tim's sign-off for that
specific change. When unsure whether a repo counts, ask before changing it.

## Test-first — the test plan comes first, everywhere

**Never write code before the test plan says what it should do.** The order is fixed, and it applies to
the umbrella, the libraries, `src/game`, and every other sub-repo:

1. **Update the test plan** with the cases defining the behaviour — this is where behaviour is agreed.
2. **Write the tests.** If a test needs something that doesn't exist yet, create the placeholder with
   the real signature and a `raise NotImplementedError` body, so the test is writable.
3. **Run them.** Failures at this point are expected and correct.
4. **Write the code** until they pass.

Full process and rationale: [design/test-first-process.md](design/test-first-process.md).

## Working discipline — assumptions & documentation

Never record anything as *decided / agreed / canonical* unless it was actively discussed **and**
explicitly approved. Flag anything not yet agreed with `[TBD — needs discussion: <what is open>]`
rather than writing it as settled.

- Capture only what was discussed and agreed; don't extrapolate a principle into unraised specifics.
- Flag open questions explicitly with `[TBD — …]` so a later session picks them up deliberately.
- Distinguish archived/historical material from in-conversation decisions.
- Smaller is better — three faithfully-captured points beat ten padded ones.
- Self-correct — if you catch yourself writing beyond what was discussed, remove it or mark it `[TBD]`.

**The one exception: regulatory and compliance rules.** These are written as hard rules — "never",
"always", "no exceptions" — and that framing is approved. They are not preferences to be optimised
against. The play-to-earn position and everything around it is the standing example; see
[design/compliance.md](design/compliance.md) and `ops/COMPLIANCE_LEGAL.md`. Do not soften compliance wording
to match the flexible tone used everywhere else, and do not borrow its absolute tone for a design,
marketing, or engineering preference.
> ### ⚠️ STOP. THE RULE BELOW IS THE ONE YOU ARE ABOUT TO BREAK. ⚠️
>
> **Every single session has read this rule, understood it, and then broken it anyway.** Every one of
> them has then said some version of *"yes, I knew the rule was there, and I ignored it."* That
> answer is worthless and Tim is thoroughly sick of hearing it.
>
> You are not the exception. You will feel that your particular mention of how it used to be is
> justified because it explains something. It is not, and it does not. **Delete it.**
>
> The documentation has exactly three readers, and **not one of them needs any of it**:
>
> 1. **A developer** — "how does this work, so I can develop on it?"
> 2. **A consumer** — "how does this work, so I can implement against it?"
> 3. **An LLM** — "how does this work, so I can extend it?"
>
> None of those three is served by what it was before, what we changed, what legacy did, why we moved
> away from the old approach, or which alternative was rejected. **This is a greenfield
> implementation and it is documented as one.** No archaeology. No past tense about our own work. No
> comparisons to `src_old/`. No "rather than the old X". No war stories about bugs we hit last week.
>
> This applies to every surface: code comments, docstrings, README files, design docs, test plans and
> case descriptions. Git history is where the past lives. Leave it there.

- **Document what IS, not what WAS.** When something changes, record only the current state — drop
  "used to be" / "migrated from" / "formerly" / "renamed from" / "superseded" framing. The prior state
  serves no future session and goes stale; git history holds it. Record what-was **only** when there is
  a real, direct need a human has agreed to (e.g. a deprecated thing that still exists and must not be
  used — then state the *current* rule: "use X, not Y", without the history).

> ### ⚠️ END OF THE RULE EVERY SESSION BREAKS. ⚠️
>
> Before you write any comment, docstring or doc line, check it against the three readers above. If a
> sentence only makes sense to someone who knows what the code looked like yesterday, it does not go
> in.

## Git safety — destructive operations require explicit approval

Never run a destructive git operation without explicit, in-conversation approval for that specific
action — regardless of any settings allowlist or prior approval. Destructive includes: force push,
hard reset, discarding uncommitted changes, `git clean -f`, force-deleting branches, history rewrites
(`rebase`, `amend` on pushed commits, `filter-branch`/`filter-repo`), dropping stashes, deleting tags,
and any `--no-verify` / `--no-gpg-sign` bypass. Force-pushing a protected branch (`main`/`master`/
`release/*`) must be refused outright. When unsure whether something can lose work or rewrite history,
treat it as destructive and ask.

