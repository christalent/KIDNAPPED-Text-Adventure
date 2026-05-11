"""
KIDNAPPED! - Floor 3: The Greenhouse
"Small plant, trap door, water cooler, paper cup, flute, and rope"

Entry from Floor 4 via Hyde passage DOWN -> Room 65.
Goal: Grow the plant to create a bridge/exit, descend to Floor 2.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 3 items
"""

FLOOR_NUMBER = 3
NEXT_FLOOR_DOWN = 2

# --------------------------------------------------------------------
# Room map (Floor 3, rooms 65-69):
# Greenhouse theme - plant growth puzzle
#
# Items from BASIC DATA:
# Room 58: WATER COOLER(-58), PAPER CUP(58) (overlaps)
# Room 59: SMALL-SIZED PLANT(59)
# Room 61: FLUTE(61), SMALL BOOK(61) (overlaps)
# Room 69: INDIAN ROPE(-69)
#
# Puzzle: WATER the plant → grows huge → creates path
# --------------------------------------------------------------------
ROOMS = {
    65: {
        "name": "GREENHOUSE ENTRANCE",
        "desc": (
            "You emerge from the Hyde passage into a warm, humid space. "
            "Glass walls fogged with condensation. The smell of earth and green things. "
            "A sign reads 'FLOOR 3 - BOTANICAL LABORATORY.' "
            "Vines creep in from the glass ceiling. "
            "The passage UP leads back to Floor 4. "
            "The greenhouse extends NORTH."
        ),
        "exits": {"N": 66, "U": "floor_4"},
        "items": [],
    },
    66: {
        "name": "TROPICAL SECTION",
        "desc": (
            "Lush tropical plants everywhere - orchids, ferns, vines. "
            "A WATER COOLER stands in the corner, still dispensing. "
            "PAPER CUPS stacked next to it. "
            "A SMALL PLANT in a pot sits on a bench - it's tiny but healthy. "
            "The entrance is to the SOUTH. "
            "The greenhouse continues NORTH and EAST."
        ),
        "exits": {"S": 65, "N": 67, "E": 68},
        "items": ["WATER COOLER", "PAPER CUP", "SMALL PLANT"],
    },
    67: {
        "name": "CACTUS CORNER",
        "desc": (
            "A dry section devoted to cacti and succulents. "
            "Sand on the floor, heat in the air. "
            "An old FLUTE lies abandoned on a cactus stand - "
            "someone's left it behind. "
            "The tropical section is to the SOUTH."
        ),
        "exits": {"S": 66},
        "items": ["FLUTE"],
    },
    68: {
        "name": "TRAP DOOR CHAMBER",
        "desc": (
            "A strange room with a TRAP DOOR in the ceiling. "
            "It leads UP to somewhere - but it's too high to reach. "
            "Below the trap door: a bed of rocks and dirt, "
            "carefully arranged. "
            "The tropical section is to the WEST."
        ),
        "exits": {"W": 66, "U": 69},
        "items": [],
    },
    69: {
        "name": "ABOVE THE TRAP DOOR",
        "desc": (
            "You climb through the trap door to find... the roof? "
            "No, another part of the building. "
            "An INDIAN ROPE hangs from a beam - coiled and waiting. "
            "A trap door in the floor leads back DOWN. "
            "A stairway leads DOWN to Floor 2."
        ),
        "exits": {"D": 68, "N": "floor_2"},
        "items": ["INDIAN ROPE"],
    },
}

SPECIAL_ROOMS = {
    "floor_4": {"target": "floor_4", "landing_room": 68},
    "floor_2": {"target": "floor_2", "landing_room": 69},
}

class Floor3Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.plant_watered = False
        self.plant_grown = False

    def _init_items(self):
        return {
            66: ["WATER COOLER", "PAPER CUP", "SMALL PLANT"],
            67: ["FLUTE"],
            69: ["INDIAN ROPE"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.plant_watered = False
        self.plant_grown = False

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
        if verb in ("USE", "WATER"):
            return self._do_use(noun, loc), False
        if verb in ("OPEN"):
            return self._do_open(noun, loc), False
        if verb in ("PLAY"):
            return self._do_play(noun, loc), False
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
            if next_target == "floor_4":
                return f"TRANSITION:{next_target}:68"
            if next_target == "floor_2":
                return f"TRANSITION:{next_target}:69"
        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        if loc == 65:
            return "The glass ceiling is too high to reach. You need something to climb."
        if loc == 68:
            return self._go("U", loc)
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 69:
            return f"TRANSITION:floor_2:69"
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

        if "WATER" in noun or "COOLER" in noun or "CUP" in noun:
            if loc == 66:
                if "PAPER CUP" not in inv:
                    return "You need a cup to get water from the cooler."
                if self.plant_watered:
                    return "The plant has already been watered."
                if "SMALL PLANT" not in self._room_items.get(66, []) and "HUGE PLANT" not in self._room_items.get(66, []):
                    return "There's no plant here to water."
                self.plant_watered = True
                return (
                    "You fill the paper cup with water from the cooler "
                    "and pour it over the soil of the SMALL PLANT. "
                    "For a moment, nothing happens. "
                    "Then... the plant begins to grow."
                )

        if "PLANT" in noun:
            if loc == 66:
                if self.plant_grown:
                    return "The plant has grown into a massive vine structure. It could hold your weight."
                if self.plant_watered:
                    self.plant_grown = True
                    self._room_items[66] = ["HUGE PLANT", "WATER COOLER", "PAPER CUP"]
                    return (
                        "The plant GROWS. Rapidly. Vines explode from the pot, "
                        "twisting and reaching upward, filling the room. "
                        "The main vine extends toward the trap door in the ceiling - "
                        "you could climb it!"
                    )
                return "A small plant in a pot. It looks healthy. Maybe it needs water."

        return "You can't figure out how to use that here."

    def _do_open(self, noun, loc):
        if "TRAP" in noun or "DOOR" in noun:
            if loc == 68:
                if self.plant_grown:
                    return "The plant has already created a path to the trap door."
                return "The trap door is too high to reach. You need something to climb."
        return "You can't open that."

    def _do_play(self, noun, loc):
        if "FLUTE" in noun or "MUSIC" in noun:
            if loc == 67:
                if "FLUTE" not in self.state.inventory:
                    return "You don't have the flute."
                return (
                    "You play a haunting melody on the flute. "
                    "The notes echo through the greenhouse. "
                    "Somewhere, a plant seems to sway in response."
                )
            return "There's no flute here."
        return "You can't play that."

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "PLANT" in noun:
            if loc == 66:
                if self.plant_grown:
                    return "A massive, room-filling plant. Its vines reach the ceiling and beyond."
                if self.plant_watered:
                    return "The plant is growing rapidly. Vines are beginning to spread."
                return "A small plant in a terracotta pot. Healthy but small. Water might help it grow."
            return "No plant here."

        if "TRAP" in noun or "DOOR" in noun:
            if loc == 68:
                if self.plant_grown:
                    return "A vine extends up to the trap door. You could climb it."
                return "The trap door is 15 feet up. You can't reach it without climbing."
            return "No trap door here."

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
