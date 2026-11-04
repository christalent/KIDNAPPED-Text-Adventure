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

Floors 1-8 have NOT been audited yet. Their room tables in the tests
are still guesses, so the source-pair validation for them is skipped
rather than validating a guess against itself (see
tests/test_all_floors_map.py).
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
# Floors whose room tables have NOT been pixel-audited yet.
# The all-floors map test skips source-pair validation for these
# instead of grading a guess against itself.
# ---------------------------------------------------------------------
UNAUDITED_FLOORS = {1, 2, 3, 4, 5, 6, 7, 8}

# Audited floors, keyed by floor number.
AUDITED_ROOMS = {
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
