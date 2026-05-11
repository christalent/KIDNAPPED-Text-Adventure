"""
KIDNAPPED! - Floor 5: The Mary Poppins Floor
"The weird one" — finding Mary Poppin's umbrella

Entry from Floor 6 via stairs DOWN -> Room 51.
Goal: Navigate the absurdist Mary Poppins-themed floor, find the umbrella, descend.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- BASIC DATA statements for Floor 5 items
"""

FLOOR_NUMBER = 5
NEXT_FLOOR_DOWN = 4

# --------------------------------------------------------------------
# Room map (Floor 5, rooms 51-59):
# Mary Poppins themed - whimsical and weird
#
# Items from BASIC DATA:
# Room 58: SIGN (fixed)
# Room 59: PUSH BUTTON (fixed)
# Room 65: FRONT DOOR (but this is floor 1)
# Room 53: GRAFFITI ON WALL (overlaps with floor 7)
# Room 61: FLUTE, SMALL BOOK (floor 4 overlap)
#
# This floor is intentionally weird per RetroGamesTroove.
# --------------------------------------------------------------------
ROOMS = {
    51: {
        "name": "CHILDE'S LANDING",
        "desc": (
            "You descend into a whimsical space. "
            "Striped wallpaper, floating candles (electric), a grand staircase. "
            "A sign reads 'FLOOR 5 - BYE-BYE.' "
            "The stairs UP lead back to Floor 6. "
            "The main hall extends NORTH."
        ),
        "exits": {"N": 52, "U": "floor_6"},
        "items": [],
    },
    52: {
        "name": "GRAND HALL",
        "desc": (
            "A grand hall decorated in a peculiar style - part Victorian, "
            "part cartoon, part dream. "
            "A SIGN on the wall reads: 'SIDE END OPEN MOST REVERSIBLE.' "
            "Doesn't make sense. "
            "Doorways lead in several directions."
        ),
        "exits": {"S": 51, "N": 53, "E": 54, "W": 55},
        "items": ["SIGN ON WALL"],
    },
    53: {
        "name": "UPSIDE DOWN ROOM",
        "desc": (
            "You enter a room where everything is upside down. "
            "Chandeliers hang from the floor, furniture clings to the ceiling. "
            "Someone has written GRAFFITI on the ceiling: "
            "'MARY POPPINS WAS HERE.' "
            "A doorway leads SOUTH."
        ),
        "exits": {"S": 52},
        "items": ["GRAFFITI ON WALL"],
    },
    54: {
        "name": "THE BIRD WOMAN'S PERCH",
        "desc": (
            "A small alcove overlooking an imaginary park. "
            "Stone birds perch on invisible ledges. "
            "A note reads: '2+2=5 OR 2+2=22.' "
            "It's nonsense but somehow profound. "
            "The main hall is to the WEST."
        ),
        "exits": {"W": 52, "N": 56},
        "items": [],
    },
    55: {
        "name": "DRAWING ROOM",
        "desc": (
            "A proper English drawing room. Tea service is laid out, "
            "though decades old and covered in dust. "
            "On the mantle: a SMALL UMBRELLA. "
            "It's not quite right - not THE umbrella, but close. "
            "The main hall is to the EAST."
        ),
        "exits": {"E": 52, "N": 57},
        "items": ["SMALL UMBRELLA"],
    },
    56: {
        "name": "MAGIC PIE SHOP",
        "desc": (
            "Tiny pies line the shelves, each labeled with impossible flavors: "
            "'REVERSIBLE PIE,' 'UP IS DOWN PIE,' 'FIVE DIMENSIONAL PIE.' "
            "A PUSH BUTTON is on the wall, labeled 'PUSH FOR MEANING.' "
            "The Bird Woman's Perch is to the SOUTH."
        ),
        "exits": {"S": 54, "E": 57},
        "items": ["PUSH BUTTON"],
    },
    57: {
        "name": "THE SUPER CALIFA GULATOR",
        "desc": (
            "You step into a room filled with spinning gears and mirrors. "
            "A machine labeled 'SUPER CALIFRAGILISTIC' whirs and clicks. "
            "It seems to be in working order but needs something to activate it. "
            "A NOTE on the machine reads: 'ONE PUSH TO BEGIN.' "
            "The Drawing Room is to the SOUTH. "
            "The Magic Pie Shop is to the WEST."
        ),
        "exits": {"S": 55, "W": 56, "N": 58},
        "items": [],
    },
    58: {
        "name": "JUMP CHAMBER",
        "desc": (
            "A room with a strange, springy floor. "
            "A sign reads: 'JUMPING RECOMMENDED.' "
            "In the center, a platform with a big red button. "
            "The Super Califragilator room is to the SOUTH."
        ),
        "exits": {"S": 57, "N": 59},
        "items": ["JUMP PLATFORM"],
    },
    59: {
        "name": "THE UMBRELLA VAULT",
        "desc": (
            "The final room of Floor 5. "
            "Umbrellas everywhere - hundreds of them, of every color. "
            "Most are ordinary. But in the center, in a glass case: "
            "MARY POPPINS' OWN UMBRELLA. "
            "It's not just an umbrella - it feels magical. "
            "A stairway leads DOWN to Floor 4."
        ),
        "exits": {"S": 58, "D": "floor_4"},
        "items": ["MAGIC UMBRELLA"],
    },
}

SPECIAL_ROOMS = {
    "floor_6": {"target": "floor_6", "landing_room": 49},
    "floor_4": {"target": "floor_4", "landing_room": 61},
}

class Floor5Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.umbrella_found = False
        self.pie_pressed = False

    def _init_items(self):
        return {
            52: ["SIGN ON WALL"],
            53: ["GRAFFITI ON WALL"],
            55: ["SMALL UMBRELLA"],
            56: ["PUSH BUTTON"],
            58: ["JUMP PLATFORM"],
            59: ["MAGIC UMBRELLA"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.umbrella_found = False
        self.pie_pressed = False

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
        if verb in ("USE", "PUSH", "PRESS"):
            return self._do_use(noun, loc), False
        if verb in ("JUMP"):
            return self._do_jump(noun, loc), False
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
            if next_target == "floor_6":
                return f"TRANSITION:{next_target}:49"
            if next_target == "floor_4":
                return f"TRANSITION:{next_target}:61"
        self.state.location = next_target
        return self._look()

    def _go_up(self, loc):
        if loc == 51:
            return f"TRANSITION:floor_6:49"
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 59:
            return f"TRANSITION:floor_4:61"
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

        if "UMBRELLA" in noun:
            if "MAGIC UMBRELLA" in inv:
                return "You open Mary Poppins' umbrella. A magical breeze lifts you momentarily!"
            if "SMALL UMBRELLA" in inv:
                return "A nice umbrella, but not the magical one."

        if "BUTTON" in noun or "PUSH" in noun:
            if loc == 56:
                self.pie_pressed = True
                return (
                    "You push the button. Somewhere, a tiny bell rings. "
                    "A trapdoor opens and a pie descends from above. "
                    "'REVERSIBLE PIE,' the label says. "
                    "You take it."
                )
            if loc == 58:
                return "The jump platform is for JUMPING, not pushing."

        return "You can't figure out how to use that here."

    def _do_jump(self, noun, loc):
        if loc == 58:
            return (
                "You leap onto the springy platform! BOING! "
                "You bounce high into the air. As you come down, "
                "you notice a hidden passage that only appears "
                "when you're at the apex of your jump. But you can't reach it now."
            )
        return "There's nothing to jump on here."

    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun = noun.upper()

        if "UMBRELLA" in noun:
            if "MAGIC UMBRELLA" in self._room_items.get(loc, []) or "MAGIC UMBRELLA" in self.state.inventory:
                return "Mary Poppins' magical umbrella. It's beautiful - cherry red with a curved handle."
            if "SMALL UMBRELLA" in self._room_items.get(loc, []) or "SMALL UMBRELLA" in self.state.inventory:
                return "A nice umbrella, but ordinary. Not the magical one."
            return "No umbrella here."

        if "MACHINE" in noun or "CALIF" in noun:
            if loc == 57:
                return "The SUPER CALIFRAGILISTIC machine. It needs a push to start."
            return "No machine here."

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
