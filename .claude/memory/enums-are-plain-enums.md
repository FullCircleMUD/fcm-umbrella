---
name: enums-are-plain-enums
description: "Enums are plain Enum; cross into strings with .value, never a str/IntEnum mixin"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7b812b27-2051-410f-83e2-f84f4af6f6c5
  modified: 2026-09-19T14:40:12.502Z
---

Declare enums as plain `Enum`. Every crossing into an attribute name, a stored dict key or a payload
goes through `.value`. Don't use `str, Enum` or `IntEnum` to make members compare directly as
strings or ints.

**Why:** repeated past problems with mixed-shape enums; coming back to a plain `Enum` with explicit
`.value` has been the solution every time. An opaque member also makes an accidental comparison
against a raw string fail loudly instead of being quietly true.

**How to apply:** new enums are plain `Enum`. Where behaviour depends on members staying opaque,
pin it with an assertion about absence (`Member != "word"`), so a later change to a `str` mixin
fails a test rather than passing silently. See [[feedback-name-the-deviation-and-its-benefits]] if
proposing a different shape.
