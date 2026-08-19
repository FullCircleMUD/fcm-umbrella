# CLAUDE.md — YouTube

Working context for the FCM YouTube effort: videos to promote the game and bring in players.

Always launch from the umbrella repo (`/Users/timbaird/Documents/fcm-umbrella`), as with all FCM work,
so the umbrella `CLAUDE.md` and `MEMORY` stay authoritative. This file loads on top of that when work
touches this folder.

## Purpose of the channel

The channel exists to **promote FullCircleMUD and attract players to the game**. Full stop. That is the
only purpose. Judge every idea against it.

## Who the channel is aimed at

What we want is **passionate communities** — people who, when something touches their area of passion,
will go and try it, and can get hooked. Reach matters less than that.

**The channel targets one niche: the XRPL community, with web3 gamers alongside it.** Both the channel
and the videos point at that group. Trying to be everything to everyone ends up being nothing to no one,
so we do not split the channel's identity across audiences.

- **XRPL community** — interested because the game runs on the XRP Ledger. A tight, die-hard community,
  and a large one on YouTube.
- **Wider web3 gamers** — interested because they like web3 games, not because of XRPL specifically. Not
  the same group, but a real presence on YouTube and reached through similar keywords and titles.

**Other communities we know exist but are not chasing.** They are not ruled out, and some will find us
anyway. Chasing them turns marketing into a full-time job, and the time is needed for development.

- Text-game people: 90s MUD nostalgia, current MUD players (Reddit, Discord, MUD listing sites), and
  adjacent genres — interactive fiction, roguelikes, terminal games.
- Indie devlog viewers — people who watch "building my game" videos. The video format suits them:
  feature walkthroughs and demonstrations rather than raw gameplay.
- AI / LLM interested people — the game leans on LLMs and vector memory.
- Tabletop RPG players — comfortable with text and imagination, but a weaker fit; they play with
  friends, not alone.

## Starting position

- **The channel already exists** — Tim's long-held YouTube account, never used, no videos on it. We
  repurpose it rather than create a new one.
- **A Discord server already exists** for FullCircleMUD.
- **No players yet.** The game has not been advertised or publicised.
- **The game is pre-alpha and buggy**, but recently reached the point where enough features are visible
  and it is playable enough for people to come in and look around.

### How a new player connects

This is settled. Details in [docs/connection-transport.md](../docs/connection-transport.md) and
[docs/website.md](../docs/website.md). The short version, which is what a video has to explain:

1. The main game domain points to a holding site that says we are in pre-alpha, and carries a button
   through to the **staging** instance. The live instance is not playable yet.
2. Staging serves a **web client** in the browser. We do not ship a MUD client. The interface protocol
   is specified and documented on the website, so anyone who wants to build or adapt one can.
3. On the web client entry screen the player types `connect`.
4. That returns a link and QR code for the **Xaman** (XUMM) wallet. The player scans it in Xaman and
   signs. It is a **signature only, not a transaction** — it proves they own that wallet.
5. The account is linked to their public wallet address. The wallet is effectively the account's
   primary key. One account can hold up to four characters.

## On camera

Tim appears on camera. A text format is not visually engaging, so a face to attach to the voice helps.

- Current working decision: a small camera box in a screen corner, away from where most of the text sits.
- Open to refining the placement and size once we see a real recording.

## Distribution

- Shorts go on YouTube first.
- The same media suits Reels, Instagram, and Facebook, so reuse it in several places.
- Prefer automating the cross-posting through **GoHighLevel**, which already publishes Tim's other,
  unrelated socials.

## Effort budget

Record a video every few days to once a week, cut shorts from it, publish, done. Development gets the
rest of the time. Any proposal that grows into a full-time marketing job is out of scope.

## Video format

The current working format:

- **Long form.** Tim records himself playing the game and talking through what he is doing, and
  demonstrates features as he goes. Target length under ten minutes.
- **A run sheet, not a full script.** Before recording, list the features to demonstrate in that video.
- **Shorts come out of the long form.** One long form video covers several features; each feature
  becomes a short. Every short links back to the long form video.
- **Plan the shorts crop before recording.** Shorts are vertical; a wide terminal does not crop to fit.
  Decide the layout at capture time.

### Standard opening — every video

Every video starts the same way, about thirty seconds:

0. A brief intro, then the **disclaimer card** on screen — see below. This comes before anything else.
1. Type `connect`. The QR code appears on screen.
2. Sign in the Xaman wallet. The phone is not on screen, so narrate it: "I'm signing on my Xaman wallet
   now… that's signed." The viewer sees the screen react.
3. Enter the game, then `ic` from the main menu.
4. Then the demonstration for that video.

**Why:** whichever video someone lands on first, they get the full web3 context up front. No video
assumes the viewer has seen another one.

Call it a **signature**, not a transaction — that distinction is the compliance point, and it is also
the more impressive fact: no payment, no gas, just proof you own the wallet.

`[Open: whether this becomes a pre-rendered standard intro clip dropped on the front of every video, or
is recorded fresh each time. A fixed clip is less work; a live one is less repetitive for returning
viewers.]`

### On-screen readability

It is a text game, so the text must be readable on a phone.

- Record zoomed in by default.
- Change the zoom during the recording to suit each shot — how much has to fit on screen depends on
  what is being demonstrated.
- Treat zoom as an active choice per shot, not a set-and-forget setting.

## Framing and expectations

We do not wait for the game to reach some standard before publishing — that costs months of exposure
and growth. Instead we set the expectation up front:

- an enthusiast and hobbyist developer building this alone,
- pre-alpha, acknowledged as buggy,
- fundamentally playable, with the major features there to see.

Framed that way, a rough game does not burn people. Framed as a professional studio's best work, it
would.

**Planned is fine; done is a claim.** We can talk about what we intend to build — "we plan to make pets
exportable, we have not done it yet" — and that suits the hobbyist framing well. What we must never do
is present a planned feature as if it already works. Say which it is, every time.

There are three states, and each gets different words on camera:

- **Working now** — show it. "You can."
- **Built and tested, but switched off** — import and export are the case here. Disabled through
  pre-alpha and alpha, largely for regulatory reasons and partly because the game is still buggy, and
  switched on at beta. Say **"you will be able to"**, not "you can".
- **Planned, not built** — say so plainly, in the future tense.

## This is not a play-to-earn game

The hardest rule on the channel. It is regulatory, not stylistic. Full detail in
[docs/compliance.md](../docs/compliance.md) and `ops/COMPLIANCE_LEGAL.md` §18.1.1.

- **Never say** "play to earn", "play and earn", or "P2E" — except inside the disclaimer, where we name
  the category in order to deny it.
- **The proximity rule:** the words "play" and "earn" never appear in the same sentence or the same
  paragraph. Not in a title, not in a description, not in a tag, not spoken on camera. Proximity alone
  creates the implication.
- Say tokens are obtained **"through gameplay"** or **"by playing"**, never "earned by playing".
- **We do not sell tokens.** Gameplay is the only way to get them.
- **We do not redeem** game gold or any game asset for anything of value outside the game — no fiat, no
  stablecoins, no XRP.

**What the XRP Ledger is actually for, and this is the line to use on camera:** two things — **market
pricing** for the in-game economy through AMM pools, and **personal ownership** of in-game assets,
including the ability to trade them outside the game.

**On people making money — say this accurately.** If the game is good and enough people play it and
value its items, some people may in fact make money trading them. That happens in an open market we do
not control. We do not claim it is impossible; that would be false. What we say is that we make **no
representation** about it, and that we do not endorse, promote or facilitate it. It has nothing to do
with us.

So the phrasing is always about **us**, never about what is possible:

- ✅ "We make no representation that you can or will make money from this game."
- ❌ "You cannot make money from this game."

### When someone else calls us play-to-earn

**"We" is the game, Tim, board members, anyone representing FullCircleMUD, and any AI assistant writing
material for it.** None of us ever use that framing.

Other content makers might. If the channel grows, someone will publish a video calling FCM play-to-earn.
We cannot stop that, and if their video sends us players, that is outside our control too.

**We do not go looking, and we do not go arguing.** No monitoring, no hunting for those videos, no
rebuttals in other people's comment sections. What they publish is their business.

**If we are asked directly** — a comment, an interview, a Discord question, anyone pointing at someone
else's video and asking us about it — we answer clearly:

> It is very clear in our project documentation, very clear in our terms and conditions, and very clear
> in everything we have published, that FullCircleMUD is not play-to-earn. We do not claim to be
> play-to-earn. We do not claim that you can make money playing our game.

Full stop. That is the end of what we do.

That answer only works if the published record backs it up, which is the real reason the language rules
above are absolute.

### When someone asks us whether people are making money

Same shape of answer — reactive, and it moves the activity outside us:

> That is the free market, and it is outside our control. We do not redeem game assets for anything of
> external value. We do not claim, or offer, or tell anyone that they can make money from this game. If
> that is happening, it is completely external to us — a free market mechanism we have no part in.

Note what this does **not** say: it does not deny that anyone is making money. We do not know and we do
not control it, so denying it would be a claim we cannot stand behind. We put it outside us instead.
That is both true and defensible.

### Keywords

**We never chase the play-to-earn keywords.** Even if a keyword tool shows the traffic is there, the
play-to-earn terms stay out of our titles, descriptions, tags and hashtags. Being found because someone
else mislabelled us is not in our control. Going looking for that traffic is a choice, and the answer
is no.

### The disclaimer card — on screen in every video

After the brief intro and before the content, a written card goes on screen and is held long enough to
read comfortably — a good couple of seconds at minimum, and longer if the wording is long.

Draft wording, for review:

> **Please read.**
>
> FullCircleMUD is a game. It is **not** a play-to-earn game.
>
> We make no representation that you can or will make money from this game.
>
> We do not sell tokens. The only way to get them is through gameplay.
>
> We do not exchange game gold or game items for money, stablecoins, XRP, or anything else of value
> outside the game.
>
> What other people do in an open market is outside our control, and is not endorsed or promoted by us.
>
> FullCircleMUD is free to play during pre-alpha. At a more developed stage it will move to a monthly
> subscription.

`[TBD — counsel has not reviewed this wording. Get it checked before video one publishes.]`

`[TBD — whether the card is silent text on screen or is also read aloud. Read aloud is stronger, since
it survives someone listening rather than watching, but it costs time at the front of every video.]`

## "Is this an investment?" — the on-camera answer

**No.** The position is already set in [docs/compliance.md](../docs/compliance.md), with the full
strategy and language policy in `ops/COMPLIANCE_LEGAL.md`. Follow those. In video terms:

- We do not sell tokens. We do not guarantee the value of tokens. It is not an investment.
- It is a game. What you earn or make in the game — gold, wheat, bread, swords, armour — can be
  exported out of the game environment and traded on separate markets if that is what you want.
- We seed AMMs **between game assets only** — every game asset paired against game gold. A player can
  hold those in their own wallet and trade at the AMM outside the game.
- **Why gold:** gold is the game's bridge currency, and the game itself is a client of those AMMs. We do
  not set prices — the pools do, so supply and demand are real. A player who crafts a sword but wants a
  potion sells the sword for gold and buys the potion with gold, through the AMMs on the XRPL.
- We do **not** seed any game asset against anything of external value — no RLUSD, no stablecoins, no
  XRP. We do not redeem game gold for anything of external value.
- If someone outside our control pairs a game asset with external value, that is outside our control.
  We do not ask for it, we do not do it, and we do not make that market.

This wording is regulatory, not stylistic. Do not loosen it for a punchier line.

## Call to action

At the end of every video, in substance:

> We would love you to come and check it out. We are in pre-alpha, so we are a bit buggy, but we are
> playable. Come check us out, join the Discord, and let us know what you think.

## What success means

**Growth, not a target number.** People trying the game, joining the Discord, getting involved in the
community — and in time, developers contributing to the project. Views are not the measure.

Whatever the current numbers are, **the goal of the next video is to increase them.** The campaign
succeeds if players, Discord members and contributors grow over time, even gradually. There is no
threshold to hit and no deadline to miss.

**The measure is people playing, not people clicking.** A million clicks and nobody plays is failure.
One click and one person plays is success. The game already counts this — every account is a linked
wallet, so new accounts and characters are readable straight from the game.

Views, clicks and click-through rates are diagnostic only. They tell us *where* the funnel leaks when
the player number does not move. They are never the score.

This will be revised as we learn what the numbers actually look like.

## Comments

### How often we look

- Review comments every day or two as a matter of routine.
- Watch more closely in the hour or two after a video goes out, when engagement is highest and the
  first questions land.

### Prepared statements

Some questions will come up on every video, and the compliance ones need a consistent answer rather than
whatever gets typed in the moment. Keep prepared statements and reuse them.

**"Can I make money from this?"** — draft, for careful review:

> FullCircleMUD is not a play-to-earn game. We do not represent that you can make money from it, and we
> do not redeem game assets for anything of external value. When the game reaches beta you will be able
> to export your assets to the chain. What you choose to do with them after that happens outside the
> game, and it is not something we control, endorse or take part in.

`[TBD — this wording needs a careful read before it goes into use. It is the compliance position in
public, so it gets the same care as the on-screen disclaimer card.]`

The two reactive answers above — for someone else calling us play-to-earn, and for people making money
— belong in the same set. See [§ When someone else calls us play-to-earn](CLAUDE.md).

`[TBD — other recurring questions worth a prepared answer are not listed yet. Add them as they show up.]`

## Cards link the videos together

Use YouTube cards to point at the video that covers a step we are skipping past.

Example: in video five Tim goes in character as Milty, a level three warrior, and says "if you want to
see how to create a character, there's a card in the top right that links to that video." Character
creation was covered in an earlier video, so we do not repeat it — we link it.

- Each video can then stay on one topic and stay short.
- Later videos build on earlier ones without re-explaining them.
- It needs a register of which video covers which feature, kept as we publish, so we know what to link.

## Series plan before video one

We do not pick video one in isolation. Plan a series first:

- Work out which features go in which video.
- Give each video a good mix of different things of interest.
- Do not spend all the best material on video one — keep enough to keep publishing.
- Features can be presented as newly developed and introduced, which suits an ongoing series.

`[TBD — the series plan itself is not written yet.]`

## Where the marketing actually happens

Getting the right people to click. That means:

- keywords,
- title,
- description,
- thumbnail.

The video shows what we are doing; these four decide who ever sees it.

## Nothing here is locked in

Everything recorded in this folder is a **current working decision**. It is never a final, locked-in,
immutable decision.

- A brainstorm is a brainstorm. Write it down as an idea under discussion, not as a settled outcome.
- Any working decision can be changed by the human user after discussion.
- Do not use language like "final", "locked in", "canonical", or "decided" for anything here.
- When you record something, make it clear what stage it is at: idea, under discussion, or current
  working decision.

### The one exception — regulatory and compliance rules

**Compliance rules are the only thing here that is written as a hard rule, and Tim has approved that
framing.** They use "never", "always", "no exceptions" language deliberately, because they are not
preferences to be optimised against.

This covers the play-to-earn position above and everything connected to it — no token sales, no
redemption, no representation that a player can or will make money — along with anything else flowing
from [docs/compliance.md](../docs/compliance.md) and `ops/COMPLIANCE_LEGAL.md`.

Everything else on this channel stays a current working decision.

So: do **not** soften compliance wording to match the flexible tone of the rest of the folder, and do
**not** borrow compliance's absolute tone for a marketing preference. Creative and marketing choices
bend; regulatory ones do not.
