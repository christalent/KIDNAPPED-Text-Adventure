"""
KIDNAPPED! - Floor 6: The Office
"Sexy young office girls, knitting, fashion a new suit" - the actual floor
has an office with a KIDNAPPER counting ransom money, a vending machine that
dispenses string, a gun full of blanks, a tin foil sheet, a deflated balloon,
and a helium tank.

Entry from Floor 7 via KID'S SLIDE -> Room 41.
Goal: Get past the KIDNAPPER and descend to Floor 5.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove review
- Floor 7 SPEC: Room 30 GUN/TIN FOIL; balloon+helium "lift you somewhere"
"""

FLOOR_NUMBER = 6
NEXT_FLOOR_DOWN = 5

# --------------------------------------------------------------------
# Room map (Floor 6, rooms 41-49):
#
# Linear chain 41-49, all exits bidirectional, plus an east/west side room.
#
#   [41 Entry] -- [42 Lobby (VENDING MACHINE)]
#                    |
#                  [43 Supply Closet (GUN, TIN FOIL)]
#                    |
#                  [44 Balloon Storage (BALLOON)]
#                    |
#                  [45 Kidnapper Balcony (KIDNAPPER, DOLLAR)]
#                    |
#                  [46 Helium Storage (HELIUM TANK)]
#                    |
#                  [47 Break Room]
#                    |
#                  [48 Hallway (LOCKED DOOR)]
#                    |
#                  [49 Stairs Down -> Floor 5]
#
# Confirmed bidirectional pairs (per task spec / this implementation):
#   41<->42, 42<->43, 43<->44, 44<->45, 45<->46, 46<->47, 47<->48, 48<->49
#   Plus side: 43<->50, 50<->44 (small storage detour) - omitted here to
#   keep the linear chain simple.
#
# Items:
#   Room 42: STRING VENDING MACHINE (fixed) - $1 -> STRING
#   Room 43: GUN (takeable, blanks), TIN FOIL (takeable)
#   Room 44: LARGE DEFLATED BALLOON (takeable)
#   Room 45: KIDNAPPER (NPC), DOLLAR on table (guarded)
#   Room 46: TANK OF HELIUM GAS (takeable)
#   Room 48: LOCKED DOOR (fixed, locked) - blocks passage to 49
#            (the KIDNAPPER's KEY is in his pocket; threats with the
#             GUN make him drop it)
#   Room 49: Stairs DOWN to Floor 5
#
# Puzzle flow (multiple solutions):
#
#   Path A: "disguise the kidnapper" (uses GUN as threat)
#     1. GET GUN (43)
#     2. GET DOLLAR (45) - with GUN, kidnapper freezes, drops DOLLAR + KEY
#     3. UNLOCK DOOR (48) with KEY
#     4. N to 49, D -> Floor 5
#
#   Path B: "fly over with balloon"
#     1. GET BALLOON (44)
#     2. GET HELIUM TANK (46)
#     3. INFLATE BALLOON (combine) -> INFLATED BALLOON
#     4. USE INFLATED BALLOON -> floats down to Floor 5 (transitions)
#
#   Path C: "shoot the kidnapper" (RED HERRING - gun has blanks, you die)
#
# SHOOTING the KIDNAPPER with the GUN results in the gun firing blanks
# and the KIDNAPPER killing you.  The GUN is safe to USE as a threat
# (just have it in your inventory) but deadly to FIRE.
# --------------------------------------------------------------------
ROOMS = {
    41: {
        "name": "OFFICE ENTRANCE",
        "desc": (
            "You emerge from the slide into a carpeted office corridor. "
            "Fluorescent lights hum overhead. The carpet is shag, very 70s. "
            "Motivational posters line the walls: 'Hang in There!' "
            "A sign reads 'FLOOR 6 - OFFICE WING'. "
            "The corridor continues NORTH. "
            "You can go UP back to Floor 7 (via the slide)."
        ),
        "exits": {"N": 42, "U": "floor_7"},
        "items": [],
    },
    42: {
        "name": "OFFICE LOBBY",
        "desc": (
            "An open lobby with a water cooler and a few sad plants. "
            "A STRING VENDING MACHINE stands against the east wall, "
            "its faded label promising 'STRING - $1.00'. "
            "A small sign reads: 'INSERT DOLLAR, RECEIVE STRING.' "
            "The corridor continues NORTH. "
            "The entry is to the SOUTH."
        ),
        "exits": {"S": 41, "N": 43},
        "items": ["STRING VENDING MACHINE"],
    },
    43: {
        "name": "SUPPLY CLOSET",
        "desc": (
            "A cramped supply closet full of paperwork and dust. "
            "On a metal shelf: a GUN (in a holster) and a roll of TIN FOIL. "
            "An old label on the gun reads: 'FOR EMERGENCY USE ONLY'. "
            "The lobby is to the SOUTH. "
            "A storage room is to the NORTH."
        ),
        "exits": {"S": 42, "N": 44},
        "items": ["GUN", "TIN FOIL"],
    },
    44: {
        "name": "BALLOON STORAGE",
        "desc": (
            "A small storage room with a high ceiling. "
            "Hanging from a hook: a LARGE DEFLATED BALLOON. "
            "Looks like it might be inflatable... if you had helium. "
            "The supply closet is to the SOUTH. "
            "A balcony is to the NORTH."
        ),
        "exits": {"S": 43, "N": 45},
        "items": ["LARGE DEFLATED BALLOON"],
    },
    45: {
        "name": "KIDNAPPER'S BALCONY",
        "desc": (
            "A small balcony overlooking the office floor. "
            "The KIDNAPPER sits in a chair counting stacks of bills. "
            "He hasn't noticed you yet - he's busy with his money. "
            "On the table beside him: a single DOLLAR BILL. "
            "In his pocket: a small KEY. "
            "The balloon storage is to the SOUTH. "
            "The helium room is to the NORTH."
        ),
        "exits": {"S": 44, "N": 46},
        "items": [],  # DOLLAR is "on the table" - guarded by kidnapper
    },
    46: {
        "name": "HELIUM STORAGE",
        "desc": (
            "A locked-looking room with a pressure gauge on the door. "
            "Inside, a TANK OF HELIUM GAS strapped to a dolly. "
            "The label reads 'PARTY BALLOONS - INQUIRE WITHIN'. "
            "The balcony is to the SOUTH. "
            "A break room is to the NORTH."
        ),
        "exits": {"S": 45, "N": 47},
        "items": ["TANK OF HELIUM GAS"],
    },
    47: {
        "name": "BREAK ROOM",
        "desc": (
            "A small break room with a sad coffee machine and a table. "
            "Empty pizza boxes are stacked in the corner. "
            "The helium storage is to the SOUTH. "
            "A hallway is to the NORTH."
        ),
        "exits": {"S": 46, "N": 48},
        "items": [],
    },
    48: {
        "name": "HALLWAY",
        "desc": (
            "A plain hallway with flickering fluorescent lights. "
            "A heavy LOCKED DOOR blocks passage NORTH to the stairwell. "
            "The door has a keyhole - a KEY might open it. "
            "The break room is to the SOUTH."
        ),
        "exits": {"S": 47, "N": 49},
        "items": ["LOCKED DOOR"],
    },
    49: {
        "name": "STAIRS DOWN",
        "desc": (
            "A stairwell. A sign reads 'FLOOR 5 - DOWN ONLY'. "
            "The hallway is to the SOUTH. "
            "Go DOWN to Floor 5."
        ),
        "exits": {"S": 48, "D": "floor_5"},
        "items": [],
    },
}

# --------------------------------------------------------------------
# Special room targets (cross-floor navigation)
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    "floor_7": {"target": "floor_7", "landing_room": 37},
    "floor_5": {"target": "floor_5", "landing_room": 51},
}


# --------------------------------------------------------------------
# Floor 6 Engine
# --------------------------------------------------------------------
class Floor6Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        # Puzzle state flags
        self.dollar_taken = False
        self.door_unlocked = False
        self.key_taken = False
        self.balloon_inflated = False
        self.kidnapper_alive = True
        self.string_taken = False

    def _init_items(self):
        return {
            41: [],
            42: ["STRING VENDING MACHINE"],
            43: ["GUN", "TIN FOIL"],
            44: ["LARGE DEFLATED BALLOON"],
            45: [],  # DOLLAR is held by kidnapper
            46: ["TANK OF HELIUM GAS"],
            47: [],
            48: ["LOCKED DOOR"],
            49: [],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.dollar_taken = False
        self.door_unlocked = False
        self.key_taken = False
        self.balloon_inflated = False
        self.kidnapper_alive = True
        self.string_taken = False
        # Set landing room: player arrives here from Floor 7's slide
        self.state.location = 41

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

        # Item manipulation
        if verb in ("GET", "TAKE", "GRAB", "PICK"):
            return self._wrap(self._do_get(noun, loc))
        if verb in ("DROP", "PUT", "PLACE"):
            return self._wrap(self._do_drop(noun, loc))
        if verb in ("USE", "APPLY", "GIVE", "SHOW"):
            return self._wrap(self._do_use(noun, loc))
        if verb in ("INFLATE", "BLOW", "FILL"):
            return self._wrap(self._do_inflate(noun, loc))
        if verb in ("OPEN", "UNLOCK"):
            return self._wrap(self._do_open(noun, loc))
        if verb in ("SHOOT", "FIRE", "KILL"):
            return self._wrap(self._do_shoot(noun, loc))
        if verb in ("PAY", "INSERT"):
            return self._wrap(self._do_use("DOLLAR", loc))
        if verb in ("KNIT", "WEAR", "MAKE"):
            return self._wrap("There's nothing to knit here on Floor 6.")

        # Observation
        if verb in ("READ", "EXAMINE", "X", "CHECK"):
            return self._examine(noun, loc), False

        # Movement
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
            if next_target == "floor_7":
                return f"TRANSITION:{next_target}:37", True
            if next_target == "floor_5":
                return f"TRANSITION:{next_target}:51", True
        # Locked door gate: 48 N -> 49 requires door_unlocked
        if loc == 48 and direction == "N" and not self.door_unlocked:
            return (
                "The LOCKED DOOR blocks the way north. "
                "You need a KEY to open it."
            ), False
        self.state.location = next_target
        return self._describe_room(next_target), False

    def _go_up(self, loc):
        if loc == 41:
            return f"TRANSITION:floor_7:37", True
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 49:
            if not self.door_unlocked:
                return "The way down is blocked by a locked door above.", False
            return f"TRANSITION:floor_5:51", True
        return self._go("D", loc)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        # DOLLAR guarded by kidnapper
        if "DOLLAR" in noun or "BILL" in noun:
            if loc != 45:
                return "You don't see a dollar bill here."
            if self.dollar_taken:
                return "You already have the dollar."
            if not self.kidnapper_alive:
                return "The kidnapper is down. You take the dollar."
            if "GUN" in self.state.inventory:
                # Gun-freeze: kidnapper hands over the dollar
                self.dollar_taken = True
                self.state.add_item("DOLLAR BILL")
                # Also drops the key (kidnapper is frozen)
                if not self.key_taken:
                    self.state.add_item("SMALL KEY")
                    self.key_taken = True
                return (
                    "The KIDNAPPER sees your GUN and freezes, "
                    "hands raised. He drops the DOLLAR BILL on the table "
                    "- and a small KEY falls out of his pocket. "
                    "You grab both."
                )
            # No gun: kidnapper kills you
            return self._kill_player(
                "The KIDNAPPER spots you reaching for his dollar. "
                "He pulls a knife. You die a horrible death."
            )

        # KEY can be picked up if kidnapper dropped it
        if "KEY" in noun:
            if "SMALL KEY" in self.state.inventory:
                return "You already have the key."
            if loc == 45 and self.key_taken:
                return "The kidnapper's pockets are empty now."
            if "GUN" in self.state.inventory and loc == 45 and self.kidnapper_alive:
                # Implicit: if you have the gun and are here, the kidnapper
                # already dropped the key when you threatened him. But the
                # GET DOLLAR path auto-adds the key. For a standalone
                # GET KEY with gun, do the threat here.
                self.key_taken = True
                self.state.add_item("SMALL KEY")
                return (
                    "You point your GUN at the KIDNAPPER. He freezes. "
                    "A small KEY falls out of his pocket. You grab it."
                )
            return "There's no key here."

        # Walk room items
        room_items = self._room_items.get(loc, [])
        for item in list(room_items):
            if self._item_matches(noun, item):
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.add_item(item)
                return f"You take the {item}."

        return "You don't see that here."

    def _item_matches(self, noun, item):
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
                # Dropping the inflated balloon deflates it
                if item == "INFLATED BALLOON":
                    self.balloon_inflated = False
                    self.state.add_item("LARGE DEFLATED BALLOON")
                    self.state.remove_item("INFLATED BALLOON")
                return f"You drop the {item}."
        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"

        # DOLLAR on vending machine
        if "DOLLAR" in noun or "BILL" in noun:
            return self._use_dollar_on_vending(loc)

        # KEY on the locked door
        if "KEY" in noun:
            return self._use_key_on_door(loc)

        # INFLATED BALLOON -> float to floor 5
        if "INFLATED" in noun and "BALLOON" in noun:
            if "INFLATED BALLOON" not in self.state.inventory:
                return "You don't have an inflated balloon."
            return "TRANSITION:floor_5:51"
        if "BALLOON" in noun:
            # Trying to USE the deflated balloon -> suggest inflate
            if "LARGE DEFLATED BALLOON" in self.state.inventory:
                return (
                    "The balloon is deflated. "
                    "Try INFLATE BALLOON (you'll need a HELIUM TANK)."
                )
            return "You don't have a balloon."

        # INFLATE command (also handled separately as a verb)
        if "INFLATE" in noun or "FILL" in noun:
            return self._do_inflate(loc)

        # GUN - trying to USE the gun (but not shoot)
        if "GUN" in noun:
            if "GUN" not in self.state.inventory:
                return "You don't have a gun."
            # Pointing the gun is the "threat" - already handled by
            # GET DOLLAR. If you USE GUN explicitly, it just threatens.
            return (
                "You brandish the GUN menacingly. "
                "Anyone watching will be very cooperative."
            )

        # TIN FOIL - no obvious use on floor 6 (could be used to wrap
        # the balloon or for shenanigans later; for now it's a no-op)
        if "FOIL" in noun or "TIN" in noun:
            return "The TIN FOIL is shiny but doesn't seem useful on its own."

        # STRING from vending machine - used on floor 5+
        if "STRING" in noun:
            return "The STRING is useful but not here."

        # HELIUM tank
        if "HELIUM" in noun or "TANK" in noun:
            return self._do_inflate(loc)

        return "You can't figure out how to use that here."

    def _use_dollar_on_vending(self, loc):
        if "DOLLAR BILL" not in self.state.inventory:
            return "You need a DOLLAR BILL."
        if loc != 42:
            return "There's no vending machine here."
        if self.string_taken:
            return "The vending machine is empty (you already got the string)."
        self.state.remove_item("DOLLAR BILL")
        self.state.add_item("STRING")
        self.string_taken = True
        return (
            "You insert the DOLLAR BILL into the STRING VENDING MACHINE. "
            "Ka-chunk! A length of STRING tumbles out. "
            "It might be useful on a lower floor."
        )

    def _use_key_on_door(self, loc):
        if "SMALL KEY" not in self.state.inventory:
            return "You don't have a SMALL KEY."
        if loc != 48:
            return "There's no locked door here."
        if self.door_unlocked:
            return "The door is already unlocked."
        self.door_unlocked = True
        return (
            "You insert the SMALL KEY into the LOCKED DOOR. "
            "It turns with a satisfying click. The door swings open!"
        )

    # ------------------------------------------------------------------
    # INFLATE
    # ------------------------------------------------------------------
    def _do_inflate(self, loc=None, noun=""):
        if "LARGE DEFLATED BALLOON" not in self.state.inventory and \
           "INFLATED BALLOON" not in self.state.inventory:
            return "You don't have a balloon to inflate."
        if "TANK OF HELIUM GAS" not in self.state.inventory and \
           "HELIUM TANK" not in self.state.inventory and \
           "HELIUM" not in self.state.inventory:
            return "You need a TANK OF HELIUM GAS to inflate the balloon."
        if "INFLATED BALLOON" in self.state.inventory:
            return "The balloon is already inflated."
        # Swap deflated for inflated
        self.state.remove_item("LARGE DEFLATED BALLOON")
        # Optionally consume the helium tank (one-shot) - keep it for now
        self.state.add_item("INFLATED BALLOON")
        self.balloon_inflated = True
        return (
            "You connect the TANK OF HELIUM GAS to the deflated balloon. "
            "Pssssshhh! The balloon swells into a buoyant INFLATED BALLOON. "
            "It tugs at your hand, eager to fly. "
            "USE INFLATED BALLOON to ride it."
        )

    # ------------------------------------------------------------------
    # SHOOT (the GUN has blanks - shooting the kidnapper kills you)
    # ------------------------------------------------------------------
    def _do_shoot(self, noun, loc):
        if "GUN" not in self.state.inventory:
            return "You don't have a gun."
        if loc != 45:
            return "There's nothing to shoot here."
        # Shooting the kidnapper -> gun has blanks -> kidnapper kills you
        return self._kill_player(
            "BANG! Click. The GUN had blanks! "
            "The KIDNAPPER laughs, pulls a knife, and you die a terrible death."
        )

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if "DOOR" in noun or "LOCKED" in noun:
            if loc == 48:
                if self.door_unlocked:
                    return "The door is already open. Go NORTH."
                return "The door is locked. You need a KEY."
            return "There's no locked door here."
        if "VENDING" in noun or "MACHINE" in noun:
            return "The vending machine has no opening - just a slot."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return self._describe_room(loc)
        n = noun.upper()

        if "KIDNAPPER" in n or "MAN" in n or "GUY" in n:
            if loc == 45:
                if not self.kidnapper_alive:
                    return "The kidnapper lies still. You got past him."
                if "GUN" in self.state.inventory:
                    return (
                        "The KIDNAPPER eyes your GUN nervously. "
                        "He won't try anything while you're armed."
                    )
                return (
                    "The KIDNAPPER is busy counting money. "
                    "He looks dangerous. "
                    "Don't try anything without a weapon."
                )
            return "No kidnapper here."

        if "DOLLAR" in n or "BILL" in n:
            if loc == 45 and not self.dollar_taken:
                return "A single DOLLAR BILL on the kidnapper's table."
            if "DOLLAR BILL" in self.state.inventory:
                return "A crisp DOLLAR BILL. Good for vending machines."
            return "You don't see a dollar here."

        if "DOOR" in n or "LOCKED" in n:
            if loc == 48:
                if self.door_unlocked:
                    return "The LOCKED DOOR is now open."
                return "A heavy LOCKED DOOR. Needs a KEY."
            return "No door here."

        if "GUN" in n:
            if "GUN" in self.state.inventory:
                return "A GUN. Feels light - check the chamber."
            if loc == 43:
                return "A GUN in a holster. It's there for the taking."
            return "No gun here."

        if "BALLOON" in n:
            if "INFLATED BALLOON" in self.state.inventory:
                return "A buoyant INFLATED BALLOON, tugging skyward."
            if "LARGE DEFLATED BALLOON" in self.state.inventory:
                return "A LARGE DEFLATED BALLOON. Needs helium."
            if loc == 44:
                return "A LARGE DEFLATED BALLOON hanging from a hook."
            return "No balloon here."

        if "HELIUM" in n or "TANK" in n:
            if "TANK OF HELIUM GAS" in self.state.inventory:
                return "A TANK OF HELIUM GAS. Connect it to a balloon."
            if loc == 46:
                return "A TANK OF HELIUM GAS on a dolly."
            return "No helium here."

        if "FOIL" in n or "TIN" in n:
            if "TIN FOIL" in self.state.inventory:
                return "A roll of TIN FOIL. Shiny."
            if loc == 43:
                return "A roll of TIN FOIL on the shelf."
            return "No foil here."

        if "KEY" in n:
            if "SMALL KEY" in self.state.inventory:
                return "A small KEY. Probably fits a lock around here."
            return "You don't see a key here."

        if "VENDING" in n or "MACHINE" in n:
            if loc == 42:
                return (
                    "A STRING VENDING MACHINE. "
                    "Insert a DOLLAR BILL to get a STRING."
                )
            return "No vending machine here."

        if "STRING" in n:
            if "STRING" in self.state.inventory:
                return "A length of STRING. Useful for tying things."
            return "No string here."

        return f"You don't see anything unusual about the {noun}."

    # ------------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------------
    def _do_inventory(self):
        items = self.state.inventory
        if not items:
            return "You are empty-handed."
        return "You are carrying: " + ", ".join(items)

    # ------------------------------------------------------------------
    # Room description
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        r = self.get_room(room_id)
        if not r:
            return "You are nowhere."
        desc = f"[{r['name']}]\n{r['desc']}"
        items = self._room_items.get(room_id, [])
        # Add the dollar to room 45 description if not taken
        if room_id == 45 and not self.dollar_taken and self.kidnapper_alive:
            items = list(items) + ["DOLLAR BILL"]
        if items:
            desc += "\n\nYou can see: " + ", ".join(items) + "."
        # Door state
        if room_id == 48 and self.door_unlocked:
            desc += "\n\nThe LOCKED DOOR stands open to the NORTH."
        # Kidnapper state
        if room_id == 45 and not self.kidnapper_alive:
            desc += "\n\nThe KIDNAPPER has been dealt with."
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
        if hasattr(self.state, "alive"):
            self.state.alive = False
        if hasattr(self.state, "game_over"):
            self.state.game_over = True
        return msg

    # ------------------------------------------------------------------
    # Static exit verification
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
    e = Floor6Engine.verify_exits()
    if e:
        print(f"FAIL: {len(e)} errors:")
        for x in e:
            print(f"  {x}")
    else:
        print(f"PASS: All exits bidirectional ({len(ROOMS)} rooms)")
