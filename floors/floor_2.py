"""
KIDNAPPED! - Floor 2: The Plant and the Flute

Floor 2 of the original listing: The Plant and the Flute.

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It carried an invented
room set, including rooms that do not exist in the listing at all, and
objects (ALLIGATOR, BURGLAR'S MASK, INDIAN ROPE) that appear nowhere in
the magazine.  Everything below is re-derived from the source pixels.

SOURCE OF TRUTH
---------------
The listing dispatches with ``ON A GOTO 11,12,...,75``, so a global room
number is the printed BASIC line number minus ten.  Floor 2 is printed
lines 68-72, i.e. global rooms 58-62.

Every room number, exit and item placement below was read from raster
crops of the printed listing - never from the PDF text layer, which reads
4 as 1, 8 as S and 0 as O.  The result was checked by replaying both
published walkthroughs (Jacob Gunness, CASA Solution Archive, Sept 2004;
Garry Francis, minimal Atari solution) command for command.

ROOM TABLE (listing lines 68-72)
    58  AN OFFICE              W=59             
    59  A LOUNGE               E=58             
    60  A CRAWLWAY             E=61             
    61  A CRAWLWAY             W=60             
    62  A STAIRCASE            -                

DATA ITEMS ON THIS FLOOR
    58  WATER COOLER  (fixed)
    59  SMALL-SIZED PLANT  (fixed)
    62  STAIRS  (fixed)
    58  PAPER CUP  (takeable)
    61  FLUTE  (takeable)

WALKTHROUGH REPLAY
  Francis: GET PAPER CUP, GET WATER  W(59) POUR WATER  GO PLANT(60)
           E(61) GET FLUTE  PLAY FLUTE  GO ROPE(62)  GO STAIRS
           -> floor 1 room 63

  Gunness: the same chain, with CLIMB PLANT and CLIMB ROPE for the two
  climbs.

INFERRED, NOT TRANSCRIBED
-------------------------
* The plant needs the cup of water before it can be climbed, and the
  flute makes the rope appear.  Both are in the walkthroughs; the exact
  gating is an interpretation.
* PLAY FLUTE creates the magic rope rather than the rope being a DATA
  item: there is no rope in DATA for this floor.

The handler code on listing pages 2-4 has not been transcribed yet, so the
puzzle state machine below is reconstructed from the two published
walkthroughs and from the items the listing actually places.  Everything
listed under INFERRED above is a port-level interpretation, not a
transcription of the magazine.
"""

FLOOR_NUMBER = 2
NEXT_FLOOR_DOWN = 1
ENTRY_ROOM = 58

# Which floor you arrive from -> the room you land in.
SPECIAL_ROOMS = {
    "floor_3": {"landing_room": 58},
}

# Fixed scenery: item name -> the room it is bolted to.
FIXED_ITEMS = {
    "WATER COOLER": 58,
    "SMALL-SIZED PLANT": 59,
    "STAIRS": 62,
}

# Takeable items -> the DATA room they start in.
ITEM_ROOMS = {
    "PAPER CUP": 58,
    "FLUTE": 61,
}

# Names the published walkthroughs use for the listing's items.
ITEM_ALIASES = {

}

ROOMS = {
    58: {
        "name": "AN OFFICE",
        "desc": "An office. A water cooler stands in the corner.",
        "exits": {"W": 59},
        "items": [],
    },
    59: {
        "name": "A LOUNGE",
        "desc": "A lounge. A potted plant stands against the wall.",
        "exits": {"E": 58},
        "items": [],
    },
    60: {
        "name": "A CRAWLWAY",
        "desc": "A crawlway, low and close.",
        "exits": {"E": 61},
        "items": [],
    },
    61: {
        "name": "A CRAWLWAY",
        "desc": "A crawlway. A rope hangs down into the dark.",
        "exits": {"W": 60},
        "items": [],
    },
    62: {
        "name": "A STAIRCASE",
        "desc": "A staircase, going down.",
        "exits": {},
        "items": [],
    },
}


# Off-grid transitions the room table cannot express: these room pairs are
# linked by a verb action, not by a compass exit.
# climbing the watered plant (59->60) and the magic rope (61->62)
VERB_LINK_PAIRS = {(59, 60), (61, 62)}

class Floor2Engine:
    """Floor 2 engine - The Plant and the Flute."""

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

    def _v_open(self, noun, loc):
        return "You can't do that here.", False

    def _v_read(self, noun, loc):
        return "You can't do that here.", False

    def _v_press(self, noun, loc):
        return "You can't do that here.", False

    def _v_push(self, noun, loc):
        """PUSH and PRESS are the same action (DATA object: PUSH BUTTON ON WALL)."""
        return self._v_press(noun, loc)

    def _orig__v_play(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_pour(self, noun, loc):
        return "You can't do that here.", False

    def _v_knit(self, noun, loc):
        return "You can't do that here.", False

    def _v_tie(self, noun, loc):
        return "You can't do that here.", False

    def _v_throw(self, noun, loc):
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

    # -- floor 2: the plant, the flute, the magic rope ------------------
    def _do_get(self, noun, loc):
        if "WATER" in noun:
            if not self._here("WATER COOLER"):
                return "There is no water here.", False
            if not self._has("PAPER CUP"):
                return "You need a cup to carry water in.", False
            self.flags["cup_water"] = True
            return "You fill the paper cup with water from the cooler.", False
        return self._orig__do_get(noun, loc)

    def _v_pour(self, noun, loc):
        if "WATER" not in noun:
            return "You can't pour that.", False
        if not self.flags.get("cup_water"):
            return "You have no water in the cup.", False
        if not self._here("SMALL-SIZED PLANT"):
            return "There is no plant here to water.", False
        if self.flags.get("grown"):
            return "The plant has already grown as far as it can.", False
        self.flags["grown"] = True
        return ("You pour the water on the plant. It drinks, and drinks, and then its stem\n"
                "keeps going - right up past the ceiling. There is a way up now."), False

    def _v_climb(self, noun, loc):
        if "PLANT" in noun:
            if not self._here("SMALL-SIZED PLANT"):
                return "There is no plant here.", False
            if not self.flags.get("grown"):
                return "The plant is far too short to climb.", False
            self.state.location = 60
            return self._look(), False
        if "ROPE" in noun:
            if not self.flags.get("magic_rope"):
                return "There is no rope to climb here.", False
            self.state.location = 62
            return self._look(), False
        if "STAIR" in noun:
            # The stairs down are a climb as well as a walk (GO STAIRS
            # is handled in _v_go); keep both verbs consistent.
            return ("TRANSITION:floor_1:63", True)
        return self._orig__v_climb(noun, loc)

    def _v_play(self, noun, loc):
        if "FLUTE" in noun:
            if not self._has("FLUTE"):
                return "You do not have the flute.", False
            self.flags["magic_rope"] = True
            return ("You play the flute. The note hangs in the air, and a rope snakes down\n"
                    "out of the dark and coils at your feet."), False
        return self._orig__v_play(noun, loc)

    def _v_go(self, noun, loc):
        if "PLANT" in noun:
            return self._v_climb(noun, loc)
        if "ROPE" in noun:
            return self._v_climb(noun, loc)
        if "STAIR" in noun:
            return ("TRANSITION:floor_1:63", True)
        return self._orig__v_go(noun, loc)

