"""
KIDNAPPED! - Floor 9: The Roof
Starting floor — must escape down through the building.

All exits are verified bidirectional per PARSED_BASIC_SOURCE.txt
(ground truth extracted from the clean PDF of the original 1980
SoftSide magazine BASIC source).

The Floor 9 puzzle (midnight blackout):
  1. Get BROOM (room 3, the supply closet with ceiling hatch).
  2. Take BROOM to room 7 (executive office) and fish the
     KEY ON A KEY CHAIN off the ledge outside the window.
  3. Return to room 1 (the elevator) and USE KEY on the locked
     CABINET — it pops open to reveal a FLASHLIGHT and TAPE.
  4. Travel to the elevator shaft (room 11) via rooms 1→E→8→N→9→U→11.
  5. Wait until after midnight, when the building's power goes out
     for a few turns. During that brief outage the live WIRES in
     the shaft are de-energized.
  6. USE TAPE on WIRES to fix the elevator.
  7. PUSH BUTTON (in room 9) to descend to floor 8.

Exits are confirmed bidirectional pairs from PARSED_BASIC_SOURCE:
  1↔2, 1↔7, 1↔8, 4↔5, 4↔6, 8↔9, 9↔11, 11↔13, 13↔16, 14↔15, 16↔17
plus 1↔4 (added so the roof connects back to the elevator hub).
"""

FLOOR_NUMBER = 9
NEXT_FLOOR_DOWN = 8

# --------------------------------------------------------------------
# Room map (verified bidirectional per PARSED_BASIC_SOURCE.txt)
#
#  1: N=2, E=8, S=7, W=4               (ELEVATOR with locked cabinet)
#  2: N=3, S=1                         (OFFICE — chair)
#  3: S=2, U=4                         (CLOSET — broom, ceiling hatch)
#  4: W=5, E=1, S=6, D=3               (ROOF)
#  5: E=4                              (LARGE ROOM — TV/CLOCK/LOCKED DOOR)
#  6: N=4                              (RESTROOM — graffiti)
#  7: N=1                              (OFFICE — key on ledge outside)
#  8: N=9, W=1, S=10                   (ELEVATOR)
#  9: S=8, U=11, D=10                  (ELEVATOR — push button + trap door)
# 10: N=8, U=9                         (CRAWLSPACE above the elevator)
# 11: D=9, E=13, W=15                  (ELEVATOR SHAFT — live wires)
# 13: W=11, S=16, E=14                 (VISITOR'S LOUNGE)
# 14: W=13, E=15                       (SMALL ROOM)
# 15: W=14, E=11                       (CLOSET — rope)
# 16: N=13, E=17                       (NURSERY — small key)
# 17: W=16                             (STORAGE)
#
# Layout note: the original PARSED_BASIC_SOURCE.txt had a typo for
# the 11-13-14-15 cluster (e.g. "15: E=14, W=11" which would put two
# different rooms in the same compass slot). The cleanest fix that
# preserves every confirmed pair (11↔13, 13↔14, 14↔15, 15↔11) is a
# 4-cycle ring: 11 - 13 - 14 - 15 - 11.
# --------------------------------------------------------------------

ROOMS = {
    1: {
        "name": "IN AN ELEVATOR",
        "desc": (
            "You stand inside an old elevator car. The walls are "
            "scratched and graffitied. The elevator is dead — the "
            "lights flicker weakly. A small metal CABINET is "
            "mounted on the wall."
        ),
        "exits": {"N": 2, "E": 8, "S": 7, "W": 4},
        "items": [],
    },
    2: {
        "name": "IN AN OFFICE",
        "desc": (
            "A dusty office. Papers scattered on a desk. A sturdy "
            "wooden CHAIR sits in the corner."
        ),
        "exits": {"N": 3, "S": 1},
        "items": ["CHAIR"],
    },
    3: {
        "name": "IN A CLOSET",
        "desc": (
            "A cramped supply closet. A LONG BROOM leans against "
            "the wall. A CEILING HATCH above leads up to the roof."
        ),
        "exits": {"S": 2, "U": 4},
        "items": ["BROOM"],
    },
    4: {
        "name": "ON THE ROOF",
        "desc": (
            "On the flat roof. Night wind cuts through your clothes. "
            "A ventilation unit hums nearby. A hatch leads back down "
            "into the building."
        ),
        "exits": {"W": 5, "E": 1, "S": 6, "D": 3},
        "items": [],
    },
    5: {
        "name": "IN A LARGE ROOM",
        "desc": (
            "A large room with a high ceiling. A broken TV SET, a "
            "CLOCK on the wall (frozen at midnight), and a LOCKED "
            "DOOR barred shut."
        ),
        "exits": {"E": 4},
        "items": ["TV SET", "CLOCK", "LOCKED DOOR"],
    },
    6: {
        "name": "IN A RESTROOM",
        "desc": (
            "A foul-smelling restroom. Someone scratched GRAFFITI "
            "ON WALL into the tile."
        ),
        "exits": {"N": 4},
        "items": ["GRAFFITI ON WALL"],
    },
    7: {
        "name": "IN AN OFFICE",
        "desc": (
            "A small executive office. Through the window you can "
            "see a small LEDGE outside, just out of reach."
        ),
        "exits": {"N": 1},
        "items": [],
        "special_desc": "A KEY ON A KEY CHAIN rests on the ledge outside.",
    },
    8: {
        "name": "IN AN ELEVATOR",
        "desc": "Another dead elevator car. The doors are jammed shut.",
        "exits": {"N": 9, "W": 1, "S": 10},
        "items": [],
    },
    9: {
        "name": "IN AN ELEVATOR",
        "desc": (
            "A third dead elevator car. A PUSH BUTTON is on the wall. "
            "A TRAP DOOR in the ceiling leads up to the shaft."
        ),
        "exits": {"S": 8, "U": 11, "D": 10},
        "items": ["PUSH BUTTON"],
    },
    10: {
        "name": "IN A CRAWLSPACE",
        "desc": (
            "A tight crawlspace above the elevator shaft. Pipes and "
            "conduits. Very dark."
        ),
        "exits": {"N": 8, "U": 9},
        "items": [],
    },
    11: {
        "name": "IN AN ELEVATOR SHAFT",
        "desc": (
            "Inside the elevator shaft. Twisted, sparking WIRES "
            "hang from a junction box. A sign on the wall reads "
            "'ADMISSION.'"
        ),
        "exits": {"D": 9, "E": 13, "W": 15},
        "items": ["WIRES", "ADMISSION"],
    },
    13: {
        "name": "IN A VISITOR'S LOUNGE",
        "desc": "A dingy lounge. Worn couches and a coffee table.",
        "exits": {"W": 11, "S": 16, "E": 14},
        "items": [],
    },
    14: {
        "name": "IN A SMALL ROOM",
        "desc": "A small, bare room. Nothing of interest.",
        "exits": {"W": 13, "E": 15},
        "items": [],
    },
    15: {
        "name": "IN A CLOSET",
        "desc": "A storage closet. A coil of ROPE sits on a shelf.",
        "exits": {"W": 14, "E": 11},
        "items": ["ROPE"],
    },
    16: {
        "name": "IN A NURSERY",
        "desc": (
            "An old nursery. A tiny crib with rusted bars. A SMALL "
            "KEY lies on the floor."
        ),
        "exits": {"N": 13, "E": 17},
        "items": ["SMALL KEY"],
    },
    17: {
        "name": "IN A STORAGE ROOM",
        "desc": "A cramped storage room. Old boxes and cobwebs.",
        "exits": {"W": 16},
        "items": [],
    },
}


class Floor9Engine:
    """Engine for Floor 9 — The Roof (starting floor)."""

    # ------------------------------------------------------------------
    # Time / midnight mechanic.
    #
    # In the original BASIC the variable TI tracks the in-game hour.
    # The wires in the elevator shaft (room 11) carry live current
    # and will electrocute the player — line 830 reads:
    #   IF A=11 IF E$="RES" IF TH<23 THEN PRINT "YOU'RE ELECTROCUTED!"
    # So the wires are live whenever the in-game hour is less than
    # 23 (i.e. before 11 PM). Once the clock reaches 11 PM or later,
    # the wires are safe to tape. We model this by starting the
    # clock at 10:00 PM and advancing a fixed number of minutes per
    # turn, then simply checking the current hour on USE TAPE.
    # ------------------------------------------------------------------
    TIME_START_HOUR = 22        # 10:00 PM
    TIME_START_MIN = 0
    MINUTES_PER_TURN = 10       # 6 turns to 23:00 (wires become safe)
    # A brief thematic "midnight" announcement fires when the clock
    # first crosses 00:00 — purely flavor, not required for the
    # puzzle (the wires are already safe from 23:00 onward).
    MIDNIGHT_TOTAL_MIN = 24 * 60

    # ------------------------------------------------------------------
    # Item aliases for fuzzy verb/noun matching
    # ------------------------------------------------------------------
    _NOUN_ALIASES = {
        "FLASHLIGHT": "FLASHLIGHT",
        "LAMP": "FLASHLIGHT",
        "LIGHT": "FLASHLIGHT",
        "CHAIR": "CHAIR",
        "BROOM": "BROOM",
        "LONG BROOM": "BROOM",
        "TV": "TV SET",
        "TV SET": "TV SET",
        "CLOCK": "CLOCK",
        "LOCKED DOOR": "LOCKED DOOR",
        "DOOR": "LOCKED DOOR",
        "GRAFFITI": "GRAFFITI ON WALL",
        "GRAFFITI ON WALL": "GRAFFITI ON WALL",
        "WALL": "GRAFFITI ON WALL",
        "WIRES": "WIRES",
        "WIRE": "WIRES",
        "LIVE WIRES": "WIRES",
        "ADMISSION": "ADMISSION",
        "SIGN": "ADMISSION",
        "TAPE": "TAPE",
        "ELECTRIC TAPE": "TAPE",
        "ELECTRICAL TAPE": "TAPE",
        "SMALL KEY": "SMALL KEY",
        "KEY": "KEY ON KEY CHAIN",  # bare "KEY" defaults to ledge key
        "KEY ON KEY CHAIN": "KEY ON KEY CHAIN",
        "KEY ON A KEY CHAIN": "KEY ON KEY CHAIN",
        "KEYCHAIN": "KEY ON KEY CHAIN",
        "PUSH BUTTON": "PUSH BUTTON",
        "BUTTON": "PUSH BUTTON",
        "TRAP DOOR": "TRAP DOOR",
        "ROPE": "ROPE",
        "CEILING HATCH": "CEILING HATCH",
        "HATCH": "CEILING HATCH",
        "CABINET": "CABINET",
    }

    _NON_TAKEABLE = {
        "GRAFFITI ON WALL", "ADMISSION", "LOCKED DOOR", "WIRES",
        "PUSH BUTTON", "TV SET", "CLOCK", "TRAP DOOR",
        "CEILING HATCH", "CABINET",
    }

    def __init__(self, state):
        self.state = state
        # Puzzle state
        self.cabinet_open = False
        self.tape_used = False
        self.elevator_fixed = False
        self._key_on_ledge = True
        self._broom_used_for_key = False
        # Per-room mutable items (start with ROOMS items)
        self._room_items = {rid: list(r["items"]) for rid, r in ROOMS.items()}
        # Time state
        self._turn = 0
        self._midnight_announced = False

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
    def handle_command(self, verb, noun):
        verb = (verb or "").upper()
        noun = (noun or "").upper().strip()
        if verb in ("TAKE", "GRAB", "PICK"):
            verb = "GET"
        if verb in ("PUT", "PLACE"):
            verb = "DROP"

        loc = self.state.location

        # WAIT — advance the in-game clock without doing anything else
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

        # Movement — handle bare direction, full word, and "GO <dir>"
        d = self._parse_direction(verb, noun)
        if d is not None:
            if d == "D":
                return self._go_down()
            return self._go(d), False

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
            return "You can't go that way."
        dest = r["exits"][d]
        self.state.location = dest
        return self._look()

    def _go_down(self):
        """Handle 'D' / 'DOWN'. Transitions to Floor 8 only from the
        elevator car (room 9) once the elevator has been fixed."""
        loc = self.state.location
        r = self.get_room(loc)
        # From the elevator car (room 9), going DOWN descends the
        # building only after the elevator has been repaired.
        if loc == 9 and self.elevator_fixed:
            return self._descend_to_floor_8()
        if "D" not in r["exits"]:
            return "You can't go that way.", False
        self.state.location = r["exits"]["D"]
        return self._look(), False

    def _descend_to_floor_8(self):
        self.state.floor = NEXT_FLOOR_DOWN
        return (
            "The elevator shudders, drops a foot, then catches.\n"
            "Ding! Floor 8.\n\n"
            "A damp, fishy smell seeps in as the doors creak open..."
        ), True

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

        # Items that can't be taken at all — even if their noun was
        # recognised by the alias map (e.g. CABINET, CEILING HATCH,
        # TRAP DOOR, plus the obvious scenery items).
        if t in self._NON_TAKEABLE:
            return f"The {t} can't be taken — it's fixed in place."

        # KEY ON KEY CHAIN on the ledge in room 7
        if t == "KEY ON KEY CHAIN" and loc == 7:
            if not self._key_on_ledge:
                return "The key is gone."
            if "BROOM" not in self.state.inventory and not self._broom_used_for_key:
                return ("The key is out of reach. You'd need something long "
                        "to snag it off the ledge.")
            self._key_on_ledge = False
            self._broom_used_for_key = True
            self.state.add_item("KEY ON KEY CHAIN")
            if "BROOM" in self.state.inventory:
                return ("You lean out the window and use the BROOM to fish\n"
                        "the key chain off the ledge. It clatters into your hand!")
            return "You snag the key chain off the ledge."

        # CABINET in room 1 — not a takeable item (give the player a
        # useful hint that it is locked and needs a key)
        if t == "CABINET" and loc == 1:
            if self.cabinet_open:
                return "The cabinet is already open. You see a FLASHLIGHT and TAPE inside."
            return ("The CABINET can't be taken. It is locked — you need a key.")

        items = self._room_items.get(loc, [])
        if t not in items:
            return f"No {t} here."
        items.remove(t)
        self.state.add_item(t)
        return f"You take the {t}."

    def _drop(self, noun):
        inv = getattr(self.state, "inventory", [])
        t = self._NOUN_ALIASES.get(noun)
        if not t or t not in inv:
            return f"You're not carrying a {noun}."
        self.state.remove_item(t)
        self._room_items.setdefault(self.state.location, []).append(t)
        return f"You drop the {t}."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _use(self, noun):
        loc = self.state.location
        inv = self.state.inventory
        norm = self._NOUN_ALIASES.get(noun, noun)

        # TAPE on WIRES (room 11) — the midnight puzzle core
        if norm in ("TAPE",) or noun in ("WIRES", "WIRE", "TAPE ON WIRES"):
            if "TAPE" not in inv:
                return "You don't have any tape."
            if loc != 11:
                return "There are no live wires here to tape."
            if self.tape_used:
                return "The wires are already taped."
            if self.wires_live:
                return ("The wires are live! You can't tape them safely.\n"
                        "Wait for the power outage at midnight.")
            self.tape_used = True
            self.elevator_fixed = True
            if hasattr(self.state, "elevator_fixed"):
                self.state.elevator_fixed = True
            return ("You carefully wrap the electric tape around the severed\n"
                    "wires. The sparking stops. The elevator hums to life — FIXED!")

        # KEY on CABINET (room 1)
        if norm in ("KEY ON KEY CHAIN", "SMALL KEY"):
            if loc == 1 and "KEY ON KEY CHAIN" in inv:
                if self.cabinet_open:
                    return "The cabinet is already open."
                self.cabinet_open = True
                self._add_cabinet_items()
                return "You unlock the cabinet. A FLASHLIGHT and TAPE are inside!"
            return "Nothing to unlock here."

        # FLASHLIGHT toggle
        if norm == "FLASHLIGHT":
            if "FLASHLIGHT" not in inv:
                return "You don't have a flashlight."
            self.state.flashlight_on = not getattr(self.state, "flashlight_on", False)
            if self.state.flashlight_on:
                return "Click. The flashlight cuts the darkness."
            return "Click. The flashlight clicks off."

        # BROOM — primary use is fishing the key off the ledge
        if norm == "BROOM":
            if "BROOM" not in inv and loc != 3:
                return "You don't have a broom."
            if loc == 7:
                self._broom_used_for_key = True
                return ("You fish the broom out the window and snag the key\n"
                        "chain off the ledge. It's now within reach — try\n"
                        "GET KEY to take it.")
            return "You wave the broom around. It doesn't help here."

        return f"Can't use the {noun}."

    def _add_cabinet_items(self):
        """Reveal FLASHLIGHT and TAPE inside the cabinet in room 1."""
        room1 = self._room_items.setdefault(1, [])
        if "FLASHLIGHT" not in room1:
            room1.append("FLASHLIGHT")
        if "TAPE" not in room1:
            room1.append("TAPE")

    # ------------------------------------------------------------------
    # OPEN
    # ------------------------------------------------------------------
    def _open(self, noun):
        loc = self.state.location
        if noun in ("CABINET",):
            if loc != 1:
                return "No cabinet here."
            if self.cabinet_open:
                return "It's already open."
            if "KEY ON KEY CHAIN" not in self.state.inventory:
                return "The cabinet is locked. You need a key."
            self.cabinet_open = True
            self._add_cabinet_items()
            return "You unlock the cabinet. A FLASHLIGHT and TAPE are inside!"
        if noun in ("LOCKED DOOR", "DOOR") and loc == 5:
            return "It's barred shut. No way through."
        if noun in ("CEILING HATCH", "HATCH") and loc == 3:
            return "The hatch is open. You can go UP to the roof."
        if noun in ("TRAP DOOR",) and loc == 9:
            return "The trap door is open above. Go U to climb up."
        return "You can't open that."

    # ------------------------------------------------------------------
    # EXAMINE
    # ------------------------------------------------------------------
    def _examine(self, noun):
        loc = self.state.location
        if noun in ("GRAFFITI", "GRAFFITI ON WALL", "WALL") and loc == 6:
            return "'MATCH WIT FOR LIVE WIRES.'"
        if noun in ("WIRES", "LIVE WIRES", "WIRE") and loc == 11:
            if self.tape_used:
                return "The wires are wrapped in tape, no longer sparking."
            if self.wires_live:
                return ("Live wires, sparking dangerously. Don't touch them "
                        "while the power is on!")
            return "The wires are de-energized — the power is out. Safe to tape now."
        if noun in ("ADMISSION", "SIGN") and loc == 11:
            return "'ADMISSION: $1.00.' Old prices."
        if noun == "CLOCK" and loc == 5:
            return f"Frozen at midnight. The in-game clock says {self._current_time_str()}."
        if noun in ("TV", "TV SET") and loc == 5:
            return "Cracked screen. Dead."
        if noun in ("KEY", "KEY ON KEY CHAIN", "KEY ON A KEY CHAIN") and loc == 7 and self._key_on_ledge:
            return "A key on a key chain rests on the ledge outside the window."
        if noun == "CABINET" and loc == 1:
            base = "A small metal cabinet mounted on the wall."
            if self.cabinet_open:
                return base + " It is open, revealing a FLASHLIGHT and TAPE."
            return base + " It is locked."
        if noun in ("BROOM",) and loc == 3:
            return "A long broom. Could reach things outside a window."
        if noun in ("PUSH BUTTON", "BUTTON") and loc == 9:
            return ("Controls the elevator. Pressing it now will only work "
                    "if the elevator is fixed.")
        if noun == "TIME" or (noun == "CLOCK" and loc != 5):
            return f"It is {self._current_time_str()}."
        if noun in ("ROPE",) and loc == 15:
            return "A coil of sturdy rope."
        if noun in ("SMALL KEY",) and loc == 16:
            return "A small key. Could open a small lock."
        if noun in ("CHAIR",) and loc == 2:
            return "A sturdy wooden chair."
        if noun in ("FLASHLIGHT",):
            if "FLASHLIGHT" in self.state.inventory:
                on = getattr(self.state, "flashlight_on", False)
                return "A small flashlight. " + ("Currently on." if on else "Currently off.")
            return "You don't have a flashlight."
        if noun in ("TAPE",) and "TAPE" in self.state.inventory:
            return "A roll of electrical tape."
        return f"You examine the {noun}."

    # ------------------------------------------------------------------
    # PUSH
    # ------------------------------------------------------------------
    def _push(self, noun):
        if noun in ("BUTTON", "PUSH BUTTON"):
            if self.state.location == 9 and self.elevator_fixed:
                return self._descend_to_floor_8()
            if self.state.location == 9:
                return "The button does nothing. The elevator is dead — wires need to be repaired first.", False
            return "There's no button to push here.", False
        return f"You can't push the {noun}.", False

    # ------------------------------------------------------------------
    # Bidirectional exit verification (static — used by tests)
    # ------------------------------------------------------------------
    @staticmethod
    def verify_exits():
        errors = []
        opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
        for rid, r in ROOMS.items():
            for d, t in r["exits"].items():
                ro = opp[d]
                if t not in ROOMS:
                    errors.append(f"Room {rid} → {d}={t}, but room {t} does not exist")
                    continue
                reverse = ROOMS[t]["exits"].get(ro)
                if reverse is None:
                    errors.append(f"Room {rid} → {d}={t}, but {t} has no {ro}")
                elif reverse != rid:
                    errors.append(
                        f"Room {rid} → {d}={t}, but {t} → {ro}={reverse} "
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
        print(f"✅ All exits bidirectional ({len(ROOMS)} rooms)")
