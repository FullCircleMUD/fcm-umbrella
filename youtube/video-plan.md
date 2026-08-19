# Video plan — the first ten

A rough running order for review. Nothing locked in; the order and the contents both move as we learn
what works. Feature IDs refer to [feature-inventory.md](feature-inventory.md).

This doubles as the **register**: as videos publish, add the URL and the date so later videos know what
to link a card to.

**Every video** opens with the standard login sequence and goes in character before the demo — see
[CLAUDE.md § Standard opening](CLAUDE.md). Cards link back to the earlier video for anything we skip.

---

## Before video one — preparatory work

Work items, not videos. These come first.

### P1 — Set up the channel

The channel exists but has never been used, so all of this is untouched. It is also permanent keyword
real estate, which takes pressure off every individual title.

- Channel name and handle.
- Banner.
- About text — this is where the full keyword phrase lives, e.g. "Web3 MMORPG on the XRP Ledger".
- Channel trailer.
- **Thumbnail style, settled here rather than per video:** Tim's face, a game interface shot behind it,
  and a big bold heading. Getting a repeatable template out of this step means every later video just
  fills it in.
- Links out to the website and the Discord.

### P2 — Remove the EVE Online and Ultima references from the website

D5 in [feature-inventory.md](feature-inventory.md). Video one sends people to the site, so it has to be
right before then. Already on Tim's own checklist.

### P3 — Write the prepared comment statements

Drafts in [CLAUDE.md § Comments](CLAUDE.md), including the "can I make money?" answer. They need a
careful read before first use, since they are the compliance position in public.

### P4 — Measurement

**The measure is new players.** The game counts them already — every account is a linked wallet, so new
accounts and new characters are a number we can read straight out of the game. Nothing to build.

A million clicks and nobody plays is failure. One click and one person plays is success.

Clicks are **diagnostic only**, and optional: a separate Discord invite per video (Discord counts the
uses itself) and a tagged website link. Their one job is to show *where* the funnel leaks — plenty of
clicks and no players means the landing path is broken, not the video.

Thirty seconds per video, and none of it holds up recording.

---

## 1 — First look: sign in, make a character, learn the ropes

- **Covers:** A1, A2 (wallet sign-in, wallet = account), C1 (chargen), C12 (tutorial).
- **The hook:** no password, no email — you sign with your wallet and you are in.
- **Cards:** none, this is the root video.
- **Shorts:** signing in with Xaman · rolling a character · meeting Pip.
- **Note:** record the login carefully and unhurried. This take is the one we cut into the reusable
  intro clip.
- **Published:** —

## 2 — Staying alive: water, bread, and a live economy

- **Covers:** C8 (hunger), C7 (wheat → flour → bread), C9 (harvesting), A6 and A7 (AMM pricing, gold as
  the bridge currency).
- **The hook:** the shop price is not a number Tim typed. Buy a canteen and the price comes from an XRPL
  AMM. If everyone buys canteens and nobody crafts them, the price climbs. If crafters flood the market,
  it floors out and making canteens stops paying. A real market, not a price list.
- **Cards:** video 1 (character creation and tutorial).
- **Shorts:** why bread matters · milling wheat · the AMM explained in 60 seconds.
- **Note:** the tutorial rewards may already supply the wheat and wood, so the whole chain can run
  without shopping first. Worth checking before recording.
- **Published:** —

## 3 — Gearing up and taking the first quests

- **Covers:** C6 (quests), C1/C2 lightly (gear from the shop), B5 (quest-aware NPCs).
- **The hook:** spend what you earned in video 2 on gear you actually need, then take work from the
  noticeboard.
- **Cards:** video 2 (how the money was earned).
- **Shorts:** the noticeboard · first quest complete · buying your first weapon.
- **Published:** —

## 4 — It is actually on the ledger

- **Covers:** A3 (items and tokens exist on-ledger), A9 (published issuing addresses), A10 (the "is this
  an investment" answer), A4/A5 in the future tense.
- **The hook:** the flagship video for the primary audience. Show the gold and the item, then open an
  explorer and show them on the XRP Ledger. The issuing addresses are published, so viewers can check it
  themselves rather than take our word.
- **The demo that proves it, and works with export switched off:**
  1. Outside the game, in a public explorer (XRPScan or similar), inspect the **game wallet** — this
     much wheat, this much gold.
  2. Inspect the **AMM pool** — this much wheat, this much gold.
  3. Go into the game and trade wheat for gold.
  4. Go back to the explorer and refresh. The game wallet holds different amounts. The pool holds
     different amounts.

  Nothing is asserted. The viewer watches an in-game action change public ledger state, in real time, on
  infrastructure we do not control. This is the single most convincing thing we can show the XRPL
  audience, and it needs no import or export.
- **Practical:** trade a large enough amount that the numbers visibly move, and prefer an explorer the
  audience already trusts over anything of ours.
- **Must be precise:** the tokens exist and are held by the game wallet. Export to a personal wallet is
  built and tested but switched off until beta — "you will be able to". The NFT metadata API is not up
  yet, so do not imply a marketplace will render the item nicely.
- **Cards:** video 2 (the AMM economy).
- **Shorts:** find your sword on the ledger · no, this is not an investment · what happens at beta.
- **Published:** —

## 5 — Combat

- **Covers:** C2 (real-time combat), C3 (gear effects firing), C4 (weapon mastery).
- **The hook:** it reads fast and it hits. "Milty's Defender's Helm deflects the critical blow!"
- **Cards:** video 3 (where the gear came from).
- **Shorts:** a critical kill · what a helm actually does · stances and riposte.
- **Watch out:** D1 and D2 in the inventory — phantom mobs and combat not starting when you are attacked.
  Route around them or fix first.
- **Published:** —

## 6 — The NPCs are not scripted

- **Covers:** B1, B2, B3, B4 (unscripted dialogue, memory, scope-gated lore).
- **The hook:** the widest-reaching video in the plan. Ask the barman how the town was founded, then ask
  the archmage. Same lore, different access, different voice. Then ask the barman a guild secret and
  watch him deflect. Then come back later and he remembers you.
- **Cards:** video 1 (meeting the first NPCs).
- **Shorts:** the barman remembers me · same question, two NPCs · asking for a secret he should not know.
- **Note:** do not promise bosses that learn from past fights (B6) — not built yet. Fine to say planned.
- **Published:** —

## 7 — Guilds, classes and training

- **Covers:** C6 (guild initiations), E2 (playing a class), C4 (training mastery), E5 (multiclassing —
  working now, show it).
- **The hook:** join a guild by passing its initiation, then train. The guildmasters are LLM-driven, so
  this is an AI demo wearing a progression hat.
- **Cards:** video 5 (combat), video 6 (the AI layer).
- **Shorts:** one per class · the initiation quest · what mastery changes.
- **Published:** —

## 8 — Crafting a sword, end to end

- **Covers:** E1 (craft path), C7 (chains), A6 (sell it back into the market).
- **The hook:** ore out of the mine, ingot at the smelter, sword at the forge, then sell it and watch
  what that does to the price. Closes the loop opened in video 2.
- **Cards:** video 2 (the economy), video 5 (combat, for what the sword is for).
- **Shorts:** one per step of the chain.
- **Published:** —

## 9 — Into the mine

- **Covers:** C5 (the kobold mine), C11 (darkness and light), C2 (combat at pressure).
- **The hook:** a real dungeon crawl with a boss at the end. Dark rooms, a light source, a kobold pack.
- **Cards:** video 5 (combat), video 8 (the sword you are carrying).
- **Shorts:** going in without a light · the pack fight · the chieftain.
- **Published:** —

## 10 — Where this is going

- **Covers:** the roadmap. What is live, what is built but switched off until beta, what is planned.
- **The hook:** the honest state of a hobbyist project, plus the invitation. Heaviest call to action of
  the ten: come play, join the Discord, tell us what breaks.
- **Cards:** whichever videos cover the features mentioned.
- **Shorts:** what beta unlocks · the one feature I am most excited about.
- **Published:** —

---

## Later: how we make a market for NFTs

A technical explainer, for once the basics are out. Squarely on-niche for the XRPL audience.

**The content:**

- Not every NFT has a market. The powerful, high-level items must be found or crafted in the game — you
  cannot buy them. That is deliberate.
- A good share of the low-level gear, the things you need to get going through roughly the first ten
  levels, you *can* buy from shop NPCs. Those are real markets on AMMs, exactly like wheat.
- The technical question the video answers: **how do you make an AMM market for commodity NFTs?**
- The answer is a **closed-loop proxy system**. The NFT already sits in the game wallet. Behind the
  shop counter, a proxy token for that item is paired against a proxy gold token in an AMM. When you buy
  the sword, the existing NFT is assigned to your account, and the proxy trade happens in the back end
  so the price stays a market price.
- The proxy tokens never leave the game environment and cannot be exported. Their only job is to carry
  supply and demand. Buy enough swords and the pool runs short, so the price of swords rises. A true
  market dynamic, run on the back end.

**The framing line, using both words:** *"How do we make an NFT interchangeable with a fungible issued
asset?"* That is the question an XRPL audience will actually want answered, and it uses their vocabulary
correctly — the NFT is not fungible, but it is made interchangeable, and it is traded against a fungible
issued token.

**The second half of the video — how the NFTs stay interchangeable.** An AMM market only works if every
unit is the same. But items take damage and degrade with use, so two swords are not in the same
condition. The fix sits with the shopkeepers: they only accept **fully repaired** NFTs into the AMM
markets. Every item bought or sold is therefore in identical condition, so the market treats them as
interchangeable. Worn gear has to be repaired before it can be sold.

**Before recording:** [docs/design-overview.md](../docs/design-overview.md) § NFT Item Flow describes
this as the Tracker Token AMM and marks it **not yet built**. Check whether that is still current. If it
is, this is a "here is how it will work" explainer, not a demo — which is fine, as long as we say so.

## Later: damage, degradation and repair

A separate gameplay video, and a natural partner to the one above.

- Weapons and armour take damage and degrade as you use them.
- Repair costs gold, so it is one of the ways gold leaves the economy.
- It also gates selling: gear has to be fully repaired before a shopkeeper will take it, which is what
  keeps the NFT markets interchangeable.

Good standalone video, and it sets up the market explainer if we publish this one first.

## Deliberately held back

Not in the first ten, so there is material for videos 11 and beyond: procedural dungeons (C10, and see
D3), pets and mounts (C13, E7), travel and cartography (E6), spell and skill spotlights (E3), strategy
videos (E4), remort (C15), languages (B7), and the deeper economy story (A8).
