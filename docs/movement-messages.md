# Movement Messages

How the game tells a room that someone came or went. Every movement message — walking through an
exit, flying between rooms, changing height inside one — is emitted from a single seam so that the
callers who need silence can get it, and so that new movement modes are added as a rule rather than
as another parallel message source. For the exit classes themselves see
[exit-architecture.md](exit-architecture.md); for the height mechanics that decide the verb see
[vertical-movement.md](vertical-movement.md).

> **Not yet built.** Movement messages today come from two independent sources: Evennia's stock
> announce pair for every exit, plus a second pair emitted by `ExitDoor` for doors only, so a door
> traversal produces four messages instead of two. This document describes the intended design and
> the work to reach it.

## Why one seam

Evennia gates its own movement announcements on the `quiet` argument to `move_to()`: when a caller
passes `quiet=True`, `announce_move_from()` and `announce_move_to()` are skipped. Most game code
relies on this today — teleports, flee, dungeon transitions and the inventory paths overwhelmingly
move objects quietly and write their own text, because a bare "X is leaving here, heading for there"
is wrong for those cases. That is the state as it stands; the default below changes what a new or
revisited caller should do, without requiring every existing quiet caller to be touched at once.

Messages emitted anywhere else cannot be suppressed that way. `at_traverse()` and
`at_post_traverse()` on an exit fire regardless of `quiet`, so a message emitted there is
unconditional by construction — invisible to every caller that has already decided the move should
be silent. That is the defect behind the doubled door messages, and it is the reason **all** movement
messaging belongs in the two announce methods and nowhere else.

Putting it there also means one place decides wording. A verb table that lives in `announce_move_*`
serves walking, flying, swimming, mounted movement and whatever comes later; the same wording
appears whether the move came from an exit command, a follow cascade, or a flee.

**Default: every inter-room movement message goes through this seam.** A command with a distinctive
line — flee, retreat, a dungeon transition — passes its flavour in via `move_type` (and, where the
wording genuinely can't be expressed as a dispatch rule, a `msg=` override, which `move_to()`
already forwards to `announce_move_from()`/`announce_move_to()` as a `**kwargs` pass-through) rather
than writing its own `msg_contents()` call and silencing the seam with `quiet=True`. Bypassing the
seam is the exception, justified case by case, not the default — a caller that goes quiet is a
caller the system doesn't yet have a rule for, and that's a gap to close, not a permanent shape.
Teleport, give/get/drop and similar non-traversal moves are the clear exceptions, since they aren't
"arriving" or "leaving" in the sense this document describes at all.

This default is scoped to moves between rooms — anything that calls `move_to()` with a destination.
**Intra-room movement is not part of this seam and is out of scope by construction, not by
exception.** Climbing and flying/swimming up or down change height inside the current room: there is
no destination room, so `move_to()` is never called and `announce_move_from`/`announce_move_to`
never run. Those events message the room directly, the same way a door announces its own
opening — see Height changes inside a room below.

## What a movement message says

Two messages per traversal, one to each room, the mover excluded from both:

```
source room       Fred leaves north.
destination room  Fred arrives from the south.
```

Three things are deliberately absent.

**Room names.** "Fred is leaving The Harvest Moon, heading for Market Square - Northwest" tells
bystanders where someone is going, which they have no in-world way to know. It also degrades badly
where room names legitimately repeat — several adjacent rooms share the name `Old Trade Way West`,
and the stock message renders that as "leaving Old Trade Way West, heading for Old Trade Way West".

**Door names.** A door announces its own opening and closing; the movement message does not need to
repeat it. This also removes a naming inconsistency, because the two sides of a doorway are separate
objects with separate names — an observer would otherwise watch "a wooden door" open and then see
someone arrive through "a sturdy wooden door".

**Any hint of who can see it.** Visibility is handled upstream: `RoomBase.msg_contents()` filters
messages from hidden and invisible actors and muffles them for sleepers, provided `from_obj` is
passed. The announce methods pass it.

## Verb resolution

The verb comes from the mover's state at the time of the move, resolved from an ordered list of
rules checked highest-priority first, falling through to plain walking. Adding a movement mode means
appending a rule, not editing a conditional.

| Rule | Condition | Departure | Arrival |
|---|---|---|---|
| airborne | `room_vertical_position > 0` | `Fred flies north.` | `Fred flies in from the south.` |
| in water | `room_vertical_position < 0`, or `== 0` in a room whose `max_depth < 0` | `Fred swims north.` | `Fred swims in from the south.` |
| default | — | `Fred leaves north.` | `Fred arrives from the south.` |

Height alone does not decide whether a character is swimming: position `0` is the water's surface in
a room that has depth, and the ground in a room that does not. The rule therefore reads the room's
`max_depth` alongside the character's position, so someone floating on the surface swims away rather
than walking away.

`move_type` is an input to the same dispatch, so a rule can key off `"flee"` or `"follow"` as
readily as off height — see Flee and Followers and groups below for the two rules this design adds
on `move_type` rather than on height.

## Direction phrasing

Ten directions are in use — the eight compass points plus up and down. The compass points take the
plain direction word on both sides. Up and down do not read naturally that way on arrival:

| Direction | Departure | Arrival |
|---|---|---|
| north … northwest | `Fred leaves north.` | `Fred arrives from the south.` |
| up | `Fred leaves up.` | `Fred arrives from below.` |
| down | `Fred leaves down.` | `Fred arrives from above.` |

The arrival direction is taken from the reciprocal exit — the exit in the room being entered that
leads back where the mover came from — using its own `direction` attribute. Evennia's
`announce_move_to()` already resolves that exit and offers it in its mapping. One-way exits have no
reciprocal, and there the direction falls back to the opposite of the exit traversed, via
`OPPOSITES` in `utils/exit_helpers.py`.

`in` and `out` are defined in `OPPOSITES` but unused by any authored exit. The design does not cover
them; a rule can be added if they are ever built.

## Height changes inside a room

Climbing, flying and swimming up or down move a character between height layers of the same room
without changing which room they're in. These do not call `move_to()` and are outside the seam this
document defines — see the scope note above. Whatever room message they send, if any, is written
directly by the command, the same way `ExitDoor` writes its own open/close text.

Today: climbing and falling already emit a room message. Flying and swimming up/down do not — they
speak only to the mover, so nobody in the room sees a character take off, gain height, dive or
surface. Giving them one is a legitimate follow-on, but it's a `cmd_fly.py`/`cmd_swim.py` change
alongside their existing `room.msg_contents()`-shaped siblings, not a rule in the inter-room
dispatch above.

## Followers and groups

A follower cascade (`get_followers()`) moves every follower in the chain immediately after the
leader, each with `move_type="follow"`. Left as-is, this produces one departure/arrival pair per
follower — a party of five reads as ten room messages for what is, from a bystander's point of
view, one event.

The leader's own move carries the group instead. When the leader has followers in the room, the
verb-resolution messages are replaced with a single named line, independent of what mode any member
of the group is moving in (a mixed walking/flying/swimming group still reads as one line, not one
per mode):

```
source room       Fred's party leaves north.
destination room  Fred's party arrives from the south.
```

A leader moving alone (no followers in the room) gets the ordinary verb-resolved line — "party"
wording only appears when there is a party.

Followers themselves move quietly (`quiet=True` — no announce pair from their own `move_to()`) and
receive only the existing direct message, now carrying the direction:

```
You follow Fred north.
```

There is no arrival message for a follower. This keeps the room-facing side to one line per group
per room, and the follower-facing side to one line per move, with nothing duplicated between them.

## Flee

Flee is the first case of the "everything goes through the seam" default above, rather than an
exception to it. `move_type="flee"` is already passed on every flee `move_to()` call, so the dispatch
gains a `"flee"` rule:

```
source room       Fred flees north!
destination room  Fred flees in from the south!
```

This is a genuine improvement over what exists: today `cmd_flee.py` writes a departure line to the
source room but nothing to the destination room, so a fleeing arrival is currently silent. Routing
through the dispatch gives it the arrival line for free, using the same direction phrasing as every
other move.

Combat flee and the out-of-combat panic run currently use different room text ("flees north!" vs.
"panics and flees north for no apparent reason!"). That distinction is worth keeping — it's real
character, not incidental wording — so `cmd_flee.py` passes it through as a `msg=` override on its
`move_to()` call rather than collapsing to one generic line. The private message to the fleeing
character (`"You flee north!"` / `"You panic and flee north!"`) is untouched either way, since
`announce_move_from`/`announce_move_to` exclude the mover and never touch it.

## Explicitly out of scope

- **Mounted movement.** A mount travels as a follower, so a mounted move today emits the rider's
  pair *and* the mount's pair. Resolving this needs both a "rides" verb for the leader and
  suppression of the mount's own announce while ridden — a natural extension of this same dispatch,
  but deliberately sequenced after walking/flying/swimming/followers land, so the core rework isn't
  held up working out mount specifics. The base system does not regress mounted movement in the
  meantime; it emits the same four messages it does today.
- **Darkness.** Movement messages name the mover regardless of whether the room is lit. Whether an
  unlit room should read "Someone arrives from the south" affects every room message, not only
  movement, so it belongs to a broader pass rather than this document.
- **First-person echo.** The mover receives only the new room's description on arrival, as today; no
  "You leave north." is added for the person moving.

## Cleanup this design requires

`ExitDoor` emits a departure message from `at_traverse()` and an arrival message from
`at_post_traverse()`. Both are removed: they are the duplicate source, and they cannot be suppressed
by a quiet caller. The door keeps its open, close and lock messages, which are about the door rather
than about the movement.

Nothing else in the exit hierarchy emits movement text — every other exit type relies on the
announce pair alone.

Beyond the exit hierarchy, every other quiet caller — retreat, procedural-dungeon entry/exit, the
NFT/pet mirror moves — is a candidate for the same treatment under the "everything goes through the
seam" default above. Flee is the one this document resolves; the rest are for the implementation
audit to inventory and weigh individually, not a blanket rewrite.
