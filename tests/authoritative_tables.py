"""
Authoritative room tables for the Kidnapped remake's tests.

This module is the single source of truth used by the test suite to
validate floors/*.py. It is transcribed from

    /home/chris/repos/kidnapped-text-adventure/FLOOR9_AUDIT_2026-11-03.md

which is the pixel-derived corrected audit of KIDNAPPED_Original.pdf
(SoftSide, Dec 1980), reconciled against two published walkthroughs
(archive/solutions/sol_gunness.txt, archive/solutions/sol_atari.txt) and
Garry Francis's 2015 floor map.

TRUST RULES (this project failed before because these were ignored):
  * KIDNAPPED.BAS, PARSED_BASIC_SOURCE.txt, SPEC.md and the old
    floors/*.py are guesses, not truth.
  * The PDF OCR layer corrupts a printed 4 as a 1. Only pixel reads
    (pdftoppm -r 300 -gray -png + vision_analyze) are trusted.
  * Listing dispatch is ON A GOTO 11,12,...,75, so global room number
    = BASIC line number - 10.

Floors 1-5 and 7 have NOT been audited yet. Their room tables in the tests
are still guesses, so the source-pair validation for them is skipped
rather than validating a guess against itself (see
tests/test_all_floors_map.py).

Floors 6, 8 and 9 ARE audited: their tables below are the pixel-derived
corrected ones and are compared against the floor modules.
"""

# ---------------------------------------------------------------------
# FLOOR 9 - global rooms 1..11 (audited)
#
# Room 12 ("ON A VERY NARROW LEDGE.") is deliberately NOT listed: it is
# a verb-only special room, it is on no map and it appears in neither
# walkthrough.
#
# Verb transitions (NOT directional exits):
#   room  9  CLIMB CHAIR          -> room 11
#   room 11  TAPE WIRES           -> fixes the elevator
#   room  9  PRESS BUTTON        -> floor 8, room 13
# ---------------------------------------------------------------------
FLOOR9_ROOMS = {
    1: {
        "name": "IN A HALLWAY",
        "exits": {"W": 4, "N": 2, "E": 8, "S": 7},
        "items": [],
    },
    2: {
        "name": "IN AN OFFICE",
        "exits": {"N": 3, "S": 1},
        "items": ["PAPER NOTE", "DESK", "CHAIR"],
    },
    3: {
        "name": "IN A CLOSET",
        "exits": {"S": 2},
        "items": ["LONG BROOM"],
    },
    4: {
        "name": "IN A HALLWAY",
        "exits": {"N": 5, "E": 1, "S": 6},
        "items": [],
    },
    5: {
        "name": "IN AN OFFICE",
        "exits": {"S": 4},
        "items": ["TV SET", "CLOCK"],
    },
    6: {
        "name": "IN A RESTROOM",
        "exits": {"N": 4},
        "items": ["GRAFFITI ON WALL"],
    },
    7: {
        "name": "IN AN OFFICE",
        "exits": {"N": 1},
        "items": ["OPEN WINDOW", "KEY ON KEY CHAIN"],
    },
    8: {
        "name": "IN A HALLWAY",
        "exits": {"W": 1, "N": 9, "S": 10},
        "items": [],
    },
    9: {
        "name": "IN AN ELEVATOR",
        "exits": {"S": 8},
        "items": ["TRAP DOOR IN CEILING", "DOWN BUTTON"],
    },
    10: {
        "name": "IN A MAINTENANCE ROOM",
        "exits": {"N": 8},
        "items": ["CABINET", "FLASHLIGHT", "TAPE"],
    },
    11: {
        "name": "IN A CRAWLSPACE ON TOP OF THE ELEVATOR",
        "exits": {"D": 9},
        "items": ["ENDS OF 2 LIVE WIRES"],
    },
}

# ---------------------------------------------------------------------
# FLOOR 8 - global rooms 13..17 (audited)
#
# Verb transition (NOT a directional exit):
#   room 17  TIE ROPE / CLIMB ROPE -> floor 7
# ---------------------------------------------------------------------
FLOOR8_ROOMS = {
    13: {
        "name": "IN A HALLWAY",
        "exits": {"W": 14, "S": 16},
        "items": [],
    },
    14: {
        "name": "IN A VISITORS LOUNGE",
        "exits": {"W": 15, "E": 13},
        "items": ["AQUARIUM"],
    },
    15: {
        "name": "IN A CLOSET",
        "exits": {"E": 14},
        "items": ["ROPE"],
    },
    16: {
        "name": "IN AN OFFICE",
        "exits": {"N": 13, "E": 17},
        "items": ["SLEEPING PILL"],
    },
    17: {
        "name": "IN AN OFFICE",
        "exits": {"W": 16},
        "items": ["OPEN WINDOW", "DESK"],
    },
}

# ---------------------------------------------------------------------
# FLOOR 6 - global rooms 26..36 (audited 2026-11-04)
#
# Pixel read of the original listing (page 1, right column, printed
# lines 36-46; global room = printed line - 10), reconciled against
# both published walkthroughs and Francis's 2015 floor-6 map panel.
#
# Verb transitions (NOT directional exits):
#   room 33  CLIMB LEDGE / GO LEDGE   -> room 34
#   room 35  CLIMB LEDGE / GO LEDGE   -> room 36
#   room 34  CLIMB WINDOW / GO WINDOW -> room 33
#   room 36  CLIMB WINDOW / GO WINDOW -> room 35
#   room 34  JUMP                     -> floor 5
#   room 32  READ SIGN                -> "SIGN: STRING COSTS $1.00"
#   room 32  PUT DOLLAR / PAY DOLLAR  -> buys the LONG STRING
# ---------------------------------------------------------------------
FLOOR6_ROOMS = {
    26: {
        "name": "IN A HALLWAY",
        "exits": {"W": 31, "N": 27, "E": 29, "S": 30},
        "items": [],
    },
    27: {
        "name": "IN AN OFFICE",
        "exits": {"N": 28, "S": 26},
        "items": [],
    },
    28: {
        "name": "IN A CLOSET",
        "exits": {"S": 27},
        "items": ["TANK OF HELIUM GAS"],
    },
    29: {
        "name": "IN A GAME ROOM",
        "exits": {"W": 26},
        "items": ["LARGE DEFLATED BALLOON"],
    },
    30: {
        "name": "IN AN OFFICE",
        "exits": {"N": 26},
        "items": ["GUN", "LOCKED DOOR"],
    },
    31: {
        "name": "IN A HALLWAY",
        "exits": {"W": 33, "N": 32, "E": 26},
        "items": [],
    },
    32: {
        "name": "IN A STORE ROOM",
        "exits": {"S": 31},
        "items": ["SIGN ON WALL", "STRING VENDING MACHINE"],
    },
    33: {
        "name": "IN AN OFFICE",
        "exits": {"E": 31},
        "items": ["OPEN WINDOW"],
    },
    34: {
        "name": "ON A LARGE LEDGE BY WINDOW",
        "exits": {"W": 36},
        "items": [],
    },
    35: {
        "name": "IN THE VAULT",
        "exits": {"W": 36},
        "items": ["DOLLAR"],
    },
    36: {
        "name": "ON A LARGE LEDGE BY WINDOW",
        "exits": {"E": 34},
        "items": [],
    },
}

# Items that are visible on floor 6, by room.  Scenery (the sign, the
# vending machine, the open window, the locked door) carries a NEGATIVE
# room number in the source DATA rows and cannot be picked up.
FLOOR6_ITEMS = {
    28: ["TANK OF HELIUM GAS"],
    29: ["LARGE DEFLATED BALLOON"],
    30: ["GUN", "LOCKED DOOR"],
    32: ["SIGN ON WALL", "STRING VENDING MACHINE"],
    33: ["OPEN WINDOW"],
    35: ["DOLLAR"],
}

# Rooms that must NOT exist on floor 6.  Floor 6 owns exactly 26-36.
FLOOR6_FORBIDDEN_ROOMS = (set(range(1, 26)) | set(range(37, 66)))

# ---------------------------------------------------------------------
# Floors whose room tables have NOT been pixel-audited yet.
# The all-floors map test skips source-pair validation for these
# instead of grading a guess against itself.
#
# Floor 8 is audited (its table is above), so it is NOT on this list:
# floors/floor_8.py now carries the authoritative 13-17 table and the
# map test compares the two.
# ---------------------------------------------------------------------
UNAUDITED_FLOORS = {1, 2, 3, 4, 5}

# Audited floors, keyed by floor number.
# Floor 7 - listing lines 28-35 of the original BASIC listing.
# Transcribed from the printed PDF pixels (300 dpi), not from OCR.
# Rooms 18-25 fill the gap between floor 8 (13-17) and floor 6 (26-36).
#
# "items" are takeable.  "fixed_items" are scenery: the source gives
# them a NEGATIVE room number in its DATA rows, so they cannot be
# picked up.  The locked door is a verb link (24 <-> 25), not an exit.
FLOOR7_ROOMS = {
    18: {
        "name": "IN A HALLWAY",
        "exits": {"W": 20, "N": 19, "E": 24, "S": 21},
        "items": [],
        "fixed_items": [],
    },
    19: {
        "name": "IN AN OFFICE",
        "exits": {"S": 18},
        "items": [],
        "fixed_items": ["KEY MAKING MACHINE"],
    },
    20: {
        "name": "IN A TOOL CRIB",
        "exits": {"E": 18},
        "items": ["SUPER GLUE", "WOODEN STAIR STEP"],
        "fixed_items": [],
    },
    21: {
        "name": "IN A HALLWAY",
        "exits": {"N": 18, "E": 22},
        "items": [],
        "fixed_items": [],
    },
    22: {
        "name": "IN AN OFFICE",
        "exits": {"W": 21, "E": 23},
        "items": [],
        "fixed_items": [],
    },
    23: {
        "name": "IN A SMALL STORAGE ROOM",
        "exits": {"W": 22},
        "items": ["THICK COPPER SHEET"],
        "fixed_items": [],
    },
    24: {
        "name": "IN A HALLWAY",
        "exits": {"W": 18},
        "items": [],
        "fixed_items": ["LOCKED DOOR"],
    },
    25: {
        "name": "IN A NARROW STAIRWAY",
        "exits": {"W": 24},
        "items": [],
        "fixed_items": ["WOODEN STAIRS"],
    },
}

AUDITED_ROOMS = {
    6: FLOOR6_ROOMS,
    7: FLOOR7_ROOMS,
    8: FLOOR8_ROOMS,
    9: FLOOR9_ROOMS,
}

# Rooms that must NOT exist on floor 9 (audit-proven wrong/omitted).
FLOOR9_FORBIDDEN_ROOMS = {12, 13, 14, 15, 16, 17}


def source_pairs(rooms):
    """Flatten a room table into the (room, direction, target) triple form
    the map tests compare against."""
    pairs = set()
    for rid, r in rooms.items():
        for d, t in r["exits"].items():
            pairs.add((rid, d, t))
    return pairs
