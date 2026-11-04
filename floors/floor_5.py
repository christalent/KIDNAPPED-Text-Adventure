"""
KIDNAPPED! - Floor 5: The Mary Poppins Floor
"The weird one" — finding Mary Poppin's umbrella

Entry from Floor 6 via stairs DOWN -> Room 51.
Goal: Navigate the absurdist Mary Poppins-themed floor, find the umbrella, descend.

Puzzle flow (the absurd chain):
  1. SIGN in 52 hints "SIDE END OPEN MOST REVERSIBLE" - the most
     REVERSIBLE thing on the floor is the REVERSIBLE PIE.
  2. PUSH BUTTON in 56 dispenses a REVERSIBLE PIE (one-time use).
  3. USE the REVERSIBLE PIE on the SUPER CALIFRAGILISTIC machine
     in 57 - the machine runs in REVERSE and the magical barrier
     blocking the umbrella vault is disabled.
  4. JUMP at the JUMP PLATFORM in 58 - with the machine reversed,
     the bounce amplifies and carries the player up into the
     umbrella vault (59). N from 58 is also unblocked.
  5. GET the MAGIC UMBRELLA in 59 and head D to Floor 4.

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
        "items": ["SUPER CALIFRAGILISTIC MACHINE"],
    },
    58: {
        "name": "JUMP CHAMBER",
        "desc": (
            "A room with a strange, springy floor. "
            "In the center, a JUMP PLATFORM with a big red button on top. "
            "The Super Califragilator room is to the SOUTH. "
            "A shimmer in the air above suggests there's something up there, "
            "beyond reach."
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

# Items that are fixed scenery and cannot be taken.
FIXED_ITEMS = {
    "SIGN ON WALL",
    "GRAFFITI ON WALL",
    "PUSH BUTTON",
    "JUMP PLATFORM",
    "SUPER CALIFRAGILISTIC MACHINE",
}

SPECIAL_ROOMS = {
    "floor_6": {"target": "floor_6", "landing_room": 26},
    "floor_4": {"target": "floor_4", "landing_room": 61},
}


class Floor5Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        self.umbrella_found = False
        self.pie_taken = False
        self.pie_used = False
        self.machine_activated = False

    def _init_items(self):
        return {
            52: ["SIGN ON WALL"],
            53: ["GRAFFITI ON WALL"],
            55: ["SMALL UMBRELLA"],
            56: ["PUSH BUTTON"],
            57: ["SUPER CALIFRAGILISTIC MACHINE"],
            58: ["JUMP PLATFORM"],
            59: ["MAGIC UMBRELLA"],
        }

    def on_enter(self):
        self._room_items = self._init_items()
        self.umbrella_found = False
        self.pie_taken = False
        self.pie_used = False
        self.machine_activated = False
        # Player arrives from Floor 6 (stairs down) -> landing room 51.
        self.state.location = 51
        if not hasattr(self.state, "inventory"):
            self.state.inventory = []

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

        if verb in ("LOOK", "L"):
            return self._look(), False
        if verb in ("INVENTORY", "I", "INV"):
            return self._do_inventory(), False
        if verb in ("GET", "TAKE", "GRAB", "PICK"):
            return self._do_get(noun, loc), False
        if verb in ("DROP", "PUT", "PLACE"):
            return self._do_drop(noun, loc), False
        if verb in ("USE", "APPLY", "EAT"):
            return self._do_use(noun, loc), False
        if verb in ("PUSH", "PRESS"):
            return self._do_push(noun, loc), False
        if verb in ("JUMP",):
            return self._do_jump(noun, loc), False
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
            if next_target == "floor_6":
                return f"TRANSITION:{next_target}:26", True
            if next_target == "floor_4":
                return f"TRANSITION:{next_target}:61", True
        # Magical barrier in room 58 N -> 59 requires machine_activated
        if loc == 58 and direction == "N" and not self.machine_activated:
            return (
                "There's a magical barrier shimmering in the air above. "
                "The SUPER CALIFRAGILISTIC machine on the floor below is "
                "still running forward and its field blocks the way. "
                "If you could REVERSE the machine, the barrier would drop."
            ), False
        self.state.location = next_target
        return self._look(), False

    def _go_up(self, loc):
        if loc == 51:
            return f"TRANSITION:floor_6:26", True
        return self._go("U", loc)

    def _go_down(self, loc):
        if loc == 59:
            return f"TRANSITION:floor_4:61", True
        return self._go("D", loc)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"
        room_items = self._room_items.get(loc, [])

        for item in list(room_items):
            if noun.lower() in item.lower() or item.lower() in noun.lower():
                if item in FIXED_ITEMS:
                    return f"You can't take the {item}."
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.add_item(item)
                if item == "MAGIC UMBRELLA":
                    self.umbrella_found = True
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

    # ------------------------------------------------------------------
    # USE / APPLY
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"
        inv = self.state.inventory

        # UMBRELLA
        if "UMBRELLA" in noun:
            if "MAGIC UMBRELLA" in inv:
                if loc == 59:
                    return "The magic umbrella hums in your hand, ready for whatever comes next."
                return (
                    "You open Mary Poppins' umbrella. A magical breeze "
                    "lifts you momentarily - but not enough to fly."
                )
            if "SMALL UMBRELLA" in inv:
                return "A nice umbrella, but not the magical one."
            return "You don't have an umbrella to use."

        # REVERSIBLE PIE / PIE
        if "PIE" in noun:
            if "REVERSIBLE PIE" in inv:
                if loc == 57:
                    if self.machine_activated:
                        return "The SUPER CALIFRAGILISTIC machine is already running in reverse."
                    # Use the pie to activate/reverse the machine
                    self.pie_used = True
                    self.machine_activated = True
                    self.state.remove_item("REVERSIBLE PIE")
                    return (
                        "You press the REVERSIBLE PIE against the "
                        "SUPER CALIFRAGILISTIC machine. The gears grind, "
                        "then REVERSE direction with a satisfied CLUNK. "
                        "A slip of paper pops out: 'MAGICAL BARRIER IN "
                        "ATTIC DISABLED. ENJOY THE VIEW.'"
                    )
                return (
                    "You hold up the REVERSIBLE PIE. It hums with magic, "
                    "but doesn't seem to do anything here. Maybe try it "
                    "in the room with the SUPER CALIFRAGILISTIC machine."
                )
            return "You don't have a pie to use."

        return "You can't figure out how to use that here."

    # ------------------------------------------------------------------
    # PUSH / PRESS
    # ------------------------------------------------------------------
    def _do_push(self, noun, loc):
        # PUSH BUTTON is the only pushable thing worth handling
        if "BUTTON" in noun or "PUSH" in noun or noun == "":
            if loc == 56:
                if self.pie_taken:
                    return "The trapdoor is closed. Nothing more comes down."
                self.pie_taken = True
                self.state.add_item("REVERSIBLE PIE")
                return (
                    "You push the button. Somewhere, a tiny bell rings. "
                    "A trapdoor opens and a pie descends from above. "
                    "'REVERSIBLE PIE,' the label says. "
                    "You take it."
                )
            if loc == 58:
                return "The button on the JUMP PLATFORM is for JUMPING, not pushing."
            return "There's nothing here to push."
        return "You can't push that."

    # ------------------------------------------------------------------
    # JUMP
    # ------------------------------------------------------------------
    def _do_jump(self, noun, loc):
        if loc == 58:
            if self.machine_activated:
                # Successfully jump to room 59
                self.state.location = 59
                return (
                    "You leap onto the springy JUMP PLATFORM! BOING! "
                    "With the SUPER CALIFRAGILISTIC machine now running "
                    "in REVERSE, the bounce amplifies and you SOAR upward "
                    "through the disabled magical barrier! "
                    "You tumble into the umbrella vault.\n\n" + self._look()
                )
            return (
                "You leap onto the springy JUMP PLATFORM! BOING! "
                "You bounce high into the air. As you come down, "
                "you notice a hidden passage that only appears "
                "when you're at the apex of your jump. "
                "But a magical barrier blocks it. The SUPER "
                "CALIFRAGILISTIC machine below is interfering somehow."
            )
        return "There's nothing to jump on here."

    # ------------------------------------------------------------------
    # EXAMINE / READ
    # ------------------------------------------------------------------
    def _examine(self, noun, loc):
        if not noun:
            return self._look()
        noun_u = noun.upper()
        inv = self.state.inventory
        room_items = self._room_items.get(loc, [])

        if "UMBRELLA" in noun_u:
            if "MAGIC UMBRELLA" in inv or "MAGIC UMBRELLA" in room_items:
                return (
                    "Mary Poppins' magical umbrella. Cherry red with a "
                    "curved handle. You can feel the magic humming in the "
                    "handle. It's beautiful."
                )
            if "SMALL UMBRELLA" in inv or "SMALL UMBRELLA" in room_items:
                return "A nice umbrella, but ordinary. Not the magical one."
            return "No umbrella here."

        if "MACHINE" in noun_u or "CALIF" in noun_u:
            if loc == 57:
                if self.machine_activated:
                    return (
                        "The SUPER CALIFRAGILISTIC machine is now running "
                        "in REVERSE. The gears spin the other way and it "
                        "makes a satisfied humming sound. The magical "
                        "barrier in the room above is down."
                    )
                return (
                    "The SUPER CALIFRAGILISTIC machine. It needs something "
                    "to activate it. The note says: 'ONE PUSH TO BEGIN.' "
                    "A drawer at the base looks like it might accept a pie."
                )
            return "No machine here."

        if "SIGN" in noun_u:
            if loc == 52:
                return (
                    "The sign reads: 'SIDE END OPEN MOST REVERSIBLE.' "
                    "It doesn't make sense. But you wonder - the most "
                    "REVERSIBLE thing in the area might be the answer. "
                    "There's a pie shop to the EAST, perhaps?"
                )
            return "You don't see a sign here."

        if "GRAFFITI" in noun_u:
            if loc == 53:
                return "The graffiti on the ceiling reads: 'MARY POPPINS WAS HERE.'"
            return "No graffiti here."

        if "BUTTON" in noun_u:
            if loc == 56:
                if self.pie_taken:
                    return "The PUSH BUTTON. You already pressed it. The trapdoor above is closed."
                return "The PUSH BUTTON on the wall, labeled 'PUSH FOR MEANING.'"
            return "No button here."

        if "PIE" in noun_u:
            if "REVERSIBLE PIE" in inv:
                return (
                    "A REVERSIBLE PIE. The label says: "
                    "'For reversing magical mechanisms. Use with caution.'"
                )
            if loc == 56 and not self.pie_taken:
                return (
                    "There are pies on the shelves, but they are just "
                    "decorative. You need to push the button to get a real one."
                )
            return "No pie here."

        if "JUMP" in noun_u or "PLATFORM" in noun_u:
            if loc == 58:
                return "A springy JUMP PLATFORM. You can JUMP on it."
            return "No platform here."

        if "NOTE" in noun_u:
            if loc == 54:
                return "The note reads: '2+2=5 OR 2+2=22.'"
            if loc == 57:
                return "The note on the machine reads: 'ONE PUSH TO BEGIN.'"
            return "You don't see a note here."

        return "Nothing unusual."

    # ------------------------------------------------------------------
    # Inventory / look
    # ------------------------------------------------------------------
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
                    if d == "U" and t == "floor_6":
                        exit_list.append("U to Floor 6")
                    elif d == "D" and t == "floor_4":
                        exit_list.append("D to Floor 4")
                    else:
                        exit_list.append(f"{d} to {t}")
        if exit_list:
            desc += "\n\nExits: " + ", ".join(exit_list) + "."
        return desc

    # ------------------------------------------------------------------
    # Exits verification
    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        """Verify all numeric exits are bidirectional. Returns list of errors."""
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
    e = Floor5Engine.verify_exits()
    if e:
        print(f"FAIL: {len(e)} errors:")
        for x in e:
            print(f"  {x}")
    else:
        print(f"PASS: All exits bidirectional ({len(ROOMS)} rooms)")
