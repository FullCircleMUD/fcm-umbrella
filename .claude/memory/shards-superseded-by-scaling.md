---
name: shards-superseded-by-scaling
description: evennia-shards is being deprecated; evennia-scaling is the standard and the rebuild targets it
metadata: 
  node_type: memory
  type: project
  originSessionId: f7d8cab1-b454-46a6-b725-7b76d2d34e2c
  modified: 2026-10-24T19:10:29.139Z
---

`evennia-shards` is on its way out; `evennia-scaling` is the standard. The end state for shards is **retired from service and yanked from PyPI, not deleted**.

**Why:** shards has the fuller docs and CLAUDE.md, so a session would otherwise treat it as the more current of the two.

**How to apply:** don't consider shards in new library development or design decisions; don't propose features or integrations for it.
