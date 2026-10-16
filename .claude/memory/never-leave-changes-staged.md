---
name: never-leave-changes-staged
description: "Stage only in the same command as the commit — other sessions' commits sweep up whatever is left in the index"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 071e0a5b-fd32-48ca-8856-a2955ffd0e7c
  modified: 2026-10-15T13:01:04.493Z
---

Never leave anything staged between steps in a shared repo. Move files with plain `mv`, not `git mv`, and `git add` only in the same command as the `git commit`.

**Why:** 2026-10-09 — a `git mv` of assist.py and dodge.py sat staged while the rest of the move was in progress; another session's commit (2b70fa1, pushed) carried the two renames without the import fixes, and `main` failed to load the character cmdset until the completing commit landed.

2026-10-15 — staging plus `git diff --cached` in one command and the commit in the next was enough: another session's dice commit (f87a30c, pushed) swept describe_weapon in. Read the diff before staging (`git diff <paths>`), then add and commit in one command.

**How to apply:** the index is shared with every session on the repo; treat it as empty except inside a single stage-and-commit command. See [[other-sessions-uncommitted-work]] and [[feedback-read-the-staged-diff]].
