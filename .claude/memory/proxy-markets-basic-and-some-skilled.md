---
name: proxy-markets-basic-and-some-skilled
description: Game-provided proxy markets (tracking_token on an item type) are for BASIC and some SKILLED items only; higher items are player-traded
metadata:
  node_type: memory
  type: project
  originSessionId: 4acb35c5-d885-499b-bd6c-bd5b438c62c8
  modified: 2026-10-04T01:25:38.118Z
---

The current practice (Tim, 2026-10-03): the game provides AMM proxy markets — an item type's
`tracking_token` in the XRPL seed — only for BASIC items and some SKILLED ones. From part of SKILLED
up through EXPERT and above, items are traded between players only, so they carry no proxy token.

**Why:** the game's own markets cover the entry economy; above it, trade is player-led
([[player-led-economy-everything-crafted]]).

**How to apply:** a new EXPERT-or-higher item's seed row gets no `tracking_token`. Which SKILLED items
keep one is `[TBD — needs discussion: which SKILLED items get a proxy market]`. The working list is
`ops/scratch/proxy-token-inventory-2026-10-03.md` while it exists.
