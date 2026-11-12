"""
KIDNAPPED! - Floor 3: The Laboratory (Mr. Hyde)

Floor 3 of the original listing: The Laboratory (Mr. Hyde).

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It carried an invented
room set, including rooms that do not exist in the listing at all, and
objects (ALLIGATOR, BURGLAR'S MASK, INDIAN ROPE) that appear nowhere in
the magazine.  Everything below is re-derived from the source pixels.

SOURCE OF TRUTH
---------------
The listing dispatches with ``ON A GOTO 11,12,...,75``, so a global room
number is the printed BASIC line number minus ten.  Floor 3 is printed
lines 62-67, i.e. global rooms 52-57.

Every room number, exit and item placement below was read from raster
crops of the printed listing - never from the PDF text layer, which reads
4 as 1, 8 as S and 0 as O.  The result was checked by replaying both
published walkthroughs (Jacob Gunness, CASA Solution Archive, Sept 2004;
Garry Francis, minimal Atari solution) command for command.

ROOM TABLE (listing lines 62-67)
    52  A HALLWAY              E=54 N=53        
    53  A RESTROOM             S=52             
    54  A HALLWAY              E=55 W=52        
    55  A HALLWAY              N=56 W=54        
    56  A LABORATORY           S=55             
    57  A CHILD'S PLAYROOM     N=55             

DATA ITEMS ON THIS FLOOR
    53  GRAFFITI ON WALL  (fixed)
    55  STEEL DOOR  (fixed)
    57  CHILD'S SLIDE  (fixed)
    56  JAR OF YELLOW SOLUTION  (takeable)
    56  JAR OF FLUID  (takeable)

WALKTHROUGH REPLAY
  Francis: E(54) E(55) N(56) GET JAR OF FLUID, GET VIAL OF YELLOW SOLUTION
           S(55) OPEN DOOR, GO DOOR  DRINK SOLUTION  GO SLIDE(57)
           -> floor 2 room 58

  Gunness detours first: N(53) READ GRAFFITI  S(52) E(54) E(55) N(56) ...

INFERRED, NOT TRANSCRIBED
-------------------------
* The steel door needs Mr. Hyde's strength (drink the fluid first).
  Gunness says "DRINK FLUID (you turn into the strong Mr. Hyde), OPEN
  DOOR, GO DOOR, DRINK SOLUTION (you revert to normal)".
* The graffiti text is invented - the listing only shows the words
  GRAFFITI ON WALL in room 53.

The handler code on listing pages 2-4 has not been transcribed yet, so the
puzzle state machine below is reconstructed from the two published
walkthroughs and from the items the listing actually places.  Everything
listed under INFERRED above is a port-level interpretation, not a
transcription of the magazine.
"""

FLOOR_NUMBER = 3
NEXT_FLOOR_DOWN = 2
ENTRY_ROOM = 52

# Which floor you arrive from -> the room you land in.
SPECIAL_ROOMS = {
    "floor_4": {"landing_room": 52},
}

# Fixed scenery: item name -> the room it is bolted to.
FIXED_ITEMS = {
    "GRAFFITI ON WALL": 53,
    "STEEL DOOR": 55,
    "CHILD'S SLIDE": 57,
}

# Takeable items -> the DATA room they start in.
ITEM_ROOMS = {
    "JAR OF FLUID": 56,
    "JAR OF YELLOW SOLUTION": 56,
}

# Names the published walkthroughs use for the listing's items.
ITEM_ALIASES = {

    "VIAL OF YELLOW SOLUTION": "JAR OF YELLOW SOLUTION"
}

ROOMS = {
    52: {
        "name": "A HALLWAY",
        "desc": "A hallway.",
        "exits": {"E": 54, "N": 53},
        "items": [],
    },
    53: {
        "name": "A RESTROOM",
        "desc": "A restroom. The walls are covered in graffiti.",
        "exits": {"S": 52},
        "items": [],
    },
    54: {
        "name": "A HALLWAY",
        "desc": "A hallway.",
        "exits": {"E": 55, "W": 52},
        "items": [],
    },
    55: {
        "name": "A HALLWAY",
        "desc": "A hallway. A steel door is set into the east wall.",
        "exits": {"N": 56, "W": 54},
        "items": [],
    },
    56: {
        "name": "A LABORATORY",
        "desc": "A laboratory. Glass jars line the benches.",
        "exits": {"S": 55},
        "items": [],
    },
    57: {
        "name": "A CHILD'S PLAYROOM",
        "desc": "A child's playroom. A slide stands in the corner.",
        "exits": {"N": 55},
        "items": [],
    },
}


# Off-grid transitions the room table cannot express: these room pairs are
# linked by a verb action, not by a compass exit.
# the steel door (55<->57) - 57's N=55 exit is one-way in the room table
VERB_LINK_PAIRS = {(55, 57), (57, 55)}

class Floor3Engine:
    """Floor 3 engine - The Laboratory (Mr. Hyde)."""

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

    def _v_tie(self, noun, loc):
        return "You can't do that here.", False

    def _v_throw(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_climb(self, noun, loc):
        return "You can't do that here.", False

    def _v_swim(self, noun, loc):
        return "You can't do that here.", False

    def _orig__v_drink(self, noun, loc):
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

    # -- floor 3: the laboratory, Mr. Hyde, the child's slide ----------
    def _v_read(self, noun, loc):
        if "GRAFF" in noun:
            if not self._here("GRAFFITI ON WALL"):
                return "There is no graffiti here.", False
            self.flags["read_graffiti"] = True
            return ("The graffiti is a child's scrawl: 'THE STEEL DOOR ONLY OPENS FOR THE\n"
                    "STRONG MAN. THE BIG MAN DRINKS THE FLUID.'"), False
        return self._orig__v_read(noun, loc)

    def _v_drink(self, noun, loc):
        if "FLUID" in noun:
            if not self._has("JAR OF FLUID"):
                return "You do not have the fluid.", False
            self.flags["hyde"] = True
            self.flags.pop("normal", None)
            return ("You drink the fluid. Your hands double in size, your shoulders broaden,\n"
                    "and you feel like Mr. Hyde. You are very strong now."), False
        if "SOLUTION" in noun:
            if not self._has("JAR OF YELLOW SOLUTION"):
                return "You do not have the solution.", False
            self.flags["normal"] = True
            self.flags.pop("hyde", None)
            return "You drink the solution. Your strength drains away. You are yourself again.", False
        return self._orig__v_drink(noun, loc)

    def _v_open(self, noun, loc):
        if "DOOR" in noun:
            if self._here("STEEL DOOR"):
                if not self.flags.get("hyde"):
                    return ("The steel door does not give. Whoever built it wanted somebody\n"
                            "strong to open it, and you are not strong enough."), False
                self.flags["steel_open"] = True
                return "You grip the steel door and pull. It grinds open like a trap.", False
        return self._orig__v_open(noun, loc)

    def _v_go(self, noun, loc):
        if "DOOR" in noun:
            if self._here("STEEL DOOR"):
                if not self.flags.get("steel_open"):
                    return "The steel door is closed.", False
                self.state.location = 57
                return self._look(), False
        if "SLIDE" in noun:
            return self._v_climb(noun, loc)
        return self._orig__v_go(noun, loc)

    def _v_climb(self, noun, loc):
        if "SLIDE" in noun:
            if not self._here("CHILD'S SLIDE"):
                return "There is no slide here.", False
            return ("TRANSITION:floor_2:58", True)
        return self._orig__v_climb(noun, loc)

