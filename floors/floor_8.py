"""
KIDNAPPED! - Floor 8: The Visitors' Lounge and the Aquarium
==============================================================

GROUND TRUTH
------------
The authoritative description of this floor is
``FLOOR9_AUDIT_2026-11-03.md`` - the pixel-derived audit of the original
listing, reconciled against the two published walkthroughs in
``archive/solutions/`` and Garry Francis's 2015 floor plan.  That file
is the ground truth.  ``KIDNAPPED.BAS``, ``PARSED_BASIC_SOURCE.txt``,
``SPEC.md`` and the *previous* version of this module are guesses, not
evidence.

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It used an invented
room set - 21 "ELEVATOR LANDING", 22 "PIRANHA POOL - MAIN HALL",
24 "AQUARIUM STORAGE", 25 "MAINTENANCE CORRIDOR", 27 "POOL VIEWING
GALLERY", 28 "STAIRS DOWN" - together with a balloon / glue / helium
puzzle that belongs to floor 6.  The audit proves that rooms 13-17 are
floor 8, that both published walkthroughs replay exactly on them, and
that the old rooms are not in the game at all.  They are gone now.

CORRECTED GEOGRAPHY (global room numbers 13-17)
------------------------------------------------
    13  IN A HALLWAY          W->14  S->16
    14  IN A VISITORS LOUNGE  W->15  E->13      AQUARIUM
    15  IN A CLOSET           E->14               ROPE
    16  IN AN OFFICE          N->13  E->17       SLEEPING PILL
    17  IN AN OFFICE          W->16               OPEN WINDOW, DESK

Room 13 is the arrival room: floor 9's PRESS BUTTON lands the player
here (marker ``"TRANSITION:floor_8:13"``).

THE PUZZLE (published walkthrough route)
----------------------------------------
    S(16) GET PILL . N(13) . W(14) . W(15) GET ROPE . E(14)
    DROP PILL GET PIRANHA . E(13) . S(16) DROP PIRANHA . E(17)
    TIE ROPE CLIMB ROPE

  * The AQUARIUM in the visitors' lounge (14) is scenery until the
    SLEEPING PILL is dropped into the tank; then a PIRANHA can be
    fished out.  The pill is gone for good once it goes into the tank.
  * DROP PIRANHA in the office (16) disposes of the fish.
  * In 17 the rope is tied to the open window frame: TIE ROPE, then
    CLIMB ROPE (GO ROPE / USE ROPE also work) -> floor 7.

The rope crossing is a VERB transition, not a directional exit: room 17
has no "D" exit and there is no up-exit to floor 9 (the descent chain
is one way: floor 9 -> floor 8 -> floor 7).  The marker string
``"TRANSITION:floor_7:31"`` follows the codebase convention; the
dispatcher in ``kidnapped.py`` prints it and lets floor 7's
``on_enter()`` place the player (room 31, the foyer whose up-exit leads
back here).  Because floor 7 is not audited yet and its ``on_enter()``
does not set a location, floor 8 sets the landing room itself just
before it hands the player over.

Cross-floor convention used here (identical to floors 6, 7 and 9):
  * ``handle_command()`` ALWAYS returns a ``(text, transition)`` tuple.
  * A transition is a text that starts with ``"TRANSITION:floor_N:room"``.
"""

FLOOR_NUMBER = 8
NEXT_FLOOR_DOWN = 7

# --------------------------------------------------------------------
# The single cross-floor link on this floor: the rope crossing down to
# floor 7.  There is deliberately NO "floor_9" entry - the descent chain
# is one way (floor 9 -> floor 8 -> floor 7), so floor 8 can never be
# climbed back into floor 9.
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    "floor_7": {"target": "floor_7", "landing_room": 31},
}

# --------------------------------------------------------------------
# Room table - pixel-derived, see FLOOR9_AUDIT_2026-11-03.md
# --------------------------------------------------------------------
ROOMS = {
    13: {
        "name": "IN A HALLWAY",
        "desc": (
            "The lift doors have just shut behind you, leaving you on the "
            "eighth floor of a building you have no business being in. "
            "The hallway is narrow, the carpet worn thin, and a door "
            "stands open to the west."
        ),
        "exits": {"W": 14, "S": 16},
        "items": [],
    },
    14: {
        "name": "IN A VISITORS LOUNGE",
        "desc": (
            "A visitors' lounge: a rank of mouldy armchairs, a low table "
            "with a dead potted plant, and along the wall a big AQUARIUM "
            "full of green water. Small fish drift at the top of the "
            "tank."
        ),
        "exits": {"W": 15, "E": 13},
        "items": ["AQUARIUM"],
    },
    15: {
        "name": "IN A CLOSET",
        "desc": (
            "A janitor's closet, deep enough to be a room of its own. "
            "Mops, buckets, a shelf of dusty bottles. A coil of ROPE hangs "
            "on a hook by the door."
        ),
        "exits": {"E": 14},
        "items": ["ROPE"],
    },
    16: {
        "name": "IN AN OFFICE",
        "desc": (
            "A small office. A DESK under a dead lamp, a swivel chair "
            "pushed back from it, and a SLEEPING PILL lying on the desk "
            "among a scatter of paper clips."
        ),
        "exits": {"N": 13, "E": 17},
        "items": ["SLEEPING PILL"],
    },
    17: {
        "name": "IN AN OFFICE",
        "desc": (
            "Another office, larger and much emptier. A DESK stands in the "
            "middle of the floor with nothing on it. In the far wall the "
            "OPEN WINDOW gives onto a dark shaft of stairs going down and "
            "down into the building."
        ),
        "exits": {"W": 16},
        "items": ["OPEN WINDOW", "DESK"],
    },
}

# --------------------------------------------------------------------
# Items that are scenery: they can be examined, never picked up.
# --------------------------------------------------------------------
_SCENERY = {"AQUARIUM", "OPEN WINDOW", "DESK"}

# --------------------------------------------------------------------
# Noun -> canonical item name.  The published walkthroughs spell the
# same objects differently ("PILL" / "SLEEPING PILL", "PIRANHA" /
# "SLEEPING PIRANHA"), so every spelling has to work.
# --------------------------------------------------------------------
_ITEM_ALIASES = {
    "SLEEPING PILL": "SLEEPING PILL",
    "PILL": "SLEEPING PILL",
    "PIRANHA": "PIRANHA",
    "SLEEPING PIRANHA": "PIRANHA",
    "ROPE": "ROPE",
    "AQUARIUM": "AQUARIUM",
    "TANK": "AQUARIUM",
    "FISH TANK": "AQUARIUM",
    "OPEN WINDOW": "OPEN WINDOW",
    "WINDOW": "OPEN WINDOW",
    "DESK": "DESK",
}

# The room the rope is tied in (the office with the open window).
_ROPE_ROOM = 17

# The room the aquarium is in (the visitors' lounge).
_TANK_ROOM = 14


# --------------------------------------------------------------------
# Floor 8 Engine
# --------------------------------------------------------------------
class Floor8Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        # Puzzle state
        self.pill_in_tank = False
        self.piranha_asleep = False
        self.rope_tied = False

    # ------------------------------------------------------------------
    # Item initialization (reset each time the player enters floor 8)
    # ------------------------------------------------------------------
    def _init_items(self):
        """Runtime item lists: what the player can see right now."""
        return {rid: list(r.get("items", [])) for rid, r in ROOMS.items()}

    # ------------------------------------------------------------------
    # Entry / exit
    # ------------------------------------------------------------------
    def on_enter(self):
        """Called when the player arrives on Floor 8.

        The arrival room is 13 (IN A HALLWAY): floor 9's PRESS BUTTON
        produces the marker "TRANSITION:floor_8:13" and this method
        puts the player there.
        """
        if hasattr(self.state, "floor"):
            self.state.floor = FLOOR_NUMBER
        self._room_items = self._init_items()
        self.pill_in_tank = False
        self.piranha_asleep = False
        self.rope_tied = False
        self.state.location = 13

    def on_leave(self):
        """Called when the player leaves Floor 8."""
        pass

    # ------------------------------------------------------------------
    # Room access
    # ------------------------------------------------------------------
    def get_room(self, room_id):
        """Return a copy of the room record with its runtime item list."""
        if room_id not in ROOMS:
            return None
        r = dict(ROOMS[room_id])
        r["id"] = room_id
        r["items"] = list(self._room_items.get(room_id, []))
        return r

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    # ------------------------------------------------------------------
    # Command dispatch - every path returns a (text, transition) tuple
    # ------------------------------------------------------------------
    def handle_command(self, verb, noun=""):
        verb = (verb or "").upper().strip()
        noun = (noun or "").upper().strip()
        loc = self.state.location

        # Verb spellings that mean the same thing.
        if verb in ("TAKE", "GRAB", "PICK"):
            verb = "GET"
        if verb in ("PUT", "PLACE"):
            verb = "DROP"
        if verb in ("X", "CHECK", "READ"):
            verb = "EXAMINE"

        # Verb transitions have to be recognised BEFORE movement, so
        # that "GO ROPE" is not mistaken for a direction.
        if verb == "TIE":
            return self._wrap(self._tie_rope(noun, loc))
        if verb == "CLIMB":
            return self._wrap(self._climb_rope(noun, loc))
        if verb == "GO" and noun and self._is_rope(noun):
            return self._wrap(self._climb_rope(noun, loc))

        if verb in ("LOOK", "L"):
            return self._wrap(self._describe_room(loc))
        if verb in ("INVENTORY", "INV", "I"):
            return self._wrap(self._do_inventory())
        if verb == "GET":
            return self._wrap(self._do_get(noun, loc))
        if verb == "DROP":
            return self._wrap(self._do_drop(noun, loc))
        if verb in ("USE", "APPLY"):
            return self._wrap(self._do_use(noun, loc))
        if verb in ("OPEN", "UNLOCK"):
            return self._wrap(self._do_open(noun, loc))
        if verb in ("EXAMINE", "LOOK AT"):
            return self._wrap(self._examine(noun, loc))
        if verb in ("FIX", "REPAIR"):
            return self._wrap(self._do_fix(noun, loc))
        if verb in ("INFLATE", "BLOW", "FILL"):
            return self._wrap(self._do_inflate(noun))

        d = self._parse_direction(verb, noun)
        if d is not None:
            if d == "U":
                return self._wrap(self._go_up(loc))
            if d == "D":
                return self._wrap(self._go_down(loc))
            return self._wrap(self._go(d, loc))

        return "You don't know how to do that.", False

    @staticmethod
    def _wrap(text):
        """Wrap a command result into the (text, transition) tuple the
        dispatcher in kidnapped.py unpacks.

        A result whose text starts with "TRANSITION:" is a floor change;
        everything else is ordinary prose.
        """
        if isinstance(text, tuple):
            return text
        return text, text.startswith("TRANSITION:")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _parse_direction(verb, noun):
        v = (verb or "").upper()
        n = (noun or "").upper()
        if v in ("N", "NORTH") or (v == "GO" and n in ("N", "NORTH")):
            return "N"
        if v in ("S", "SOUTH") or (v == "GO" and n in ("S", "SOUTH")):
            return "S"
        if v in ("E", "EAST") or (v == "GO" and n in ("E", "EAST")):
            return "E"
        if v in ("W", "WEST") or (v == "GO" and n in ("W", "WEST")):
            return "W"
        if v in ("U", "UP") or (v == "GO" and n in ("U", "UP")):
            return "U"
        if v in ("D", "DOWN") or (v == "GO" and n in ("D", "DOWN")):
            return "D"
        return None

    @staticmethod
    def _canonical_item(noun):
        """Map a noun phrase onto a canonical item name (or None)."""
        n = (noun or "").upper().strip()
        if n.startswith("THE "):
            n = n[4:].strip()
        if not n:
            return None
        if n in _ITEM_ALIASES:
            return _ITEM_ALIASES[n]
        for alias in _ITEM_ALIASES:
            if alias in n:
                return _ITEM_ALIASES[alias]
        return None

    @staticmethod
    def _is_rope(noun):
        return Floor8Engine._canonical_item(noun) == "ROPE"

    def _add_to_inventory(self, item):
        """Add an item to the player's inventory (tolerates either a
        real GameState with add_item/remove_item or a plain test double
        that only carries an inventory list)."""
        add = getattr(self.state, "add_item", None)
        if callable(add):
            add(item)
        inv = getattr(self.state, "inventory", None)
        if inv is not None and item not in inv:
            inv.append(item)

    def _remove_from_inventory(self, item):
        """Remove an item from the player's inventory."""
        remove = getattr(self.state, "remove_item", None)
        if callable(remove):
            remove(item)
        inv = getattr(self.state, "inventory", None)
        if inv is not None and item in inv:
            inv.remove(item)

    def _carrying(self, item):
        inv = getattr(self.state, "inventory", None) or []
        return item in inv

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _go(self, direction, loc):
        r = self.get_room(loc)
        if not r:
            return "You are nowhere."
        exits = r.get("exits", {})
        next_target = exits.get(direction)
        if next_target is None:
            return f"You can't go {direction} from here."
        if isinstance(next_target, str):
            # No directional exit leaves floor 8 (the rope crossing is a
            # verb), but keep the branch honest if one is ever added.
            return f"TRANSITION:{next_target}:{self._landing(next_target)}"
        self.state.location = next_target
        return self._describe_room(next_target)

    def _go_up(self, loc):
        # There is no way back up to floor 9: the descent chain is one way.
        return self._go("U", loc)

    def _go_down(self, loc):
        # There is no way down by walking either - the rope is the only
        # way to floor 7, and it is a verb, not a direction.
        return self._go("D", loc)

    @staticmethod
    def _landing(target):
        """Landing room for an inter-floor marker (only floor_7 is used)."""
        return SPECIAL_ROOMS.get(target, {}).get("landing_room", 1)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        room_items = self._room_items.get(loc, [])
        item = self._canonical_item(noun)

        # ---- SLEEPING PILL (room 16) ----
        if item == "SLEEPING PILL":
            if "SLEEPING PILL" in room_items:
                room_items.remove("SLEEPING PILL")
                self._room_items[loc] = room_items
                self._add_to_inventory("SLEEPING PILL")
                return "You take the SLEEPING PILL."
            if self.pill_in_tank and loc == _TANK_ROOM:
                return ("The pill is at the bottom of the tank, dissolving "
                        "in the green water. It is gone for good.")
            return "There's no pill here."

        # ---- ROPE (room 15) ----
        if item == "ROPE":
            if "ROPE" in room_items:
                room_items.remove("ROPE")
                self._room_items[loc] = room_items
                self._add_to_inventory("ROPE")
                return ("You lift the coil of ROPE off the hook. It is "
                        "coarse, old, and strong enough.")
            return "There's no rope here."

        # ---- PIRANHA (lying in a room, or asleep in the tank) ----
        if item == "PIRANHA":
            if "PIRANHA" in room_items:
                room_items.remove("PIRANHA")
                self._room_items[loc] = room_items
                self._add_to_inventory("PIRANHA")
                return "You take the piranha."
            if self.piranha_asleep and loc == _TANK_ROOM:
                self.piranha_asleep = False
                self._add_to_inventory("PIRANHA")
                return ("You fish the sleeping piranha out of the tank. It "
                        "hangs limp in your hands, quite dead to the "
                        "world.")
            return ("There is no piranha to take - the tank holds nothing "
                    "but fish.")

        # ---- Scenery: never takeable ----
        if item in _SCENERY:
            return "That's not something you can pick up."

        # Generic: any other item lying in the room.
        for candidate in list(room_items):
            if noun.lower() in candidate.lower() or candidate.lower() in noun.lower():
                room_items.remove(candidate)
                self._room_items[loc] = room_items
                self._add_to_inventory(candidate)
                return f"You take the {candidate}."
        return "You don't see that here."

    # ------------------------------------------------------------------
    # DROP
    # ------------------------------------------------------------------
    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"

        item = self._canonical_item(noun)

        # ---- SLEEPING PILL ----
        if item == "SLEEPING PILL":
            if not self._carrying("SLEEPING PILL"):
                return "You're not carrying that."
            self._remove_from_inventory("SLEEPING PILL")
            if loc == _TANK_ROOM:
                # Into the aquarium. The pill is spent; the piranha sleeps.
                self.pill_in_tank = True
                self.piranha_asleep = True
                return ("You drop the SLEEPING PILL into the aquarium. It "
                        "sinks through the green water and settles on the "
                        "gravel. Something at the bottom of the tank stops "
                        "moving.")
            self._room_items.setdefault(loc, []).append("SLEEPING PILL")
            return "You drop the SLEEPING PILL on the floor."

        # ---- PIRANHA ----
        if item == "PIRANHA":
            if not self._carrying("PIRANHA"):
                return "You're not carrying that."
            self._remove_from_inventory("PIRANHA")
            self._room_items.setdefault(loc, []).append("PIRANHA")
            if loc == 16:
                return ("You drop the piranha on the office floor. It hits "
                        "the carpet and lies still, out of your hands.")
            return ("You drop the piranha. It flops once and goes stiff on "
                    "the floor.")

        # ---- ROPE ----
        if item == "ROPE":
            if not self._carrying("ROPE"):
                return "You're not carrying that."
            self._remove_from_inventory("ROPE")
            self._room_items.setdefault(loc, []).append("ROPE")
            return "You drop the coil of ROPE."

        # Generic: anything else you happen to be carrying.
        inv = getattr(self.state, "inventory", None) or []
        for candidate in list(inv):
            if noun.lower() in candidate.lower() or candidate.lower() in noun.lower():
                self._remove_from_inventory(candidate)
                self._room_items.setdefault(loc, []).append(candidate)
                return f"You drop the {candidate}."
        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"

        item = self._canonical_item(noun)

        # ---- ROPE: use it the way the walkthrough does ----
        if item == "ROPE":
            return self._climb_rope("ROPE", loc)

        # ---- SLEEPING PILL into the aquarium ----
        if item == "SLEEPING PILL":
            if loc == _TANK_ROOM:
                return self._do_drop("SLEEPING PILL", loc)
            return "You have no use for it here."

        # ---- AQUARIUM ----
        if item == "AQUARIUM":
            return self._examine("AQUARIUM", loc)

        # ---- DESK ----
        if item == "DESK":
            return ("You rummage through the desk. Paper clips, a dead "
                    "battery, nothing you can use.")

        # ---- OPEN WINDOW ----
        if item == "OPEN WINDOW":
            return ("The window is open already, and the drop beyond it "
                    "goes a long way down.")

        return "You can't figure out how to use that here."

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        item = self._canonical_item(noun)
        if item == "OPEN WINDOW":
            if loc != _ROPE_ROOM:
                return "There is no window here."
            return ("The window is already open - that is how the rope will "
                    "reach the floor below.")
        if item == "DESK":
            if loc not in (16, 17):
                return "There is no desk here."
            return ("You open the desk. Nothing inside but dust and a "
                    "screwed-in envelope you cannot get at.")
        if item == "AQUARIUM":
            return ("The aquarium has no lid you could lift. The glass is "
                    "too heavy to shift.")
        return "You can't open that."

    # ------------------------------------------------------------------
    # TIE ROPE / CLIMB ROPE - the verb transition down to floor 7
    # ------------------------------------------------------------------
    def _tie_rope(self, noun, loc):
        if noun and not self._is_rope(noun):
            return "You can't tie that."
        if not self._carrying("ROPE"):
            return "You don't have a rope to tie."
        if loc != _ROPE_ROOM:
            return ("There is nothing here to tie the rope to. The office "
                    "at the end of the hall has an open window - try "
                    "there.")
        if self.rope_tied:
            return "The rope is already knotted around the window frame."
        self.rope_tied = True
        return ("You tie one end of the rope around the window frame and "
                "feed the rest out into the dark. The knot holds. The "
                "rope hangs down into the stairwell.")

    def _climb_rope(self, noun, loc):
        if noun and not self._is_rope(noun):
            return f"You can't climb the {noun.lower()}."
        if not self._carrying("ROPE"):
            return "You don't have a rope."
        if loc != _ROPE_ROOM:
            return ("There is nothing here to climb. The rope would have "
                    "to be tied to the open window in the office at the "
                    "end of the hall.")
        if not self.rope_tied:
            return ("The rope is not tied to anything. Tie it to the "
                    "window frame first.")
        # Verb transition to floor 7.  The dispatcher prints the marker
        # and hands over to floor 7's on_enter(); floor 7 is not audited
        # yet and its on_enter() does not set a location, so floor 8
        # sets the landing room (31 - the foyer whose up-exit leads back
        # here) itself before handing the player over.
        landing = self._landing("floor_7")
        self.state.location = landing
        return f"TRANSITION:floor_7:{landing}"

    # ------------------------------------------------------------------
    # Vestigial helpers kept for API compatibility
    # ------------------------------------------------------------------
    def _do_fix(self, noun, loc):
        """Nothing on this floor needs mending any more."""
        return "There's nothing here to fix."

    def _do_inflate(self, noun):
        """Nothing on this floor needs inflating any more."""
        return "There's nothing here to inflate."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return self._describe_room(loc)

        item = self._canonical_item(noun)
        room_items = self._room_items.get(loc, [])

        if item == "AQUARIUM":
            if loc != _TANK_ROOM:
                return "There is no aquarium here."
            if self.pill_in_tank:
                return ("A big tank of green water along the wall. The "
                        "sleeping pill lies on the gravel at the bottom, "
                        "and the piranha hangs upside down in front of "
                        "it, quite asleep.")
            return ("A big tank of green water along the wall. Small fish "
                    "drift at the top. Nothing in there but fish.")

        if item == "PIRANHA":
            if self.piranha_asleep and loc == _TANK_ROOM:
                return ("The piranha hangs motionless in the green water, "
                        "belly up, fast asleep.")
            if self._carrying("PIRANHA"):
                return ("A heavy, toothy fish. It hangs limp and "
                        "uninterested in your hands.")
            return "There is no piranha here."

        if item == "SLEEPING PILL":
            if "SLEEPING PILL" in room_items:
                return "A single small pill, white, lying on the desk."
            if self._carrying("SLEEPING PILL"):
                return "A single small pill, white, in your pocket."
            if self.pill_in_tank and loc == _TANK_ROOM:
                return ("The pill is on the gravel at the bottom of the "
                        "tank, dissolving.")
            return "There is no pill here."

        if item == "ROPE":
            if "ROPE" in room_items:
                return "A coil of coarse rope hanging on a hook."
            if self._carrying("ROPE"):
                if self.rope_tied:
                    return ("Your rope, knotted around the window frame, "
                            "hanging down into the dark.")
                return ("A coil of coarse rope, strong enough to hold "
                        "your weight.")
            return "There is no rope here."

        if item == "OPEN WINDOW":
            if loc != _ROPE_ROOM:
                return "There is no window here."
            return ("The window stands open on a shaft of stairs going "
                    "down. It is a long way down, and a rope would reach "
                    "it.")

        if item == "DESK":
            if loc not in (16, 17):
                return "There is no desk here."
            return ("A plain desk. The drawer is stiff and full of "
                    "paperwork nobody has read since 1980.")

        if "LOUNGE" in noun:
            return ("A visitors' lounge: armchairs, a dead plant, and a "
                    "big aquarium against the wall.")
        if "HALLWAY" in noun:
            return ("A narrow hallway. The lift doors behind you are "
                    "already shut.")
        if "CLOSET" in noun:
            return ("A janitor's closet, mops and buckets and a coil of "
                    "rope.")
        if "OFFICE" in noun:
            return "A bare office with a desk and a dead lamp."

        return "You don't see anything unusual."

    # ------------------------------------------------------------------
    # INVENTORY
    # ------------------------------------------------------------------
    def _do_inventory(self):
        items = getattr(self.state, "inventory", None) or []
        if not items:
            return "You are empty-handed."
        return "You are carrying: " + ", ".join(items)

    # ------------------------------------------------------------------
    # Room description
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        r = self.get_room(room_id)
        if not r:
            return "You are nowhere."
        desc = f"[{r['name']}]\n{r.get('desc', '')}"
        items = self._room_items.get(room_id, [])
        if items:
            desc += "\n\nYou can see: " + ", ".join(items) + "."
        exits = r.get("exits", {})
        exit_list = []
        for d in ("N", "S", "E", "W", "U", "D"):
            if d in exits:
                t = exits[d]
                if isinstance(t, int):
                    target_name = ROOMS.get(t, {}).get("name", f"Room {t}")
                    exit_list.append(f"{d} to {target_name}")
                else:
                    exit_list.append(f"{d} to {t}")
        if exit_list:
            desc += "\n\nExits: " + ", ".join(exit_list) + "."
        return desc
