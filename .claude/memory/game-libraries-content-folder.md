---
name: game-libraries-content-folder
description: Library-declared content in the game lives in src/router/libraries/<library-name>/ — one folder per library.
metadata: 
  node_type: memory
  type: project
  originSessionId: ec8709eb-feba-4e03-9ef4-988743d934bf
  modified: 2026-09-14T20:28:33.151Z
---

Content a library requires the game to declare — settings modules, data files, anything an install
step asks for — goes in `src/router/libraries/<library-name>/`, one folder per library.

**Why:** installs stay self-describing and reversible. What a library added is in one place, named
after it, instead of scattered through `world/`, `typeclasses/` and `server/conf/`.

**How to apply:** `src/router/libraries/` is *inside the game*, not the umbrella's own `libraries/`
directory of repo checkouts — always write the full path, since "the libraries folder" means two
different things in this workspace.
