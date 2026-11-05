"""
KIDNAPPED! - Floor 6: The Office Complex, the Ledges and the Vault
==================================================================

GROUND TRUTH
------------
The authoritative source for this floor is the pixel read of the
original listing (KIDNAPPED_Original.pdf, SoftSide, Dec 1980) recorded
in ``audit/FLOOR6_PIXEL_NOTES.md``, reconciled against both published
walkthroughs in ``archive/solutions/`` (Jacob Gunness, CASA Solution
Archive, Sept 2004; Garry Francis, minimal Atari solution) and Garry
Francis's 2015 floor map.

The listing dispatch is ``ON A GOTO 11,12,...,75``, so a global room
number is the printed BASIC line number minus ten.  Floor 6 is printed
lines 36-46, i.e. global rooms 26-36.

THE PREVIOUS VERSION OF THIS MODULE WAS WRONG.  It carried an invented
room set (the "balloon / glue / helium" puzzle in rooms that belong to
other floors) and linked to floor 7 room 41 and floor 5 room 49 - both
stale numbers from the discarded numbering.  Everything below is
re-derived from the source pixels and replays both walkthroughs
command-for-command.

ROOM TABLE (pixel-verified, page 1 right column, lines 36-46)
-------------------------------------------------------------
    26  IN A HALLWAY               W=31  N=27  E=29  S=30
    27  IN AN OFFICE                N=28           S=26
    28  IN A CLOSET                         S=27   TANK OF HELIUM GAS
    29  IN A GAME ROOM                W=26          LARGE DEFLATED BALLOON
    30  IN AN OFFICE                         N=26   GUN
    31  IN A HALLWAY               W=33  N=32           E=26
    32  IN A STORE ROOM                      S=31   SIGN ON WALL
                                                       STRING VENDING MACHINE
    33  IN AN OFFICE                         E=31   OPEN WINDOW
    34  ON A LARGE LEDGE BY WINDOW     W=36
    35  IN THE VAULT                    W=36        DOLLAR
    36  ON A LARGE LEDGE BY WINDOW            E=34

ROOM NAMES
----------
``J$`` is the shared string for the two hallways and ``N$`` for the
three offices (both are assigned once in the listing's variable block:
``J$="IN A HALLWAY."`` / ``N$="IN AN OFFICE."``).  The remaining room
names are printed literally in the listing.  Francis's 2015 floor-6 map
panel agrees exactly: two Hallway boxes, three Office boxes, a Closet,
a Storeroom, a Game Room, two Ledges and the Vault.

VERB TRANSITIONS (NOT directional exits)
----------------------------------------
The source matches verbs on the LAST THREE LETTERS of the object, so
the same handler catches several spellings.  Behaviour below is taken
from the pixel-verified handler blocks on pages 2-3.

    room 33  CLIMB LEDGE / GO LEDGE   -> room 34   (handler 610, "DGE")
    room 35  CLIMB LEDGE / GO LEDGE   -> room 36   (handler 610, "DGE")
    room 34  CLIMB WINDOW / GO WINDOW -> room 33   (handler 608, "DOW")
    room 36  CLIMB WINDOW / GO WINDOW -> room 35   (handler 608, "DOW")
    room 34  JUMP                     -> floor 5   (the vault is below
                                               the left-hand ledge)
    room 32  READ SIGN                -> "SIGN: STRING COSTS $1.00"
    room 32  PUT DOLLAR / PAY DOLLAR  -> buys the LONG STRING (550)
    anywhere INFLATE BALLOON          -> needs the helium tank (950)
    anywhere TIE BALLOON / TIE STRING -> needs the inflated balloon (835)

Items are placed from the DATA rows read off page 4:

    2010 ... TANK OF HELIUM GAS,28, LARGE DEFLATED BALLOON,29
    2020 LOCKED DOOR,-30, GUN,30, SIGN ON WALL,-32,
          STRING VENDING MACHINE,-32, OPEN WINDOW,-33, ...

A negative room number marks scenery that cannot be picked up.

UNRESOLVED / PENDING
--------------------
* The arrival room from floor 5 (the balloon carries you down one floor
  to global room 43) still uses the stale floor-5 numbering, because
  floor 5 has not been audited yet.  Floor 5's own module will need
  rewriting before that link can be trusted.
* The exact floor-5 landing room is marked in ``SPECIAL_ROOMS`` below.
"""

FLOOR_NUMBER = 6
NEXT_FLOOR_DOWN = 5

# ---------------------------------------------------------------------
# The single cross-floor link on this floor: JUMP off the right-hand
# ledge (room 34) drops you to floor 5.  There is no way back up -
# the descent chain runs 9 -> 8 -> 7 -> 6 -> 5.
# ---------------------------------------------------------------------
SPECIAL_ROOMS = {
    # UNRESOLVED: floor 5 is not audited yet.  The original drops the
    # player on global room 43 (the balloon-carry handler); floor 5's
    # module still uses the discarded numbering.
    "floor_5": {"target": "floor_5", "landing_room": 43},
}

# ---------------------------------------------------------------------
# Verb-linked room pairs.
#
# The listing prints these exits exactly as they are, and they are NOT
# symmetric:
#
#     room 34  W = 36      room 35  W = 36      room 36  E = 34
#
# The return path from 36 to the vault (35) and from 34 to the office
# (33) is the verb link, not a direction: handler 610 moves A from 33
# or 35 up one room (CLIMB LEDGE) and handler 608 moves A from 34 or 36
# down one room (CLIMB WINDOW / DOWN).  Declared here so the generic map
# tests can tell a deliberate verb link apart from a missing reverse
# exit.
# ---------------------------------------------------------------------
VERB_LINK_PAIRS = {(33, 34), (34, 33), (35, 36), (36, 35)}

# ---------------------------------------------------------------------
# Room table - pixel-derived, see audit/FLOOR6_PIXEL_NOTES.md
# ---------------------------------------------------------------------
ROOMS = {
    26: {
        "name": "IN A HALLWAY",
        "desc": (
            "A long hallway crosses this wing of the building, its walls "
            "painted the same tired green from end to end. Doorways open "
            "north, east, south and west. You are alone down here, and "
            "somewhere above you a kidnapper is counting money."
        ),
        "exits": {"W": 31, "N": 27, "E": 29, "S": 30},
        "items": [],
    },
    27: {
        "name": "IN AN OFFICE",
        "desc": (
            "A small office with a bare desk pushed against the wall. "
            "The north door leads to a closet; the way back south leads "
            "to the hallway."
        ),
        "exits": {"N": 28, "S": 26},
        "items": [],
    },
    28: {
        "name": "IN A CLOSET",
        "desc": (
            "A closet barely wider than your shoulders. A tank of helium "
            "gas is wedged in the corner, hissing faintly."
        ),
        "exits": {"S": 27},
        "items": ["TANK OF HELIUM GAS"],
    },
    29: {
        "name": "IN A GAME ROOM",
        "desc": (
            "A game room: a ping-pong table with a warped net, a dart "
            "board, chairs stacked against the wall. A large deflated "
            "balloon lies on the floor where somebody dropped it."
        ),
        "exits": {"W": 26},
        "items": ["LARGE DEFLATED BALLOON"],
    },
    30: {
        "name": "IN AN OFFICE",
        "desc": (
            "Another office, larger than the last. A locked door is set "
            "into the far wall, and a gun sits on the desk, close enough "
            "to take."
        ),
        "exits": {"N": 26},
        "items": ["GUN", "LOCKED DOOR"],
    },
    31: {
        "name": "IN A HALLWAY",
        "desc": (
            "The hallway turns here. It runs east toward the offices you "
            "came from, north toward a storeroom, and west toward a "
            "window at the end of the building."
        ),
        "exits": {"W": 33, "N": 32, "E": 26},
        "items": [],
    },
    32: {
        "name": "IN A STORE ROOM",
        "desc": (
            "A storeroom of shelves and filing cabinets. A sign on the "
            "wall reads: STRING COSTS $1.00. Beside it stands a vending "
            "machine full of nothing but string."
        ),
        "exits": {"S": 31},
        "items": ["SIGN ON WALL", "STRING VENDING MACHINE"],
    },
    33: {
        "name": "IN AN OFFICE",
        "desc": (
            "The last office on this floor, with an open window giving "
            "onto a narrow ledge outside. The ledge runs away to the "
            "west, along the face of the building."
        ),
        "exits": {"E": 31},
        "items": ["OPEN WINDOW"],
    },
    34: {
        "name": "ON A LARGE LEDGE BY WINDOW",
        "desc": (
            "You are outside on a wide ledge, with the wall of the "
            "building at your back and the night air in your face. "
            "The ledge continues west toward another window. There is "
            "nothing below you but a long drop."
        ),
        "exits": {"W": 36},
        "items": [],
    },
    35: {
        "name": "IN THE VAULT",
        "desc": (
            "A vault, small and square, its door standing open. A single "
            "desk sits inside it, with a fat roll of money on top."
        ),
        "exits": {"W": 36},
        "items": ["DOLLAR"],
    },
    36: {
        "name": "ON A LARGE LEDGE BY WINDOW",
        "desc": (
            "The far end of the ledge, above a window. From here you "
            "could go back east along the ledge, or down through the "
            "window into the room below."
        ),
        "exits": {"E": 34},
        "items": [],
    },
}

# --------------------------------------------------------------------
# Scenery: in the listing these items carry a NEGATIVE room number,
# which is the source's way of saying "here, but you cannot take it".
# --------------------------------------------------------------------
FIXED_ITEMS = {
    "SIGN ON WALL",
    "STRING VENDING MACHINE",
    "OPEN WINDOW",
    "LOCKED DOOR",
}

# --------------------------------------------------------------------
# Noun -> canonical item name.  The published walkthroughs spell the
# same objects differently ("GAS" / "TANK OF HELIUM GAS", "BALLOON" /
# "LARGE DEFLATED BALLOON", "STRING" / "LONG STRING"), so every
# spelling has to work.
# --------------------------------------------------------------------
_ITEM_ALIASES = {
    "TANK OF HELIUM GAS": "TANK OF HELIUM GAS",
    "HELIUM TANK": "TANK OF HELIUM GAS",
    "HELIUM GAS": "TANK OF HELIUM GAS",
    "HELIUM": "TANK OF HELIUM GAS",
    "GAS": "TANK OF HELIUM GAS",
    "TANK": "TANK OF HELIUM GAS",
    "LARGE DEFLATED BALLOON": "LARGE DEFLATED BALLOON",
    "DEFLATED BALLOON": "LARGE DEFLATED BALLOON",
    "BALLOON": "LARGE DEFLATED BALLOON",
    "LARGE INFLATED BALLOON": "LARGE INFLATED BALLOON",
    "INFLATED BALLOON": "LARGE INFLATED BALLOON",
    "GUN": "GUN",
    "DOLLAR": "DOLLAR",
    "LONG STRING": "LONG STRING",
    "STRING": "LONG STRING",
    "SIGN ON WALL": "SIGN ON WALL",
    "SIGN": "SIGN ON WALL",
    "STRING VENDING MACHINE": "STRING VENDING MACHINE",
    "VENDING MACHINE": "STRING VENDING MACHINE",
    "OPEN WINDOW": "OPEN WINDOW",
    "WINDOW": "OPEN WINDOW",
    "LOCKED DOOR": "LOCKED DOOR",
}

# The room the helium tank is in.
_TANK_ROOM = 28
# The room the deflated balloon is in.
_BALLOON_ROOM = 29
# The room the gun is in.
_GUN_ROOM = 30
# The storeroom with the sign and the string vending machine.
_STORE_ROOM = 32
# The vault with the money.
_VAULT_ROOM = 35
# The right-hand ledge (jump down to floor 5) and the left-hand ledge.
_LEDGE_RIGHT = 34
_LEDGE_LEFT = 36


# ---------------------------------------------------------------------
# Floor 6 Engine
# ---------------------------------------------------------------------
class Floor6Engine:
    def __init__(self, state):
        self.state = state
        self._room_items = self._init_items()
        # "deflated" -> "inflated" -> "tied"
        self.balloon_state = "deflated"
        # True once the dollar has bought the string in room 32.
        self.string_bought = False
        # Set if the player shoots the gun in the vault (handler 960).
        self.shot_up = False
        # Flavour text for the last floor transition (the dispatcher
        # cannot carry prose alongside a transition marker).
        self.last_transition_note = ""

    # ------------------------------------------------------------------
    # Item initialization (reset each time the player enters floor 6)
    # ------------------------------------------------------------------
    def _init_items(self):
        """Runtime item lists: what the player can see right now."""
        return {rid: list(r.get("items", [])) for rid, r in ROOMS.items()}

    # ------------------------------------------------------------------
    # Entry / exit
    # ------------------------------------------------------------------
    def on_enter(self):
        """Called when the player arrives on Floor 6.

        The arrival room is 26 (IN A HALLWAY): both published
        walkthroughs start their floor-6 section with the moves that only
        work from room 26 (N N to the helium tank, S to the gun).
        """
        if hasattr(self.state, "floor"):
            self.state.floor = FLOOR_NUMBER
        self._room_items = self._init_items()
        self.balloon_state = "deflated"
        self.string_bought = False
        self.shot_up = False
        self.last_transition_note = ""
        self.state.location = 26

    def on_leave(self):
        """Called when the player leaves Floor 6."""
        pass

    # ------------------------------------------------------------------
    # Room access
    # ------------------------------------------------------------------
    def get_room(self, room_id):
        """Return a copy of the room record with its runtime item list."""
        if room_id not in ROOMS:
            return None
        r = dict(ROOMS[room_id])
        r["id"] = room_id
        r["items"] = list(self._room_items.get(room_id, []))
        return r

    def get_current_room(self):
        return ROOMS.get(self.state.location)

    # ------------------------------------------------------------------
    # Small helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _wrap(text):
        """Wrap a command result into the (text, transition) tuple the
        dispatcher in kidnapped.py unpacks.

        A result whose text starts with "TRANSITION:" is a floor change;
        everything else is ordinary prose.
        """
        if isinstance(text, tuple):
            return text
        return text, text.startswith("TRANSITION:")

    def _add_to_inventory(self, item):
        add = getattr(self.state, "add_item", None)
        if callable(add):
            add(item)
        inv = getattr(self.state, "inventory", None)
        if inv is not None and item not in inv:
            inv.append(item)

    def _remove_from_inventory(self, item):
        remove = getattr(self.state, "remove_item", None)
        if callable(remove):
            remove(item)
        inv = getattr(self.state, "inventory", None)
        if inv is not None and item in inv:
            inv.remove(item)

    def _carrying(self, item):
        inv = getattr(self.state, "inventory", None) or []
        return item in inv

    def _inventory(self):
        inv = getattr(self.state, "inventory", None) or []
        if not inv:
            return "You're carrying nothing."
        return "You are carrying: " + ", ".join(inv)

    @staticmethod
    def _canonical_item(noun):
        """Map a noun phrase onto a canonical item name (or None)."""
        n = (noun or "").upper().strip()
        if n.startswith("THE "):
            n = n[4:].strip()
        if not n:
            return None
        if n in _ITEM_ALIASES:
            return _ITEM_ALIASES[n]
        for alias in _ITEM_ALIASES:
            if alias in n:
                return _ITEM_ALIASES[alias]
        return None

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
    # Command dispatch - every path returns a (text, transition) tuple
    # ------------------------------------------------------------------

    # ----------------------------------------------------------------
    # Vault rules - source lines 467 / 960 / 1515 / 1516.
    #
    # Original listing line 467:
    #   IF A=35 IF E$="PER" OR (E$="LAR" OR E$="NEY") IF I(27)=0 THEN
    #   PRINT"YOU GET TOO CLOSE TO HIM, HE JUMPS UP AND STRANGLES YOU.":
    #   GOTO7300 ELSE IF I(27)=1 THEN PRINT"KIDNAPPER SEES YOUR GUN AND
    #   FREEZES. YOU GRAB A DOLLAR":A$(56)="DOLLAR":H$(56)=A$(56):
    #   A(56)=35:PM=1:E$="LAR"
    #
    # Original listing line 960 (the gun branch):
    #   IF D(B)<>14 THEN 970 ELSE IF E$="GUN" OR E$="PER" IF I(27)=1
    #   IF A=35 THEN PRINT"GUN HAD BLANKS! KIDNAPPER SHOOTS YOU.":
    #   GOTO7200 ELSE PRINT"GUN MISFIRES":GOTO5000
    #
    # E$ is the last three letters of the noun: KIDNAPPER->PER,
    # DOLLAR->LAR, MONEY->NEY.  I(27) is the GUN (DATA item 27).
    # The DOLLAR is NOT a DATA item - it is created at run time here.
    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # Vault rules - source lines 467 / 960 / 1515 / 1516.
    #
    # Original listing line 467 (PDF logical line 1060):
    #   IF A=35 IF E$="PER" OR (E$="LAR" OR E$="NEY") IF I(27)=0 THEN
    #   PRINT"YOU GET TOO CLOSE TO HIM, HE JUMPS UP AND STRANGLES YOU.":
    #   GOTO7300 ELSE IF I(27)=1 PRINT"KIDNAPPER SEES YOUR GUN AND
    #   FREEZES. YOU GRAB A DOLLAR":A$(56)="DOLLAR":H$(56)=A$(56):
    #   A(56)=35:PM=1:E$="LAR"
    #
    # Original listing line 960 (the gun branch):
    #   IF D(B)<>14 THEN 970 ELSE IF E$="GUN" OR E$="PER" IF I(27)=1
    #   IF A=35 THEN PRINT"GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!":
    #   GOTO7200 ELSE PRINT"GUN MISFIRES":GOTO5000
    #
    # E$ is the last three letters of the noun: KIDNAPPER->PER,
    # DOLLAR->LAR, MONEY->NEY.  I(27) is the GUN (DATA item 27).
    # The DOLLAR is NOT a DATA item - it is created at run time here.
    # ----------------------------------------------------------------
    # Vault rules - original listing lines 1060 and 960 (room 35),
    # plus the room descriptions 1515 / 1516.
    #
    #   1060 IFA=35 AND (E$="PER" OR E$="LAR" OR E$="NEY") THEN
    #        IF I(27)=0 THEN PRINT"YOU GET TOO CLOSE TO HIM, HE JUMPS UP
    #        AND STRANGLES YOU.":GOTO7300
    #        ELSE IF I(27)=1 THEN PRINT"KIDNAPPER SEES YOUR GUN AND
    #        FREEZES. YOU GRAB A DOLLAR":A$(56)="DOLLAR":H$(56)=A$(56):
    #        A(56)=35:PM=1:E$="LAR"
    #
    #    960 IF D(B)<>14 THEN 970 ELSE IF E$="GUN" OR E$="PER" IF I(27)=1
    #        IF A=35 THEN PRINT"GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!":
    #        GOTO7200 ELSE PRINT"GUN MISFIRES":GOTO5000
    #
    # E$ is the last three letters of the noun: KIDNAPPER->PER,
    # DOLLAR->LAR, MONEY->NEY.  I(27) is the GUN (DATA item 27).
    # The DOLLAR is NOT a DATA item - it is created at run time here.
    # ----------------------------------------------------------------
    def _vault_rules(self, verb, noun):
        """Apply the source-accurate rules for the vault (room 35)."""
        v = (verb or "").upper()
        n = (noun or "").upper().strip()
        if not n:
            return None
        e = n[-3:] if len(n) >= 3 else n
        in_vault = getattr(self.state, "location", None) == 35
        inv = [str(i).upper() for i in getattr(self.state, "inventory", [])]
        has_gun = "GUN" in inv

        # 1060 - the money in the vault
        if v in ("GET", "TAKE") and e in ("PER", "LAR", "NEY"):
            if not in_vault:
                return None
            if getattr(self.state, "pm_scared", False):
                # 1516: the money is gone once he is scared.
                return ("The money is gone.", False)
            if not has_gun:
                # GOTO7300
                return (self._vault_death(
                    "YOU GET TOO CLOSE TO HIM, HE JUMPS UP AND STRANGLES YOU."),
                    False)
            # A$(56)="DOLLAR":H$(56)=A$(56):A(56)=35:PM=1:E$="LAR"
            setattr(self.state, "pm_scared", True)
            if "DOLLAR" not in inv:
                add = getattr(self.state, "add_item", None)
                if callable(add):
                    add("DOLLAR")
                else:
                    self.state.inventory.append("DOLLAR")
            return ("KIDNAPPER SEES YOUR GUN AND FREEZES. YOU GRAB A DOLLAR",
                    False)

        # 960 - the gun branch (source verb 14 = SHOOT; USE is the
        # remake's alias for the same action)
        if v in ("SHOOT", "FIRE", "USE") and e in ("GUN", "PER"):
            if not has_gun:
                return None
            if in_vault:
                # GOTO7200 -> GOTO7300
                return (self._vault_death(
                    "GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!",
                    VAULT_DEATH_7200), False)
            # 960: away from the vault the gun only misfires.
            return ("GUN MISFIRES", False)
        return None

    def _vault_death(self, message, extra=""):
        """GOTO7200 / GOTO7300 - the player is dead and the game is over.

        Returns the TEXT only; the caller wraps it in the (text, move)
        tuple the dispatcher expects.
        """
        try:
            self.state.alive = False
        except Exception:
            pass
        try:
            self.state.game_over = True
        except Exception:
            pass
        parts = [message]
        if extra:
            parts.append(extra)
        parts.append(VAULT_DEATH_7300)
        return "\n".join(parts)

    def handle_command(self, verb, noun=""):
        verb = (verb or "").upper().strip()
        noun = (noun or "").upper().strip()
        loc = self.state.location

        if verb in ("TAKE", "GRAB", "PICK"):
            verb = "GET"
        if verb in ("X", "CHECK"):
            verb = "EXAMINE"

        # Vault (room 35) rules - source lines 1060 and 960.  These must
        # run AFTER the verb aliases are normalised, and they must be
        # given the real noun (an empty noun used to short-circuit them).
        _vr = self._vault_rules(verb, noun)
        if _vr is not None:
            return _vr

        # Verb transitions have to be recognised BEFORE movement, so
        # that "GO LEDGE" is not mistaken for a direction.
        if verb == "CLIMB":
            if noun.startswith("LEDGE"):
                return self._wrap(self._climb_ledge(loc))
            if noun.startswith("WINDOW"):
                return self._wrap(self._climb_window(loc))
            return self._wrap(f"You can't climb the {noun}.")
        if verb == "GO" and noun:
            if noun.startswith("LEDGE"):
                return self._wrap(self._climb_ledge(loc))
            if noun.startswith("WINDOW"):
                return self._wrap(self._climb_window(loc))
        if verb == "JUMP":
            return self._wrap(self._jump(loc))
        if verb == "INFLATE":
            return self._wrap(self._inflate(loc, noun))
        if verb == "TIE":
            return self._wrap(self._tie(loc, noun))
        if verb == "PAY":
            return self._wrap(self._buy_string(loc, noun))
        if verb == "PUT" and "DOLLAR" in noun:
            return self._wrap(self._buy_string(loc, noun))

        if verb in ("LOOK", "L"):
            return self._wrap(self._describe_room(loc))
        if verb in ("INVENTORY", "INV", "I"):
            return self._wrap(self._inventory())
        if verb == "GET":
            return self._wrap(self._do_get(noun, loc))
        if verb == "DROP":
            return self._wrap(self._do_drop(noun, loc))
        if verb in ("USE", "APPLY"):
            return self._wrap(self._do_use(noun, loc))
        if verb in ("OPEN", "UNLOCK"):
            return self._wrap(self._do_open(noun, loc))
        if verb in ("EXAMINE", "READ"):
            return self._wrap(self._examine(noun, loc))
        if verb in ("PUSH", "PRESS"):
            return self._wrap(self._do_push(noun, loc))

        # Movement
        d = self._parse_direction(verb, noun)
        if d is not None:
            return self._wrap(self._go(d, loc))
        return self._wrap("You can't do that.")

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _go(self, d, loc):
        r = self.get_room(loc)
        if r is None:
            return "You are nowhere."
        if d == "D":
            # Handler 608: DOWN at a ledge takes you off it.
            if loc == _LEDGE_RIGHT:
                self.state.location = 33
                return self._describe_room(33)
            if loc == _LEDGE_LEFT:
                self.state.location = _VAULT_ROOM
                return self._describe_room(_VAULT_ROOM)
        if d == "U":
            return "There's no way up from here."
        dest = r["exits"].get(d)
        if dest is None:
            return "You can't go that way."
        self.state.location = dest
        return self._describe_room(dest)

    def _climb_ledge(self, loc):
        """Handler 610: CLIMB LEDGE (or GO LEDGE) from 33 -> 34, 35 -> 36."""
        if loc == 33:
            self.state.location = _LEDGE_RIGHT
            return self._describe_room(_LEDGE_RIGHT)
        if loc == _VAULT_ROOM:
            self.state.location = _LEDGE_LEFT
            return self._describe_room(_LEDGE_LEFT)
        if loc == _LEDGE_LEFT:
            return "You are already on the ledge."
        return "There's no ledge to climb here."

    def _climb_window(self, loc):
        """Handler 608: CLIMB WINDOW (or GO WINDOW) from 34 -> 33, 36 -> 35."""
        if loc == _LEDGE_RIGHT:
            self.state.location = 33
            return self._describe_room(33)
        if loc == _LEDGE_LEFT:
            self.state.location = _VAULT_ROOM
            return self._describe_room(_VAULT_ROOM)
        if loc == _VAULT_ROOM:
            return "The vault has no window to climb."
        return "There's no window here."

    def _jump(self, loc):
        """JUMP off the right-hand ledge (room 34) drops to floor 5.

        With a tied balloon the source prints "BALLOON CARRIES YOU DOWN
        ONE FLOOR" (handler 800); without one you simply jump.
        """
        if loc != _LEDGE_RIGHT:
            return "There's nothing to jump from here."
        landing = SPECIAL_ROOMS.get("floor_5", {}).get("landing_room", 43)
        # The marker has to be the WHOLE result: the dispatcher in
        # kidnapped.py only parses a result that starts with
        # "TRANSITION:floor_N:room", and it suppresses any result that
        # starts with "TRANSITION:" when printing.  The flavour line is
        # kept on the engine for the arrival side to use.
        if self.balloon_state == "tied":
            self.last_transition_note = "BALLOON CARRIES YOU DOWN ONE FLOOR"
        else:
            self.last_transition_note = "YOU JUMP DOWN TO THE NEXT FLOOR"
        return f"TRANSITION:floor_5:{landing}"

    # ------------------------------------------------------------------
    # Room description
    # ------------------------------------------------------------------
    def _describe_room(self, loc):
        r = self.get_room(loc)
        if r is None:
            return "You are nowhere."
        lines = [f"**{r['name']}**", r["desc"]]
        items = self._room_items.get(loc, [])
        if items:
            lines.append(f"Things here: {', '.join(items)}.")
        lines.append(f"Exits: {', '.join(r['exits'].keys())}.")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # GET / DROP
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"
        room_items = self._room_items.get(loc, [])
        item = self._canonical_item(noun)

        # The balloon changes identity as the puzzle proceeds.
        if "BALLOON" in noun:
            if self.balloon_state != "deflated":
                if self.balloon_state == "inflated":
                    return "You already have the balloon inflated."
                return "You already have the balloon tied to a string."
            if "LARGE DEFLATED BALLOON" not in room_items:
                return "No balloon here."
            room_items.remove("LARGE DEFLATED BALLOON")
            self._room_items[loc] = room_items
            self._add_to_inventory("LARGE DEFLATED BALLOON")
            return "You take the large deflated balloon."

        if "STRING" in noun and "VENDING" not in noun and "SIGN" not in noun:
            if self.string_bought and "LONG STRING" in room_items:
                room_items.remove("LONG STRING")
                self._room_items[loc] = room_items
                self._add_to_inventory("LONG STRING")
                return "You take the long string."
            if self.string_bought:
                return "You already have the string."
            return "No string here."

        if item is None or item not in room_items:
            return f"No {noun} here."
        if item in FIXED_ITEMS:
            return f"The {item} can't be taken - it's fixed in place."
        room_items.remove(item)
        self._room_items[loc] = room_items
        self._add_to_inventory(item)
        return f"You take the {item}."

    def _do_drop(self, noun, loc):
        inv = getattr(self.state, "inventory", None) or []
        item = self._canonical_item(noun)
        if item is None or item not in inv:
            return f"You're not carrying a {noun}."
        self._remove_from_inventory(item)
        self._room_items.setdefault(loc, []).append(item)
        return f"You drop the {item}."

    # ------------------------------------------------------------------
    # The puzzle verbs
    # ------------------------------------------------------------------
    def _inflate(self, loc, noun):
        """Handler 950: INFLATE BALLOON needs the helium tank."""
        if noun and "BALLOON" not in noun:
            return f"You can't inflate the {noun}."
        if self.balloon_state == "inflated":
            return "The balloon is already inflated."
        if self.balloon_state == "tied":
            return "The balloon is already tied to the string."
        if not self._carrying("LARGE DEFLATED BALLOON"):
            return "You don't have a balloon to inflate."
        if not self._carrying("TANK OF HELIUM GAS"):
            return "You need something to inflate it with."
        self._remove_from_inventory("LARGE DEFLATED BALLOON")
        self._add_to_inventory("LARGE INFLATED BALLOON")
        self.balloon_state = "inflated"
        return ("You twist the valve on the tank and the balloon swells up "
                "fat and round.")

    def _tie(self, loc, noun):
        """Handler 835: TIE BALLOON / TIE STRING needs an inflated balloon."""
        if noun and "BALLOON" not in noun and "STRING" not in noun:
            return f"You can't tie the {noun}."
        if self.balloon_state == "tied":
            return "The balloon is already tied to the string."
        if self.balloon_state != "inflated":
            return "You need an inflated balloon to tie the string to."
        if not self._carrying("LONG STRING"):
            return "You need a string to tie to the balloon."
        self._remove_from_inventory("LARGE INFLATED BALLOON")
        self._remove_from_inventory("LONG STRING")
        self._add_to_inventory("INFLATED BALLOON WITH STRING")
        self.balloon_state = "tied"
        return ("You tie the string to the balloon and hold on. The "
                "balloon tugs gently at your hand.")

    def _buy_string(self, loc, noun):
        """Handler 550: PUT DOLLAR (or PAY DOLLAR) in the vending machine."""
        if loc != _STORE_ROOM:
            return "There's no machine to put money into here."
        if noun and "DOLLAR" not in noun and "MONEY" not in noun:
            return f"You can't buy the {noun}."
        if not self._carrying("DOLLAR"):
            return "You don't have any money."
        if self.string_bought:
            return "You've already bought the string."
        self._remove_from_inventory("DOLLAR")
        self.string_bought = True
        items = self._room_items.setdefault(_STORE_ROOM, [])
        items.append("LONG STRING")
        return ("You drop the dollar into the machine. It clunks, and a "
                "long string drops out of the slot.")

    # ------------------------------------------------------------------
    # Misc verbs
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if "GUN" in noun:
            if loc == _VAULT_ROOM and self._carrying("GUN"):
                self.shot_up = True
                return ("GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!")
            if not self._carrying("GUN"):
                return "You aren't carrying a gun."
            return "GUN MISFIRES"
        if "BALLOON" in noun:
            return self._inflate(loc, noun)
        if "STRING" in noun:
            return self._tie(loc, noun)
        if "DOLLAR" in noun:
            return self._buy_string(loc, noun)
        return f"You can't use the {noun}."

    def _do_open(self, noun, loc):
        if "DOOR" in noun:
            if loc == 30:
                return "THE DOOR'S LOCKED"
            return "There's no door here."
        if "WINDOW" in noun:
            if loc == 33:
                return "The window is already open."
            return "There's no window here."
        return f"You can't open the {noun}."

    def _examine(self, noun, loc):
        if "SIGN" in noun:
            if loc == _STORE_ROOM:
                return "SIGN: STRING COSTS $1.00"
            return "There's no sign here."
        if "MACHINE" in noun or "VENDING" in noun:
            if loc == _STORE_ROOM:
                if self.string_bought:
                    return "The machine is empty now."
                return "The machine is full of string. It costs $1.00."
            return "There's no machine here."
        if "DOLLAR" in noun or "MONEY" in noun:
            if loc == _VAULT_ROOM:
                return "A fat roll of money, worth about a dollar."
            return "There's no money here."
        if "GUN" in noun:
            if loc == _GUN_ROOM:
                return "A gun, lying on the desk."
            if self._carrying("GUN"):
                return "A small handgun. The chambers are empty."
            return "You aren't carrying a gun."
        if "BALLOON" in noun:
            if self.balloon_state == "tied":
                return "A large balloon, inflated and tied to a long string."
            if self.balloon_state == "inflated":
                return "A large balloon, round and tight with helium."
            if self._carrying("LARGE DEFLATED BALLOON"):
                return "A large balloon, limp and folded over."
            return "There's no balloon here."
        if "TANK" in noun or "HELIUM" in noun:
            if loc == _TANK_ROOM:
                return "A tank of helium gas, hissing faintly."
            return "There's no tank here."
        if "LEDGE" in noun:
            return ("A narrow ledge along the outside of the building. "
                    "It runs west toward another window.")
        if "WINDOW" in noun:
            if loc == 33:
                return "An open window, giving onto the ledge."
            return "There's no window here."
        if "KIDNAPPER" in noun:
            return "He's counting money and doesn't see you yet."
        return f"You can't see anything special about the {noun}."

    def _do_push(self, noun, loc):
        if "BUTTON" in noun:
            return "There's no button here."
        return f"You can't push the {noun}."


# --------------------------------------------------------------------
# Vault (room 35) descriptions - source lines 1515 and 1516.
#   1515 PRINT"KIDNAPPER IS COUNTING MONEY. HE DOESN'T SEE YOU YET."
#   1516 PRINT"KIDNAPPER IS SCARED"
# --------------------------------------------------------------------
VAULT_DESC_COUNTING = (
    "A vault, small and square, its door standing open. A single "
    "desk sits inside it, with a fat roll of money on top. A "
    "KIDNAPPER IS COUNTING MONEY, HE DOESN'T SEE YOU YET."
)
VAULT_DEATH_7200 = 'YOU SEEM TO HAVE GOTTEN YOURSELF KILLED!'
VAULT_DEATH_7300 = "TO TRY AGAIN YOU'LL HAVE TO START OVER FROM THE 9TH FLOOR."

VAULT_DESC_SCARED = (
    "A vault, small and square, its door standing open. The money is "
    "gone. The KIDNAPPER IS SCARED."
)

if isinstance(ROOMS.get(35), dict):
    ROOMS[35]["desc"] = VAULT_DESC_COUNTING

_orig_get_room = getattr(Floor6Engine, "get_room", None)
if _orig_get_room is not None:
    def _wrapped_get_room(self, *a, **kw):
        data = _orig_get_room(self, *a, **kw)
        try:
            room = a[0] if a else kw.get("room")
            if room == 35 and isinstance(data, dict):
                data = dict(data)
                data["desc"] = (VAULT_DESC_SCARED
                                if getattr(self.state, "pm_scared", False)
                                else VAULT_DESC_COUNTING)
                items = list(data.get("items") or [])
                if getattr(self.state, "pm_scared", False):
                    items = [i for i in items if i != "DOLLAR"]
                data["items"] = items
        except Exception:
            pass
        return data
    Floor6Engine.get_room = _wrapped_get_room
