---
name: feedback-dont-design-around-legacy-bug-theories
description: "The rebuild is not shaped by unproven theories about legacy bugs (e.g. ghost mobs); design on merits, deal with a bug if it shows up in the rebuild"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 66e431a4-180f-4afc-93fd-e9a26d5cd9cf
  modified: 2026-10-19T09:47:46.359Z
---

Don't let a theory about a legacy bug drive rebuild design. Ghost mobs are the example: many legacy theories and fixes, none solved it, and it isn't known to exist in the rebuild.

**Why:** a fresh theory is no more trustworthy than the many that failed, and the rebuild may not have the problem at all.

**How to apply:** design each piece on its merits. If the bug appears in the rebuild, investigate it there. The legacy notes (`ops` history, `scratch/ghost-mob-diagnosis-2026-08-21.md` at `829932d`) are reference only. Related: [[feedback_cheap_tests_over_theory]], [[rebuild-not-retrofit]].
