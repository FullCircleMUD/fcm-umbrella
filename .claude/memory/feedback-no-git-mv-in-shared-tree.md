---
name: feedback-no-git-mv-in-shared-tree
description: "Don't stage early in a working tree other sessions share — git mv stages at once, and another session's commit can sweep it up."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dcc6756-b34a-48cd-9cb5-5460230836d1
  modified: 2026-10-09T22:57:01.365Z
---

Rename with plain `mv` and stage the paths only at commit time; never `git mv` (or any early `git add`) while other sessions work in the same repo.

**Why:** 2026-10-09, `git mv died.py self_died.py` in `src/router` was swept into another session's commit (`80b9dcf`) without the edits, leaving pushed `main` unable to import `mob_ai` until the follow-up commit.
**How to apply:** keep the index empty of my work until the commit step; stage, read `git diff --cached`, commit in one go. Related: [[other-sessions-uncommitted-work]], [[feedback-read-the-staged-diff]].
