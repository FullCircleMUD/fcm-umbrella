---
name: cosigner-push-auto-deploys
description: "Pushing utilities/cosigner redeploys the live mainnet cosigner (tx.fcmud.world) — the CLAUDE.md \"pushing needs no approval\" premise does not hold there"
metadata:
  node_type: memory
  type: project
  originSessionId: 9fc032d4-d4f0-4ae0-93e2-c6e4aff205c0
  modified: 2026-10-11T02:06:55.324Z
---

A push to `utilities/cosigner` triggers an automatic redeploy of the live cosigner at `tx.fcmud.world` (Tim, 2026-10-10).

**Why:** CLAUDE.md's "pushing needs no approval" rests on nothing deploying automatically; the cosigner is the exception.

**How to apply:** never push the cosigner without Tim's explicit go for that push. Any `wallets.json` or env change the new code needs goes onto the service first — Tim uploads it, then the commit and push. See [[xrpl-testing-runs-on-mainnet]].
