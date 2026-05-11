"""
KIDNAPPED! - Floor 8: The Aquarium
Piranha pool, guard dog, helium balloon puzzle.
Entry from Floor 9 via elevator DOWN -> Room 21.
Goal: Get past the piranha pool and descend via stairs to Floor 7.
"""

FLOOR_NUMBER = 8
NEXT_FLOOR_DOWN = 7

# --------------------------------------------------------------------
# Room map (verified bidirectional):
#  21: S=floor_9, N=22, D=floor_7 (elevator landing + stairs in same area)
#  22: S=21, N=24, E=25, W=27
#  24: S=22, N=28
#  25: W=22
#  27: E=22
#  28: S=24, D=floor_7
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
        "exits": {"S": "floor_9", "U": "floor_9", "N": 22, "D": "floor_7"},
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
            "A narrow side corridor running west from the main hall. "
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

        # ---- ROPE ----
        # Rope is not on this floor; it was on Floor 7 (bank vault storage)
        if "ROPE" in noun:
            return "No rope on this floor."

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
        if ("HELIUM" in noun or "TANK" in noun):
            if "TANK OF HELIUM GAS" not in inv:
                return "You don't have the helium tank."
            if "LARGE DEFLATED BALLOON" not in inv:
                return "You don't have a balloon to fill."
            if self.balloon_inflated:
                return "The balloon is already inflated."
            self.balloon_inflated = True
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
        if "GLUE" in noun or "SUPER GLUE" in noun:
            if "SUPER GLUE" not in inv:
                return "You don't have any glue."
            if loc == 28:
                return self._do_fix("STEP", loc)
            return "There's nothing here that needs gluing right now."

        # ---- USE CURTAIN ----
        if "CURTAIN" in noun or "SHEET" in noun:
            if "THICK CURTAIN SHEET" not in inv:
                return "You don't have the curtain."
            return "The heavy curtain sheet could protect you from something..."

        return "You can't figure out how to use that here."

    # ------------------------------------------------------------------
    # FIX / REPAIR
    # ------------------------------------------------------------------
    def _do_fix(self, noun, loc):
        inv = self.state.inventory
        if not noun:
            return "Fix what?"
        if "STEP" in noun or "STAIR" in noun or "BROKEN" in noun or "GLUE" in noun:
            if loc != 28:
                return "There's nothing here that needs fixing."
            if "SUPER GLUE" not in inv:
                return "You need SUPER GLUE to fix the broken step."
            if self.stairs_fixed:
                return "The step is already fixed."
            self.stairs_fixed = True
            return (
                "You squeeze the SUPER GLUE into the cracked joint of the "
                "broken wooden step. Hold it steady for a moment... "
                "The glue sets. The step is solid again. "
                "The way DOWN is now safe."
            )
        return "Nothing here needs fixing."

    # ------------------------------------------------------------------
    # INFLATE
    # ------------------------------------------------------------------
    def _do_inflate(self, noun):
        inv = self.state.inventory
        if "BALLOON" in noun or "HELIUM" in noun:
            if "TANK OF HELIUM GAS" not in inv:
                return "You don't have a helium tank."
            if "LARGE DEFLATED BALLOON" not in inv:
                return "You don't have a deflated balloon."
            if self.balloon_inflated:
                return "The balloon is already inflated."
            self.balloon_inflated = True
            return (
                "You attach the helium tank to the balloon valve and open the nozzle. "
                "The balloon swells, grows buoyant, and tugs at your hand! "
                "You've got a LIVE HELIUM BALLOON."
            )
        return "Inflate what?"

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if not noun:
            return "Open what?"
        if "HATCH" in noun and loc == 27:
            return "The maintenance hatch is sealed tight. You'd need tools to open it."
        if "TANK" in noun and loc == 28:
            return "The helium tank is ready - just use it to fill the balloon."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE / READ
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return "Examine what?"

        # ---- PIRANHAS / POOL ----
        if any(k in noun for k in ("PIRANHA", "PIRANA", "POOL", "WATER", "FISH", "TANK")):
            if loc in (22, 27):
                if self.balloon_inflated:
                    return (
                        "The piranhas circle below, eyeing the floating "
                        "helium balloon. They surge upward when it dips "
                        "close to the water. You could cross the pool "
                        "if you stayed above the surface - the balloon "
                        "would keep you aloft."
                    )
                return (
                    "The piranhas are not friendly. Sharp teeth, dark eyes. "
                    "They circle in synchronized fury. Do NOT touch the water."
                )

        # ---- BALLOON ----
        if "BALLOON" in noun:
            if "LARGE DEFLATED BALLOON" in self.state.inventory:
                return "A large, limp balloon. Big enough to carry you - if filled with helium."
            if loc == 24 and "LARGE DEFLATED BALLOON" in self._room_items.get(24, []):
                return "A large deflated balloon wedged in the corner of the storage room."
            if "LIVE HELIUM BALLOON" in self.state.inventory:
                return "A large balloon inflated with helium. It tugs upward at the end of an invisible tether."
            return "You don't see a balloon."

        # ---- HELIUM / TANK ----
        if "HELIUM" in noun or "TANK" in noun:
            if "TANK OF HELIUM GAS" in self.state.inventory:
                return "A dented helium tank with a standard inflation valve."
            if loc == 28:
                return "A dented but functional TANK OF HELIUM GAS on a cart, labeled 'AQUARIUM EVENTS ONLY.'"
            return "You don't see a helium tank."

        # ---- STEP / STAIRS ----
        if "STEP" in noun or "STAIR" in noun:
            if loc == 28:
                if self.stairs_fixed:
                    return "The wooden step is solid - the SUPER GLUE held."
                return "The wooden step is cracked and broken at the glue joint. Dangerous. Need SUPER GLUE to fix it."
            return "Nothing broken here."

        # ---- SUPER GLUE ----
        if "GLUE" in noun:
            if "SUPER GLUE" in self.state.inventory:
                return "Industrial-strength SUPER GLUE. Bonds instantly."
            if loc == 25 and "SUPER GLUE" in self._room_items.get(25, []):
                return "A tube of industrial SUPER GLUE on the workbench, still usable."
            return "You don't see any glue."

        # ---- CURTAIN ----
        if "CURTAIN" in noun or "SHEET" in noun:
            if "THICK CURTAIN SHEET" in self.state.inventory:
                return "A heavy, thick curtain sheet. Good for wrapping or protecting."
            if loc == 22 and "THICK CURTAIN SHEET" in self._room_items.get(22, []):
                return "A heavy THICK CURTAIN SHEET hanging on the south wall."
            return "No curtain here."

        # ---- HATCH ----
        if "HATCH" in noun and loc == 27:
            return "A small maintenance hatch set into the floor near the wall. Sealed tight."

        # ---- SIGN ----
        if "SIGN" in noun:
            if loc == 21:
                return "'AQUARIUM WING.'"
            if loc == 25:
                return "'HELIUM FILLS - BALLOON RENTALS AVAILABLE.'"
            if loc == 28:
                return "'FLOOR 7 - BANK OF DESCENT.' The sign also notes the broken step."

        # ---- ELEVATOR ----
        if "ELEVATOR" in noun and loc == 21:
            return "The old elevator doors stand open. You came UP from Floor 9."

        return f"You examine the {noun}."

    # ------------------------------------------------------------------
    # INVENTORY
    # ------------------------------------------------------------------
    def _do_inventory(self):
        inv = self.state.inventory
        items = []
        for item in inv:
            if item == "LARGE DEFLATED BALLOON" and self.balloon_inflated:
                items.append("LIVE HELIUM BALLOON")
            else:
                items.append(item)
        if not items:
            return "You are carrying nothing."
        lines = ["You are carrying:"]
        for item in items:
            lines.append(f"  {item}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Room description helper
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        room = self.get_room(room_id)
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

        # Stairs status at room 28
        if room_id == 28:
            if self.stairs_fixed:
                lines.append("The broken step looks solid now.")
            else:
                lines.append("One of the wooden steps is cracked - dangerous!")

        # Balloon status at pool hall
        if room_id == 22 and self.balloon_inflated:
            lines.append("A LIVE HELIUM BALLOON bobs above the piranha pool.")

        # Exits
        exits = room.get("exits", {})
        exit_dirs = list(exits.keys())
        if exit_dirs:
            dir_names = {"N": "NORTH", "S": "SOUTH", "E": "EAST", "W": "WEST", "U": "UP", "D": "DOWN"}
            exit_strs = [dir_names.get(d, d) for d in exit_dirs]
            lines.append("")
            lines.append(f"Exits: {', '.join(exit_strs)}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Verify exits (bidirectional check)
    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        errors = []
        opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
        for rid, r in ROOMS.items():
            for d, t in r["exits"].items():
                ro = opp[d]
                # Special transitions don't have reverse exits in ROOMS - skip
                if isinstance(t, str):
                    continue
                if t not in ROOMS:
                    errors.append(f"Room {rid} -> {d}={t}, but room {t} does not exist")
                    continue
                if ro not in ROOMS[t].get("exits", {}):
                    errors.append(f"Room {rid} -> {d}={t}, but {t} has no {ro} exit")
                elif ROOMS[t]["exits"][ro] != rid:
                    errors.append(f"Room {rid} -> {d}={t}, but {t} -> {ro}={ROOMS[t]['exits'][ro]} (expected {rid})")
        return errors


if __name__ == "__main__":
    e = Floor8Engine.verify_exits()
    if e:
        print(f"FAIL: {len(e)} errors:")
        for x in e:
            print(f"  {x}")
    else:
        print(f"OK: All exits bidirectional ({len(ROOMS)} rooms)")
