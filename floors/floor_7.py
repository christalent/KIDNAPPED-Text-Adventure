"""
KIDNAPPED! - Floor 7: The Bank Vault
Hardest floor — wrest a dollar from a burglar.

Entry from Floor 8 via stairs DOWN -> Room 31.
Goal: Navigate the vault, deal with the burglar, descend to Floor 6.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review: https://www.retrogamestrove.com/game-149-kidnapped-1980/
- Confirmed bidirectional pairs: 31↔32, 32↔39, 36↔37
"""

FLOOR_NUMBER = 7
NEXT_FLOOR_DOWN = 6

# --------------------------------------------------------------------
# Room map (Floor 7, rooms 31-39 + vault 55-57):
# Based on BASIC analysis + RetroGamesTroove review
#
# Layout (approximate, based on confirmed pairs):
#   [33] --- [32] Bank Floor --- [31] Entry from Floor 8
#    |          |                    |
#   [39]      [36]---[37]          [35] Stairs UP
#   (vault   (comb.
#    office   office)
#                |
#               [38]---[34]---[33]
#                       |
#                      [35]
#
# Confirmed pairs: 31↔32, 32↔39, 36↔37
# Items from BASIC DATA:
# Room 37: SMALL KEY (takeable)
# Room 39: BALL OF YARN (takeable), KNITTING NEEDLES (takeable, room 40)
# Room 55: STEEL DOOR (fixed, locked)
# Room 56: JAR OF YELLOW SOLUTION, JAR OF FLUID (takeable)
# Room 57: KID'S SLIDE (fixed)
# Room 32: STRING VENDING MACHINE (fixed), TIN FOIL (takeable, room 33)
# Room 30: GUN (takeable)
# Room 33: LOCKED DOOR (fixed)
# --------------------------------------------------------------------
ROOMS = {
    # === FLOOR 7 LAYOUT ===
    # Confirmed pairs: 31↔32, 36↔37, 37↔55, 55↔56
    # The BASIC OCR is too garbled for full reconstruction.
    # Layout built from confirmed pairs + RetroGamesTroove review.
    #
    #   [33 Storage]---[31 Entry]---[32 Main Bank]---[36 Comb. Office]---[37 Antechamber]
    #                     |               |                              |
    #                   [38 Corridor]---[39 Vault Office]              [55 Vault]---[56 Playroom]
    #                                                (burglar here)
    # --------------------------------------------------------------------
    31: {
        "name": "BANK ENTRY",
        "desc": (
            "You descend the stairs into a wide marble foyer. "
            "The air smells of old money and dust. "
            "Ornate frescoes line the ceiling, now cracked and peeling. "
            "A sign reads 'FIRST NATIONAL BANK OF DESCENT.' "
            "To the NORTH, the main bank floor stretches out. "
            "To the WEST, a small storage room. "
            "The stairs lead UP back to Floor 8."
        ),
        "exits": {"N": 32, "W": 33, "U": "floor_8"},
        "items": [],
    },
    32: {
        "name": "MAIN BANK FLOOR",
        "desc": (
            "You're in the heart of the old bank. "
            "Rotting velvet ropes section off the former teller windows. "
            "A STRING VENDING MACHINE stands against the west wall - "
            "it takes bills, dispenses unknown items. "
            "To the EAST, a combination office. "
            "To the NORTH, a vault office. "
            "The entry is to the SOUTH."
        ),
        "exits": {"S": 31, "E": 36, "N": 39},
        "items": ["STRING VENDING MACHINE"],
    },
    33: {
        "name": "VAULT STORAGE",
        "desc": (
            "A small storage room adjacent to the vault. "
            "Shelves of old bank records, rusted metal boxes. "
            "A SMALL KEY lies on a shelf - someone dropped it. "
            "A JAR OF YELLOW SOLUTION sits on another shelf. "
            "To the EAST, the bank entry."
        ),
        "exits": {"E": 31},
        "items": ["SMALL KEY", "JAR OF YELLOW SOLUTION"],
    },
    36: {
        "name": "COMBINATION OFFICE",
        "desc": (
            "A cramped office lined with safety deposit boxes. "
            "A single desk holds a TIN FOIL sheet and some papers. "
            "The walls are covered in combination notes. "
            "A BALL OF YARN sits on the desk - someone's hobby left behind. "
            "To the WEST, the main bank floor. "
            "To the EAST, the vault antechamber."
        ),
        "exits": {"W": 32, "E": 37},
        "items": ["TIN FOIL", "BALL OF YARN"],
    },
    37: {
        "name": "VAULT ANTECHAMBER",
        "desc": (
            "You stand in the vault antechamber. "
            "A massive STEEL DOOR to the north is closed and locked. "
            "The door has a keyhole - a SMALL KEY might open it. "
            "Through a gap in the door, you glimpse gold inside. "
            "To the WEST, the combination office. "
            "To the SOUTH, the main bank floor."
        ),
        "exits": {"W": 36, "N": 55, "S": 32},
        "items": [],
    },
    38: {
        "name": "BANK CORRIDOR",
        "desc": (
            "A narrow corridor runs north-south through the old bank. "
            "Faded photographs of prosperous merchants line the walls. "
            "A heavy LOCKED DOOR blocks the east passage. "
            "The corridor continues NORTH to the vault office and SOUTH to the entry."
        ),
        "exits": {"S": 31, "N": 39},
        "items": [],
    },
    39: {
        "name": "VAULT OFFICE",
        "desc": (
            "A private office inside the vault area. "
            "A BURGLAR crouches behind the desk, clutching a DOLLAR BILL. "
            "He's watching you warily. "
            "On the desk: KNITTING NEEDLES and some documents. "
            "The BURGLAR has the remains of the kidnapper in his mouth. "
            "The corridor is to the SOUTH."
        ),
        "exits": {"S": 38},
        "items": ["KNITTING NEEDLES"],
    },
    33: {
        "name": "OLD VAULT STORAGE",
        "desc": (
            "A small storage room adjacent to the vault. "
            "Shelves of old bank records, rusted metal boxes. "
            "A SMALL KEY lies on a shelf - someone dropped it. "
            "A JAR OF YELLOW SOLUTION sits on another shelf. "
            "To the EAST, the bank entry."
        ),
        "exits": {"E": 31},
        "items": ["SMALL KEY", "JAR OF YELLOW SOLUTION"],
    },
    55: {
        "name": "THE VAULT",
        "desc": (
            "You step inside the First National Bank vault. "
            "Gold bars and cash stacks fill the space - millions untouched "
            "since the bank closed. "
            "A child's slide - a KID'S SLIDE - has been set up from the "
            "vault to some lower level. "
            "There's also a JAR OF FLUID here - unlabeled. "
            "The antechamber is to the SOUTH."
        ),
        "exits": {"S": 37, "N": 56},
        "items": ["JAR OF FLUID", "KID'S SLIDE"],
    },
    56: {
        "name": "CHILD'S PLAYROOM",
        "desc": (
            "A small child's playroom connects to the vault area. "
            "Toys scattered everywhere, a small bed in the corner. "
            "Someone lived here after the bank closed. "
            "The vault is to the SOUTH."
        ),
        "exits": {"S": 55},
        "items": [],
    },
}

# --------------------------------------------------------------------
# Special room targets
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    "floor_8":  {"target": "floor_8",  "landing_room": 28},
    "floor_6":  {"target": "floor_6",  "landing_room": 41},
}


# --------------------------------------------------------------------
# Floor 7 Engine
# --------------------------------------------------------------------
class Floor7Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.vault_unlocked = False
        self.burglar_defeated = False
        self.dollar_taken = False
        self.gun_fired = False

    def _init_items(self):
        return {
            31: [],
            32: ["STRING VENDING MACHINE"],
            33: ["SMALL KEY", "JAR OF YELLOW SOLUTION"],
            36: ["TIN FOIL", "BALL OF YARN"],
            37: [],
            38: [],
            39: ["KNITTING NEEDLES"],
            55: ["JAR OF FLUID", "KID'S SLIDE"],
            56: [],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.vault_unlocked = False
        self.burglar_defeated = False
        self.dollar_taken = False
        self.gun_fired = False

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
            return self._describe_room(loc), False
        if verb in ("INVENTORY", "I"):
            return self._do_inventory(), False
        if verb in ("GET", "TAKE", "GRAB"):
            return self._do_get(noun, loc), False
        if verb in ("DROP", "PUT", "PLACE"):
            return self._do_drop(noun, loc), False
        if verb in ("USE", "APPLY", "GIVE"):
            return self._do_use(noun, loc), False
        if verb in ("OPEN", "UNLOCK"):
            return self._do_open(noun, loc), False
        if verb in ("READ", "EXAMINE", "X", "CHECK"):
            return self._examine(noun, loc), False
        if verb in ("SHOOT", "FIRE", "KILL"):
            return self._do_shoot(noun, loc), False
        if verb in ("PAY", "INSERT", "PUT"):
            return self._do_pay(noun, loc), False

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
            if next_target == "floor_8":
                return f"TRANSITION:{next_target}:28"
            if next_target == "floor_6":
                return f"TRANSITION:{next_target}:41"
            if next_target == "vault_door":
                if not self.vault_unlocked:
                    return "The steel vault door is locked. You need a SMALL KEY."
                return f"TRANSITION:vault:55"
        self.state.location = next_target
        return self._describe_room(next_target)

    def _go_up(self, loc):
        if loc == 31:
            return f"TRANSITION:floor_8:28"
        return self._go("U", loc)

    def _go_down(self, loc):
        # Can only descend via the slide in the vault or other special exit
        if loc == 55:
            return (
                "You climb onto the KID'S SLIDE and zoom down! "
                "You land in a new area - Floor 6."
            )
        return self._go("D", loc)

    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"
        room_items = self._room_items.get(loc, [])

        if "YARN" in noun:
            if loc == 36:
                if "BALL OF YARN" in room_items:
                    room_items.remove("BALL OF YARN")
                    self._room_items[36] = room_items
                    self.state.add_item("BALL OF YARN")
                    return "You take the BALL OF YARN."
            return "No yarn here."

        if "NEEDLE" in noun:
            if loc == 39:
                if "KNITTING NEEDLES" in room_items:
                    room_items.remove("KNITTING NEEDLES")
                    self._room_items[39] = room_items
                    self.state.add_item("KNITTING NEEDLES")
                    return "You take the KNITTING NEEDLES."
            return "No knitting needles here."

        if "TIN FOIL" in noun or "FOIL" in noun:
            if loc == 36:
                if "TIN FOIL" in room_items:
                    room_items.remove("TIN FOIL")
                    self._room_items[36] = room_items
                    self.state.add_item("TIN FOIL")
                    return "You take the TIN FOIL."
            return "No tin foil here."

        if "SOLUTION" in noun or "FLUID" in noun or "JAR" in noun:
            for room, items in list(self._room_items.items()):
                for item in list(items):
                    if "JAR" in item and (noun in item or noun in ["JAR", "SOLUTION", "FLUID"]):
                        items.remove(item)
                        self._room_items[room] = items
                        self.state.add_item(item)
                        return f"You take the {item}."

        if "DOLLAR" in noun or "BILL" in noun or "DOLLAR BILL" in noun:
            if loc == 39 and not self.dollar_taken:
                if self.burglar_defeated:
                    self.dollar_taken = True
                    self.state.add_item("DOLLAR BILL")
                    return "You carefully take the DOLLAR BILL from the burglar's things."
                return "The BURGLAR has the dollar. You'll need to deal with him first."

        if "GUN" in noun:
            if "GUN" in self.state.inventory:
                return "You're already carrying the gun."
            if loc == 30:  # Gun on floor 8 or somewhere
                return "The gun isn't on this floor."

        # General check
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

        # USE SMALL KEY on vault door
        if "KEY" in noun or "VAULT" in noun or "DOOR" in noun:
            if "SMALL KEY" not in inv:
                return "You don't have a key."
            if loc == 37:
                self.vault_unlocked = True
                return (
                    "You insert the SMALL KEY into the vault door lock. "
                    "It turns with a satisfying CLICK! "
                    "The massive steel door swings open, revealing the vault beyond."
                )
            return "There's no lock to use the key on here."

        # USE DOLLAR on vending machine
        if "DOLLAR" in noun or "VENDING" in noun or "MACHINE" in noun:
            if "DOLLAR BILL" not in inv:
                return "You need a dollar bill for the vending machine."
            if loc == 32:
                self.state.remove_item("DOLLAR BILL")
                self.state.add_item("UNKNOWN ITEM FROM VENDING MACHINE")
                return (
                    "You insert the DOLLAR BILL into the STRING VENDING MACHINE. "
                    "Ka-chunk! Something tumbles out: an UNKNOWN ITEM. "
                    "It might be useful... or not."
                )
            return "There's no vending machine here."

        # USE YARN + NEEDLES (KNIT)
        if ("YARN" in noun or "KNIT" in noun) and ("NEEDLE" in noun or "KNIT" in noun):
            if "BALL OF YARN" not in inv or "KNITTING NEEDLES" not in inv:
                return "You need both yarn and knitting needles to knit."
            return (
                "You sit down and KNIT a rough but serviceable SUIT from the yarn. "
                "It's not pretty, but it'll do. You put it on."
            )

        return "You can't figure out how to use that here."

    def _do_open(self, noun, loc):
        if "DOOR" in noun or "VAULT" in noun:
            if loc == 37:
                if self.vault_unlocked:
                    return "The vault door is already open. Go NORTH."
                return "The steel vault door is locked. You need the SMALL KEY."
            if loc == 33:
                return "The locked door won't budge. You need a key."
        return "You can't open that."

    def _do_shoot(self, noun, loc):
        if "GUN" not in self.state.inventory and "GUN" not in noun:
            return "You don't have a gun."
        if loc == 39 and "BURGLAR" in noun or "HIM" in noun or noun == "":
            if not self.burglar_defeated:
                self.burglar_defeated = True
                return (
                    "BANG! The gun fires. The BURGLAR drops the dollar and "
                    "collapses. He won't be bothering anyone anymore. "
                    "You can now take the DOLLAR BILL."
                )
            return "The burglar is already down."
        return "You can't shoot that."

    def _do_pay(self, noun, loc):
        if "DOLLAR" in noun or "BILL" in noun:
            return self._do_use("DOLLAR", loc)
        return "You can't pay with that."

    def _examine(self, noun, loc):
        if not noun:
            return self._describe_room(loc)
        noun = noun.upper()

        if "BURGLAR" in noun or "MAN" in noun:
            if loc == 39:
                if self.burglar_defeated:
                    return "The burglar lies defeated on the floor. A DOLLAR BILL sits near him."
                return (
                    "A rough-looking burglar, armed and dangerous. "
                    "He's clutching a DOLLAR BILL and watching you intently. "
                    "The remains of the kidnapper are in his mouth - he guards them fiercely. "
                    "You could SHOOT him, or try to get the drop on him somehow."
                )
            return "No burglar here."

        if "DOLLAR" in noun or "BILL" in noun:
            if loc == 39:
                return "A crisp dollar bill. The burglar is holding it."
            return "You don't see a dollar here."

        if "VAULT" in noun or "STEEL DOOR" in noun:
            if loc == 37:
                if self.vault_unlocked:
                    return "The vault door stands open. GOLD gleams inside."
                return "A massive steel door with a keyhole. It's locked."
            return "No vault here."

        if "VENDING" in noun or "MACHINE" in noun:
            if loc == 32:
                return "An old string vending machine. It takes dollar bills and dispenses... stuff. Worth a try?"
            return "No vending machine here."

        if "YARN" in noun:
            if "BALL OF YARN" in self._room_items.get(loc, []) or "BALL OF YARN" in self.state.inventory:
                return "A ball of knitting yarn. Red and white. You could KNIT something with it if you had needles."
            return "No yarn here."

        if "NEEDLE" in noun:
            if "KNITTING NEEDLES" in self._room_items.get(loc, []) or "KNITTING NEEDLES" in self.state.inventory:
                return "Sharp metal knitting needles. Long and thin."
            return "No knitting needles here."

        return "You don't see anything unusual."

    def _do_inventory(self):
        items = self.state.inventory
        if not items:
            return "You are empty-handed."
        return "You are carrying: " + ", ".join(items)

    def _describe_room(self, room_id):
        r = self.get_room(room_id)
        if not r:
            return "You are nowhere."
        desc = f"[{r['name']}]\n{r['desc']}"
        items = self._room_items.get(room_id, [])
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
