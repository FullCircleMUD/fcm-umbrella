---
name: logging-extension-settings-window-loss
description: "evennia-logging-extension loses settings-window writes in twistd child processes — observed live from database-cascade, to be raised with the extension"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1ba3580e-a35a-4536-9bd9-bd812f7f3a26
  modified: 2026-09-11T03:44:30.915Z
---

Observed 2026-09-11 in evennia-database-cascade's demo: a line logged while the consumer's settings
module is still executing lands from the launcher process but is silently lost in the twistd-spawned
portal and server processes — it reaches neither the library's log nor `pre-startup.log`. Lines
written after `django.setup()` land from every process. Full debugging record:
`ops/scratch/BUG-logging-extension-settings-window-loss-2026-09-11.md` (evidence, repro, the code
path, hypotheses). Not a cascade defect; raise with `evennia-logging-extension` before relying on
settings-window logging in child processes.
