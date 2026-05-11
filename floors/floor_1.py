"""
KIDNAPPED! - Floor 1: Ground Floor - ESCAPE!
"A burglar's mask blocks your way east. He has the remains of the kidnapper in his mouth."

Entry from Floor 2 via tightrope CROSS -> Room 65.
Goal: Deal with the alligator and burglar's mask, reach the front door, ESCAPE!

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 1 items
"""

FLOOR_NUMBER = 1
NEXT_FLOOR_DOWN = None  # This is the final floor!

# --------------------------------------------------------------------
# Room map (Floor 1, rooms 65-75):
# Ground floor - final escape
#
# Items from BASIC DATA:
# Room 65: FRONT DOOR(-65), ALLIGATOR(-65)
#
# Win condition: Navigate past the burglar's mask + alligator,
# reach the FRONT DOOR and ESCAPE!
# --------------------------------------------------------------------
ROOMS = {
    65: {
        "name": "MAIN FLOOR - ENTRANCE HALL",
        "desc": (
            "You step into the grand entrance hall of the building. "
            "Marble floors, a grand staircase - this is the ground floor. "
            "The front door is directly ahead, your escape! "
            "But an ALLIGATOR blocks the path, jaw agape. "
            "A burglar's mask hangs on a hook nearby. "
            "The stairway UP leads back to Floor 2. "
            "The hall extends NORTH toward the exit."
        ),
        "exits": {"N": 66, "U": "floor_2"},
        "items": ["BURGLAR'S MASK"],
    },
    66: {
        "name": "NORTH HALL",
        "desc": (
            "The hallway north of the entrance. "
            "Old paintings watch you from the walls. "
            "The alligator is just to the SOUTH. "
            "A doorway leads EAST, and another NORTH."
        ),
        "exits": {"S": 65, "N": 67, "E": 68},
        "items": [],
    },
    67: {
        "name": "SIDE ROOM",
        "desc": (
            "A small side room with a worn couch and old magazines. "
            "Nothing of interest - but a clear path back SOUTH."
        ),
        "exits": {"S": 66},
        "items": [],
    },
    68: {
        "name": "NEAR THE EXIT",
        "desc": (
            "You approach the front door. "
            "The ALLIGATOR is close - it's massive, teeth like knives. "
            "The FRONT DOOR is right there - your freedom! "
            "The hallway is to the WEST."
        ),
        "exits": {"W": 66, "E": "front_door"},
        "items": [],
    },
}

SPECIAL_ROOMS = {
    "floor_2": {"target": "floor_2", "landing_room": 69},
}

class Floor1Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.mask_worn = False
        self.alligator_dead = False
        self.escaped = False

    def _init_items(self):
        return {
            65: ["BURGLAR'S MASK"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.mask_worn = False
        self.alligator_dead = False
        self.escaped = False

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
        if verb in ("USE", "WEAR"):
            return self._do_use(noun, loc), False
        if verb in ("OPEN"):
            return self._do_open(noun, loc), False
        if verb in ("EXAMINE", "READ", "X"):
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
            if next_target == "floor_2":
                return f"TRANSITION:{next_target}:69"
            if next_target == "front_door":
                return self._try_escape()

        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        if loc == 65:
            return f"TRANSITION:floor_2:69"
        return "You can't go up from here."

    def _try_escape(self):
        if not self.alligator_dead:
            return (
                "The ALLIGATOR lunges as you approach the door! "
                "You barely dodge back. You'll need to deal with it first."
            )
        self.escaped = True
        return (
            "YOU ESCAPE!\n\n"
            "You push through the front door and burst into the cool night air. "
            "You're free! The building looms behind you. "
            "You don't look back.\n\n"
            "========================================\n"
            "  CONGRATULATIONS! YOU ESCAPED!\n"
            "  KIDNAPPED! - A SoftSide Adventure\n"
            "  (c) 1980 by Peter Kirsch\n"
            "========================================\n\n"
            "Thank you for playing!"
        )

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

        if "MASK" in noun or "WEAR" in noun:
            if "BURGLAR'S MASK" not in inv:
                return "You don't have the mask."
            if self.mask_worn:
                return "You're already wearing the mask."
            self.mask_worn = True
            return (
                "You pull on the BURGLAR'S MASK. "
                "Your face is now hidden. "
                "The alligator might not recognize you as a threat now."
            )

        if "FLASHLIGHT" in noun or "LIGHT" in noun:
            if "FLASHLIGHT" not in inv:
                return "You don't have a flashlight."
            if loc in (65, 66, 68):
                return "The alligator doesn't seem affected by the light. You need something else."

        return "You can't figure out how to use that here."

    def _do_open(self, noun, loc):
        if "DOOR" in noun or "FRONT" in noun:
            if loc == 68:
                return self._try_escape()
            if loc == 65:
                return "The front door is right there, but the alligator blocks the way."
            return "There's no door to open here."

        if "ALLIGATOR" in noun or "GATOR" in noun:
            return self._examine("ALLIGATOR", loc)

        return "You can't open that."

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "ALLIGATOR" in noun or "GATOR" in noun:
            if loc in (65, 66, 68):
                if self.alligator_dead:
                    return "The alligator lies still. It won't be bothering anyone."
                if self.mask_worn:
                    return "The alligator eyes you warily. It's confused - you look like a burglar, not prey. Maybe it will let you pass if you're careful."
                return (
                    "A massive alligator, teeth bared, blocking the path to the front door. "
                    "It's very much alive and very hungry. "
                    "It seems to recognize you as prey. "
                    "A burglar's mask might confuse it."
                )
            return "No alligator here."

        if "MASK" in noun or "BURGLAR" in noun:
            if "BURGLAR'S MASK" in self._room_items.get(loc, []) or "BURGLAR'S MASK" in self.state.inventory:
                if self.mask_worn:
                    return "You're wearing the burglar's mask. It smells like sweat and crime."
                return "A dark mask with eye holes. The kind a burglar would wear."
            return "No mask here."

        if "DOOR" in noun or "FRONT" in noun:
            if loc == 65 or loc == 68:
                return "The front door. Freedom is just on the other side - if you can get past the alligator."
            return "No front door here."

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

        if self.escaped:
            return desc

        if loc == 65:
            if self.alligator_dead:
                desc = desc.replace("an ALLIGATOR blocks the path", "a dead ALLIGATOR blocks the path")
            if self.mask_worn:
                desc += "\n\nYou're wearing the burglar's mask."

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
