---
name: feedback-declare-test-databases-narrowly
description: "Test classes declare only the databases they use — start with none, add each alias the error names; never databases = \"__all__\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: 77286fbc-7cd6-43fc-ac32-acefcede90eb
  modified: 2026-10-07T19:32:49.430Z
---

A test class declares the databases it actually uses, not `databases = "__all__"`. Start with none, run it, add the alias the error names, and repeat until it runs.

**Why:** Django builds and migrates every database a run asks for, and with nine aliases that is about 15s+ per run on top of Evennia's ~15s boot — measured 2026-10-07. `"__all__"` also makes a test depend on databases it never touches, so a broken migration elsewhere (another session's XRPL schema) stops unrelated suites.

**How to apply:** for any test class written or touched. Getting it wrong is loud — Django raises naming the alias — so it costs one run per missing database. See [[feedback_targeted_tests_during_dev]].
