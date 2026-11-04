"""
KIDNAPPED! - Floor 9: The Elevator Hallway (starting floor)

Ground truth: FLOOR9_AUDIT_2026-11-03.md - pixel-derived room and item
tables read from KIDNAPPED_Original.pdf (SoftSide, Dec 1980), reconciled
against two published walkthroughs (sol_gunness.txt, sol_atari.txt) and
Garry Francis's 2015 floor map. Every move of both walkthroughs replays
cleanly on the table below. Do not trust KIDNAPPED.BAS, PARSED_BASIC_SOURCE.txt,
SPEC.md or the earlier version of this file - the PDF OCR layer reads a
printed 4 as a 1, and the old port had rooms 13-17 filed here.

Floor 9 = global rooms 1-11 ONLY.

  room  description                                  exits
    1   J$ "IN A HALLWAY."                    W=4  N=2  E=8  S=7
    2   N$ "IN AN OFFICE."                    N=3           S=1
    3      "IN A CLOSET."                                  S=2
    4   J$ "IN A HALLWAY."                    N=5  E=1     S=6
    5   N$ "IN AN OFFICE."                                S=4
    6      "IN A RESTROOM."                       N=4
    7   N$ "IN AN OFFICE."                                N=1
    8   J$ "IN A HALLWAY."                    W=1  N=9     S=10
    9      "IN AN ELEVATOR."                              S=8
   10      "IN A MAINTENANCE ROOM."             N=8
   11      "IN A CRAWLSPACE ON TOP OF THE ELEVATOR."    D=9

Items:
    room 2   PAPER NOTE, DESK(scenery), CHAIR
    room 3   LONG BROOM
    room 5   TV SET(scenery), CLOCK(scenery)
    room 6   GRAFFITI ON WALL(scenery)
    room 7   OPEN WINDOW(scenery), KEY ON KEY CHAIN (fish it down with the BROOM)
    room 9   TRAP DOOR IN CEILING(scenery), DOWN BUTTON(scenery)
    room 10  CABINET(scenery) hiding FLASHLIGHT and TAPE
    room 11  ENDS OF 2 LIVE WIRES(scenery)

What this floor is actually about (all port prose, the room and item
names are the magazine's):
  1. GET CHAIR (room 2) and GET LONG BROOM (room 3).
  2. Fish the KEY ON KEY CHAIN off the ledge outside the window in room 7
     with the LONG BROOM.
  3. Unlock the CABINET in room 10 with that key; take the FLASHLIGHT
     and the TAPE.
  4. Carry the CHAIR into the elevator (room 9), DROP it under the
     TRAP DOOR IN CEILING and CLIMB CHAIR to reach the crawlspace (room 11).
  5. The ends of two LIVE WIRES are live until 11 PM; after that the
     power is out and TAPE WIRES repairs the elevator.
  6. Press the DOWN BUTTON in room 9 to descend to floor 8, room 13.

Room 1 is a HALLWAY, not the elevator - the elevator is room 9.
The CABINET is in room 10 (the maintenance room), not in room 1.
The BROOM is in room 3 (the closet).

Note: room 12 ("ON A VERY NARROW LEDGE.") is deliberately NOT here. It is
a verb-only special room: it is on no map and in neither walkthrough.
"""

FLOOR_NUMBER = 9
NEXT_FLOOR_DOWN = 8

# --------------------------------------------------------------------
# Verb-linked room pairs. The up-link from the elevator (9) to the
# crawlspace (11) is a verb transition (CLIMB CHAIR), not a directional
# exit, so room 11 carries D=9 while room 9 carries no matching U.
# Declared here so the generic map tests can tell a deliberate
# verb link apart from a missing reverse exit.
# --------------------------------------------------------------------
VERB_LINK_PAIRS = {(9, 11), (11, 9)}

# Items that sit behind the CABINET in room 10 until it is unlocked.
CABINET_CONTENTS = ("FLASHLIGHT", "TAPE")

# --------------------------------------------------------------------
# Room table - pixel-derived, see FLOOR9_AUDIT_2026-11-03.md sec. 2/3
# --------------------------------------------------------------------
ROOMS = {
    1: {
        "name": "IN A HALLWAY",
        "desc": (
            "A bare corridor, office carpet gone tacky with age. Four "
            "doorways open off it and the ceiling is a low grey grid. "
            "Nobody has dusted this hallway in years."
        ),
        "exits": {"W": 4, "N": 2, "E": 8, "S": 7},
        "items": [],
    },
    2: {
        "name": "IN AN OFFICE",
        "desc": (
            "A small office. A DESK with a pad of paper on it, a CHAIR "
            "pushed back from the desk, and a stale smell of old coffee."
        ),
        "exits": {"N": 3, "S": 1},
        "items": ["PAPER NOTE", "DESK", "CHAIR"],
    },
    3: {
        "name": "IN A CLOSET",
        "desc": (
            "A narrow janitor's closet. Coats hang from a rail, a shelf "
            "holds a bucket, and a LONG BROOM leans in the corner."
        ),
        "exits": {"S": 2},
        "items": ["LONG BROOM"],
    },
    4: {
        "name": "IN A HALLWAY",
        "desc": (
            "Another corridor, older than the first. The lights here are "
            "frozen on and buzz faintly. Doors lead north, east and south."
        ),
        "exits": {"N": 5, "E": 1, "S": 6},
        "items": [],
    },
    5: {
        "name": "IN AN OFFICE",
        "desc": (
            "An office with the lights off. A TV SET sits on a stand, its "
            "screen dark, and a CLOCK on the wall has stopped at midnight."
        ),
        "exits": {"S": 4},
        "items": ["TV SET", "CLOCK"],
    },
    6: {
        "name": "IN A RESTROOM",
        "desc": (
            "A restroom. Two stalls, a row of sinks, and something "
            "scratched into the tile: GRAFFITI ON WALL."
        ),
        "exits": {"N": 4},
        "items": ["GRAFFITI ON WALL"],
    },
    7: {
        "name": "IN AN OFFICE",
        "desc": (
            "An office whose OPEN WINDOW has been forced. Cold night air "
            "comes through it, and just outside, on a narrow ledge, a key "
            "on a chain catches the light."
        ),
        "exits": {"N": 1},
        "items": ["OPEN WINDOW", "KEY ON KEY CHAIN"],
        "special_desc": (
            "A KEY ON KEY CHAIN glints on the ledge outside the window, "
            "just out of reach."
        ),
    },
    8: {
        "name": "IN A HALLWAY",
        "desc": (
            "A service hallway ending in a dead end of damp concrete. "
            "One way leads back west, one north, one south."
        ),
        "exits": {"W": 1, "N": 9, "S": 10},
        "items": [],
    },
    9: {
        "name": "IN AN ELEVATOR",
        "desc": (
            "The elevator car, dead and dark. A DOWN BUTTON is set into "
            "the wall panel, and there is a TRAP DOOR IN CEILING above "
            "the light fixture."
        ),
        "exits": {"S": 8},
        "items": ["TRAP DOOR IN CEILING", "DOWN BUTTON"],
    },
    10: {
        "name": "IN A MAINTENANCE ROOM",
        "desc": (
            "A maintenance room of shelves, pipe and paint cans. A CABINET "
            "is bolted to the wall, its door shut tight."
        ),
        "exits": {"N": 8},
        "items": ["CABINET", "FLASHLIGHT", "TAPE"],
    },
    11: {
        "name": "IN A CRAWLSPACE ON TOP OF THE ELEVATOR",
        "desc": (
            "A crawlspace on top of the elevator car. Dust, dead cabling "
            "and the ends of two WIRES sticking out of a junction box, "
            "sparking."
        ),
        "exits": {"D": 9},
        "items": ["ENDS OF 2 LIVE WIRES"],
    },
}


class Floor9Engine:
    """Engine for Floor 9 - the elevator hallway (starting floor)."""

    # ------------------------------------------------------------------
    # Time / midnight mechanic.
    #
    # In the original BASIC the variable TH tracks the in-game hour.
    # The ends of the two live wires in room 11 carry current, and the
    # magazine's check reads:
    #   IF A=11 IF E$="RES" IF TH<23 THEN PRINT "YOU'RE ELECTROCUTED!"
    # So the wires are live while the hour is below 23 (before 11 PM).
    # Once the clock reaches 23:00 the power is out and they can be
    # taped. We model this by starting the clock at 10:00 PM and
    # advancing a fixed number of minutes per turn.
    # ------------------------------------------------------------------
    TIME_START_HOUR = 22        # 10:00 PM
    TIME_START_MIN = 0
    MINUTES_PER_TURN = 10       # 6 turns to 23:00 (wires become safe)
    # A brief thematic "midnight" announcement fires when the clock
    # first crosses 00:00 - purely flavor, not required for the
    # puzzle (the wires are already safe from 23:00 onward).
    MIDNIGHT_TOTAL_MIN = 24 * 60

    # ------------------------------------------------------------------
    # Item aliases for fuzzy verb/noun matching
    # ------------------------------------------------------------------
    _NOUN_ALIASES = {
        "PAPER NOTE": "PAPER NOTE",
        "NOTE": "PAPER NOTE",
        "DESK": "DESK",
        "CHAIR": "CHAIR",
        "LONG BROOM": "LONG BROOM",
        "BROOM": "LONG BROOM",
        "TV": "TV SET",
        "TV SET": "TV SET",
        "CLOCK": "CLOCK",
        "GRAFFITI": "GRAFFITI ON WALL",
        "GRAFFITI ON WALL": "GRAFFITI ON WALL",
        "WALL": "GRAFFITI ON WALL",
        "OPEN WINDOW": "OPEN WINDOW",
        "WINDOW": "OPEN WINDOW",
        "KEY": "KEY ON KEY CHAIN",
        "KEY ON KEY CHAIN": "KEY ON KEY CHAIN",
        "KEY ON A KEY CHAIN": "KEY ON KEY CHAIN",
        "KEYCHAIN": "KEY ON KEY CHAIN",
        "DOWN BUTTON": "DOWN BUTTON",
        "BUTTON": "DOWN BUTTON",
        "PUSH BUTTON": "DOWN BUTTON",
        "TRAP DOOR": "TRAP DOOR IN CEILING",
        "TRAP DOOR IN CEILING": "TRAP DOOR IN CEILING",
        "CABINET": "CABINET",
        "FLASHLIGHT": "FLASHLIGHT",
        "LAMP": "FLASHLIGHT",
        "LIGHT": "FLASHLIGHT",
        "TAPE": "TAPE",
        "ELECTRIC TAPE": "TAPE",
        "ELECTRICAL TAPE": "TAPE",
        "SLEEPING PILL": "SLEEPING PILL",
        "PILL": "SLEEPING PILL",
        "ENDS OF 2 LIVE WIRES": "ENDS OF 2 LIVE WIRES",
        "WIRES": "ENDS OF 2 LIVE WIRES",
        "WIRE": "ENDS OF 2 LIVE WIRES",
        "LIVE WIRES": "ENDS OF 2 LIVE WIRES",
    }

    _NON_TAKEABLE = {
        "DESK", "TV SET", "CLOCK", "GRAFFITI ON WALL", "OPEN WINDOW",
        "TRAP DOOR IN CEILING", "DOWN BUTTON", "CABINET",
        "ENDS OF 2 LIVE WIRES",
    }

    def __init__(self, state):
        self.state = state
        # Puzzle state
        self.cabinet_open = False
        self.tape_used = False
        self.elevator_fixed = False
        self._key_on_ledge = True
        self._broom_used_for_key = False
        # Per-room mutable items (start from the room table)
        self._room_items = self._init_room_items()
        # Time state
        self._turn = 0
        self._midnight_announced = False

    # ------------------------------------------------------------------
    # Item initialization
    # ------------------------------------------------------------------
    def _init_room_items(self):
        """Runtime item lists: what the player can actually see right now.

        Two items are held back from the static table:
          - FLASHLIGHT and TAPE are behind the CABINET in room 10 until
            the cabinet is unlocked with the key.
          - the KEY ON KEY CHAIN is in room 7 but out of reach until the
            LONG BROOM is used to fish it down.
        """
        items = {}
        for rid, r in ROOMS.items():
            lst = list(r["items"])
            if rid == 10:
                for it in CABINET_CONTENTS:
                    if it in lst:
                        lst.remove(it)
            if rid == 7 and "KEY ON KEY CHAIN" in lst:
                lst.remove("KEY ON KEY CHAIN")
            items[rid] = lst
        return items

    # ------------------------------------------------------------------
    # Time / midnight helpers
    # ------------------------------------------------------------------
    def _current_time_str(self):
        total = (self.TIME_START_HOUR * 60 + self.TIME_START_MIN
                 + self._turn * self.MINUTES_PER_TURN)
        day_offset, minute = divmod(total, 24 * 60)
        hour24, minute = divmod(minute, 60)
        suffix = "AM" if hour24 < 12 else "PM"
        hour12 = hour24 % 12
        if hour12 == 0:
            hour12 = 12
        return f"{hour12:02d}:{minute:02d} {suffix}"

    def _is_past_midnight(self):
        total = (self.TIME_START_HOUR * 60 + self.TIME_START_MIN
                 + self._turn * self.MINUTES_PER_TURN)
        return total >= self.MIDNIGHT_TOTAL_MIN

    def _advance_time(self):
        """Advance the in-game clock by one turn."""
        self._turn += 1
        if hasattr(self.state, "turns"):
            self.state.turns = self._turn
        if hasattr(self.state, "game_time"):
            self.state.game_time = self._current_time_str()

    @property
    def wires_live(self):
        """Wires are live whenever the in-game clock is before 11 PM.

        Mirrors the BASIC check `IF TH<23 THEN ELECTROCUTED`. The
        game starts at 10:00 PM and time only moves forward, so we
        compare the absolute minute count from game start against
        the 11 PM threshold (23 * 60 = 1380 minutes). After
        midnight the clock rolls over to 00:00+ but is still
        considered "after 11 PM" for puzzle purposes.
        """
        total = (self.TIME_START_HOUR * 60 + self.TIME_START_MIN
                 + self._turn * self.MINUTES_PER_TURN)
        return total < 23 * 60

    # ------------------------------------------------------------------
    # Room access
    # ------------------------------------------------------------------
    def get_room(self, rid):
        if rid not in ROOMS:
            return None
        r = dict(ROOMS[rid])
        r["id"] = rid
        r["items"] = list(self._room_items.get(rid, []))
        return r

    def on_enter(self):
        """Called when the player enters Floor 9 (game start)."""
        self.state.floor = FLOOR_NUMBER
        self.state.location = 1
        self.state.dark = False
        if not hasattr(self.state, "flashlight_on"):
            self.state.flashlight_on = False
        if not hasattr(self.state, "turns"):
            self.state.turns = 0
        if not hasattr(self.state, "power_out"):
            self.state.power_out = False
        if not hasattr(self.state, "game_time"):
            self.state.game_time = "10:00 PM"
        # Reset all per-floor state
        self.__init__(self.state)

    # ------------------------------------------------------------------
    # Command dispatcher
    # ------------------------------------------------------------------
    def handle_command(self, verb, noun=""):
        verb = (verb or "").upper().strip()
        noun = (noun or "").upper().strip()
        if verb in ("TAKE", "GRAB", "PICK"):
            verb = "GET"
        if verb in ("PUT", "PLACE"):
            verb = "DROP"
        if verb in ("WATCH", "VIEW"):
            verb = "EXAMINE"

        loc = self.state.location

        # WAIT - advance the in-game clock without doing anything else
        if verb in ("WAIT", "Z"):
            self._advance_time()
            extra = ""
            if not self._midnight_announced and self._is_past_midnight():
                self._midnight_announced = True
                extra = ("\nThe lights flicker... midnight. The building "
                         "loses power briefly. The elevator shaft goes dark.")
            return f"You wait. It is now {self._current_time_str()}.{extra}", False

        # Every other action also advances time
        self._advance_time()

        # Movement - handle bare direction, full word, and "GO <dir>"
        d = self._parse_direction(verb, noun)
        if d is not None:
            if d == "D":
                return self._go_down()
            return self._go(d), False

        # Verb transitions
        if verb == "CLIMB" or (verb == "GO" and noun in (
                "CHAIR", "TRAP DOOR", "TRAP DOOR IN CEILING")):
            return self._climb(noun)

        if verb in ("LOOK", "L"):
            return self._look(), False
        if verb == "GET":
            return self._get(noun), False
        if verb == "DROP":
            return self._drop(noun), False
        if verb in ("USE", "APPLY"):
            return self._use(noun), False
        if verb in ("TIE", "TAPE"):
            return self._use("TAPE"), False
        if verb in ("OPEN", "UNLOCK"):
            return self._open(noun), False
        if verb in ("EXAMINE", "READ", "X", "CHECK", "LOOK AT"):
            return self._examine(noun), False
        if verb in ("PUSH", "PRESS"):
            return self._push(noun)
        if verb in ("INVENTORY", "INV", "I"):
            return self._inventory(), False
        return "You can't do that.", False

    @staticmethod
    def _parse_direction(verb, noun):
        v = (verb or "").upper()
        n = (noun or "").upper()
        if v in ("N", "NORTH") or (v == "GO" and n in ("N", "NORTH")):
            return "N"
        if v in ("S", "SOUTH") or (v == "GO" and n in ("S", "SOUTH")):
            return "S"
        if v in ("E", "EAST") or (v == "GO" and n in ("E", "EAST")):
            return "E"
        if v in ("W", "WEST") or (v == "GO" and n in ("W", "WEST")):
            return "W"
        if v in ("U", "UP") or (v == "GO" and n in ("U", "UP")):
            return "U"
        if v in ("D", "DOWN") or (v == "GO" and n in ("D", "DOWN")):
            return "D"
        return None

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _go(self, d):
        r = self.get_room(self.state.location)
        if d not in r["exits"]:
            return self._blocked(d)
        dest = r["exits"][d]
        self.state.location = dest
        return self._look()

    def _blocked(self, d):
        """Message for a direction that does not exist from here."""
        if self.state.location == 9 and d == "U":
            return ("The TRAP DOOR IN CEILING is above your head, out of "
                    "reach. You'd need something to climb on.")
        return "You can't go that way."

    def _go_down(self):
        """Handle 'D' / 'DOWN'."""
        r = self.get_room(self.state.location)
        if "D" not in r["exits"]:
            return self._blocked("D"), False
        self.state.location = r["exits"]["D"]
        return self._look(), False

    def _climb(self, noun):
        """Verb transition: CLIMB CHAIR in the elevator (room 9) -> room 11.

        The only way up is the trap door in the ceiling of the elevator
        car, and the only way to reach it is to stand on the CHAIR.
        """
        loc = self.state.location
        n = (noun or "").upper().strip()
        if n and n not in ("CHAIR", "TRAP DOOR", "TRAP DOOR IN CEILING"):
            return f"You can't climb the {n}.", False
        if loc != 9:
            return "There's nothing here to climb.", False
        chair_here = "CHAIR" in self._room_items.get(9, [])
        chair_carried = "CHAIR" in self.state.inventory
        if not (chair_here or chair_carried):
            return ("The TRAP DOOR IN CEILING is too high to reach. You'd "
                    "need something to stand on - a chair, perhaps."), False
        self.state.location = 11
        return self._look(), False

    def _descend_to_floor_8(self):
        """PRESS BUTTON in the elevator (room 9) -> floor 8, room 13.

        Uses the codebase's cross-floor convention: a
        'TRANSITION:floor_N:room' marker with transition=True. The
        main engine drops to the next floor and calls its on_enter(),
        which puts the player in the landing room.
        """
        return "TRANSITION:floor_8:13", True

    # ------------------------------------------------------------------
    # Look / inventory
    # ------------------------------------------------------------------
    def _look(self):
        loc = self.state.location
        r = self.get_room(loc)
        lines = [f"**{r['name']}**", r["desc"]]
        if loc == 7 and self._key_on_ledge:
            lines.append(r.get("special_desc", ""))
        items = self._room_items.get(loc, [])
        if items:
            lines.append(f"Things here: {', '.join(items)}.")
        lines.append(f"Exits: {', '.join(r['exits'].keys())}.")
        lines.append(f"Time: {self._current_time_str()}.")
        if self._midnight_announced:
            lines.append("The building is dark. Power returned after the midnight flicker, but the shaft is calm.")
        return "\n".join(lines)

    def _inventory(self):
        inv = getattr(self.state, "inventory", [])
        if not inv:
            return "You're carrying nothing."
        return "You are carrying: " + ", ".join(inv)

    # ------------------------------------------------------------------
    # GET / DROP
    # ------------------------------------------------------------------
    def _get(self, noun):
        loc = self.state.location
        t = self._NOUN_ALIASES.get(noun)
        if not t:
            return f"No '{noun}' here."

        # Items that can't be taken at all - even if their noun was
        # recognised by the alias map (CABINET, TRAP DOOR, scenery...).
        if t in self._NON_TAKEABLE:
            return f"The {t} can't be taken - it's fixed in place."

        # KEY ON KEY CHAIN on the ledge outside the window in room 7
        if t == "KEY ON KEY CHAIN":
            if loc != 7:
                return f"No {t} here."
            if not self._key_on_ledge:
                return "The key is gone."
            has_broom = "LONG BROOM" in self.state.inventory
            if not has_broom and not self._broom_used_for_key:
                return ("The key is out of reach on the ledge. You'd need "
                        "something long to hook it down.")
            self._key_on_ledge = False
            self._broom_used_for_key = True
            self.state.add_item("KEY ON KEY CHAIN")
            if has_broom:
                return ("You lean out the window and use the LONG BROOM to "
                        "hook the key chain off the ledge. It clatters into "
                        "your hand!")
            return "You hook the key chain off the ledge and pocket it."

        items = self._room_items.get(loc, [])
        if t not in items:
            return f"No {t} here."
        items.remove(t)
        self._room_items[loc] = items
        self.state.add_item(t)
        return f"You take the {t}."

    def _drop(self, noun):
        inv = getattr(self.state, "inventory", [])
        t = self._NOUN_ALIASES.get(noun)
        if not t or t not in inv:
            return f"You're not carrying a {noun}."
        self.state.remove_item(t)
        self._room_items.setdefault(self.state.location, []).append(t)
        msg = f"You drop the {t}."
        # Setting the chair down in the maintenance room uncovers
        # something that was lying under it.
        if (t == "CHAIR" and self.state.location == 10
                and "SLEEPING PILL" not in self._room_items[10]):
            self._room_items[10].append("SLEEPING PILL")
            msg += (" As the chair settles, a SLEEPING PILL rolls out from "
                    "underneath it.")
        return msg

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _use(self, noun):
        loc = self.state.location
        inv = self.state.inventory
        norm = self._NOUN_ALIASES.get(noun, noun)

        # TAPE on the live wires (room 11) - the midnight puzzle core
        if norm == "TAPE" or noun in ("WIRES", "WIRE", "LIVE WIRES",
                                      "ENDS OF 2 LIVE WIRES"):
            if "TAPE" not in inv:
                return "You don't have any tape."
            if loc != 11:
                return "There are no live wires here to tape."
            if self.tape_used:
                return "The wires are already taped."
            if self.wires_live:
                return ("The wires are live! You can't tape them safely.\n"
                        "Wait for the power to go out after 11 PM.")
            self.tape_used = True
            self.elevator_fixed = True
            if hasattr(self.state, "elevator_fixed"):
                self.state.elevator_fixed = True
            return ("You carefully wrap the electrical tape around the two "
                    "severed wires. The sparking stops. The elevator hums "
                    "to life - FIXED!")

        # KEY on the CABINET (room 10)
        if norm == "KEY ON KEY CHAIN":
            if loc == 10:
                return self._open_cabinet()
            return "Nothing here needs that key."

        # FLASHLIGHT toggle
        if norm == "FLASHLIGHT":
            if "FLASHLIGHT" not in inv:
                return "You don't have a flashlight."
            self.state.flashlight_on = not getattr(self.state, "flashlight_on", False)
            if self.state.flashlight_on:
                return "Click. The flashlight cuts the darkness."
            return "Click. The flashlight clicks off."

        # LONG BROOM - its main use is fishing the key off the ledge
        if norm == "LONG BROOM":
            if "LONG BROOM" not in inv and loc != 3:
                return "You don't have a broom."
            if loc == 7:
                self._broom_used_for_key = True
                return ("You fish the LONG BROOM out the window and hook "
                        "the key chain toward you. It's within reach now - "
                        "try GET KEY.")
            return "You wave the LONG BROOM around. It doesn't help here."

        if norm == "CHAIR":
            return ("You set the CHAIR down. From here the TRAP DOOR IN "
                    "CEILING is just about within reach.")

        return f"Can't use the {noun}."

    def _open_cabinet(self):
        """Unlock the CABINET in room 10 and reveal its contents."""
        if "KEY ON KEY CHAIN" not in self.state.inventory:
            return "The cabinet is locked. You need a key."
        if self.cabinet_open:
            return "The cabinet is already open."
        self.cabinet_open = True
        self._add_cabinet_items()
        return ("You unlock the cabinet with the KEY ON KEY CHAIN. Inside: "
                "a FLASHLIGHT and a roll of TAPE.")

    def _add_cabinet_items(self):
        """Reveal FLASHLIGHT and TAPE inside the cabinet in room 10."""
        room10 = self._room_items.setdefault(10, [])
        for it in CABINET_CONTENTS:
            if it not in room10:
                room10.append(it)

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _open(self, noun):
        loc = self.state.location
        t = self._NOUN_ALIASES.get(noun, noun)
        if t == "CABINET":
            if loc != 10:
                return "No cabinet here."
            if self.cabinet_open:
                return "It's already open."
            return self._open_cabinet()
        if t == "OPEN WINDOW" and loc == 7:
            return "The window is already open."
        if t == "TRAP DOOR IN CEILING" and loc == 9:
            return ("The trap door is in the ceiling, above your head. "
                    "You'd need something to climb on.")
        if t == "OPEN WINDOW" and loc == 17:
            return "The window is already open."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun):
        loc = self.state.location
        t = self._NOUN_ALIASES.get(noun, noun)
        if t == "PAPER NOTE" and loc == 2:
            return ("The note is scrawled on a pad left on the desk:\n"
                    "  'THE LIFT IS DEAD. THE WIRES UP IN THE CRAWLSPACE "
                    "OVER THE CAR ARE STILL LIVE.\n"
                    "   TAPE THEM BEFORE YOU RIDE IT DOWN.'")
        if t == "GRAFFITI ON WALL" and loc == 6:
            return "'MATCH WIT FOR LIVE WIRES.'"
        if t == "ENDS OF 2 LIVE WIRES" and loc == 11:
            if self.tape_used:
                return "The wires are wrapped in tape, no longer sparking."
            if self.wires_live:
                return ("Live wires, sparking dangerously. Don't touch them "
                        "while the power is on!")
            return "The wires are de-energized - the power is out. Safe to tape now."
        if t == "CLOCK" and loc == 5:
            return (f"Frozen at midnight. The in-game clock says "
                    f"{self._current_time_str()}.")
        if t == "TV SET" and loc == 5:
            return ("The screen is dark and snowy. Whatever this building "
                    "broadcasts, it isn't tonight.")
        if t == "KEY ON KEY CHAIN" and loc == 7 and self._key_on_ledge:
            return "A key on a key chain rests on the ledge outside the window."
        if t == "CABINET" and loc == 10:
            base = "A metal cabinet bolted to the wall."
            if self.cabinet_open:
                return base + " It is open, showing a FLASHLIGHT and TAPE."
            return base + " It is locked."
        if t == "LONG BROOM" and loc == 3:
            return "A long broom. Long enough to hook things out of windows."
        if t == "CHAIR" and loc == 2:
            return "A sturdy wooden chair."
        if t == "TRAP DOOR IN CEILING" and loc == 9:
            return ("A square hatch in the ceiling of the elevator car, "
                    "shut but not latched. Too high to reach on foot.")
        if t == "DOWN BUTTON" and loc == 9:
            return ("The elevator's DOWN BUTTON. Pressing it now will only "
                    "work if the elevator is repaired.")
        if t == "OPEN WINDOW" and loc == 7:
            return ("The window stands open onto the night. A narrow ledge "
                    "runs just outside it.")
        if t == "FLASHLIGHT":
            if "FLASHLIGHT" in self.state.inventory:
                on = getattr(self.state, "flashlight_on", False)
                return "A small flashlight. " + ("Currently on." if on else "Currently off.")
            return "You don't have a flashlight."
        if t == "TAPE" and "TAPE" in self.state.inventory:
            return "A roll of electrical tape."
        if t == "DESK" and loc == 2:
            return "A desk with a pad of paper on it."
        return f"You examine the {noun}."

    # ------------------------------------------------------------------
    # PUSH
    # ------------------------------------------------------------------
    def _push(self, noun):
        loc = self.state.location
        t = self._NOUN_ALIASES.get(noun, noun)
        if t == "DOWN BUTTON":
            if loc != 9:
                return "There's no button to push here.", False
            if self.elevator_fixed:
                return self._descend_to_floor_8()
            return ("The button does nothing. The elevator is dead - the "
                    "wires need to be repaired first."), False
        return f"You can't push the {noun}.", False

    # ------------------------------------------------------------------
    # Bidirectional exit verification (static - used by tests)
    #
    # Directional exits must be bidirectionally consistent, with one
    # documented exception: room 11 -> room 9 (D) has no reverse U in
    # room 9, because the up-link is the CLIMB CHAIR verb transition.
    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        errors = []
        opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
        for rid, r in ROOMS.items():
            for d, t in r["exits"].items():
                if not isinstance(t, int):
                    continue
                if t not in ROOMS:
                    errors.append(f"Room {rid} -> {d}={t}, but room {t} does not exist")
                    continue
                if (rid, t) in VERB_LINK_PAIRS:
                    # Verb-linked pair: the reverse direction is a verb
                    # transition, not a directional exit.
                    continue
                reverse = ROOMS[t]["exits"].get(opp[d])
                if reverse is None:
                    errors.append(f"Room {rid} -> {d}={t}, but {t} has no {opp[d]}")
                elif reverse != rid:
                    errors.append(
                        f"Room {rid} -> {d}={t}, but {t} -> {opp[d]}={reverse} "
                        f"(expected {rid})"
                    )
        return errors


if __name__ == "__main__":
    errs = Floor9Engine.verify_exits()
    if errs:
        print(f"❌ {len(errs)} errors:")
        for e in errs:
            print(f"  {e}")
    else:
        print(f"✅ All exits consistent ({len(ROOMS)} rooms)")
