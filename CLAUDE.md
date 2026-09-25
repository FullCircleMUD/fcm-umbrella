# CLAUDE.md — FCM umbrella

## What this project is

**FullCircleMUD (FCM)** is a text-based multiplayer online game (a MUD) distinguished by two layers:
real **on-chain item and currency ownership** on the XRP Ledger, and an **LLM-driven AI layer** that
gives NPCs memory and emergent behaviour. This **umbrella repo is the development workspace** for the
game, its supporting libraries, and its infrastructure — the coordination layer over the many
independent repositories that build and run FCM. It carries the shared Claude tooling; each working
repo stays version-controlled by its own remote.

**How it fits together:** the game runs on **Evennia** (Python/Django) in `src/router`, with its
shard instances beside it in `src/`. Evennia extension libraries live in `libraries/`, one repo each.
Game content — world, mobs, lore — is under `content/`, and supporting tools, including the XRPL
integration, under `utilities/`. Marketing and operational material is secondary and kept in private
repos (e.g. `ops/`).

**No inventory is kept here** — listings of repos, files and docs go stale; `ls` and `find` answer
them. Validate the paths above the same way, and if one differs, say so rather than quietly working
around it.

**`src_old/` is the legacy game** — the build FCM ran on before this one. It is authoritative for
nothing, and is read as reference: for ideas, and for porting code across one piece at a time. The
rules governing that are in *The rebuild* below.

**Deliberately not:** a financial product — no redemption, peg, or backing. Blockchain is FCM's
*database* for genuine ownership, not an investment; XRPL tokens are how the game implements items and
currency.

**Project status** is not tracked here (it would go stale) — see `MEMORY` for current state.

**MEMORY** (`.claude/memory/MEMORY.md`) is auto-loaded and is an **index**: each line points to a
topic file holding the actual fact. Open the topic file before relying on a line.

**Sub-repo context arrives on its own.** A nested repo may carry its own `CLAUDE.md`, loaded
automatically when I read a file in that repo — no need to fetch one up front.

## The rebuild — nothing carries over unexamined

**Never bulk-copy, bulk-port or bulk-rewrite anything out of `src_old/`.** Not into `src/`, not into
a library, not into `content/`. No `cp -r`, no `sed` across files, no "port this module across", no
find-and-replace sweep over the docs. Not once, not for the easy cases, not to save time.

The entire point of the rebuild is that every element gets re-evaluated on its merits and exists in
the rebuild because it was decided to, not because it was there before. A bulk operation is the one
move that guarantees the opposite: it carries the old design across without anyone looking at it, and
the reasons it was wrong come with it.

So: one thing at a time, with a reason for keeping it. This covers code, settings, content, tests,
and documentation references alike. `src_old/` is reference material to read and learn from — never a
source to copy from.

## Approval — commits need Tim's sign-off

**Never commit to any repo, anywhere, without Tim's explicit approval for that specific commit.**
Approval never carries forward to the next one.

**Pushing needs none.** What is committed was already approved, and no deployment follows a push —
deploys are done by hand. Push the branch with whatever is on it, including commits another session
left unpushed.

> That holds because the game is not running live and nothing deploys automatically. **When either
> stops being true, this is out of date** — say so and ask, rather than relying on it.

Local work — editing, running, testing, analysis — needs no approval.

## Test-first — the test plan comes first, everywhere

**Never write code before the test plan says what it should do.** The order is fixed, and it applies to
the umbrella, the libraries, `src/`, and every other sub-repo:

1. **Update the test plan** with the cases defining the behaviour — this is where behaviour is agreed.
2. **Write the tests.** If a test needs something that doesn't exist yet, create the placeholder with
   the real signature and a `raise NotImplementedError` body, so the test is writable.
3. **The red run.** Failures here are expected and correct. Some cases pass anyway, because the
   condition they would fail on does not exist yet — note which ones, they are step 5.
4. **Write the code** until they pass.
5. **Mutate everything that passed green on the red run.** A case that has never failed has never
   been shown to test anything. Break what it covers, confirm it fails, put it back. A case that
   still passes is vacuous — rewrite it or drop it, and say which.

## Working discipline — record the practice, never a decision

**Nothing here is *decided*, *agreed* or *canonical*. Record what we are currently doing, and write
it so it reads as changeable.** "The current practice is X", not "we decided X".

The project is iterative. Something gets worked out, and weeks later a better way surfaces while
we are doing something else. A note written as settled gets quoted back at Tim as a constraint —
*"you can't, this was decided"* — and at that point the note is doing harm rather than work. It was
never a rule; it was what we were doing at the time.

- **Never cite an earlier record as a reason Tim cannot change something.** Say what the current
  practice is and what changing it would affect. The call is his, every time.
- Capture only what was discussed; don't extrapolate a principle into unraised specifics.
- Flag what is still open with `[TBD — needs discussion: <what is open>]` so a later session picks it
  up deliberately rather than inheriting a guess.
- Smaller is better — three faithfully-captured points beat ten padded ones.
- Self-correct — if you catch yourself writing beyond what was discussed, remove it or mark it `[TBD]`.

**The one exception: regulatory and compliance rules.** These are written as hard rules — "never",
"always", "no exceptions" — and that framing is approved. They are not preferences to be optimised
against. The play-to-earn position and everything around it is the standing example; see
`ops/COMPLIANCE_LEGAL.md`. Do not soften compliance wording
to match the flexible tone used everywhere else, and do not borrow its absolute tone for a design,
marketing, or engineering preference.
## Documentation — write what is, never what was

**Before any comment, docstring, README line, test plan or case description, ask which of these three
readers needs the sentence:**

1. **A developer** — "how does this work, so I can develop on it?"
2. **A consumer** — "how does this work, so I can implement against it?"
3. **An LLM** — "how does this work, so I can extend it?"

None of the three is served by what the thing was before, what changed, what legacy did, why an
approach was dropped, or which alternative lost. **This is a greenfield implementation and it is
documented as one.** Git history holds the past.

> You will feel that your particular mention of how it used to be is justified because it explains
> something. It is not, and it does not. **Delete it.**

Catch these as you type them: *used to be · migrated from · formerly · renamed from · superseded ·
previously · no longer · rather than the old*. Same for past tense about our own work, comparisons to
`src_old/`, and war stories about bugs already fixed.

**The one exception** is a deprecated thing that still exists and must not be used. State the current
rule — "use X, not Y" — without the history behind it. Anything beyond that needs a human to agree
there is a direct need.

## Git safety — destructive operations require explicit approval

Never run a destructive git operation without explicit, in-conversation approval for that specific
action — regardless of any settings allowlist or prior approval. Destructive includes:

- **Losing uncommitted work** — hard reset, discarding changes (`git restore`/`checkout` over a
  path), `git clean -f`, `git stash` (it moves work out of the tree), `git rm`,
  `git worktree remove --force`
- **Rewriting history** — force push, `rebase`, `amend` on a pushed commit,
  `filter-branch`/`filter-repo`
- **Destroying references** — force-deleting branches, deleting tags, deleting a remote branch
  (`git push --delete`), `git update-ref -d`, dropping stashes
- **Removing the recovery net** — `git reflog expire`, `git gc --prune`. These are what make the
  other mistakes survivable
- **Bypassing checks** — any `--no-verify` / `--no-gpg-sign`

Force-pushing a protected branch (`main`/`master`/`release/*`) must be refused outright. When unsure
whether something can lose work or rewrite history, treat it as destructive and ask.

