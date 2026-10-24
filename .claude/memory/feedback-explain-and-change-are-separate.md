---
name: feedback-explain-and-change-are-separate
description: Explaining something and changing a system are separate phases — never slip a command that changes a box into an explanation; label every change command as one.
metadata:
  node_type: memory
  type: feedback
  originSessionId: eb39a4d7-311c-402d-8f37-35f7d2c9f880
  modified: 2026-10-24T15:56:54.497Z
---

Explaining how something works and making a change on a system are distinct phases of the
conversation. While explaining, give no command that changes anything; when a change is wanted, say
plainly that the block changes the box, and what it changes.

**Why:** 2026-10-24 — explaining `needrestart`, I included the drop-in command as part of the
explanation; Tim ran it and only found out later that it had changed the staging box.

**How to apply:** read-only commands (checks, logs, status) can go anywhere. A command that writes a
file, changes config, restarts a service or alters a database goes in its own step, introduced as a
change ("this changes the box: …"), only once Tim has asked for the change.
