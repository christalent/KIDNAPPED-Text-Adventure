"""
KIDNAPPED! - Floor 7: Tool Crib, Storage Room and the Narrow Stairway

Source: SoftSide Vol 3 No 03 (March 1980), BASIC listing for
"KIDNAPPED" by Peter Kirsch.  Floor 7 occupies listing lines 28-35,
which are global rooms 18-25.  The room table below was transcribed
from the printed PDF pixels (300 dpi), not from OCR.

ROOM TABLE (listing lines 28-35)
    18  IN A HALLWAY             W=20  N=19  E=24  S=21
    19  IN AN OFFICE             S=18                 KEY MAKING MACHINE (item 18, fixed)
    20  IN A TOOL CRIB           E=18                 SUPER GLUE (19), WOODEN STAIR STEP (20)
    21  IN A HALLWAY             N=18  E=22
    22  IN AN OFFICE             W=21  E=23
    23  IN A SMALL STORAGE ROOM  W=22                 THICK COPPER SHEET (21)
    24  IN A HALLWAY             W=18                 LOCKED DOOR (22, fixed)
    25  IN A NARROW STAIRWAY     W=24                 WOODEN STAIRS (23, fixed)

DATA (listing line 2010 onward, item numbers verified from pixels)
    19 = SUPER GLUE            in room 20   (takeable)
    20 = WOODEN STAIR STEP     in room 20   (takeable)
    21 = THICK COPPER SHEET    in room 23   (takeable)
    22 = LOCKED DOOR           in room 24   (fixed scenery)
    23 = WOODEN STAIRS         in room 25   (fixed scenery)

HANDLERS (listing lines 900 and 930)
    900  IF D(B)<>11 THEN 930 ELSE IF A=19 IF E$="KEY" IF I(21)=1
         A$(56)="CRUDE KEY":H$(56)=A$(56):A(56)=19:GOTO4900
         -> "MAKE KEY" in room 19 with the THICK COPPER SHEET (item 21)
            makes a CRUDE KEY in room 19 (A(56) is the room it lies in).
    930  IF D(B)<>12 THEN 950 ELSE IF A=25 IF I(19)=1 IF I(20)=1
         IF E$="TEP" OR E$="IRS" PRINT"STAIR'S FIXED":SC=1:RS="":K3=20:GOSUB1100
         -> "GLUE STEP" in room 25 with SUPER GLUE (19) and WOODEN STAIR STEP (20)
            fixes the staircase and consumes the step.

TRANSITIONS
    Floor 8 -> Floor 7 lands in room 18 (the stair descent from floor 8).
    Floor 7 -> Floor 6 lands in room 26 (the top of floor 6).
    There is no way back up: the chain runs 9 -> 8 -> 7 -> 6 -> 5.
"""

FLOOR_NUMBER = 7
NEXT_FLOOR_DOWN = 6

# ---------------------------------------------------------------------
# Rooms.  "items" are takeable; "fixed_items" are scenery (the source
# gives them negative room numbers, which marks them immovable).
# ---------------------------------------------------------------------
ROOMS = {
    18: {
        "name": "IN A HALLWAY",
        "desc": (
            "A grey corridor on the seventh floor. Paint the colour of old "
            "dishwater, a ceiling of acoustic tiles, no windows. Something "
            "heavy was dragged along this floor once - the carpet wears a "
            "long bald stripe down the middle."
        ),
        "exits": {"W": 20, "N": 19, "E": 24, "S": 21},
        "items": [],
        "fixed_items": [],
    },
    19: {
        "name": "IN AN OFFICE",
        "desc": (
            "A small office with a desk bolted to the floor. On the desk "
            "sits a KEY MAKING MACHINE, the size of a heavy typewriter with "
            "a crank on the side and a brass plate half worn away."
        ),
        "exits": {"S": 18},
        "items": [],
        "fixed_items": ["KEY MAKING MACHINE"],
    },
    20: {
        "name": "IN A TOOL CRIB",
        "desc": (
            "A closet the size of a phone box, shelves sagging under a "
            "SUPER GLUE and a WOODEN STAIR STEP. Whoever left them here "
            "was planning something."
        ),
        "exits": {"E": 18},
        "items": ["SUPER GLUE", "WOODEN STAIR STEP"],
        "fixed_items": [],
    },
    21: {
        "name": "IN A HALLWAY",
        "desc": (
            "Another stretch of corridor. The paint is a slightly different "
            "grey here, which means somebody repainted one hallway and "
            "never got round to this one."
        ),
        "exits": {"N": 18, "E": 22},
        "items": [],
        "fixed_items": [],
    },
    22: {
        "name": "IN AN OFFICE",
        "desc": (
            "A second office, smaller and more abused than the first. A "
            "filing cabinet with no door, a swivel chair bolted down, and "
            "paperwork spread across every available surface."
        ),
        "exits": {"W": 21, "E": 23},
        "items": [],
        "fixed_items": [],
    },
    23: {
        "name": "IN A SMALL STORAGE ROOM",
        "desc": (
            "A storage room barely wider than the door. Shelves, a broken "
            "fan, and a THICK COPPER SHEET rolled against the back wall."
        ),
        "exits": {"W": 22},
        "items": ["THICK COPPER SHEET"],
        "fixed_items": [],
    },
    24: {
        "name": "IN A HALLWAY",
        "desc": (
            "The corridor stops here at a LOCKED DOOR. Office issue steel, "
            "with a brass keyhole worn shiny from use."
        ),
        "exits": {"W": 18},
        "items": [],
        "fixed_items": ["LOCKED DOOR"],
    },
    25: {
        "name": "IN A NARROW STAIRWAY",
        "desc": (
            "A narrow stairway wedged between the walls, going down and "
            "down. One of the wooden steps is missing and the rest has "
            "gone soft with damp."
        ),
        "exits": {"W": 24},
        "items": [],
        "fixed_items": ["WOODEN STAIRS"],
    },
}

# The locked door is a verb transition, not a directional exit: you open
# it with a key and then "GO DOOR" from room 24 into room 25.
VERB_LINK_PAIRS = {(24, 25), (25, 24)}

SPECIAL_ROOMS = {
    "floor_6": {"target": "floor_6", "landing_room": 26},
}

FIXED_ITEM_TEXT = {
    "KEY MAKING MACHINE": (
        "A battered cast-iron machine with a crank and a feed slot. The "
        "brass plate reads KEY MAKING MACHINE."
    ),
    "LOCKED DOOR": (
        "A steel door with a brass keyhole. It is locked, and the frame "
        "around it has been walked through more than once."
    ),
    "WOODEN STAIRS": (
        "A wooden staircase going down, treads soft with damp. One step is "
        "missing from the middle."
    ),
}


class Floor7Engine:
    """The seventh floor: make a key, unlock the door, glue a stair step."""

    _DIRS = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST",
             "U": "UP", "D": "DOWN"}
    _DIRWORDS = {
        "NORTH": "N", "N": "N", "SOUTH": "S", "S": "S", "EAST": "E", "E": "E",
        "WEST": "W", "W": "W", "UP": "U", "U": "U", "DOWN": "D", "D": "D",
    }

    def __init__(self, state):
        self.state = state
        self._init_items()
        self.door_unlocked = False
        self.stairs_fixed = False

    # ------------------------------------------------------------------
    # Item initialization (reset each time the player enters floor 7)
    # ------------------------------------------------------------------
    def _init_items(self):
        self.room_items = {rid: list(r["items"]) for rid, r in ROOMS.items()}
        self.room_fixed = {
            rid: list(r.get("fixed_items", [])) for rid, r in ROOMS.items()
        }

    def on_enter(self):
        self.state.floor = FLOOR_NUMBER
        self.state.location = 18

    def on_leave(self):
        pass

    # ------------------------------------------------------------------
    def get_room(self, room_id):
        return ROOMS.get(room_id)

    def get_current_room(self):
        return getattr(self.state, "location", 18)

    @staticmethod
    def _wrap(text):
        """Wrap a command result into the (text, transition) tuple the
        dispatcher in kidnapped.py unpacks."""
        return (text, False)

    # ------------------------------------------------------------------
    def handle_command(self, verb, noun=""):
        """Public entry point.  Always returns (text, transition).

        The top-level parser may hand us either "MAKE" + "KEY" or the
        whole phrase "MAKE KEY", so split a multi-word verb here.
        """
        verb = (verb or "").strip()
        noun = (noun or "").strip()
        if " " in verb:
            first, rest = verb.split(None, 1)
            noun = (rest + " " + noun).strip()
            verb = first
        result = self._dispatch(verb, noun)
        if isinstance(result, tuple):
            return result
        return (result, False)

    def _dispatch(self, verb, noun=""):
        v = (verb or "").strip().upper()
        n = (noun or "").strip().upper()
        loc = self.get_current_room()

        if v in ("LOOK", "L"):
            return self._describe_room(loc)
        if v in ("INVENTORY", "I", "INV"):
            return self._do_inventory()
        if v in ("EXAMINE", "X"):
            return self._examine(n, loc)
        if v in ("GET", "TAKE"):
            return self._do_get(n, loc)
        if v in ("DROP", "DISCARD"):
            return self._do_drop(n, loc)
        if v in ("OPEN", "UNLOCK"):
            return self._do_open(n, loc)
        if v in ("USE", "APPLY", "PUT"):
            return self._do_use(n, loc)
        if v == "MAKE":
            return self._do_make(n, loc)
        if v == "GLUE":
            return self._do_glue(n, loc)
        if v in ("CLIMB", "DESCEND"):
            return self._descend(loc)
        if v == "GO" or v in self._DIRWORDS:
            return self._go(v, n, loc)
        return "You can't do that here."

    # ------------------------------------------------------------------
    def _go(self, verb, noun, loc):
        target = noun.strip().upper()
        if verb == "GO":
            if not target:
                return "Go where?"
            if target in self._DIRWORDS:
                return self._move(self._DIRWORDS[target], loc)
            if "DOOR" in target:
                return self._do_door(loc)
            if "STAIR" in target or target == "STEP":
                return self._descend(loc)
            return "You can't go that way."
        return self._move(self._DIRWORDS[verb], loc)

    def _move(self, direction, loc):
        exits = ROOMS.get(loc, {}).get("exits", {})
        if direction not in exits:
            return "You can't go that way."
        target = exits[direction]
        if isinstance(target, str):
            return "You can't go that way."
        self.state.location = target
        return self._describe_room(target)

    def _do_door(self, loc):
        if loc == 24:
            if not self.door_unlocked:
                return "The LOCKED DOOR is locked."
            self.state.location = 25
            return self._describe_room(25)
        return "There is no door here."

    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Get what?"
        match = self._match_item(noun, self.room_items.get(loc, []))
        if match:
            self.room_items[loc].remove(match)
            self.state.add_item(match)
            return "You take the {0}.".format(match)
        fixed = self._match_item(noun, self.room_fixed.get(loc, []))
        if fixed:
            return "The {0} is part of the building. You can't take it.".format(fixed)
        return "You don't see that here."

    def _do_drop(self, noun, loc):
        match = self._match_item(noun, list(self.state.inventory))
        if not match:
            return "You aren't carrying that."
        self.state.remove_item(match)
        self.room_items.setdefault(loc, []).append(match)
        return "You drop the {0}.".format(match)

    def _do_open(self, noun, loc):
        if "DOOR" in noun:
            if loc != 24:
                return "There is no door to open here."
            if self.door_unlocked:
                return "The door is already open."
            if self._carries("CRUDE KEY"):
                self.door_unlocked = True
                return "The lock turns over and the LOCKED DOOR swings open."
            return "You need a key to open this door."
        return "You can't open that."

    def _do_use(self, noun, loc):
        if loc == 24 and ("KEY" in noun or "DOOR" in noun):
            return self._do_open("DOOR", loc)
        if loc == 25 and ("STEP" in noun or "STAIR" in noun):
            return self._do_glue("STEP", loc)
        if loc == 19 and ("SHEET" in noun or "COPPER" in noun or "KEY" in noun):
            return self._do_make("KEY", loc)
        return "You can't use that here."

    def _do_make(self, noun, loc):
        if loc != 19:
            return "There is no key-making machine here."
        if "KEY" not in noun:
            return "Make what?"
        if self._carries("CRUDE KEY"):
            return "You already have a crude key."
        if not self._carries("THICK COPPER SHEET"):
            return "You need a thick copper sheet to make a key."
        if "CRUDE KEY" not in self.room_items[19]:
            self.room_items[19].append("CRUDE KEY")
        return "You feed the copper sheet into the machine. A CRUDE KEY appears."

    def _do_glue(self, noun, loc):
        if loc != 25:
            return "There is nothing here to glue."
        if not ("STEP" in noun or "STAIR" in noun):
            return "Glue what?"
        if self.stairs_fixed:
            return "The step is already glued in place."
        if not self._carries("SUPER GLUE"):
            return "You need super glue to glue a step in place."
        here = "WOODEN STAIR STEP" in self.room_items.get(25, [])
        if not (self._carries("WOODEN STAIR STEP") or here):
            return "You need a wooden stair step to fit in the gap."
        self.state.remove_item("WOODEN STAIR STEP")
        if here:
            self.room_items[25].remove("WOODEN STAIR STEP")
        self.stairs_fixed = True
        return "STAIR'S FIXED"

    def _descend(self, loc):
        if loc != 25:
            return "There are no stairs here."
        if not self.stairs_fixed:
            return ("The staircase is rotten and one wooden step is missing. "
                    "Glue a step into place before you try to climb down.")
        return "TRANSITION:floor_6:26", True

    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        present = list(self.room_items.get(loc, [])) + list(self.room_fixed.get(loc, []))
        match = self._match_item(noun, present)
        if not match:
            return "You don't see that here."
        if match in FIXED_ITEM_TEXT:
            return FIXED_ITEM_TEXT[match]
        return "It is a {0}.".format(match.lower())

    def _do_inventory(self):
        if not self.state.inventory:
            return "You are carrying nothing."
        return "You are carrying: " + ", ".join(self.state.inventory) + "."

    def _describe_room(self, room_id):
        room = ROOMS.get(room_id)
        if not room:
            return "You are nowhere."
        lines = [room["name"] + ".", room["desc"], ""]
        exits = room.get("exits", {})
        if exits:
            lines.append("EXITS ARE: " + ", ".join(
                self._DIRS[d] for d in sorted(exits) if d in self._DIRS))
        else:
            lines.append("NO EXIT")
        lines.append("")
        present = list(self.room_items.get(room_id, [])) + list(self.room_fixed.get(room_id, []))
        if present:
            lines.append("THINGS YOU SEE HERE:")
            for item in present:
                lines.append("  " + item)
        if room_id == 25:
            lines.append("")
            if self.stairs_fixed:
                lines.append("The glued step holds firm in its socket.")
            else:
                lines.append("A gap where a step should be.")
        lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def _carries(self, keyword):
        keyword = keyword.upper()
        for item in self.state.inventory:
            if keyword in item.upper():
                return True
        return False

    @staticmethod
    def _match_item(noun, items):
        noun = (noun or "").strip().upper()
        if not noun:
            return None
        for item in items:
            if item.upper() == noun:
                return item
        for item in items:
            if item.upper().endswith(noun):
                return item
        for item in items:
            if noun in item.upper() or item.upper() in noun:
                return item
        return None

    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        """Return a list of exit problems (empty list when the map is
        consistent).  Verb-linked pairs are allowed to be one-way."""
        errors = []
        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}
        for rid, room in ROOMS.items():
            for direction, target in room.get("exits", {}).items():
                if isinstance(target, str):
                    continue
                if target not in ROOMS:
                    errors.append(
                        "Room {0}->{1}={2}: target room does not exist".format(rid, direction, target))
                    continue
                if (rid, target) in VERB_LINK_PAIRS:
                    continue
                rev = opposite.get(direction)
                if not rev:
                    continue
                back = ROOMS[target].get("exits", {}).get(rev)
                if back != rid:
                    errors.append(
                        "Room {0}->{1}={2}, but {2}->{3}={4} (expected {0})".format(
                            rid, direction, target, rev, back))
        return errors
