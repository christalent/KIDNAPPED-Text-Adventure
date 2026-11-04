"""
KIDNAPPED! - Floor 7: The Bank Vault
Hardest floor - wrest a dollar from a burglar.

Entry from Floor 8 via stairs DOWN -> Room 31.
Goal: Knit a disguise, get the dollar from the burglar, slide down to Floor 6.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review: https://www.retrogamestrove.com/game-149-kidnapped-1980/
- Confirmed bidirectional pairs: 31<->32, 32<->37, 36<->37, 38<->31, 38<->35, 38<->39
"""

FLOOR_NUMBER = 7
NEXT_FLOOR_DOWN = 6

# --------------------------------------------------------------------
# Room map (Floor 7, rooms 31-39 + vault 55-56):
#
#   [33]---[31 Bank Entry]---[32 Main Floor]---[36 Combo Office]---[37 Antechamber]
#    |        |                  |    |                              |
#   [33]   [38 Corridor]------[35 Stairs]                         [55 Vault]---[56 Playroom]
#            |                  |
#           [38]--------------[39 Vault Office (BURGLAR + DOLLAR)]
#
# Confirmed bidirectional pairs (per task spec):
#   31<->32, 31<->33, 31<->38, 32<->36, 32<->37, 32<->39, 35<->38,
#   36<->37, 37<->55, 38<->39, 55<->56
#
# Items:
#   Room 33: SMALL KEY (takeable), JAR OF YELLOW SOLUTION (takeable)
#   Room 32: STRING VENDING MACHINE (fixed)
#   Room 36: TIN FOIL (takeable)
#   Room 37: STEEL DOOR (fixed, locked until SMALL KEY used)
#   Room 39: BALL OF YARN (takeable), KNITTING NEEDLES (takeable),
#            DOLLAR BILL (held by BURGLAR, only gettable when disguised)
#   Room 55: JAR OF FLUID (takeable), KID'S SLIDE (fixed, descends to floor 6)
#   Room 56: (no items)
#
# Puzzle flow:
#   1. Get SMALL KEY from 33
#   2. Use SMALL KEY on STEEL DOOR in 37 to unlock vault (37 N -> 55)
#   3. Get BALL OF YARN and KNITTING NEEDLES from 39 (burglar tolerates)
#   4. Get TIN FOIL from 36
#   5. KNIT YARN + NEEDLES -> HAND-KNIT SUIT (auto-worn)
#   6. Get DOLLAR BILL from 39 (burglar does not recognize you)
#   7. (Optional) Use DOLLAR on STRING VENDING MACHINE in 32 -> STRING
#   8. Go 37 -> 55 (vault is open)
#   9. USE KID'S SLIDE in 55 -> descend to Floor 6
# --------------------------------------------------------------------
ROOMS = {
    31: {
        "name": "BANK ENTRY",
        "desc": (
            "You descend the stairs into a wide marble foyer. "
            "The air smells of old money and dust. "
            "Ornate frescoes line the ceiling, now cracked and peeling. "
            "A sign reads 'FIRST NATIONAL BANK OF DESCENT.' "
            "To the NORTH, the main bank floor stretches out. "
            "To the WEST, a small storage room. "
            "To the EAST, a long corridor. "
            "The stairs lead UP back to Floor 8."
        ),
        "exits": {"N": 32, "W": 33, "E": 38, "U": "floor_8"},
        "items": [],
    },
    32: {
        "name": "MAIN BANK FLOOR",
        "desc": (
            "You're in the heart of the old bank. "
            "Rotting velvet ropes section off the former teller windows. "
            "An old STRING VENDING MACHINE stands against one wall - "
            "it takes bills and dispenses... something. "
            "To the WEST, a vault office. "
            "To the NORTH, the vault antechamber. "
            "To the EAST, the combination office. "
            "The entry is to the SOUTH."
        ),
        "exits": {"S": 31, "E": 36, "N": 37, "W": 39},
        "items": ["STRING VENDING MACHINE"],
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
    35: {
        "name": "STAIRS UP",
        "desc": (
            "A narrow side stairway with concrete steps. "
            "A faded sign reads 'STAIRS TO FLOOR 8'. "
            "Looks like an alternate way back up. "
            "The bank corridor is to the WEST."
        ),
        "exits": {"W": 38, "U": "floor_8"},
        "items": [],
    },
    36: {
        "name": "COMBINATION OFFICE",
        "desc": (
            "A cramped office lined with safety deposit boxes. "
            "A single desk holds some papers and a sheet of TIN FOIL. "
            "The walls are covered in combination notes. "
            "To the WEST, the main bank floor. "
            "To the EAST, the vault antechamber."
        ),
        "exits": {"W": 32, "E": 37},
        "items": ["TIN FOIL"],
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
            "The corridor continues NORTH to the vault office. "
            "The bank entry is to the WEST. "
            "Side stairs lead EAST up to Floor 8."
        ),
        "exits": {"W": 31, "E": 35, "N": 39},
        "items": [],
    },
    39: {
        "name": "VAULT OFFICE",
        "desc": (
            "A private office inside the vault area. "
            "A BURGLAR crouches behind the desk, eyes darting. "
            "He is clutching something - looks like a DOLLAR BILL. "
            "On the desk: BALL OF YARN and KNITTING NEEDLES, "
            "left by some previous visitor. "
            "The main bank floor is to the EAST. "
            "The corridor is to the SOUTH."
        ),
        "exits": {"S": 38, "E": 32},
        "items": ["BALL OF YARN", "KNITTING NEEDLES"],
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
            "The antechamber is to the SOUTH. "
            "A playroom lies to the NORTH."
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
        self.suit_worn = False
        self.dollar_taken = False
        self.burglar_alerted = False

    def _init_items(self):
        return {
            31: [],
            32: ["STRING VENDING MACHINE"],
            33: ["SMALL KEY", "JAR OF YELLOW SOLUTION"],
            35: [],
            36: ["TIN FOIL"],
            37: [],
            38: [],
            39: ["BALL OF YARN", "KNITTING NEEDLES"],
            55: ["JAR OF FLUID", "KID'S SLIDE"],
            56: [],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.vault_unlocked = False
        self.suit_worn = False
        self.dollar_taken = False
        self.burglar_alerted = False

    def on_leave(self):
        pass

    def get_room(self, room_id):
        return ROOMS.get(room_id)

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    # ------------------------------------------------------------------
    # Command dispatch
    # ------------------------------------------------------------------
    def handle_command(self, verb, noun=""):
        loc = self.state.location
        verb = verb.upper().strip()
        noun = noun.upper().strip() if noun else ""

        # Observation / inventory
        if verb in ("LOOK", "L"):
            return self._describe_room(loc), False
        if verb in ("INVENTORY", "I", "INV"):
            return self._do_inventory(), False

        # Item manipulation -- these may return TRANSITION strings (for
        # USE SLIDE). Parse the string and return the proper tuple.
        if verb in ("GET", "TAKE", "GRAB", "PICK"):
            return self._wrap(self._do_get(noun, loc))
        if verb in ("DROP", "PUT", "PLACE"):
            return self._wrap(self._do_drop(noun, loc))
        if verb in ("USE", "APPLY"):
            return self._wrap(self._do_use(noun, loc))
        if verb in ("KNIT", "WEAR", "MAKE", "FASHION"):
            return self._wrap(self._do_knit_or_wear(noun, loc))
        if verb in ("OPEN", "UNLOCK"):
            return self._wrap(self._do_open(noun, loc))
        if verb in ("PAY", "INSERT"):
            return self._wrap(self._do_use("DOLLAR", loc))

        # Observation
        if verb in ("READ", "EXAMINE", "X", "CHECK"):
            return self._examine(noun, loc), False

        # Movement (returns a (text, transition_flag) tuple directly)
        if verb in ("N", "NORTH") or (verb == "GO" and noun in ("N", "NORTH", "")):
            return self._go("N", loc)
        if verb in ("S", "SOUTH") or (verb == "GO" and noun in ("S", "SOUTH", "")):
            return self._go("S", loc)
        if verb in ("E", "EAST") or (verb == "GO" and noun in ("E", "EAST", "")):
            return self._go("E", loc)
        if verb in ("W", "WEST") or (verb == "GO" and noun in ("W", "WEST", "")):
            return self._go("W", loc)
        if verb in ("U", "UP") or (verb == "GO" and noun in ("U", "UP", "")):
            return self._go_up(loc)
        if verb in ("D", "DOWN") or (verb == "GO" and noun in ("D", "DOWN", "")):
            return self._go_down(loc)

        return "You don't know how to do that.", False

    @staticmethod
    def _wrap(result):
        """Wrap an action result string into a (text, transition_flag) tuple.
        A 'TRANSITION:floor_N:room' prefix is treated as a transition.
        """
        if isinstance(result, str) and result.startswith("TRANSITION:"):
            return result, True
        return result, False

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _go(self, direction, loc):
        r = self.get_room(loc)
        if not r:
            return "You are nowhere.", False
        exits = r.get("exits", {})
        next_target = exits.get(direction)
        if next_target is None:
            return f"You can't go {direction} from here.", False
        if isinstance(next_target, str):
            # Floor transitions
            if next_target == "floor_8":
                return f"TRANSITION:{next_target}:28", True
            if next_target == "floor_6":
                return f"TRANSITION:{next_target}:41", True
        # Vault door gate: only enter 55 from 37 when vault is unlocked
        if loc == 37 and direction == "N" and not self.vault_unlocked:
            return (
                "The massive STEEL DOOR is locked. "
                "You need a SMALL KEY to open it."
            ), False
        self.state.location = next_target
        return self._describe_room(next_target), False

    def _go_up(self, loc):
        # Rooms 31 and 35 have U=floor_8
        if loc in (31, 35):
            return f"TRANSITION:floor_8:28", True
        return self._go("U", loc)

    def _go_down(self, loc):
        # Only the KID'S SLIDE in 55 descends to floor 6
        if loc == 55:
            return (
                "You climb onto the KID'S SLIDE and zoom down! "
                "You land with a thump on Floor 6."
            ), False  # Description only; USE SLIDE triggers the transition
        return self._go("D", loc)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        # Special: burglar guards the DOLLAR BILL
        if "DOLLAR" in noun or "BILL" in noun:
            if loc != 39:
                return "You don't see a dollar bill here."
            if self.dollar_taken:
                return "You already have the dollar bill."
            if "HAND-KNIT SUIT" in self.state.inventory or self.suit_worn:
                # Disguised: burglar does not recognize you
                self.dollar_taken = True
                self.state.add_item("DOLLAR BILL")
                self.burglar_alerted = False
                return (
                    "The BURGLAR blinks at your finely tailored suit "
                    "and assumes you're the bank owner. "
                    "He sheepishly hands over the DOLLAR BILL."
                )
            if "GUN" in self.state.inventory:
                # Alternate solution per BASIC: GUN freezes the burglar
                self.dollar_taken = True
                self.state.add_item("DOLLAR BILL")
                return (
                    "The BURGLAR sees your GUN and freezes. "
                    "He drops the DOLLAR BILL and you grab it."
                )
            # No protection: burglar kills you
            return self._kill_player(
                "The BURGLAR spots you reaching for his dollar. "
                "He lunges. You die a terrible death."
            )

        room_items = self._room_items.get(loc, [])

        # Walk room items, matching by substring
        for item in list(room_items):
            if self._item_matches(noun, item):
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.add_item(item)
                return f"You take the {item}."

        return "You don't see that here."

    def _item_matches(self, noun, item):
        """Case-insensitive substring match for items."""
        n = noun.upper().strip()
        i = item.upper().strip()
        if not n:
            return False
        return n in i or i in n

    # ------------------------------------------------------------------
    # DROP
    # ------------------------------------------------------------------
    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"
        for item in list(self.state.inventory):
            if self._item_matches(noun, item):
                self.state.remove_item(item)
                self._room_items.setdefault(loc, []).append(item)
                # Dropping the suit removes disguise
                if item == "HAND-KNIT SUIT":
                    self.suit_worn = False
                return f"You drop the {item}."
        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        """Return a string. Transitions are signalled via the
        'TRANSITION:floor_N:room' prefix; the caller parses it.
        """
        if not noun:
            return "Use what?"
        inv = self.state.inventory

        # USE SMALL KEY on the vault door
        if "KEY" in noun and ("SMALL" in noun or "VAULT" in noun or "DOOR" in noun):
            return self._use_small_key(loc)
        if "KEY" in noun:
            return self._use_small_key(loc)

        # USE YARN + NEEDLES (also handles KNIT command)
        if "YARN" in noun or "NEEDLE" in noun:
            return self._knit_suit(loc)

        # USE DOLLAR / BILL on vending machine
        if "DOLLAR" in noun or "BILL" in noun:
            return self._use_dollar_on_vending(loc)

        # USE TIN FOIL (no-op for now, future-proofing)
        if "FOIL" in noun or "TIN" in noun:
            return "The TIN FOIL is shiny but doesn't seem useful on its own."

        # USE SUIT
        if "SUIT" in noun:
            return self._wear_suit(loc)

        # USE SLIDE / RIDE / GO (descend to floor 6)
        if "SLIDE" in noun:
            if loc == 55:
                return f"TRANSITION:floor_6:41"
            return "There's no slide here."

        # USE YELLOW SOLUTION / FLUID (no-op for floor 7)
        if "SOLUTION" in noun or "FLUID" in noun or "JAR" in noun:
            return "The jar is sealed. Probably best not to open it here."

        return "You can't figure out how to use that here."

    def _use_small_key(self, loc):
        if "SMALL KEY" not in self.state.inventory:
            return "You don't have a SMALL KEY."
        if loc != 37:
            return "There's no vault door here."
        if self.vault_unlocked:
            return "The vault door is already unlocked."
        self.vault_unlocked = True
        return (
            "You insert the SMALL KEY into the vault door lock. "
            "It turns with a satisfying CLICK! "
            "The massive STEEL DOOR swings open, "
            "revealing the vault beyond."
        )

    def _use_dollar_on_vending(self, loc):
        if "DOLLAR BILL" not in self.state.inventory:
            return "You need a DOLLAR BILL."
        if loc != 32:
            return "There's no vending machine here."
        self.state.remove_item("DOLLAR BILL")
        self.state.add_item("STRING")
        return (
            "You insert the DOLLAR BILL into the STRING VENDING MACHINE. "
            "Ka-chunk! A length of STRING tumbles out. "
            "It might be useful... or not."
        )

    def _knit_suit(self, loc):
        if "BALL OF YARN" not in self.state.inventory:
            return "You need BALL OF YARN to knit."
        if "KNITTING NEEDLES" not in self.state.inventory:
            return "You need KNITTING NEEDLES to knit."
        if "HAND-KNIT SUIT" in self.state.inventory or self.suit_worn:
            return "You already have a suit."
        self.state.remove_item("BALL OF YARN")
        self.state.remove_item("KNITTING NEEDLES")
        self.state.add_item("HAND-KNIT SUIT")
        self.suit_worn = True
        return (
            "You sit down and KNIT a rough but serviceable SUIT from the yarn. "
            "It's not pretty, but it'll do. You put it on. "
            "You feel like a proper bank owner."
        )

    def _wear_suit(self, loc):
        if "HAND-KNIT SUIT" not in self.state.inventory:
            return "You don't have a suit to wear."
        if self.suit_worn:
            return "You're already wearing the suit."
        self.suit_worn = True
        return "You put on the HAND-KNIT SUIT. You feel very professional."

    # ------------------------------------------------------------------
    # KNIT / WEAR
    # ------------------------------------------------------------------
    def _do_knit_or_wear(self, noun, loc):
        if "SUIT" in noun.upper():
            return self._wear_suit(loc)
        if "KNIT" in noun.upper() or noun == "":
            return self._knit_suit(loc)
        return "You can't do that."

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if "DOOR" in noun or "VAULT" in noun or "STEEL" in noun:
            if loc == 37:
                if self.vault_unlocked:
                    return "The vault door is already open. Go NORTH."
                return "The STEEL DOOR is locked. You need a SMALL KEY."
            return "There's no locked door here."
        if "VENDING" in noun or "MACHINE" in noun:
            if loc == 32:
                return "The vending machine has no opening - just a coin slot."
            return "No vending machine here."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return self._describe_room(loc)
        n = noun.upper()

        if "BURGLAR" in n or "MAN" in n or "THIEF" in n:
            if loc == 39:
                if self.dollar_taken:
                    return (
                        "The burglar looks dazed - you've got his dollar. "
                        "He doesn't look like he'll bother you."
                    )
                if self.suit_worn or "HAND-KNIT SUIT" in self.state.inventory:
                    return (
                        "The burglar peers at your HAND-KNIT SUIT. "
                        "He seems to think you belong here. "
                        "He won't give up the dollar easily - "
                        "but he might not stop you either."
                    )
                return (
                    "A rough-looking burglar, watchful and tense. "
                    "He's clutching a DOLLAR BILL. "
                    "He will not let you take it without a fight."
                )
            return "No burglar here."

        if "DOLLAR" in n or "BILL" in n:
            if loc == 39 and not self.dollar_taken:
                return "A crisp DOLLAR BILL clutched by the burglar."
            if "DOLLAR BILL" in self.state.inventory:
                return "A crisp DOLLAR BILL. Good for vending machines."
            return "You don't see a dollar here."

        if "VAULT" in n or "STEEL" in n or "DOOR" in n:
            if loc == 37:
                if self.vault_unlocked:
                    return "The vault door stands open. Gold gleams inside."
                return "A massive STEEL DOOR with a keyhole. It's locked."
            return "No vault door here."

        if "VENDING" in n or "MACHINE" in n:
            if loc == 32:
                return (
                    "An old string vending machine. "
                    "It takes dollar bills and dispenses STRING. "
                    "Worth a try?"
                )
            return "No vending machine here."

        if "YARN" in n:
            if "BALL OF YARN" in self.state.inventory:
                return "A ball of red-and-white knitting yarn."
            return "No yarn here."

        if "NEEDLE" in n:
            if "KNITTING NEEDLES" in self.state.inventory:
                return "Sharp metal knitting needles."
            return "No needles here."

        if "SLIDE" in n:
            if loc == 55:
                return (
                    "A KID'S SLIDE leading down into darkness. "
                    "It seems to lead to Floor 6. "
                    "USE SLIDE to ride it."
                )
            return "No slide here."

        if "SUIT" in n:
            if "HAND-KNIT SUIT" in self.state.inventory:
                if self.suit_worn:
                    return "You're wearing a HAND-KNIT SUIT. Very dapper."
                return "A HAND-KNIT SUIT in your inventory."
            return "You don't have a suit."

        if "SOLUTION" in n or "FLUID" in n or "JAR" in n:
            return "A jar of fluid, sealed tight. The label is smudged."

        return f"You don't see anything unusual about the {noun}."

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------
    def _do_inventory(self):
        items = self.state.inventory
        if not items:
            return "You are empty-handed."
        suffix = " (wearing suit)" if self.suit_worn else ""
        return "You are carrying: " + ", ".join(items) + suffix

    # ------------------------------------------------------------------
    # Room description
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        r = self.get_room(room_id)
        if not r:
            return "You are nowhere."
        desc = f"[{r['name']}]\n{r['desc']}"
        items = self._room_items.get(room_id, [])
        if items:
            desc += "\n\nYou can see: " + ", ".join(items) + "."
        # Vault state
        if room_id == 37 and self.vault_unlocked:
            desc += "\n\nThe STEEL DOOR stands open to the NORTH."
        # Burglar state
        if room_id == 39 and not self.dollar_taken:
            desc += "\n\nThe BURGLAR clutches his DOLLAR BILL."
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

    # ------------------------------------------------------------------
    # Player death helper
    # ------------------------------------------------------------------
    def _kill_player(self, msg):
        # The engine reads the return value; death is reported as a
        # non-transition result and the runner handles game over.
        if hasattr(self.state, "alive"):
            self.state.alive = False
        if hasattr(self.state, "game_over"):
            self.state.game_over = True
        return msg

    # ------------------------------------------------------------------
    # Static exit verification (mirrors floor 9's pattern)
    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        errors = []
        opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
        for rid, r in ROOMS.items():
            for d, t in r["exits"].items():
                if isinstance(t, str):
                    continue
                if t not in ROOMS:
                    errors.append(f"Room {rid} -> {d}={t}, but room {t} does not exist")
                    continue
                ro = opp[d]
                reverse = ROOMS[t]["exits"].get(ro)
                if reverse is None:
                    errors.append(f"Room {rid} -> {d}={t}, but {t} has no {ro}")
                elif reverse != rid:
                    errors.append(
                        f"Room {rid} -> {d}={t}, but {t} -> {ro}={reverse} (not back to {rid})"
                    )
        return errors


if __name__ == "__main__":
    e = Floor7Engine.verify_exits()
    if e:
        print(f"FAIL: {len(e)} errors:")
        for x in e:
            print(f"  {x}")
    else:
        print(f"PASS: All exits bidirectional ({len(ROOMS)} rooms)")
