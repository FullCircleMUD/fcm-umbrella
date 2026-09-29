---
name: router-tests-use-settings-router
description: "Run src/router tests with --settings settings_router.py; settings.py is Evennia's stock file and fails every EvenniaTest on the Account typeclass"
metadata:
  node_type: memory
  type: reference
  originSessionId: 329ea1b4-1469-4c2c-aa46-12816f64fcef
  modified: 2026-09-26T12:12:44.637Z
---

From `src/router`: `../venv/bin/evennia test --settings settings_router.py <label>`.

`server/conf/settings.py` is the stock Evennia file. Under it every `EvenniaTest` errors in `setUp` with an empty `ImportError` for `typeclasses.accounts.Account` — the real class is `typeclasses.accounts.accounts.Account`, set in `settings_common.py`, which `settings_router.py` imports.

Related: [[feedback_targeted_tests_during_dev]].
