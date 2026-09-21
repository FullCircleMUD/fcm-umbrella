---
name: property-writes-by-assignment
description: "Custom properties are always written by whole-value assignment, never in-place mutation"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 80027444-c228-4e6b-af15-f4d84750ce8e
  modified: 2026-09-19T20:06:31.326Z
---

Write an Evennia custom property by assigning the whole value. Never mutate in place.

**Why:** validation lives in `at_set`, which only runs on assignment. Evennia's `_SaverSet` /
`_SaverList` persist `.add()`, `.update()`, `.remove()` etc. straight to the attribute, skipping
it. This is known and accepted, not a defect to design around — closing it would mean custom
collection types standing in for Evennia's.

**How to apply:** `obj.thing = obj.thing | {new}`, not `obj.thing.add(new)`. Don't propose guards
against in-place mutation, and don't caveat a validating property with it. Deviating needs an
incredibly powerful reason.

Related: [[enums-are-plain-enums]]
