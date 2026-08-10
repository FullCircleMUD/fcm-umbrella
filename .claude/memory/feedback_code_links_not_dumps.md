---
name: feedback-code-links-not-dumps
description: "When asked to show code, give a file link and line number — don't print the code out"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c41cb4a-335c-4edf-8beb-92321dc36d13
  modified: 2026-08-08T22:18:41.229Z
---

When Tim asks to see code, respond with a markdown link to the file and a line
number where relevant. Do not paste the code into the reply.

**Why:** he reads it in the IDE, where he has full context, navigation and
history. A printed copy is redundant, costs him scrolling, and goes stale the
moment the file changes.

**How to apply:** `[cmd_deposit.py:64](src/game/commands/room_specific_cmds/bank/cmd_deposit.py#L64)`
rather than a fenced block. Quote at most a line or two when the specific
wording *is* the point being made — an error string, a comparison operator, a
setting value. Explanation and analysis are still wanted; it is the code dump
that isn't. See [[feedback-stop-on-each-problem]] for the related preference
about volume.
