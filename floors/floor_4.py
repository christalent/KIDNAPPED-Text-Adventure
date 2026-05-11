"""
KIDNAPPED! - Floor 4: Jekyll/Hyde Laboratory
"Turn yourself into Mr. Hyde to deal with the steel door"

Entry from Floor 5 via stairs DOWN -> Room 61.
Goal: Find potion, drink it, transform into Hyde, open steel door, descend.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 4 items
"""

FLOOR_NUMBER = 4
NEXT_FLOOR_DOWN = 3

# --------------------------------------------------------------------
# Room map (Floor 4, rooms 61-69):
# Jekyll/Hyde transformation theme
#
# Items from BASIC DATA:
# Room 61: FLUTE(61), SMALL BOOK(61)
# Room 63: PIANO(-63), LONG ROPE(63)
#
# Puzzle: DRINK POTION → become Mr. Hyde → can open steel door
# --------------------------------------------------------------------
ROOMS = {
    61: {
        "name": "LAB ENTRANCE",
        "desc": (
            "You descend into a dimly lit laboratory. "
            "The air smells of chemicals and old leather. "
            "Glass beakers, bubbling retorts, stacks of books. "
            "A sign reads 'FLOOR 4 - PRIVATE LABORATORY.' "
            "The stairs UP lead back to Floor 5. "
            "The lab extends NORTH."
        ),
        "exits": {"N": 62, "U": "floor_5"},
        "items": ["SMALL BOOK"],
    },
    62: {
        "name": "MAIN LABORATORY",
        "desc": (
            "The heart of the laboratory. "
            "A large PIANO dominates one corner - old, dusty. "
            "Bookshelves line the walls, stuffed with journals. "
            "A note lies on the desk. "
            "The entrance is to the SOUTH. "
            "A doorway leads EAST to the experiment chamber."
        ),
        "exits": {"S": 61, "E": 63, "N": 64},
        "items": ["SMALL BOOK", "PIANO"],
    },
    63: {
        "name": "POTION STORAGE",
        "desc": (
            "Rows of labeled bottles line the shelves. "
            "POISON! DANGER! CAUTION! "
            "One bottle labeled 'EXPERIMENTAL - DR. J' sits apart from the rest. "
            "A LONG ROPE hangs from a hook on the wall. "
            "The main lab is to the WEST."
        ),
        "exits": {"W": 62, "N": 65},
        "items": ["EXPERIMENTAL POTION", "LONG ROPE"],
    },
    64: {
        "name": "STORAGE CLOSET",
        "desc": (
            "A cramped storage closet. Old equipment, spare parts. "
            "A FLUTE lies on a shelf - someone's forgotten hobby. "
            "The main lab is to the SOUTH."
        ),
        "exits": {"S": 62},
        "items": ["FLUTE"],
    },
    65: {
        "name": "TRANSFORMATION CHAMBER",
        "desc": (
            "A reinforced chamber with heavy restraints bolted to the floor. "
            "Mirrors on all walls - you'd see yourself from every angle. "
            "A steel door on the north wall is sealed tight. "
            "The potion storage is to the SOUTH. "
            "A small reading nook is to the WEST."
        ),
        "exits": {"S": 63, "E": 67, "W": 66},
        "items": [],
    },
    66: {
        "name": "READING ALCOVE",
        "desc": (
            "A small, cozy nook with a worn leather chair. "
            "A journal lies open on the side table. "
            "It describes the transformation process: "
            "'...the serum unlocks the darker aspects of personality...' "
            "The transformation chamber is to the EAST."
        ),
        "exits": {"E": 65},
        "items": ["RESEARCH JOURNAL"],
    },
    67: {
        "name": "EAST CORRIDOR",
        "desc": (
            "A narrow corridor leading east from the transformation chamber. "
            "The steel door is here, but it's locked. "
            "Only Mr. Hyde could open it. "
            "The transformation chamber is to the WEST."
        ),
        "exits": {"W": 65, "N": 68},
        "items": [],
    },
    68: {
        "name": "HYDE'S PASSAGE",
        "desc": (
            "A secret passage, only accessible after the steel door opens. "
            "Dusty and narrow, but it leads DOWN. "
            "The corridor is to the SOUTH."
        ),
        "exits": {"S": 67, "D": "floor_3"},
        "items": [],
        "_requires_hyde": True,
    },
}

SPECIAL_ROOMS = {
    "floor_5": {"target": "floor_5", "landing_room": 59},
    "floor_3": {"target": "floor_3", "landing_room": 65},
}

class Floor4Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.hyded = False  # True when transformed into Hyde

    def _init_items(self):
        return {
            61: ["SMALL BOOK"],
            62: ["SMALL BOOK", "PIANO"],
            63: ["EXPERIMENTAL POTION", "LONG ROPE"],
            64: ["FLUTE"],
            66: ["RESEARCH JOURNAL"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.hyded = False

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
        if verb in ("USE", "DRINK"):
            return self._do_use(noun, loc), False
        if verb in ("OPEN", "UNLOCK"):
            return self._do_open(noun, loc), False
        if verb in ("READ", "EXAMINE", "X"):
            return self._examine(noun, loc), False
        if verb in ("PLAY"):
            return self._do_play(noun, loc), False

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

        # Special: Hyde's passage requires being Hyde
        if isinstance(next_target, int) and next_target == 68 and not self.hyded:
            return "The passage is blocked by rubble. Only someone small and agile could squeeze through."

        if isinstance(next_target, str):
            if next_target == "floor_5":
                return f"TRANSITION:{next_target}:59"
            if next_target == "floor_3":
                return f"TRANSITION:{next_target}:65"
        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        if loc == 61:
            return f"TRANSITION:floor_5:59"
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 68:
            if not self.hyded:
                return "The passage is too narrow for normal access. Only Hyde could squeeze through."
            return f"TRANSITION:floor_3:65"
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
        inv = self.state.inventory

        if "POTION" in noun or "DRINK" in noun:
            if "EXPERIMENTAL POTION" not in inv:
                return "You don't have the potion."
            if self.hyded:
                return "You're already Hyde."
            if loc != 65:
                return "You should drink the potion in the transformation chamber."
            self.hyded = True
            self.state.remove_item("EXPERIMENTAL POTION")
            self.state.add_item("HYDE FORM")
            return (
                "You drink the experimental potion. "
                "Your bones crack and reshape. Your skin crawls. "
                "In the mirrors you see yourself transform - "
                "smaller, meaner, hungrier. You are MR. HYDE. "
                "The steel door can now be opened."
            )

        if "ROPE" in noun:
            if "LONG ROPE" not in inv:
                return "You don't have the rope."
            return "The rope might be useful for something, but not right now."

        return "You can't figure out how to use that here."

    def _do_open(self, noun, loc):
        if "DOOR" in noun or "STEEL" in noun:
            if loc != 67:
                return "There's no steel door here."
            if not self.hyded:
                return (
                    "The steel door is locked tight. It's completely immovable - "
                    "nothing short of superhuman strength could open it. "
                    "Perhaps if you were... different... you could manage it."
                )
            self._room_items[67] = []
            return (
                "HYDE SMASH! You throw your weight against the steel door. "
                "It buckles and swings open with a shriek of metal. "
                "The secret passage beyond awaits."
            )

        if "BOOK" in noun or "JOURNAL" in noun:
            if "SMALL BOOK" in inv or "RESEARCH JOURNAL" in inv:
                return self._examine(noun, loc)
            return "You don't have anything to read."

        return "You can't open that."

    def _do_play(self, noun, loc):
        if "PIANO" in noun or "MUSIC" in noun:
            if loc == 62:
                return (
                    "You play a jaunty tune on the old piano. "
                    "It echoes through the lab. Nothing special happens, "
                    "but it sounds nice."
                )
            return "There's no piano here."
        return "You can't play that."

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "HYDE" in noun or "MR." in noun:
            if self.hyded:
                return "You are MR. HYDE. Small, vicious, and very strong."
            return "You're yourself - Dr. Jekyll. Normal, average, not very Hyde-like at all."

        if "DOOR" in noun or "STEEL" in noun:
            if loc == 67:
                if self.hyded:
                    return "The steel door is open. A dark passage awaits beyond."
                return "A massive steel door, sealed tight. It would take superhuman strength to open."
            return "No steel door here."

        if "POTION" in noun or "BOTTLE" in noun:
            if "EXPERIMENTAL POTION" in self._room_items.get(loc, []) or "EXPERIMENTAL POTION" in self.state.inventory:
                return "A dark, viscous liquid in a glass vial. Labeled 'DR. J - EXPERIMENTAL.' Smells like sulfur and regret."
            return "No potion here."

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
        if loc == 65 and self.hyded:
            desc += "\n\nYou are MR. HYDE. The strongest version of yourself."
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
