---
name: libraries-installed-editable-until-beta
description: Libraries are editable-installed from checkouts on localhost and staging; publishing to any pip provider (PyPI included) is deferred until close to beta
metadata: 
  node_type: memory
  type: project
  originSessionId: 3060eb0d-a2db-4fc3-b557-3730a2f55dea
  modified: 2026-09-14T00:07:34.557Z
---

**Current plan as at 2026-09-13**, open to review like any other. Every library in `libraries/` is
consumed as a **local editable install** until the game is close to beta.

- **Localhost rebuild** — editable installs from the checkouts in `libraries/`.
- **Staging** — clone every library down and editable-install those too, so a bug found in testing or
  a refactor the game needs can be made and picked up immediately, with no publish step in between.
- **Production** — the first deployment that installs from a published package. Not before.

PyPI is included in the deferral: no library is mature enough to avoid several more versions, and
republishing on each would cost more than it buys.

**So a library's `installing.md` naming no pip provider is deferred on purpose, not an oversight.**
`fcm-subscriptions` and `fcm-xrpl` both carry a `[TBD]` for the install line; leave them until the
provider question is actually taken up near beta.

Relates to [[rebuild-not-retrofit]] — the rebuilt game is the consumer doing the installing.
