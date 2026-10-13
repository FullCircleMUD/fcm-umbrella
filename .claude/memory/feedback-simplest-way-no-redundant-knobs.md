---
name: feedback-simplest-way-no-redundant-knobs
description: Build the desired output the simplest way — never add a setting an existing mechanism already covers
metadata:
  node_type: memory
  type: feedback
  originSessionId: e22219b7-f51d-408c-97ba-54252b909d4c
  modified: 2026-10-06T14:23:24.220Z
---

Reach the desired output in the simplest possible way. Before adding an attribute, flag or default, check whether an existing mechanism already does it (e.g. a mixin's own property default, a preference a builder can set). If it does, don't add it, and don't set a default on another component's behalf.

**Why:** `starts_auto_assisting` duplicated what preferences already offer; Tim (2026-10-06) does not want time spent going back to fix redundancy that should never have gone in.

**How to apply:** catch it at case-drafting time, not after commit. Once something is in and works, keep moving forward rather than proposing a cleanup unless Tim asks. Related: [[feedback-every-choice-is-tims]].
