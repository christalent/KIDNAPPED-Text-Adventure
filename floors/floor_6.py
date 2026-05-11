"""
KIDNAPPED! - Floor 6: The Office
"Sexy young office girls, knitting, fashion a new suit"

Entry from Floor 7 via slide -> Room 41.
Goal: Navigate past the office workers, descend to Floor 5.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 6 items
"""

FLOOR_NUMBER = 6
NEXT_FLOOR_DOWN = 5

# --------------------------------------------------------------------
# Room map (Floor 6, rooms 41-49):
# Approximate layout from BASIC analysis + review:
#
#   [41] Entry (from Floor 7 slide)
#    |
#   [42] Office corridor
#    |
#   [43-47] Open plan office (SEXY GIRL OFFICE WORKERS here)
#    |
#   [48] Office supplies / storage
#    |
#   [49] Stairs DOWN to Floor 5
#
# Items from BASIC DATA:
# Room 47: BOOK (takeable)
# Room 50: EVERY PUPIL'S LAMP (fixed)
# Room 51: OPEN WINDOW (fixed)
# Room 53: GRAFFITI ON WALL (fixed)
# Room 58: WATER COOLER, PAPER CUP (room 58 is floor 5? use anyway)
# Room 59: SMALL-SIZED PLANT (room 59 is floor 5? use anyway)
# Room 61: FLUTE (room 61 is floor 4? use anyway)
# Room 63: PIANO (fixed), LONG ROPE (takeable)
# Room 65: FRONT DOOR (fixed - but this is on floor 5/1?)
#
# NOTE: Due to room number overlap in BASIC DATA, some items may be
# assigned to wrong rooms. This is a best-effort reconstruction.
# --------------------------------------------------------------------
ROOMS = {
    # Simple linear chain: 41→42→43→45→46→47→48→49
    # Branch: 43E→44 (dead-end storage)
    # All bidirectional exits verified
    41: {
        "name": "OFFICE ENTRANCE",
        "desc": (
            "You emerge from the slide into a carpeted office corridor. "
            "Fluorescent lights hum overhead. The carpet is shag, very 70s. "
            "Motivational posters line the walls: 'Hang in There!' "
            "A sign reads 'FLOOR 6 - OFFICE WING'. "
            "The corridor continues NORTH. "
            "You can go UP to Floor 7."
        ),
        "exits": {"N": 42, "U": "floor_7"},
        "items": [],
    },
    42: {
        "name": "OPEN PLAN OFFICE",
        "desc": (
            "A large open-plan office space. "
            "Cubes, water coolers, the works. "
            "A small BOOK lies on one of the desks. "
            "A PIANO sits in the corner - someone's been playing it. "
            "The corridor is to the SOUTH. "
            "More office space extends NORTH."
        ),
        "exits": {"S": 41, "N": 43},
        "items": ["BOOK"],
    },
    43: {
        "name": "CUBICLE FARM",
        "desc": (
            "Rows of beige cubicles stretch out before you. "
            "It's quiet. Too quiet. "
            "Then you see them: the SEYOUNG GIRL OFFICE WORKERS. "
            "They block your path, chatting away. "
            "A PAPER CUP sits on a desk nearby. "
            "A doorway leads EAST to a storage room. "
            "The open office is to the SOUTH. "
            "The corridor continues NORTH."
        ),
        "exits": {"S": 42, "N": 45, "E": 44},
        "items": ["PAPER CUP"],
    },
    44: {
        "name": "OFFICE SUPPLIES",
        "desc": (
            "A storage room full of office supplies. "
            "Copier paper, staplers, pens. "
            "A LONG ROPE has been coiled in the corner. "
            "The cubicle farm is to the WEST."
        ),
        "exits": {"W": 43},
        "items": ["LONG ROPE"],
    },
    45: {
        "name": "EXEC OFFICE",
        "desc": (
            "A corner executive office. Mahogany desk, leather chair. "
            "A SMALL PLANT sits on the windowsill. "
            "The door is open to the SOUTH. "
            "A narrow passage leads NORTH."
        ),
        "exits": {"S": 43, "N": 46},
        "items": ["SMALL PLANT"],
    },
    46: {
        "name": "COPY ROOM",
        "desc": (
            "A cramped copy room. An ancient Xerox machine squats in the corner. "
            "Someone has graffitied the wall with marker. "
            "The executive office is to the SOUTH. "
            "The boss's office is to the NORTH."
        ),
        "exits": {"S": 45, "N": 47},
        "items": ["GRAFFITI ON WALL"],
    },
    47: {
        "name": "BOSS'S OFFICE",
        "desc": (
            "The boss's corner office. Everything is neat and tidy. "
            "A framed photo shows... a KANGAROO? "
            "A BOOK sits on the bookshelf. "
            "The copy room is to the SOUTH. "
            "The break room is to the NORTH."
        ),
        "exits": {"S": 46, "N": 48},
        "items": ["BOOK"],
    },
    48: {
        "name": "BREAK ROOM",
        "desc": (
            "A break room. Vending machines, a water cooler. "
            "A BALL OF YARN and KNITTING NEEDLES sit on a table. "
            "The boss's office is to the SOUTH. "
            "The stairs DOWN are to the NORTH."
        ),
        "exits": {"S": 47, "N": 49},
        "items": ["BALL OF YARN", "KNITTING NEEDLES"],
    },
    49: {
        "name": "STAIRS DOWN",
        "desc": (
            "A stairwell. A sign reads 'FLOOR 5 - DOWN ONLY'. "
            "A FLUTE has been left on the landing. "
            "The break room is to the SOUTH. "
            "Go DOWN to Floor 5."
        ),
        "exits": {"S": 48, "D": "floor_5"},
        "items": ["FLUTE"],
    },
}

SPECIAL_ROOMS = {
    "floor_7": {"target": "floor_7", "landing_room": 37},
    "floor_5": {"target": "floor_5", "landing_room": 51},
}

class Floor6Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.suit_knitted = False

    def _init_items(self):
        return {
            42: ["BOOK"],
            43: ["PAPER CUP"],
            44: ["LONG ROPE"],
            45: ["SMALL PLANT"],
            46: ["GRAFFITI ON WALL"],
            47: ["BOOK"],
            48: ["BALL OF YARN", "KNITTING NEEDLES"],
            49: ["FLUTE"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.suit_knitted = False

    def on_leave(self):
        pass

    def get_room(self, room_id):
        return ROOMS.get(room_id)

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    def handle_command(self, verb, noun=""):
        loc = self.state.location
        verb = verb.upper().strip()
        noun = noun.upper().strip() if noun else ""

        if verb in ("LOOK", "L"):
            return self._look(), False
        if verb in ("INVENTORY", "I"):
            return self._do_inventory(), False
        if verb in ("GET", "TAKE", "GRAB"):
            return self._do_get(noun, loc), False
        if verb in ("DROP", "PUT", "PLACE"):
            return self._do_drop(noun, loc), False
        if verb in ("USE", "APPLY"):
            return self._do_use(noun, loc), False
        if verb in ("KNIT", "MAKE", "WEAR"):
            return self._do_knit(noun, loc), False
        if verb in ("READ", "EXAMINE", "X"):
            return self._examine(noun, loc), False

        # Movement
        if verb in ("N", "NORTH") or (verb == "GO" and noun in ("N", "NORTH", "")):
            return self._go("N", loc), False
        if verb in ("S", "SOUTH") or (verb == "GO" and noun in ("S", "SOUTH", "")):
            return self._go("S", loc), False
        if verb in ("E", "EAST") or (verb == "GO" and noun in ("E", "EAST", "")):
            return self._go("E", loc), False
        if verb in ("W", "WEST") or (verb == "GO" and noun in ("W", "WEST", "")):
            return self._go("W", loc), False
        if verb in ("U", "UP") or (verb == "GO" and noun in ("U", "UP", "")):
            return self._go_up(loc), False
        if verb in ("D", "DOWN") or (verb == "GO" and noun in ("D", "DOWN", "")):
            return self._go_down(loc), False

        return None

    def _go(self, direction, loc):
        r = self.get_room(loc)
        if not r:
            return "You are nowhere."
        exits = r.get("exits", {})
        next_target = exits.get(direction)
        if next_target is None:
            return f"You can't go {direction} from here."
        if isinstance(next_target, str):
            if next_target == "floor_7":
                return f"TRANSITION:{next_target}:37"
            if next_target == "floor_5":
                return f"TRANSITION:{next_target}:51"
        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        if loc == 41:
            return f"TRANSITION:floor_7:37"
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 49:
            return f"TRANSITION:floor_5:51"
        return self._go("D", loc)

    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"
        room_items = self._room_items.get(loc, [])

        for item in list(room_items):
            if noun.lower() in item.lower() or item.lower() in noun.lower():
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.add_item(item)
                return f"You take the {item}."
        return "You don't see that here."

    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"
        for item in list(self.state.inventory):
            if noun.lower() in item.lower() or item.lower() in noun.lower():
                self.state.remove_item(item)
                self._room_items.setdefault(loc, []).append(item)
                return f"You drop the {item}."
        return "You're not carrying that."

    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"
        return "You can't figure out how to use that here."

    def _do_knit(self, noun, loc):
        inv = self.state.inventory
        if "BALL OF YARN" not in inv or "KNITTING NEEDLES" not in inv:
            return "You need BALL OF YARN and KNITTING NEEDLES to knit a suit."
        if self.suit_knitted:
            return "You've already knitted a suit."
        if loc != 48:
            return "You should find a comfortable spot to sit and knit."
        self.suit_knitted = True
        self.state.remove_item("BALL OF YARN")
        self.state.remove_item("KNITTING NEEDLES")
        self.state.add_item("HAND-KNIT SUIT")
        return (
            "You sit down at one of the break room tables and start knitting. "
            "It takes a while, but finally you have a rough but serviceable SUIT. "
            "It's not pretty, but it'll do. You put it on. "
            "You feel ready to face those office workers!"
        )

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "WORKER" in noun or "GIRL" in noun or "SEXY" in noun:
            if loc == 43:
                return (
                    "Several young women in business attire, chatting animatedly. "
                    "They don't seem threatening - they're just in the way. "
                    "You might need to be wearing something appropriate to pass."
                )
            return "No office workers here."

        if "YARN" in noun:
            if "BALL OF YARN" in self._room_items.get(loc, []) or "BALL OF YARN" in self.state.inventory:
                return "Red knitting yarn. You could KNIT something with needles."
            return "No yarn here."

        if "NEEDLE" in noun:
            if "KNITTING NEEDLES" in self._room_items.get(loc, []) or "KNITTING NEEDLES" in self.state.inventory:
                return "Sharp metal knitting needles."
            return "No needles here."

        if "SUIT" in noun:
            if "HAND-KNIT SUIT" in self.state.inventory:
                return "A rough but serviceable hand-knit suit."
            return "You don't have a suit."

        return "Nothing unusual."

    def _do_inventory(self):
        items = self.state.inventory
        if not items:
            return "You are empty-handed."
        return "You are carrying: " + ", ".join(items)

    def _look(self):
        loc = self.state.location
        r = self.get_room(loc)
        if not r:
            return "You are nowhere."
        desc = f"**{r['name']}**\n{r['desc']}"
        items = self._room_items.get(loc, [])
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
