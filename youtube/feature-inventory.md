# Feature inventory — raw material for the video series

A first pass at everything FCM could show on camera, for Tim to review. Nothing here is decided. This
is a menu, not a plan; the series plan comes after.

**How the readiness column was set:** from the design docs in [docs/](../docs/INDEX.md) and the
2026-08-16 play-test notes. Nothing here was verified by running the game. Treat every "unverified" as
a question for Tim, not a claim.

- **Live** — seen working, or documented as built and live.
- **Built, unverified** — the docs describe it as built; I have not confirmed it runs on staging.
- **Not built** — the docs say the code is not there yet. Do not put it in a video as if it works.

Audience column: **XRPL** = the primary niche, **W3G** = web3 gamers, **All** = works for anyone.

---

## A. Ownership and the chain — the XRPL hook

This is the block that speaks directly to the primary audience. It is also the hardest to show, because
most of it is state rather than action.

| # | Feature | What a viewer sees | Ready | Audience |
|---|---|---|---|---|
| A1 | **Xaman wallet sign-in** | Type `connect`, get a QR code, scan in Xaman, sign, you are in. A signature, not a transaction — no gas, no payment. | Live | XRPL |
| A2 | **The wallet is the account** | One wallet, one account, up to four characters. No password, no email. | Live | XRPL |
| A3 | **Items are real NFTs** | Loot a sword, then look it up on an XRPL explorer. The thing in your inventory exists on-ledger, and you can look it up right now. | Live — **and demo-able today.** All tokens and NFTs already exist on the ledger; they are held by the game wallet until export is enabled. Enough supply is minted for early demand, and more gets minted as the game grows. The issuing addresses are published on the website, so a viewer can verify it themselves. What waits for beta is only the move from the game wallet to a personal wallet. | XRPL, W3G |
| A4 | **Export to your own wallet** | `deposit` at the bank, `export` from OOC, sign in Xaman, and the item is in your wallet outside the game. | **Disabled in pre-alpha and alpha** — see the note below. Talk about it in the future tense. | XRPL, W3G |
| A5 | **Import back in** | The reverse trip: an asset in your wallet becomes usable in the game. | **Disabled in pre-alpha and alpha** — same as A4. | XRPL, W3G |
| A6 | **AMM-set prices** | Prices in the shop are not numbers Tim typed. The game reads them from XRPL AMM pools. Craft a sword you don't want, sell it for gold, buy the potion you do want. | Built, unverified | XRPL, W3G |
| A7 | **Gold as the bridge currency** | Every game asset pairs against game gold. Explains why the economy has real supply and demand. | Built, unverified | XRPL |
| A8 | **The economy responds to itself** | When a resource gets scarce and its price rises, the world spawns more of it. Self-correcting supply. Hard to show live; better as a whiteboard-style explainer over gameplay. | Built, unverified | XRPL, W3G |
| A9 | **Transparency** | The treasury and the ledger are public. The issuing and wallet addresses are published on the website, so anyone can audit the supply themselves. | Live — addresses are published. (I have not checked what else the `transparency` repo publishes.) | XRPL |
| A10 | **The "is this an investment?" answer** | Not a feature, but it belongs in the series: no redemption, no external-value pairs, no market-making. See the compliance section in [CLAUDE.md](CLAUDE.md). | n/a | XRPL, W3G |

> **Import and export are built and tested, but switched off until beta.** The feature is complete — it
> is disabled deliberately, largely for regulatory reasons and partly because the game is still buggy at
> this stage. It gets switched on when the game reaches beta. So on camera the accurate phrasing is
> **"you will be able to import and export"**, never "you can". This applies to A4 and A5, and to
> anything else that leans on assets leaving the game — including exportable pets (C13, E7).

> **NFT metadata is not served yet.** An NFT carries a URI, and a wallet or marketplace has to call that
> API to show the name, picture and stats. This is normal for NFTs — but **our NFT API is not stood up**,
> and the current plan is to stand it up at beta. So on camera: the NFT exists on the ledger and can be
> verified, but do not imply it will render nicely in a marketplace yet. Be precise about the difference
> between the token existing and its metadata resolving.
>
> `[TBD — Tim is reconsidering whether to stand the NFT API up during pre-alpha/alpha and switch the
> endpoint at beta, rather than waiting.]`

---

## B. The AI layer — the strongest "you have not seen this before" material

Secondary audience on paper, but this is the most video-friendly content in the whole game. It is
visual in a text medium, because it *is* text.

| # | Feature | What a viewer sees | Ready | Audience |
|---|---|---|---|---|
| B1 | **NPCs talk back, unscripted** | Say anything to Rowan the barman and get a real answer, in character. | Live | All |
| B2 | **NPCs remember you** | Come back later and Rowan recalls what you asked and what you bought. | Live | All |
| B3 | **Same question, different NPC, different answer** | Ask the barman how Millholm was founded, then ask the archmage. Same lore base, different access, different voice. A very strong 60-second short. | Live | All |
| B4 | **NPCs know only what they should** | Ask the barman a guild secret and he deflects, because the lore is scope-tagged. | Live | All |
| B5 | **Quest-aware NPCs** | Rowan changes what he pitches based on where you are in the game. | Live | All |
| B6 | **Bosses that learn from past fights** | Lose to a boss twice and the third fight opens differently. | **Not built** — the strategy bot, post-combat summariser and approach triggers are not written. Good "coming soon", not a demo. | All |
| B7 | **Languages and garbled speech** | Speech you do not know the language of arrives garbled. | Built, unverified | All |

---

## C. The game itself — proof it is a real game, not a demo

| # | Feature | What a viewer sees | Ready | Audience |
|---|---|---|---|---|
| C1 | **Character creation** | Race, class, 27-point buy, starting skills. | Built, unverified | All |
| C2 | **Real-time combat** | Swings, misses, grazes, crits, kills. Reads fast and looks alive on screen. | Live | All |
| C3 | **Gear that does something** | "Milty's Defender's Helm deflects the critical blow!" — equipment firing its own effects mid-fight. | Live | All |
| C4 | **Weapon mastery** | The same weapon hits harder as your mastery tier climbs. | Built, unverified | All |
| C5 | **The kobold mine** | Descend into a dark mine, fight a pack, work toward the Chieftain. | Live (with known bugs — see D) | All |
| C6 | **Quests** | The rat cellar, and the four guild initiations. | Built, unverified | All |
| C7 | **Crafting chains** | Wheat → flour → bread. Ore → ingot → sword. Ties straight back to A6. | Built, unverified | All |
| C8 | **Hunger** | You have to eat. Bread costs 5–6 gold, and that price anchors the whole economy. | Built, unverified | All |
| C9 | **Harvesting** | Mine ore, farm wheat, gather arcane dust in the faerie hollow. | Built, unverified | All |
| C10 | **Procedural dungeons** | A dungeon generated per run rather than hand-built. | Built, but see D3 | All |
| C11 | **Weather and darkness** | Rain starts, rooms go dark, you need a light source. Cheap atmosphere, good for shorts. | Live | All |
| C12 | **The tutorial** | Pip walks a new player through their first moves. | Live | All |
| C13 | **Pets and mounts** | Persistent pets, familiars, taming. | Live — pets exist in the game (confirmed by Tim). Whether a pet is an exportable NFT is **not yet validated** — on Tim's backlog. | All |
| C14 | **Travel and cartography** | Zone-to-zone travel, mapping districts, map NFTs. | Unverified — design doc exists, build state unknown. | All |
| C15 | **Remort** | Reset at level 40 and keep the advantages. | Unverified — and only relevant much later. | All |

---

## D. Known rough edges — do not put these on camera yet

From the 2026-08-16 play-test notes. Being pre-alpha is fine and we say so, but a bug that ruins a take
is worth routing around.

| # | Problem | Effect on a recording |
|---|---|---|
| D1 | Phantom mobs (room `contents_cache` drift, ~100 rooms) | Mobs that are not really there. Attacks fail on ghosts. Would confuse a viewer badly. |
| D2 | Being attacked does not always start combat (kobolds, crows) | You get hit and cannot fight back. Looks broken rather than rough. |
| D3 | Procedural dungeons dump you back to the inn mid-run | "Your current location has ceased to exist" — kills a dungeon video outright. |
| D4 | Item spawn appears to run at ~1 per hour | Nothing to loot when the camera is on. Plan the take, or fix first. |
| D5 | Website still references EVE Online and Ultima | If a video sends people to the site, this shows. Small fix, worth doing before video one. |

---

## E. Repeatable formats — one idea, many videos

These are not single features. Each is a template that yields a run of small videos, which is what keeps
a channel publishing without inventing something new every week.

| # | Format | The run of videos it gives | Ready | Audience |
|---|---|---|---|---|
| E1 | **How to craft X** | One per path: bread, a sword, a potion, an enchanted item, gem insetting. Each shows the full chain from raw resource to finished item. Naturally ties into the AMM story — you made a thing, now sell it. | Built, unverified | All, XRPL |
| E2 | **Playing a &lt;class&gt;** | One per class: warrior, thief, mage, cleric, paladin, bard. What the class does, how it feels, what its skills are. | Built, unverified — 6 classes exist; only Warrior, Thief, Mage and Cleric are joinable in Millholm. | All |
| E3 | **Spell and skill spotlights** | One per spell or skill. Short, self-contained, ideal shorts material. | Built, unverified | All |
| E4 | **Strategy and tactics** | How to fight with a given class, stances, parry and riposte, dual wield, how to survive the mine. | Built, unverified | All |
| E5 | **Multiclassing** | Joining a second guild, the initiation quest, how the levels stack. The guild initiations are themselves LLM-driven, so this doubles as an AI-layer demo. | Live — confirmed by Tim. Classes stack in `db.classes`, gated by race, alignment, remort and ability scores. | All |

| E6 | **Getting around** | Travelling between zones, `explore` / `travel` / `sail`, ship tiers, mapping a district, route and map NFTs. The map NFTs pull this back to the XRPL story. | Unverified — see C14. | All, XRPL |
| E7 | **Pets and mounts** | One per topic: how to get a pet, how to train it, how to ride a horse, familiars, stabling, taming. | Pets are live; see C13. On the chain hook, say what is true: exportable pets are **planned, not built yet**. Never state it as done. | All, XRPL |

Each of these also feeds the shorts pipeline cleanly: one long form video on a class, cut into a short
per spell.

The pattern under all of them is the same: **pick one thing, show it end to end, keep it short.** The
supply of these is effectively unlimited — every skill, spell, craft, class and system in the game is a
candidate.

## Patterns I noticed while listing these

Offered as observations for the series plan, not decisions.

- **The strongest openers pair an XRPL idea with a visible game moment.** "Kill a kobold, loot a sword,
  look it up on the ledger" is one video, one hook, and it is exactly our primary audience.
- **The AI NPC material is the most shareable but the least on-niche.** It will travel further on shorts
  than anything else here. Worth deciding whether we use it as reach bait that funnels back to the XRPL
  story, or keep it secondary.
- **Several of the best items are "built, unverified".** Before the series plan is worth much, someone
  has to walk the game and check what actually works today. That is a short session, not a project.
- **The economy is the deepest story and the hardest to film.** Prices, spawn rates, and supply are
  systems, not scenes. They probably need a different video format — narrated explainer over footage —
  rather than a live walkthrough.
