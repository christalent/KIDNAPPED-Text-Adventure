"""
KIDNAPPED! - Floor 4: The Pool and the Umbrella

Floor 4 of the original listing: The Pool and the Umbrella.

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It carried an invented
room set, including rooms that do not exist in the listing at all, and
objects (ALLIGATOR, BURGLAR'S MASK, INDIAN ROPE) that appear nowhere in
the magazine.  Everything below is re-derived from the source pixels.

SOURCE OF TRUTH
---------------
The listing dispatches with ``ON A GOTO 11,12,...,75``, so a global room
number is the printed BASIC line number minus ten.  Floor 4 is printed
lines 55-61, i.e. global rooms 45-51.

Every room number, exit and item placement below was read from raster
crops of the printed listing - never from the PDF text layer, which reads
4 as 1, 8 as S and 0 as O.  The result was checked by replaying both
published walkthroughs (Jacob Gunness, CASA Solution Archive, Sept 2004;
Garry Francis, minimal Atari solution) command for command.

ROOM TABLE (listing lines 55-61)
    45  A HALLWAY              E=48 N=46 S=47   
    46  AN OFFICE              S=45             
    47  A LIBRARY              N=45             
    48  A SWIM ROOM            W=45             
    49  A SWIM ROOM            E=51 N=50        
    50  A LAUNDRY ROOM         S=49             
    51  A DINING ROOM          W=49             

DATA ITEMS ON THIS FLOOR
    46  PUSH BUTTON ON WALL  (fixed)
    51  OPEN WINDOW  (fixed)
    47  BOOK  (takeable)
    50  MARY POPPIN'S UMBRELLA  (takeable)

WALKTHROUGH REPLAY
  Francis: N(46) PRESS BUTTON  S(45) S(47) GET BOOK  READ BOOK  N(45)
           E(48) SWIM(49)  N(50) GET MARY POPPIN'S UMBRELLA  OPEN UMBRELLA
           S(49) E(51) JUMP -> floor 3 room 52

  Gunness stops at OPEN UMBRELLA and jumps from room 50; Francis walks
  on to 51 first.  The listing's room table has both routes open, so the
  jump is accepted from room 50 and from room 51.

INFERRED, NOT TRANSCRIBED
-------------------------
* SWIM needs both the filled pool (button in room 46) and the swimming
  chapter of the book (room 47).  Both are in the walkthroughs; the
  dependency on both is an interpretation.
* JUMP is accepted from room 50 (Gunness) and from room 51 (Francis).

The handler code on listing pages 2-4 has not been transcribed yet, so the
puzzle state machine below is reconstructed from the two published
walkthroughs and from the items the listing actually places.  Everything
listed under INFERRED above is a port-level interpretation, not a
transcription of the magazine.
"""

FLOOR_NUMBER = 4
NEXT_FLOOR_DOWN = 3
ENTRY_ROOM = 45

# Which floor you arrive from -> the room you land in.
SPECIAL_ROOMS = {
    "floor_5": {"landing_room": 45},
}

# Fixed scenery: item name -> the room it is bolted to.
FIXED_ITEMS = {
    "PUSH BUTTON ON WALL": 46,
    "OPEN WINDOW": 51,
}

# Takeable items -> the DATA room they start in.
ITEM_ROOMS = {
    "BOOK": 47,
    "MARY POPPIN'S UMBRELLA": 50,
}

# Names the published walkthroughs use for the listing's items.
ITEM_ALIASES = {

}

ROOMS = {
    45: {
        "name": "A HALLWAY",
        "desc": "A hallway.",
        "exits": {"E": 48, "N": 46, "S": 47},
        "items": [],
    },
    46: {
        "name": "AN OFFICE",
        "desc": "A small office. A button is set into the wall.",
        "exits": {"S": 45},
        "items": [],
    },
    47: {
        "name": "A LIBRARY",
        "desc": "A library. Books line the walls.",
        "exits": {"N": 45},
        "items": [],
    },
    48: {
        "name": "A SWIM ROOM",
        "desc": "A swim room. An empty pool.",
        "exits": {"W": 45},
        "items": [],
    },
    49: {
        "name": "A SWIM ROOM",
        "desc": "A swim room. The pool is full of water.",
        "exits": {"E": 51, "N": 50},
        "items": [],
    },
    50: {
        "name": "A LAUNDRY ROOM",
        "desc": "A laundry room, damp and echoing.",
        "exits": {"S": 49},
        "items": [],
    },
    51: {
        "name": "A DINING ROOM",
        "desc": "A dining room. A window stands open to the night.",
        "exits": {"W": 49},
        "items": [],
    },
}


# Off-grid transitions the room table cannot express: these room pairs are
# linked by a verb action, not by a compass exit.
# swimming the pool (48->49)
VERB_LINK_PAIRS = {(48, 49)}

class Floor4Engine:
    """Floor 4 engine - The Pool and the Umbrella."""

    def __init__(self, state):
        self.state = state
        self.flags = {}
        self._init_items()

    # -- setup ---------------------------------------------------------
    def _init_items(self):
        """Per-instance item state.

        Module-level ROOMS is never mutated: each game instance keeps its
        own copy of the room item lists, so two engines running in the
        same process cannot see each other's pickups.
        """
        self._room_items = {rid: list(r.get("items", [])) for rid, r in ROOMS.items()}
        self._room_fixed = {rid: list(r.get("fixed_items", [])) for rid, r in ROOMS.items()}
        for item, room in FIXED_ITEMS.items():
            if room in self._room_fixed and item not in self._room_fixed[room]:
                self._room_fixed[room].append(item)
        for item, room in ITEM_ROOMS.items():
            if room in self._room_items and item not in self._room_items[room]:
                self._room_items[room].append(item)
        return self._room_items
    def on_enter(self):
        self.state.floor = FLOOR_NUMBER
        if self.state.location not in ROOMS:
            self.state.location = ENTRY_ROOM

    def on_leave(self):
        pass

    # -- queries -------------------------------------------------------
    def get_room(self, room_id):
        return ROOMS.get(room_id)

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    def _room(self):
        return ROOMS.get(self.state.location, {})

    def _here(self, item):
        """Is this object present in the current room?

        Fixed scenery lives in _room_fixed (or FIXED_ITEMS), takeable
        objects in _room_items.  Both count as here: the listing puts
        PUSH BUTTON ON WALL, LOCKED DOOR, STEEL DOOR, FRONT DOOR, PIANO,
        WATER COOLER, SMALL-SIZED PLANT and CHILD'S SLIDE in the room
        description, not in the takeable list.
        """
        loc = self.state.location
        if item in self._room_items.get(loc, []):
            return True
        if item in getattr(self, "_room_fixed", {}).get(loc, []):
            return True
        return FIXED_ITEMS.get(item) == loc
    def _has(self, item):
        return item in self.state.inventory

    def _take(self, item):
        items = self._room_items.setdefault(self.state.location, [])
        if item in items:
            items.remove(item)
        if item not in self.state.inventory:
            self.state.inventory.append(item)
    def _drop(self, item):
        if item in self.state.inventory:
            self.state.inventory.remove(item)
        self._room_items.setdefault(self.state.location, []).append(item)
    def _find_item(self, noun):
        """Match a typed noun against the listing's item names.

        The original matches on the first three letters for GET and DROP
        and the last three for everything else; the published walkthroughs
        also use short forms such as GET BOOK for SMALL BOOK, so both
        conventions and whole-word matches are accepted here.
        """
        n = (noun or "").strip().upper()
        if not n:
            return None
        n = ITEM_ALIASES.get(n, n)
        pool = (list(self._room_items.get(self.state.location, []))
                + list(self.state.inventory))
        for item in pool:
            if item == n:
                return item
        for item in pool:
            words = item.split()
            if n in words:
                return item
        if len(n) >= 3:
            for item in pool:
                words = item.split()
                if item.startswith(n[:3]) or item.endswith(n[-3:]):
                    return item
                if any(w.startswith(n[:3]) or w.endswith(n[-3:]) for w in words):
                    return item
        return None

    # -- movement ------------------------------------------------------
    def _go(self, direction, loc):
        target = self._room().get("exits", {}).get(direction)
        if target is None:
            return "You can't go that way."
        self.state.location = target
        return self._look()

    def _go_up(self, loc):
        return "You can't go that way."

    def _look(self):
        room = self._room()
        if not room:
            return "You are nowhere."
        out = [room.get("desc", room.get("name", ""))]
        exits = room.get("exits", {})
        dirs = [d for d in ("N", "S", "E", "W") if d in exits]
        out.append("Exits: " + ", ".join(f"{d} to {exits[d]}" for d in dirs)
                   if dirs else "No way out that you can see.")
        stuff = list(self._room_items.get(self.state.location, []))
        if stuff:
            out.append("You can see: " + ", ".join(stuff))
        return "\n".join(out)

    def _do_inventory(self):
        if not self.state.inventory:
            return "You are carrying nothing."
        return "You are carrying:\n" + "\n".join(f"  - {i}" for i in self.state.inventory)

    def _examine(self, noun, loc):
        item = self._find_item(noun)
        if item:
            return f"You look at the {item}."
        return "You see nothing like that here."

    # -- items ---------------------------------------------------------
    def _do_get(self, noun, loc):
        item = self._find_item(noun)
        if item is None:
            return "You don't see that here.", False
        if item in FIXED_ITEMS:
            return f"The {item} is fixed in place.", False
        self._take(item)
        return f"You pick up the {item}.", False

    def _do_drop(self, noun, loc):
        item = self._find_item(noun)
        if item is None:
            return "You aren't carrying that.", False
        self._drop(item)
        return f"You drop the {item}.", False

    def _do_use(self, noun, loc):
        return self._dispatch("USE", noun, loc)

    # -- generic verbs (overridden per floor) --------------------------
    def _v_use(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_open(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_read(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_press(self, noun, loc):
        return "You can't do that here.", False

    def _v_play(self, noun, loc):
        return "You can't do that here.", False

    def _v_pour(self, noun, loc):
        return "You can't do that here.", False

    def _v_knit(self, noun, loc):
        return "You can't do that here.", False

    def _v_tie(self, noun, loc):
        return "You can't do that here.", False

    def _v_throw(self, noun, loc):
        return "You can't do that here.", False

    def _v_climb(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_swim(self, noun, loc):
        return "You can't do that here.", False

    def _v_drink(self, noun, loc):
        return "You can't do that here.", False

    def _v_make(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_jump(self, noun, loc):
        return "You can't do that here.", False

    def _v_go(self, noun, loc):
        return "You can't do that here.", False

    # -- dispatch ------------------------------------------------------
    def _dispatch(self, verb, noun, loc):
        handler = getattr(self, "_v_" + verb.lower(), None)
        if handler is None:
            return "You can't do that here.", False
        return handler(noun, loc)

    def handle_command(self, verb, noun):
        verb = (verb or "").upper()
        noun = (noun or "").upper()
        if verb in ("LOOK", "L"):
            return self._look(), False
        if verb in ("INVENTORY", "INV", "I"):
            return self._do_inventory(), False
        if verb in ("N", "S", "E", "W"):
            return self._go(verb, self.state.location), False
        if verb == "GO":
            target = noun.strip()
            if target in ("N", "S", "E", "W"):
                return self._go(target, self.state.location), False
            if target in ("UP", "U"):
                return self._go_up(self.state.location), False
            if target in ("DOWN", "D"):
                return self._v_go("DOWN", self.state.location)
            return self._v_go(target, self.state.location)
        if verb == "GET":
            return self._do_get(noun, self.state.location)
        if verb == "DROP":
            return self._do_drop(noun, self.state.location)
        if verb in ("EXAMINE", "X"):
            return self._examine(noun, self.state.location), False
        if verb in ("USE", "OPEN", "READ", "PRESS", "PUSH", "PLAY", "POUR",
                    "KNIT", "TIE", "THROW", "CLIMB", "SWIM", "DRINK", "MAKE",
                    "JUMP", "PUT", "PAY", "LIGHT", "TAPE", "INFLATE"):
            return self._dispatch(verb, noun, self.state.location)
        return "You can't do that here.", False

    # -- floor 4: fill the pool, learn to swim, jump with the umbrella --
    def _v_press(self, noun, loc):
        if "BUTTON" not in noun:
            return "You can't do that here.", False
        if not self._here("PUSH BUTTON ON WALL"):
            return "There is no button here.", False
        if self.flags.get("filled"):
            return "The pool is already full.", False
        self.flags["filled"] = True
        return ("You press the button. Somewhere below, pipes shudder and the empty pool\n"
                "begins to fill with water."), False

    def _v_push(self, noun, loc):
        """PUSH and PRESS are the same action (DATA object: PUSH BUTTON ON WALL)."""
        return self._v_press(noun, loc)

    def _v_read(self, noun, loc):
        if "BOOK" in noun:
            if not self._has("BOOK"):
                return "You don't have the book.", False
            self.flags["can_swim"] = True
            return ("The book is 'How To Walk A Tightrope', with a chapter on swimming\n"
                    "wedged in the middle. Now you know how to swim."), False
        return self._orig__v_read(noun, loc)

    def _v_swim(self, noun, loc):
        if loc not in (48, 49):
            return "There is no water here.", False
        if not self.flags.get("filled"):
            return "The pool is dry. You would need water in it.", False
        if not self.flags.get("can_swim"):
            return "You flail about and go under. You need to learn how to swim first.", False
        self.state.location = 49
        return self._look(), False

    def _v_open(self, noun, loc):
        if "UMBREL" in noun:
            if not self._has("MARY POPPIN'S UMBRELLA"):
                return "You do not have the umbrella.", False
            self.flags["umbrella_open"] = True
            return "You open the umbrella. It is a ridiculous thing to do indoors.", False
        if "WINDOW" in noun:
            return "The window is already open.", False
        return self._orig__v_open(noun, loc)

    def _v_jump(self, noun, loc):
        if loc not in (50, 51):
            return "There is nothing to jump from here.", False
        if not self.flags.get("umbrella_open"):
            return ("Jumping without the umbrella would kill you. Open the umbrella first."), False
        return ("TRANSITION:floor_3:52", True)

