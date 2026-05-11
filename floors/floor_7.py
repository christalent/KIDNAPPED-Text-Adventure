"""
Floor 7: Bank Vault
Entry from Floor 8 via Gold's Stairway (Room 31).
Goal: Unlock the vault, grab what you need, descend via Gold's Slide.
"""

FLOOR_NUMBER = 7

# --------------------------------------------------------------------
# Room definitions for Floor 7 (rooms 31-39 + vault rooms 55-57)
# --------------------------------------------------------------------
ROOMS = {
    # ---- Main Bank Floor (rooms 31-39) ----
    31: {
        "name": "NARROW STAIRWAY",
        "desc": (
            "You stand in a narrow concrete stairway between floors. "
            "The air smells of old money and gunpowder. A dusty sign reads "
            "'BANK OF DESCENT - PRIVATE.' The stairs lead UP to Floor 8 "
            "and SOUTH into the bank corridor."
        ),
        "exits": {"U": "floor_8_stairs", "S": 32},
        "items": [],
    },
    32: {
        "name": "BANK FLOOR - VAULT CORRIDOR",
        "desc": (
            "You are in a long marble-floored corridor. The walls are lined "
            "with faded portraits of stern bank presidents. "
            "To the NORTH is the vault mechanism room. "
            "To the EAST is a side room. "
            "To the SOUTH the manager's office awaits. "
            "To the WEST the old vault entrance awaits."
        ),
        "exits": {"N": 34, "E": 33, "S": 36, "W": 39},
        "items": [],
    },
    33: {
        "name": "SIDE ROOM",
        "desc": (
            "A cramped utility room filled with old ledgers and a broken "
            "typewriter. A dusty shelf holds a roll of TIN FOIL, left here "
            "decades ago. The only exit is WEST, back to the corridor."
        ),
        "exits": {"W": 32},
        "items": ["TIN FOIL"],
    },
    34: {
        "name": "VAULT MECHANISM ROOM",
        "desc": (
            "A cold room dominated by massive clockwork gears and a wall "
            "of combination dials. This is where the old vault's combination "
            "was once set. A small PLASTIC SIGN on the wall reads: "
            "'STRING VENDING MACHINE - INSERT TIN FOIL - $1.00 REFUND'. "
            "Exits lead SOUTH to the corridor, EAST to the guard post, "
            "and WEST to the old vault entrance."
        ),
        "exits": {"S": 32, "E": 35, "W": 39},
        "items": [],
    },
    35: {
        "name": "GUARD POST",
        "desc": (
            "An old security desk blocks the way. Bulletproof glass looks "
            "out onto the manager's office beyond. A coffee mug labeled "
            "'KIDNAPPER' sits next to an empty donut box. "
            "Exits lead WEST to the vault mechanism room and EAST to "
            "the manager's office."
        ),
        "exits": {"W": 34, "E": 36},
        "items": [],
    },
    36: {
        "name": "MANAGER'S OFFICE",
        "desc": (
            "A wood-paneled corner office. A massive oak desk dominates the "
            "room, papers scattered everywhere. Someone left in a hurry. "
            "To the EAST is the key room. To the WEST the guard post. "
            "The corridor lies to the NORTH."
        ),
        "exits": {"W": 35, "E": 37, "N": 32},
        "items": [],
    },
    37: {
        "name": "KEY ROOM",
        "desc": (
            "A small room lined with brass hooks and empty key racks. "
            "One hook still holds a SMALL KEY, left behind by some "
            "careless employee. A sign reads 'KEYS: MANAGER ONLY.' "
            "The exit is WEST back to the manager's office."
        ),
        "exits": {"W": 36},
        "items": ["SMALL KEY"],
    },
    38: {
        "name": "SAFE DEPOSIT BOXES",
        "desc": (
            "Rows upon rows of small steel deposit boxes line the walls. "
            "Most are rusted shut. A few lie open and empty. "
            "The only exit is SOUTH, back to the old vault entrance."
        ),
        "exits": {"S": 39},
        "items": [],
    },
    39: {
        "name": "OLD VAULT ENTRANCE",
        "desc": (
            "The entrance to the old bank vault, built decades before the "
            "new one. The massive door stands open — the mechanism still "
            "works but everyone moved to the new vault. "
            "A heavy steel door leads WEST into the vault chamber. "
            "The vault mechanism room lies to the EAST. "
            "Safe deposit boxes are to the NORTH. "
            "The corridor is to the SOUTH."
        ),
        "exits": {"S": 32, "N": 38, "E": 34, "W": 55},
        "items": [],
    },
    # ---- Vault (rooms 55-57) ----
    55: {
        "name": "THE VAULT",
        "desc": (
            "The inner vault chamber. Massive steel walls ring this cold, "
            "circular room. Empty wire racks line the walls where gold "
            "bars once sat. In the center of the room, a small trapdoor "
            "in the floor leads to a slide. A sign reads: "
            "'GOLD'S SLIDE - ONE WAY DOWN.' "
            "The exit is EAST, back to the old vault entrance."
        ),
        "exits": {"E": 39, "S": 56, "D": "floor_6"},
        "items": [],
    },
    56: {
        "name": "CHEMICAL STORAGE",
        "desc": (
            "A cramped chamber lined with corroded shelves of old chemicals. "
            "Two jars remain: one half-full of YELLOW SOLUTION, the other "
            "filled with a murky FLUID. Labels read: "
            "'SOLUTION: ANTIDOTE' and 'FLUID: INKPERSIBLE'. "
            "A small door leads NORTH into the vault chamber. "
            "The slide room is to the EAST."
        ),
        "exits": {"N": 55, "E": 57},
        "items": ["JAR OF YELLOW SOLUTION", "JAR OF FLUID"],
    },
    57: {
        "name": "GOLD'S SLIDE",
        "desc": (
            "A polished brass slide curves down into darkness. "
            "A sign at the top reads: 'GOLD'S SLIDE - NO RETURN.' "
            "Once you go down, you're on Floor 6. "
            "The chemical storage room is to the WEST."
        ),
        "exits": {"W": 56, "D": "floor_6"},
        "items": [],
    },
}


# --------------------------------------------------------------------
# Special room targets (cross-floor navigation)
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    "floor_8_stairs": {"target": "floor_8", "landing_room": 41},
    "floor_6": {"target": "floor_6", "landing_room": 57},
}


# --------------------------------------------------------------------
# Floor 7 Engine
# --------------------------------------------------------------------
class Floor7Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.vault_door_open = False   # Steel door at room 55
        self.vending_activated = False

    # ------------------------------------------------------------------
    # Item initialization (reset each time player enters floor 7)
    # ------------------------------------------------------------------
    def _init_items(self):
        return {
            33: ["TIN FOIL"],
            37: ["SMALL KEY"],
            56: ["JAR OF YELLOW SOLUTION", "JAR OF FLUID"],
        }

    # ------------------------------------------------------------------
    # Entry point from engine
    # ------------------------------------------------------------------
    def on_enter(self):
        """Called when player arrives on Floor 7."""
        self._room_items = self._init_items()
        self.vault_door_open = False
        self.vending_activated = False

    def on_leave(self):
        """Called when player leaves Floor 7."""
        pass

    # ------------------------------------------------------------------
    # Room access
    # ------------------------------------------------------------------
    def get_room(self, room_id):
        return ROOMS.get(room_id)

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    # ------------------------------------------------------------------
    # Command handling
    # ------------------------------------------------------------------
    def handle_command(self, verb, noun=""):
        loc = self.state.location

        # ---- LOOK ----
        if verb == "LOOK":
            return self._describe_room(loc)

        # ---- INVENTORY ----
        if verb == "INVENTORY" or (verb == "I" and noun == ""):
            return self._do_inventory()

        # ---- GET ----
        if verb == "GET" or verb == "TAKE" or verb == "GRAB":
            return self._do_get(noun, loc)

        # ---- DROP ----
        if verb == "DROP":
            return self._do_drop(noun, loc)

        # ---- USE ----
        if verb == "USE":
            return self._do_use(noun, verb, loc)

        # ---- OPEN ----
        if verb == "OPEN":
            return self._do_open(noun, loc)

        # ---- READ ----
        if verb == "READ":
            return self._do_read(noun, loc)

        # ---- GO / DIRECTION ----
        if verb in ("NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN",
                    "N", "S", "E", "W", "U", "D", "GO"):
            return self._do_move(verb, noun, loc)

        return None  # Fall through to engine

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _do_move(self, verb, noun, loc):
        # Normalize direction: handle GO NOUN, single-letter, or full-word verbs
        dir_map = {"N": "N", "NORTH": "N",
                   "S": "S", "SOUTH": "S",
                   "E": "E", "EAST": "E",
                   "W": "W", "WEST": "W",
                   "U": "U", "UP": "U",
                   "D": "D", "DOWN": "D"}
        verb_up = verb.upper()
        # Normalize: try verb first, then noun (for GO NOUN case)
        d_candidate = dir_map.get(verb_up, verb_up if len(verb_up) == 1 else None)
        if d_candidate is None and noun:
            d_candidate = dir_map.get(noun.upper(), noun.upper() if len(noun.upper()) == 1 else None)
        direction = d_candidate

        if not direction:
            return "Go where?"

        room = ROOMS.get(loc)
        if not room:
            return "You are nowhere."

        exits = room.get("exits", {})
        next_target = exits.get(direction)

        if next_target is None:
            return f"You can't go {direction} from here."

        # ---- Special: Floor 8 stairs (UP from room 31) ----
        if next_target == "floor_8_stairs":
            return "TRANSITION:floor_8:41"

        # ---- Special: Gold's Slide (DOWN from room 55 or 57) ----
        if next_target == "floor_6":
            return "TRANSITION:floor_6:57"

        # ---- Vault door (room 55, WEST from room 39) ----
        if next_target == 55:
            if loc == 39:
                if not self.vault_door_open:
                    if "SMALL KEY" in self.state.inventory:
                        self.vault_door_open = True
                        return (
                            "You insert the SMALL KEY into the steel door. "
                            "With a satisfying CLUNK, the lock disengages. "
                            "The heavy door swings open, revealing the vault chamber beyond."
                        )
                    else:
                        return (
                            "The steel door is locked tight. "
                            "There is a small keyhole — you need the SMALL KEY."
                        )
                else:
                    self.state.location = 55
                    return self._describe_room(55)
            else:
                self.state.location = 55
                return self._describe_room(55)

        # Normal room-to-room movement
        self.state.location = next_target
        return self._describe_room(next_target)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        # Normalize
        target = noun.upper().strip()

        # Special: SMALL KEY
        if "KEY" in target or "SMALL" in target:
            if loc == 37:
                items = self._room_items.get(37, [])
                if "SMALL KEY" in items:
                    items.remove("SMALL KEY")
                    self._room_items[37] = items
                    self.state.inventory.append("SMALL KEY")
                    self.state.flags["small_key_taken"] = True
                    return "You take the SMALL KEY from the hook. It feels heavy and important."
            return "You don't see that here."

        # Special: TIN FOIL
        if "TIN" in target or "FOIL" in target:
            if loc == 33:
                items = self._room_items.get(33, [])
                if "TIN FOIL" in items:
                    items.remove("TIN FOIL")
                    self._room_items[33] = items
                    self.state.inventory.append("TIN FOIL")
                    self.state.flags["tin_foil_taken"] = True
                    return "You grab the roll of TIN FOIL. It's a bit crinkled but usable."
            return "You don't see that here."

        # Special: JAR OF YELLOW SOLUTION
        if "SOLUTION" in target or "YELLOW" in target:
            if loc == 56:
                items = self._room_items.get(56, [])
                if "JAR OF YELLOW SOLUTION" in items:
                    items.remove("JAR OF YELLOW SOLUTION")
                    self._room_items[56] = items
                    self.state.inventory.append("JAR OF YELLOW SOLUTION")
                    self.state.flags["solution_taken"] = True
                    return "You take the JAR OF YELLOW SOLUTION. The label reads 'ANTIDOTE'."
            return "You don't see that here."

        # Special: JAR OF FLUID
        if "FLUID" in target or "INK" in target:
            if loc == 56:
                items = self._room_items.get(56, [])
                if "JAR OF FLUID" in items:
                    items.remove("JAR OF FLUID")
                    self._room_items[56] = items
                    self.state.inventory.append("JAR OF FLUID")
                    return "You take the JAR OF FLUID. The label warns 'INKPERSIBLE'."
            return "You don't see that here."

        # General: check if item is in the room
        room_items = self._room_items.get(loc, [])
        for item in room_items:
            if target.lower() in item.lower() or item.lower() in target.lower():
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.inventory.append(item)
                return f"You take the {item}."

        return "You don't see that here."

    # ------------------------------------------------------------------
    # DROP
    # ------------------------------------------------------------------
    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"

        target = noun.upper().strip()

        # Remove from inventory
        for item in list(self.state.inventory):
            if target.lower() in item.lower() or item.lower() in target.lower():
                self.state.inventory.remove(item)
                # Add back to current room
                if loc not in self._room_items:
                    self._room_items[loc] = []
                self._room_items[loc].append(item)
                return f"You drop the {item}."

        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, verb, loc):
        if not noun:
            return "Use what?"

        target = noun.upper().strip()

        # ---- USE TIN FOIL on vending machine (room 34) ----
        if ("TIN" in target or "FOIL" in target) and loc == 34:
            if "TIN FOIL" not in self.state.inventory:
                return "You don't have any tin foil."
            if self.vending_activated:
                return "The vending machine already dispensed its refund."
            self.vending_activated = True
            # Tin foil is consumed
            if "TIN FOIL" in self.state.inventory:
                self.state.inventory.remove("TIN FOIL")
            self.state.flags["vending_used"] = True
            return (
                "You stuff the TIN FOIL into the string vending machine. "
                "It sputters, whirs, and spits out a crisp DOLLAR BILL. "
                "A small banner unfurls: 'STRING VENDING MACHINE - THANK YOU!' "
                "The dollar lands at your feet."
            )

        # ---- USE SMALL KEY on steel door (room 32 or 39) ----
        if "KEY" in target and loc in (32, 39):
            if "SMALL KEY" not in self.state.inventory:
                return "You don't have the small key."
            if self.vault_door_open:
                return "The vault door is already open."
            self.vault_door_open = True
            return (
                "You insert the SMALL KEY into the steel door's lock. "
                "A heavy CLUNK echoes through the corridor. The door swings inward."
            )

        # ---- USE DOLLAR on anything ----
        if "DOLLAR" in target or "DOLLAR BILL" in target:
            if "DOLLAR" not in self.state.inventory:
                return "You don't have a dollar."
            return "There's nothing here that takes dollar bills."

        return "You can't figure out how to use that here."

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if not noun:
            return "Open what?"

        target = noun.upper().strip()

        # ---- OPEN STEEL DOOR ----
        if "DOOR" in target or "STEEL" in target:
            if loc == 32 or loc == 39:
                if self.vault_door_open:
                    self.state.location = 55
                    return self._describe_room(55)
                else:
                    if "SMALL KEY" in self.state.inventory:
                        self.vault_door_open = True
                        return (
                            "You unlock the steel door with the SMALL KEY. "
                            "It swings open with a groan."
                        )
                    else:
                        return "The steel door is locked. You need the SMALL KEY."
            return "There's no door like that here."

        # ---- OPEN VENDING MACHINE ----
        if "VEND" in target:
            if loc == 34:
                return "The vending machine doesn't open. It has a slot labeled 'TIN FOIL - $1.00'."
            return "You don't see a vending machine here."

        # ---- OPEN JAR ----
        if "JAR" in target:
            return "The jars are open already. Just pick one up if you want it."

        return "You can't open that."

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------
    def _do_read(self, noun, loc):
        if not noun:
            return "Read what?"

        target = noun.upper().strip()

        if "SIGN" in target:
            if loc == 32:
                return (
                    "The sign on the wall reads:\n"
                    "  'GOLD''S STAIRWAY - FLOOR 8 ABOVE'\n"
                    "  'BANK OF DESCENT - VAULT FLOOR'"
                )
            if loc == 34:
                return (
                    "The plastic sign reads:\n"
                    "  'STRING VENDING MACHINE'\n"
                    "  'INSERT TIN FOIL - $1.00 REFUND'"
                )
            if loc == 37:
                return "The sign reads: 'KEYS: MANAGER ONLY'."
            if loc == 55:
                return "The sign reads: 'GOLD'S SLIDE - ONE WAY DOWN'."
            if loc == 57:
                return "The sign reads: 'GOLD'S SLIDE - NO RETURN'."
            if loc == 56:
                return (
                    "Labels on the jars:\n"
                    "  YELLOW SOLUTION: 'ANTIDOTE'\n"
                    "  FLUID: 'INKPERSIBLE'"
                )

        if "SIGN ON WALL" in target:
            if loc == 32:
                return (
                    "The sign on the marble wall reads:\n"
                    "  'GOLD'S STAIRWAY - FLOOR 8 ABOVE'\n"
                    "  'BANK OF DESCENT - VAULT FLOOR'"
                )

        if "VENDING" in target or "MACHINE" in target:
            if loc == 34:
                return (
                    "The string vending machine reads:\n"
                    "  'STRING VENDING MACHINE'\n"
                    "  'INSERT TIN FOIL - $1.00 REFUND'"
                )

        return "You can't read that."

    # ------------------------------------------------------------------
    # INVENTORY
    # ------------------------------------------------------------------
    def _do_inventory(self):
        if not self.state.inventory:
            return "You are carrying nothing."
        lines = ["You are carrying:"]
        for item in self.state.inventory:
            lines.append(f"  {item}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Room description helper
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        room = ROOMS.get(room_id)
        if not room:
            return "You are in a dark void."

        lines = [f"== {room['name']} ==", "", room["desc"]]

        # List items in the room
        items = self._room_items.get(room_id, [])
        if items:
            lines.append("")
            lines.append("You see:")
            for item in items:
                lines.append(f"  {item}")

        # Vault door status
        if room_id == 32:
            if self.vault_door_open:
                lines.append("The steel door to the WEST is OPEN.")
            else:
                lines.append("The steel door to the WEST is LOCKED.")

        # Exits
        exits = room.get("exits", {})
        exit_dirs = list(exits.keys())
        if exit_dirs:
            dir_names = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST", "U": "UP", "D": "DOWN"}
            exit_strs = [dir_names.get(d, d) for d in exit_dirs]
            lines.append("")
            lines.append(f"Exits: {', '.join(exit_strs)}")

        return "\n".join(lines)
