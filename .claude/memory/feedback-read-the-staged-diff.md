---
name: feedback-read-the-staged-diff
description: "Read `git diff --cached` before every commit, above all when staging by patch in a file other sessions touch"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e22219b7-f51d-408c-97ba-54252b909d4c
  modified: 2026-10-07T00:24:19.572Z
---

Before committing, read `git diff --cached` against HEAD. When staging only my hunks by patch, build the patch from HEAD as it is at that moment, then read the staged diff.

**Why:** 2026-10-06 — another session committed `event.py` (my enum lines included) between my edit and my commit; my patch re-added them, `main` broke on a duplicate `Enum` member and was pushed. The staged diff would have shown it.

**How to apply:** every commit, and always in shared files. The content, not `--stat` — the same day a `--stat` read let another session's red test into a commit. A whole-file `git add` of a file with someone else's hunks commits them too. Related: [[other-sessions-uncommitted-work]].
