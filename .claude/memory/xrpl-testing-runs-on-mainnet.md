---
name: xrpl-testing-runs-on-mainnet
description: Current practice — XRPL live testing and staging run on mainnet; the cosigner is configured for mainnet only
metadata:
  node_type: memory
  type: project
  originSessionId: 9fc032d4-d4f0-4ae0-93e2-c6e4aff205c0
  modified: 2026-10-08T15:03:12.414Z
---

Current practice (2026-10-08): live XRPL testing, staging included, runs on mainnet, not testnet. The deployed cosigner's `wallets.json` holds mainnet wallets only.

**Why:** testnet is reset from time to time, which wipes the fungibles and account setup the game needs to run.

**How to apply:** plan live tests (e.g. fcm-xrpl Phase 8) against mainnet; don't propose a testnet cosigner entry or testnet staging unless Tim reopens it.
