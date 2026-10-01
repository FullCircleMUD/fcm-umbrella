---
name: design-principles-outrank-library-principles
description: "design/design-principles.md is Tim's and authoritative; a library CLAUDE.md's principles were written by Claude and lose any conflict"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 80acec2b-ec61-4894-bc9b-a497be0449f4
  modified: 2026-09-29T18:26:38.386Z
---

`design/design-principles.md` holds the principles Tim specifically asked to be written. The "load-bearing principles" in a library's `CLAUDE.md` were largely written by Claude on its own initiative. Where the two conflict, the design document wins.

**Why:** evennia-equipment's principle 6 ("a name is resolved against what the wearer holds") had `wear()`/`remove()` resolve names and refuse inside the execution method — the opposite of design principle 6 ("commands decide, then execute"), and it went unchallenged because it read as authoritative (2026-09-29).

**How to apply:** check `design/design-principles.md` before relying on or citing a library's own principles. When a library principle conflicts with it, say so and treat the library's as the thing to change. Related: [[feedback-use-library-tooling]].
