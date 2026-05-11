"""
KIDNAPPED! - Floor 2: The Quicksand Floor
"Small book, some quicksand, rope, and a piano"

Entry from Floor 3 via stairs DOWN -> Room 69.
Goal: Play piano → rope stretches → cross quicksand → descend to Floor 1.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 2 items
"""

FLOOR_NUMBER = 2
NEXT_FLOOR_DOWN = 1

# --------------------------------------------------------------------
# Room map (Floor 2, rooms 69-73):
# Quicksand / piano puzzle
#
# Items from BASIC DATA:
# Room 63: PIANO(-63), LONG ROPE(63) (overlaps with floor 4)
# Room 61: SMALL BOOK(61) (overlaps)
# Room 65: FRONT DOOR(-65) (overlaps with floor 1)
#
# Puzzle: PLAY PIANO → rope stretches tight → cross quicksand
# --------------------------------------------------------------------
ROOMS = {
    69: {
        "name": "QUICKSAND EDGE",
        "desc": (
            "You descend into a vast underground chamber. "
            "The floor is sandy, and in the center: a massive patch of QUICKSAND. "
            "It looks bottomless. On the far side, you can see a stairway leading DOWN. "
            "A LONG ROPE is coiled on a tent stake on this side. "
            "A PIANO sits against the west wall. "
            "The entrance is to the SOUTH."
        ),
        "exits": {"S": 70, "N": 71},
        "items": ["LONG ROPE"],
    },
    70: {
        "name": "ROPE STAKES AREA",
        "desc": (
            "Near the quicksand, a tent STAKE is driven into the ground. "
            "The rope could be tied here. "
            "A SMALL BOOK lies in the sand. "
            "The quicksand edge is to the NORTH. "
            "A narrow ledge runs EAST along the wall."
        ),
        "exits": {"N": 69, "E": 72},
        "items": ["SMALL BOOK", "TENT STAKE"],
    },
    71: {
        "name": "QUICKSAND CROSSING",
        "desc": (
            "You stand at the edge of the quicksand. "
            "The rope - when properly stretched - would connect here to the far side. "
            "The far side (north) has a stairway DOWN to Floor 1. "
            "The rope stakes area is to the SOUTH."
        ),
        "exits": {"S": 69},
        "items": [],
    },
    72: {
        "name": "PIANO ALCOVE",
        "desc": (
            "A small alcove with a dusty PIANO. "
            "Sheet music sits on the stand, open to a waltz. "
            "Someone has been playing here. "
            "The rope stakes area is to the WEST."
        ),
        "exits": {"W": 70, "N": 73},
        "items": ["PIANO"],
    },
    73: {
        "name": "BOOKSHELF NICHE",
        "desc": (
            "A small niche lined with old books and papers. "
            "One book lies open: it describes how to cross quicksand using rope tension. "
            "'...play a sustained chord to tighten the rope...' "
            "The piano alcove is to the SOUTH."
        ),
        "exits": {"S": 72},
        "items": ["TIGHTROPE BOOK"],
    },
}

SPECIAL_ROOMS = {
    "floor_3": {"target": "floor_3", "landing_room": 69},
    "floor_1": {"target": "floor_1", "landing_room": 65},
}

class Floor2Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.rope_tied = False
        self.rope_stretched = False
        self.book_read = False

    def _init_items(self):
        return {
            69: ["LONG ROPE"],
            70: ["SMALL BOOK", "TENT STAKE"],
            72: ["PIANO"],
            73: ["TIGHTROPE BOOK"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.rope_tied = False
        self.rope_stretched = False
        self.book_read = False

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
        if verb in ("USE", "TIE", "KNOT"):
            return self._do_use(noun, loc), False
        if verb in ("PLAY"):
            return self._do_play(noun, loc), False
        if verb in ("TIE"):
            return self._do_tie(noun, loc), False
        if verb in ("READ", "EXAMINE", "X"):
            return self._examine(noun, loc), False
        if verb in ("CROSS"):
            return self._do_cross(noun, loc), False

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
            if next_target == "floor_3":
                return f"TRANSITION:{next_target}:69"
            if next_target == "floor_1":
                return f"TRANSITION:{next_target}:65"
        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        return "You can't go up from here."

    def _go_down(self, loc):
        if loc == 71 and self.rope_stretched:
            return f"TRANSITION:floor_1:65"
        if loc == 71:
            return "The quicksand blocks your path. You need a way to cross safely."
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

        if "ROPE" in noun:
            if "LONG ROPE" not in inv:
                return "You don't have the rope."
            if self.rope_tied:
                return "The rope is already tied to the stake."
            if loc == 70:
                return self._do_tie("ROPE", loc)
            return "You should TIE the rope to the stake first."

        if "STAKE" in noun or "TENT" in noun:
            if loc == 70:
                return "The tent stake is driven firmly into the ground. You need rope to tie to it."
            return "There's no stake here."

        return "You can't figure out how to use that here."

    def _do_tie(self, noun, loc):
        if loc != 70:
            return "There's nothing to tie the rope to here."
        if "LONG ROPE" not in self.state.inventory:
            return "You don't have the rope."
        if self.rope_tied:
            return "The rope is already tied."
        self.rope_tied = True
        self.state.remove_item("LONG ROPE")
        return (
            "You tie the LONG ROPE securely to the TENT STAKE. "
            "The other end dangles across the quicksand toward the far side. "
            "It's loose though - you need to tighten it somehow. "
            "Maybe the PIANO could help create some vibration to tighten a rope?"
        )

    def _do_play(self, noun, loc):
        if "PIANO" in noun or "MUSIC" in noun or noun == "":
            if loc != 72:
                return "There's no piano here."
            if not self.rope_tied:
                return (
                    "You play a beautiful waltz on the piano. "
                    "The notes echo through the chamber. "
                    "But nothing special happens - the rope isn't here to benefit from the vibrations."
                )
            if self.rope_stretched:
                return "The rope is already stretched tight from your previous playing."
            self.rope_stretched = True
            return (
                "You play a sustained, thunderous chord on the piano. "
                "The vibrations travel through the ground, up the rope... "
                "and PING! The rope snaps taut! "
                "It now forms a tightrope across the quicksand. "
                "You can now CROSS north to the far side."
            )

        if "FLUTE" in noun or "BOOK" in noun:
            return "You can't play that."

        return "Play what?"

    def _do_cross(self, noun, loc):
        if loc == 69:
            return "You can't cross from here - the rope is on the other side of the quicksand."
        if loc == 71:
            if not self.rope_stretched:
                return "There's no way to cross the quicksand. The rope is loose and dangles uselessly."
            return f"TRANSITION:floor_1:65"
        if loc == 72:
            return "You need to be at the quicksand edge to cross."
        return "There's nothing to cross here."

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "QUICKSAND" in noun:
            return (
                "Dark, murky, bottomless-looking quicksand. "
                "It would swallow you in seconds. "
                "A tightrope - if properly stretched - could get you across."
            )

        if "ROPE" in noun:
            if "LONG ROPE" in self.state.inventory:
                if self.rope_tied:
                    return "The rope is tied to the stake, dangling across the quicksand."
                return "A long rope. Could be useful for crossing the quicksand."
            if self.rope_tied:
                return "A rope stretched across the quicksand, tied to the stake."
            return "No rope here."

        if "BOOK" in noun:
            if "TIGHTROPE BOOK" in self._room_items.get(73, []) or "TIGHTROPE BOOK" in self.state.inventory:
                return self.book_read and "The book explains how to tighten a rope using musical vibrations."
            if "SMALL BOOK" in self._room_items.get(70, []) or "SMALL BOOK" in self.state.inventory:
                return "A worn book. The text is too faded to read."
            return "No book here."

        if "PIANO" in noun:
            if loc == 72:
                return "An old upright piano. Dusty but playable. The strings could create quite a vibration."
            return "No piano here."

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

        if loc == 69 and self.rope_tied and not self.rope_stretched:
            desc += "\n\nThe rope is tied to the stake, dangling across the quicksand. Loose."
        elif loc == 69 and self.rope_stretched:
            desc += "\n\nA tightrope of rope spans the quicksand! You can CROSS north."

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
