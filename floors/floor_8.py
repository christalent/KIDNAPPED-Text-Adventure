"""
KIDNAPPED! - Floor 8: The Aquarium
Piranha pool, guard dog, helium balloon puzzle.

Entry from Floor 9 via elevator DOWN -> Room 21.
Goal: Get past the piranha pool and descend via stairs to Floor 7.

Based on:
- BASIC source from SoftSide Vol 3 No 03 (clean PDF)
- RetroGamesTroove map: https://www.retrogamestrove.com/game-149-kidnapped-1980/
- Confirmed bidirectional pairs from BASIC analysis
"""

FLOOR_NUMBER = 8
NEXT_FLOOR_DOWN = 7

# --------------------------------------------------------------------
# Room map (Floor 8, rooms 21-28):
# Based on RetroGamesTroove + BASIC item data
#
# Layout:
#   [28] Stairs DOWN to Floor 7
#    |
#   [24] Storage (balloon)
#    |
# [27]--[22] Pool Hall (piranhas)---[25] Maintenance (glue)
#          |
#         [21] Elevator from Floor 9
#
# Items (from BASIC DATA statements):
# Room 20 (Floor 9): THICK CURTAIN SHEET, SUPER GLUE, WOODEN STAIR STEP
#   NOTE: These items appear in Floor 9's DATA but are referenced for Floor 8 puzzles
# Room 24: LARGE DEFLATED BALLOON (from BASIC DATA room 29)
# Room 28: HELIUM TANK (from BASIC DATA room 28)
# --------------------------------------------------------------------
ROOMS = {
    21: {
        "name": "ELEVATOR LANDING",
        "desc": (
            "You step out of the elevator into a wide, humid corridor. "
            "The air is thick with the smell of fish food and chlorine. "
            "Blue LED strips flicker overhead, casting rippling light on the walls "
            "- like being underwater. A sign reads 'AQUARIUM WING.' "
            "The elevator doors stand open to the SOUTH - you came from Floor 9. "
            "A concrete stairway in the same area leads DOWN to Floor 7. "
            "The main aquarium corridor lies to the NORTH."
        ),
        "exits": {"N": 22, "D": "floor_7"},  # S=elevator handled specially
        "items": [],
    },
    22: {
        "name": "PIRANHA POOL - MAIN HALL",
        "desc": (
            "You stand in the heart of the aquarium wing. A massive "
            "rectangular pool dominates the room, its water murky and "
            "dark. Glinting scales. A row of needle-sharp teeth. "
            "PIRANHAS. Dozens of them, circling just below the surface. "
            "A heavy THICK CURTAIN SHEET hangs on the south wall - "
            "someone's emergency supply. "
            "To the SOUTH, the elevator landing. "
            "To the NORTH, the aquarium storage area. "
            "To the EAST, a maintenance corridor. "
            "To the WEST, a pool viewing gallery."
        ),
        "exits": {"S": 21, "N": 24, "E": 25, "W": 27},
        "items": ["THICK CURTAIN SHEET"],
    },
    24: {
        "name": "AQUARIUM STORAGE",
        "desc": (
            "A cramped storage room lined with shelving units. "
            "Bags of fish food, water testing kits, replacement filters. "
            "A LARGE DEFLATED BALLOON is wedged in the corner - "
            "left behind by some long-gone party. "
            "The main pool hall is to the SOUTH. "
            "A stairway is to the NORTH."
        ),
        "exits": {"S": 22, "N": 28},
        "items": ["LARGE DEFLATED BALLOON"],
    },
    25: {
        "name": "MAINTENANCE CORRIDOR",
        "desc": (
            "A narrow side corridor running east from the main hall. "
            "Tanks of exotic fish line the walls - jellyfish, seahorses, "
            "a grumpy octopus. A faded sign reads: "
            "'HELIUM FILLS - BALLOON RENTALS AVAILABLE.' "
            "A cluttered WORKBENCH holds cleaning supplies and spare parts. "
            "On the workbench, a tube of SUPER GLUE - still usable. "
            "The main pool hall is to the WEST."
        ),
        "exits": {"W": 22},
        "items": ["SUPER GLUE"],
    },
    27: {
        "name": "POOL VIEWING GALLERY",
        "desc": (
            "A wide gallery with reinforced glass panels overlooking the "
            "piranha pool from the west side. The fish circle in dark, "
            "synchronous patterns below. A small MAINTENANCE HATCH is "
            "set into the floor near the wall. "
            "The main hall is to the EAST."
        ),
        "exits": {"E": 22},
        "items": [],
    },
    28: {
        "name": "STAIRS DOWN",
        "desc": (
            "A narrow concrete stairway at the north end of the storage "
            "area leads DOWN into darkness. A sign reads: 'FLOOR 7 - "
            "BANK OF DESCENT.' "
            "One of the wooden steps is CRACKED AND BROKEN - "
            "the glue joint gave way. You could use SUPER GLUE "
            "to fix it before descending. "
            "A TANK OF HELIUM GAS sits strapped to a cart in the corner, "
            "labeled 'AQUARIUM EVENTS ONLY.' "
            "The storage area is to the SOUTH."
        ),
        "exits": {"S": 24, "D": "floor_7"},
        "items": ["TANK OF HELIUM GAS"],
    },
}

# --------------------------------------------------------------------
# Special room targets (cross-floor navigation)
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    "floor_9":  {"target": "floor_9",  "landing_room": 9},
    "floor_7":  {"target": "floor_7",  "landing_room": 31},
}


# --------------------------------------------------------------------
# Floor 8 Engine
# --------------------------------------------------------------------
class Floor8Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.balloon_inflated = False
        self.stairs_fixed = False

    # ------------------------------------------------------------------
    # Item initialization (reset each time player enters floor 8)
    # ------------------------------------------------------------------
    def _init_items(self):
        return {
            22: ["THICK CURTAIN SHEET"],
            24: ["LARGE DEFLATED BALLOON"],
            25: ["SUPER GLUE"],
            28: ["TANK OF HELIUM GAS"],
        }

    # ------------------------------------------------------------------
    # Entry point from engine
    # ------------------------------------------------------------------
    def on_enter(self):
        """Called when player arrives on Floor 8."""
        self._room_items = self._init_items()
        self.balloon_inflated = False
        self.stairs_fixed = False

    def on_leave(self):
        """Called when player leaves Floor 8."""
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

        # Normalize verb
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
        if verb in ("USE", "APPLY"):
            return self._do_use(noun, loc), False
        if verb in ("READ", "EXAMINE", "X", "CHECK"):
            return self._examine(noun, loc), False
        if verb in ("FIX", "REPAIR"):
            return self._do_fix(noun, loc), False
        if verb in ("INFLATE", "BLOW", "FILL"):
            return self._do_inflate(noun), False
        if verb in ("OPEN", "UNLOCK"):
            return self._do_open(noun, loc), False

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

        return None  # Fall through to engine

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _go(self, direction, loc):
        r = self.get_room(loc)
        if not r:
            return "You are nowhere."
        exits = r.get("exits", {})
        next_target = exits.get(direction)
        if next_target is None:
            return f"You can't go {direction} from here."
        # Handle special transitions
        if isinstance(next_target, str):
            if next_target == "floor_9":
                return f"TRANSITION:{next_target}:9"
            if next_target == "floor_7":
                if not self.stairs_fixed:
                    return (
                        "You start down the stairs - but the broken step "
                        "gives way! You'd better FIX it first."
                    )
                return f"TRANSITION:{next_target}:31"
        self.state.location = next_target
        return self._describe_room(next_target)

    def _go_up(self, loc):
        # Elevator: going UP from room 21 goes back to floor 9
        if loc == 21:
            return f"TRANSITION:floor_9:9"
        return self._go("U", loc)

    def _go_down(self, loc):
        # Special case: stairs down from room 28
        if loc == 28:
            if not self.stairs_fixed:
                return (
                    "You start down - but the broken step gives way! "
                    "You catch yourself. That step is dangerous. "
                    "You'll need to FIX it before you can safely descend."
                )
            return f"TRANSITION:floor_7:31"
        return self._go("D", loc)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        room_items = self._room_items.get(loc, [])

        # ---- THICK CURTAIN SHEET ----
        if any(k in noun for k in ("CURTAIN", "SHEET", "CLOTH")):
            if loc == 22:
                if "THICK CURTAIN SHEET" in room_items:
                    room_items.remove("THICK CURTAIN SHEET")
                    self._room_items[22] = room_items
                    self.state.add_item("THICK CURTAIN SHEET")
                    return "You take the THICK CURTAIN SHEET. Heavy-duty fabric."
                return "No curtain here."
            return "No curtain here."

        # ---- SUPER GLUE ----
        if "GLUE" in noun:
            if loc == 25:
                if "SUPER GLUE" in room_items:
                    room_items.remove("SUPER GLUE")
                    self._room_items[25] = room_items
                    self.state.add_item("SUPER GLUE")
                    return "You pocket the tube of SUPER GLUE."
                return "No glue here."
            return "You don't see any glue here."

        # ---- TANK OF HELIUM ----
        if "HELIUM" in noun or "TANK" in noun:
            if loc == 28:
                if "TANK OF HELIUM GAS" in room_items:
                    room_items.remove("TANK OF HELIUM GAS")
                    self._room_items[28] = room_items
                    self.state.add_item("TANK OF HELIUM GAS")
                    return "You wheel out the TANK OF HELIUM GAS. It's heavy but manageable."
                return "No helium tank here."
            return "You don't see a helium tank here."

        # ---- LARGE DEFLATED BALLOON ----
        if "BALLOON" in noun:
            if loc == 24:
                if "LARGE DEFLATED BALLOON" in room_items:
                    room_items.remove("LARGE DEFLATED BALLOON")
                    self._room_items[24] = room_items
                    self.state.add_item("LARGE DEFLATED BALLOON")
                    return "You grab the LARGE DEFLATED BALLOON. It's limp but large - big enough to carry you."
                return "No balloon here."
            return "You don't see a balloon here."

        # General check
        for item in list(room_items):
            if noun.lower() in item.lower() or item.lower() in noun.lower():
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.add_item(item)
                return f"You take the {item}."
        return "You don't see that here."

    # ------------------------------------------------------------------
    # DROP
    # ------------------------------------------------------------------
    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"
        for item in list(self.state.inventory):
            if noun.lower() in item.lower() or item.lower() in noun.lower():
                self.state.remove_item(item)
                self._room_items.setdefault(loc, []).append(item)
                return f"You drop the {item}."
        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"
        inv = self.state.inventory

        # ---- USE HELIUM TANK on BALLOON ----
        if "HELIUM" in noun or "TANK" in noun:
            if "TANK OF HELIUM GAS" not in inv:
                return "You don't have the helium tank."
            if "LARGE DEFLATED BALLOON" not in inv:
                return "You don't have a balloon to fill."
            if self.balloon_inflated:
                return "The balloon is already inflated."
            self.balloon_inflated = True
            # Update balloon to inflated version
            self.state.remove_item("LARGE DEFLATED BALLOON")
            self.state.add_item("LIVE HELIUM BALLOON")
            return (
                "You attach the nozzle of the helium tank to the balloon's "
                "valve and crack it open. The balloon hisses and inflates, "
                "growing large and round - and begins to tug upward, pulling "
                "your hand! You've got a LIVE HELIUM BALLOON now. "
                "It floats at the end of an invisible tether."
            )

        # ---- USE BALLOON / HELIUM BALLOON ----
        if "BALLOON" in noun or "HELIUM" in noun:
            if "LARGE DEFLATED BALLOON" not in inv and "LIVE HELIUM BALLOON" not in inv:
                return "You don't have a balloon."
            if not self.balloon_inflated:
                return "The balloon is still deflated. You need to INFLATE it first."
            if loc == 22 or loc == 27:
                return (
                    "You hold the LIVE HELIUM BALLOON over the piranha pool. "
                    "The fish surge toward it, thrashing! The balloon floats "
                    "just above the water's surface. You could cross the pool "
                    "if you stayed aloft - the balloon keeps you above the water."
                )
            return "The helium balloon bobs at the end of an invisible tether."

        # ---- USE SUPER GLUE ----
        if "GLUE" in noun or "SUPER" in noun:
            if "SUPER GLUE" not in inv:
                return "You don't have any glue."
            if loc == 28:
                return self._do_fix("STEP", loc)
            return "There's nothing here that needs gluing right now."

        # ---- USE CURTAIN ----
        if "CURTAIN" in noun or "SHEET" in noun:
            if "THICK CURTAIN SHEET" not in inv:
                return "You don't have the curtain."
            return "You could use the curtain as a safety line, but the balloon is more direct."

        return "You can't figure out how to use that here."

    # ------------------------------------------------------------------
    # FIX / REPAIR
    # ------------------------------------------------------------------
    def _do_fix(self, noun, loc):
        if not noun:
            return "Fix what?"
        if "STEP" in noun or "STAIR" in noun:
            if loc != 28:
                return "There's no broken step here."
            if "SUPER GLUE" not in self.state.inventory:
                return "You need something to fix it with. SUPER GLUE would work."
            if self.stairs_fixed:
                return "The step is already fixed."
            self.stairs_fixed = True
            return (
                "You apply the SUPER GLUE to the cracked wooden step, "
                "pressing the broken pieces together. It holds! "
                "The step is solid now. You can safely go DOWN."
            )
        return "Nothing to fix here."

    # ------------------------------------------------------------------
    # INFLATE
    # ------------------------------------------------------------------
    def _do_inflate(self, noun):
        if "BALLOON" in noun or "HELIUM" in noun:
            if "LARGE DEFLATED BALLOON" not in self.state.inventory:
                return "You don't have a balloon."
            if self.balloon_inflated:
                return "The balloon is already inflated."
            # Redirect to USE HELIUM
            return self._do_use("HELIUM", self.state.location)
        return "Inflate what?"

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if "CABINET" in noun or "DOOR" in noun or "HATCH" in noun:
            if loc == 25:
                return "The maintenance hatch is already open. Nothing useful inside."
            if loc == 22:
                return "The curtain is hanging loose, not in a cabinet."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return self._describe_room(loc)
        noun = noun.upper()
        room_items = self._room_items.get(loc, [])
        inv = self.state.inventory

        if "POOL" in noun or "PIRANHA" in noun:
            if loc in (22, 27):
                return (
                    "The piranha pool is murky and dark. Dozens of sharp-toothed "
                    "fish circle just below the surface. They're fast and vicious - "
                    "you wouldn't last a second in that water."
                )
            return "You don't see a pool here."

        if "HELIUM" in noun or "TANK" in noun:
            if "TANK OF HELIUM GAS" in room_items or "TANK OF HELIUM GAS" in inv:
                return "A heavy steel tank labeled 'AQUARIUM EVENTS ONLY'. The helium inside is still pressurized."
            return "No helium tank here."

        if "BALLOON" in noun:
            if "LARGE DEFLATED BALLOON" in room_items or "LARGE DEFLATED BALLOON" in inv:
                if self.balloon_inflated:
                    return "A large, round helium balloon. It tugs upward gently."
                return "A large, limp balloon. It needs helium to inflate."
            return "No balloon here."

        if "GLUE" in noun:
            if "SUPER GLUE" in room_items or "SUPER GLUE" in inv:
                return "A tube of strong adhesive. Should fix just about anything."
            return "No glue here."

        if "CURTAIN" in noun or "SHEET" in noun:
            if "THICK CURTAIN SHEET" in room_items or "THICK CURTAIN SHEET" in inv:
                return "Heavy-duty curtain fabric. Could be useful as a safety line."
            return "No curtain here."

        if "STAIR" in noun or "STEP" in noun:
            if loc == 28:
                if self.stairs_fixed:
                    return "The wooden step is solid - the glue held perfectly."
                return "One of the wooden steps is cracked and loose. A blob of glue would fix it."
            return "No stairs here."

        if "GALLERY" in noun or "VIEW" in noun:
            if loc == 27:
                return "Reinforced glass panels overlook the piranha pool. The fish circle below."
            return "Nothing special."

        return "You don't see anything unusual."

    # ------------------------------------------------------------------
    # INVENTORY
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
