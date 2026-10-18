---
name: feedback-precedent-is-not-a-reason
description: That the codebase rarely does something (e.g. type annotations) is not an argument against doing it now; judge the practice on its merits.
metadata:
  node_type: memory
  type: feedback
  originSessionId: 38d07b26-d19a-4ceb-886d-a917919bc5b1
  modified: 2026-10-17T17:17:00.145Z
---

Don't weigh a good practice down with "the codebase rarely does this". Rarity in existing code is history, not a reason. Judge it on what it buys here.

**Why:** when Tim proposed type annotations on the `EncounterMemory` interface (2026-10-17), I noted they appear in ~22 of ~2,200 functions. Tim: "just because it might not have been done previously does not mean that it's not good practice for us to do here."

**How to apply:** mention existing convention only when matching it is the actual point (consistency a reader relies on); never as a soft objection. Type annotations on interface signatures are welcome. Related: [[feedback_no_manufactured_objections]], [[rebuild-not-retrofit]].
