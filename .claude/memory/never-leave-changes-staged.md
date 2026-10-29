---
name: never-leave-changes-staged
description: "Stage only in the same command as the commit — other sessions' commits sweep up whatever is left in the index"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 071e0a5b-fd32-48ca-8856-a2955ffd0e7c
  modified: 2026-10-29T15:28:52.196Z
---

Never leave anything staged between steps in a shared repo. Move files with plain `mv`, not `git mv`, and `git add` only in the same command as the `git commit`.

**Why:** 2026-10-09 — a `git mv` of assist.py and dodge.py sat staged while the rest of the move was in progress; another session's commit (2b70fa1, pushed) carried the two renames without the import fixes, and `main` failed to load the character cmdset until the completing commit landed.

2026-10-15 — staging plus `git diff --cached` in one command and the commit in the next was enough: another session's dice commit (f87a30c, pushed) swept describe_weapon in. Read the diff before staging (`git diff <paths>`), then add and commit in one command.

2026-10-24 — add and commit were in one command, but the commit hit another session's `index.lock` and failed, leaving the add staged; that session's commit (1453eb5, pushed) swept in the whole conversational_npc component. A failed commit must unstage in the same command: `git add <paths> && git commit … || git reset -q -- <paths>`.

The shell is zsh, which does not word-split `$VAR`: a path list in a variable is one pathspec and the add fails. Use an array: `P=(path/one path/two)`, then `git add -- $P`.

2026-10-29 — the array was built from `git diff --name-only` at commit time, and another session had edited a file in the seconds since the status check; its 38 lines of `player_trade/test-plan.md` went into my commit (f81542f, pushed). **Name every path explicitly**; never derive the list from the tree at commit time.

**How to apply:** the index is shared with every session on the repo; treat it as empty except inside a single stage-and-commit command. See [[other-sessions-uncommitted-work]] and [[feedback-read-the-staged-diff]].
