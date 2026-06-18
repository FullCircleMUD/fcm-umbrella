---
name: git-crypt setup for src/game secrets
description: src/game encrypts server/conf/secret_settings.local with git-crypt (symmetric key, shared out-of-band). A fresh clone is locked; unlock with the key file before the game runs locally.
type: reference
---
The `src/game` repo uses **git-crypt** to encrypt secrets committed to the repo. Only one path is
encrypted, declared in `src/game/.gitattributes`:

- `server/conf/secret_settings.local` → `filter=git-crypt diff=git-crypt`

(Note: an unencrypted `server/conf/secret_settings.py.bak` also exists in the repo. It is **not a
secret** — it lists the field *names* that need to be set, with **no values** filled in (a template),
so it is not compromising. It is still deny-listed in permissions as a precaution. The active
encrypted file is the `.local` one, not `secret_settings.py`.)

**Key model:** symmetric **key file**, not GPG collaborators — there is no committed `.git-crypt/keys/`
directory. The same key is shared between the Mac and Windows dev machines and lives **outside any
repo** (home dir / password manager). It must never be committed.

**Why this matters for setup:** `git clone` brings git-crypt'd files down **encrypted**; git-crypt does
**not** auto-unlock. So any fresh clone of `src/game` (including the one inside the umbrella) has an
encrypted `secret_settings.local` and won't run locally until unlocked.

**How to apply — unlock a fresh clone (on any machine):**
1. Ensure `git-crypt` is installed (`brew install git-crypt` / `choco install git-crypt`).
2. Obtain the shared symmetric key file. To export it from an already-unlocked clone:
   `cd <unlocked>/src/game && git-crypt export-key <path-outside-repo>/fcm-game-gitcrypt.key`
3. Unlock the new clone: `cd <new>/src/game && git-crypt unlock <path>/fcm-game-gitcrypt.key`

**Security discipline:** never `git diff` the encrypted file before committing (exposes plaintext);
just stage and commit. See the Security Rules in [[MEMORY]]. This is also documented in the umbrella's
`docs/` new-machine setup guide.
