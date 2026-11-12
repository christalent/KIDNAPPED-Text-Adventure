"""
KIDNAPPED! - Floor 1: Ground Floor - ESCAPE!

Floor 1 of the original listing: Ground Floor - ESCAPE!.

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It carried an invented
room set, including rooms that do not exist in the listing at all, and
objects (ALLIGATOR, BURGLAR'S MASK, INDIAN ROPE) that appear nowhere in
the magazine.  Everything below is re-derived from the source pixels.

SOURCE OF TRUTH
---------------
The listing dispatches with ``ON A GOTO 11,12,...,75``, so a global room
number is the printed BASIC line number minus ten.  Floor 1 is printed
lines 73-75, i.e. global rooms 63-65.

Every room number, exit and item placement below was read from raster
crops of the printed listing - never from the PDF text layer, which reads
4 as 1, 8 as S and 0 as O.  The result was checked by replaying both
published walkthroughs (Jacob Gunness, CASA Solution Archive, Sept 2004;
Garry Francis, minimal Atari solution) command for command.

ROOM TABLE (listing lines 73-75)
    63  A LOUNGE               E=64             
    64  A HALLWAY              W=63             
    65  AN ENTRANCE HALL       -                

DATA ITEMS ON THIS FLOOR
    63  PIANO  (fixed)
    65  FRONT DOOR  (fixed)
    63  LONG ROPE  (takeable)
    64  SMALL BOOK  (takeable)

WALKTHROUGH REPLAY
  Francis: GET KEY (off the piano, room 63)  GET LONG ROPE  E(64)
           GET BOOK  READ BOOK  TIE ROPE  THROW ROPE  GO ROPE(65)
           OPEN DOOR, GO DOOR -> escaped

  Gunness: GET ROPE, GET KEY, E, GET BOOK ("How to walk a tightrope),
           READ BOOK, TIE ROPE (to the stake), THROW ROPE (it catches on
           to the hook), CLIMB ROPE (you cross the pit), OPEN DOOR,
           GO DOOR (you have escaped!)

INFERRED, NOT TRANSCRIBED
-------------------------
* The piano yields the key ("well, pianos have keys!").  There is no
  KEY in DATA on this floor, so it is a found object.
* TIE ROPE needs the book read first; the book is described as
  "How to walk a tightrope".

The handler code on listing pages 2-4 has not been transcribed yet, so the
puzzle state machine below is reconstructed from the two published
walkthroughs and from the items the listing actually places.  Everything
listed under INFERRED above is a port-level interpretation, not a
transcription of the magazine.
"""

FLOOR_NUMBER = 1
NEXT_FLOOR_DOWN = None
ENTRY_ROOM = 63

# Which floor you arrive from -> the room you land in.
SPECIAL_ROOMS = {
    "floor_2": {"landing_room": 63},
}

# Fixed scenery: item name -> the room it is bolted to.
FIXED_ITEMS = {
    "PIANO": 63,
    "FRONT DOOR": 65,
}

# Takeable items -> the DATA room they start in.
ITEM_ROOMS = {
    "LONG ROPE": 63,
    "SMALL BOOK": 64,
}

# Names the published walkthroughs use for the listing's items.
ITEM_ALIASES = {

    "BOOK": "SMALL BOOK"
}

ROOMS = {
    63: {
        "name": "A LOUNGE",
        "desc": "A lounge. An upright piano stands against the wall.",
        "exits": {"E": 64},
        "items": [],
    },
    64: {
        "name": "A HALLWAY",
        "desc": "A hallway. A pit opens in the floor ahead.",
        "exits": {"W": 63},
        "items": [],
    },
    65: {
        "name": "AN ENTRANCE HALL",
        "desc": "The entrance hall. The front door is right there.",
        "exits": {},
        "items": [],
    },
}


# Off-grid transitions the room table cannot express: these room pairs are
# linked by a verb action, not by a compass exit.
# tightrope (TIE/THROW/CLIMB ROPE) from the hallway to the entrance hall
VERB_LINK_PAIRS = {(64, 65)}

class Floor1Engine:
    """Floor 1 engine - Ground Floor - ESCAPE!."""

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
    def _orig__do_get(self, noun, loc):
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

    def _v_press(self, noun, loc):
        return "You can't do that here.", False

    def _v_push(self, noun, loc):
        """PUSH and PRESS are the same action (DATA object: PUSH BUTTON ON WALL)."""
        return self._v_press(noun, loc)

    def _v_play(self, noun, loc):
        return "You can't do that here.", False

    def _v_pour(self, noun, loc):
        return "You can't do that here.", False

    def _v_knit(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_tie(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_throw(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_climb(self, noun, loc):
        return "You can't do that here.", False

    def _v_swim(self, noun, loc):
        return "You can't do that here.", False

    def _v_drink(self, noun, loc):
        return "You can't do that here.", False

    def _v_make(self, noun, loc):
        return "You can't do that here.", False

    def _v_jump(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_go(self, noun, loc):
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

    # -- floor 1: piano key, rope, book, tightrope, the front door ------
    def _do_get(self, noun, loc):
        if "KEY" in noun:
            if self._here("PIANO"):
                if "KEY" not in self.state.inventory:
                    self.state.inventory.append("KEY")
                    return ("You work a key loose from the piano. It is a small, black,\n"
                            "ivory-tipped key - and it opens things."), False
            return self._orig__do_get(noun, loc)
        return self._orig__do_get(noun, loc)

    def _v_read(self, noun, loc):
        if "BOOK" in noun:
            if not self._has("SMALL BOOK"):
                return "You do not have the book.", False
            self.flags["know_rope"] = True
            return ("'How To Walk A Tightrope', by a man with one eye. Chapter one:\n"
                    "'Tie the rope to something solid. Throw it. Catch the hook.'"), False
        return self._orig__v_read(noun, loc)

    def _v_tie(self, noun, loc):
        if "ROPE" not in noun:
            return "You can't tie that.", False
        if not self._has("LONG ROPE"):
            return "You do not have the rope.", False
        if not self.flags.get("know_rope"):
            return "You have no idea how to tie a rope for this.", False
        if self.flags.get("tied"):
            return "The rope is already tied.", False
        self.flags["tied"] = True
        return "You tie one end of the rope around a post, tight and true.", False

    def _v_throw(self, noun, loc):
        if "ROPE" not in noun:
            return "You can't throw that.", False
        if not self.flags.get("tied"):
            return "The rope is not tied to anything yet.", False
        if self.flags.get("hooked"):
            return "The rope is already thrown.", False
        self.flags["hooked"] = True
        return ("You throw the rope across the pit. It catches on a hook in the far wall\n"
                "with a thwap that echoes."), False
        return None

    def _v_climb(self, noun, loc):
        if "ROPE" in noun:
            if not self.flags.get("hooked"):
                return "There is no rope to climb.", False
            self.state.location = 65
            return self._look(), False
        return self._orig__v_climb(noun, loc)

    def _v_go(self, noun, loc):
        if "ROPE" in noun:
            return self._v_climb(noun, loc)
        if "DOOR" in noun:
            if self._here("FRONT DOOR"):
                if not self.flags.get("front_open"):
                    return "The front door is shut.", False
                return ("You have escaped the building.", True)
        return self._orig__v_go(noun, loc)

    def _v_open(self, noun, loc):
        if "DOOR" in noun:
            if self._here("FRONT DOOR"):
                if not self._has("KEY"):
                    return "The front door is locked. You need a key.", False
                self.flags["front_open"] = True
                return "The piano key fits the lock. The front door swings open.", False
        return self._orig__v_open(noun, loc)

