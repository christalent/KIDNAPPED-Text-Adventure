#!/usr/bin/env python3
"""
End-to-end escape test: floor 9 -> the street, through the REAL engine.

This is the integration test the repo was missing.  Every other test in
tests/ drives ONE floor's engine in isolation, so a defect that only
shows up when two floors meet - a transition marker naming the wrong
landing room, a carry-over item shadowing another floor's item, a verb
one floor understands and the next does not - cannot be caught by them.

What this file does:

  1. Replays BOTH published solutions (Garry Francis' minimal Atari
     solution and Jacob Gunness' CASA walkthrough) command for command
     through ``kidnapped.GameRunner`` - the same dispatcher the REPL
     uses.  The test drives the real game loop, not a re-implementation
     of it.

  2. Checks every room the player lands in against the PIXEL-VERIFIED
     room tables in tests/authoritative_tables.py (floors 1-5 are loaded
     from audit/floors_1_5_verified.json, floors 6-9 from the audited
     tables).  The expected room is computed from the audit table, so
     this test cannot grade the engine against itself.

  3. Checks every floor transition: the marker must name the right
     target floor, and the player must land in that floor's audited
     arrival room.

  4. Checks the game ends in a real escape: floor 1's front door.

The two published solutions take different routes through the same
rooms - Francis reads the note on floor 9, Gunness watches the TV;
Francis crosses floor 6's vault with GO LEDGE, Gunness with CLIMB
LEDGE; Francis uses GO ROPE on floor 1, Gunness CLIMB ROPE.  Both must
escape.

Run:  python3 tests/test_full_game_escape.py
"""

import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import authoritative_tables
from kidnapped import GameRunner


# ---------------------------------------------------------------------
# The audited room tables.  Everything below is checked against THESE,
# never against the floor modules.
# ---------------------------------------------------------------------
ROOMS = authoritative_tables.AUDITED_ROOMS

# The room the player lands in on each floor, from the audit:
#   floors 1-5  audit/floors_1_5_verified.json ("entry")
#   floor 6     audit/FLOOR6_2026-11-05.md - arrival hall, room 26
#   floor 7     audit/FLOOR7_2026-11-05.md - entry room 18
#   floor 8     floor 9's PRESS BUTTON lands in room 13
#   floor 9     the game starts in room 1
AUDITED_ARRIVALS = {
    9: 1,
    8: 13,
    7: 18,
    6: 26,
    5: 43,
    4: 45,
    3: 52,
    2: 58,
    1: 63,
}

# Verb moves that change room WITHOUT a compass exit.  Each is recorded
# in the audit notes next to the room table it belongs to:
#
#   floor 4 room 48  SWIM          -> room 49 (the pool fills)
#   floor 3 room 55  GO DOOR       -> room 57 (through the steel door)
#   floor 2 room 59  GO PLANT      -> room 60 (the plant has grown)
#   floor 2 room 61  GO ROPE       -> room 62 (the flute's rope)
#   floor 1 room 64  GO ROPE       -> room 65 (across the pit)
#   floor 5 room 43  GO DOOR       -> room 44 (through the locked door)
#   floor 7 room 24  GO DOOR       -> room 25 (the narrow stairway)
#   floor 6 room 33  GO/CLIMB LEDGE   -> room 34
#   floor 6 room 35  GO/CLIMB LEDGE   -> room 36
#   floor 6 room 34  GO/CLIMB WINDOW  -> room 33
#   floor 6 room 36  GO/CLIMB WINDOW  -> room 35
#   floor 9 room  9  GO/CLIMB CHAIR   -> room 11
#
# Keyed by (floor, room, verb, noun); the noun is upper-cased.
VERB_MOVES = {
    (4, 48, "SWIM", ""): 49,
    (3, 55, "GO", "DOOR"): 57,
    (2, 59, "GO", "PLANT"): 60,
    (2, 59, "CLIMB", "PLANT"): 60,
    (2, 61, "GO", "ROPE"): 62,
    (2, 61, "CLIMB", "ROPE"): 62,
    (1, 64, "GO", "ROPE"): 65,
    (1, 64, "CLIMB", "ROPE"): 65,
    (5, 43, "GO", "DOOR"): 44,
    (7, 24, "GO", "DOOR"): 25,
    (6, 33, "GO", "LEDGE"): 34,
    (6, 33, "CLIMB", "LEDGE"): 34,
    (6, 35, "GO", "LEDGE"): 36,
    (6, 35, "CLIMB", "LEDGE"): 36,
    (6, 34, "GO", "WINDOW"): 33,
    (6, 34, "CLIMB", "WINDOW"): 33,
    (6, 36, "GO", "WINDOW"): 35,
    (6, 36, "CLIMB", "WINDOW"): 35,
    (9, 9, "GO", "CHAIR"): 11,
    (9, 9, "CLIMB", "CHAIR"): 11,
}

# Responses that mean the step did NOT do what the walkthrough says.
# Exact refusal strings taken from the engine source.  Matching is
# exact-prefix, not substring: floor 6's room description contains
# "There is nothing below you but a long drop", and a substring
# test for "there is no" flagged that legitimate description as a
# refusal.
# Exact refusal strings taken from the engine source.  Matching is
# exact-prefix, not substring: floor 6's room description contains
# "There is nothing below you but a long drop", and a substring
# test for "there is no" flagged that legitimate description as a
# refusal.  Only whole refusal sentences qualify - fragments of
# prose scraped out of the middle of a description do not.
REFUSALS = (
    "The wires are live! You can't tape them safely.\\\\n",
    "The {0} is part of the building. You can't take it.",
    "You aren't carrying a gun.",
    "You aren't carrying that.",
    "You can't buy the {noun}.",
    "You can't climb the {noun.lower()}.",
    "You can't climb the {noun}.",
    "You can't climb the {n}.",
    "You can't do that here.",
    "You can't do that.",
    "You can't figure out how to use that here.",
    "You can't go that way.",
    "You can't go {direction} from here.",
    "You can't inflate the {noun}.",
    "You can't knit that.",
    "You can't open that.",
    "You can't open the {noun}.",
    "You can't pour that.",
    "You can't push the {noun}.",
    "You can't see anything special about the {noun}.",
    "You can't throw that.",
    "You can't tie that.",
    "You can't tie the {noun}.",
    "You can't use that here.",
    "You can't use the {noun}.",
    "You do not have the book.",
    "You do not have the fluid.",
    "You do not have the flute.",
    "You do not have the rope.",
    "You do not have the solution.",
    "You do not have the umbrella.",
    "You don't have a balloon to inflate.",
    "You don't have a broom.",
    "You don't have a flashlight.",
    "You don't have a rope to tie.",
    "You don't have a rope.",
    "You don't have any money.",
    "You don't have any tape.",
    "You don't have the book.",
    "You don't know how to do that.",
    "You don't see anything unusual.",
    "You don't see that here.",
    "You have no idea how to tie a rope for this.",
    "You have no use for it here.",
    "You have no water in the cup.",
    "You see nothing like that here.",
    "You're not carrying a {noun}.",
    "You're not carrying that.",
)


def D(direction):
    """A bare compass direction as the walkthroughs write it."""
    return ("GO", direction)


# ---------------------------------------------------------------------
# The two published solutions, transcribed from archive/solutions/.
#
# sol_atari.txt  = Garry Francis, minimal Atari solution
# sol_gunness.txt = Jacob Gunness, CASA Solution Archive, Sept 2004
#
# Each floor section is (list of steps, exit step).  The exit step is
# (verb, noun, target_floor, landing_room); for floor 1 the target is
# the string "escape".
# ---------------------------------------------------------------------

FRANCIS = [
    (9, [
        D("N"), ("GET", "CHAIR"),
        D("N"), ("GET", "LONG BROOM"),
        D("S"), D("S"), D("S"),
        ("GET", "KEY"),
        D("N"), D("E"), D("S"),
        ("OPEN", "CABINET"),
        ("GET", "FLASHLIGHT"), ("LIGHT", "FLASHLIGHT"),
        ("GET", "ELECTRICAL TAPE"),
        D("N"), D("N"),
        ("DROP", "CHAIR"), ("WAIT", ""),
        ("GO", "CHAIR"),
        ("TAPE", "WIRES"),
        D("D"),
    ], ("PRESS", "BUTTON", 8, 13)),
    (8, [
        D("S"), ("GET", "SLEEPING PILL"),
        D("N"), D("W"),
        ("DROP", "SLEEPING PILL"), ("GET", "SLEEPING PIRANHA"),
        D("W"), ("GET", "ROPE"),
        D("E"), D("E"), D("S"),
        ("DROP", "SLEEPING PIRANHA"),
        D("E"), ("TIE", "ROPE"),
    ], ("GO", "ROPE", 7, 18)),
    (7, [
        D("S"), D("E"), D("E"),
        ("GET", "THICK COPPER SHEET"),
        D("W"), D("W"), D("N"), D("N"),
        ("MAKE", "KEY"), ("GET", "CRUDE KEY"),
        D("S"), D("W"),
        ("GET", "SUPER GLUE"), ("GET", "WOODEN STAIR STEP"),
        D("E"), D("E"),
        ("OPEN", "DOOR"), ("GO", "DOOR"),
        ("GLUE", "STEP"),
    ], ("GO", "STAIRS", 6, 26)),
    (6, [
        D("S"), ("GET", "GUN"),
        D("N"), D("E"), ("GET", "LARGE DEFLATED BALLOON"),
        D("W"), D("N"), D("N"),
        ("GET", "TANK OF HELIUM GAS"), ("INFLATE", "BALLOON"),
        D("S"), D("S"), D("W"), D("W"),
        ("GO", "LEDGE"), D("W"), ("GO", "WINDOW"), ("GET", "DOLLAR"),
        D("W"), D("E"), ("GO", "WINDOW"), D("E"), D("N"),
        ("PAY", "DOLLAR"), ("GET", "LONG STRING"), ("TIE", "STRING"),
        D("S"), D("W"), ("GO", "LEDGE"),
    ], ("JUMP", "", 5, 43)),
    (5, [
        D("E"), D("S"), ("PRESS", "BUTTON"),
        D("N"), D("W"), D("W"), D("S"),
        ("GET", "KNITTING NEEDLES"),
        D("N"), D("N"), ("GET", "BALL OF YARN"), ("KNIT", "CLOTHES"),
        D("S"), D("E"), D("E"), D("N"),
        ("GET", "SMALL KEY"),
        D("S"), D("W"), ("OPEN", "DOOR"), ("GO", "DOOR"),
    ], ("GO", "STAIRS", 4, 45)),
    (4, [
        D("N"), ("PRESS", "BUTTON"),
        D("S"), D("S"),
        ("GET", "BOOK"), ("READ", "BOOK"),
        D("N"), D("E"), ("SWIM", ""), D("N"),
        ("GET", "MARY POPPIN'S UMBRELLA"), ("OPEN", "UMBRELLA"),
        D("S"), D("E"),
    ], ("JUMP", "", 3, 52)),
    (3, [
        D("E"), D("E"), D("N"),
        ("GET", "JAR OF FLUID"), ("DRINK", "FLUID"),
        ("GET", "VIAL OF YELLOW SOLUTION"),
        D("S"), ("OPEN", "DOOR"), ("DRINK", "SOLUTION"), ("GO", "DOOR"),
    ], ("GO", "SLIDE", 2, 58)),
    (2, [
        ("GET", "PAPER CUP"), ("GET", "WATER"),
        D("W"), ("POUR", "WATER"), ("GO", "PLANT"),
        D("E"), ("GET", "FLUTE"), ("PLAY", "FLUTE"), ("GO", "ROPE"),
    ], ("GO", "STAIRS", 1, 63)),
    (1, [
        ("GET", "KEY"), ("GET", "LONG ROPE"),
        D("E"), ("GET", "BOOK"), ("READ", "BOOK"),
        ("TIE", "ROPE"), ("THROW", "ROPE"), ("GO", "ROPE"),
        ("OPEN", "DOOR"),
    ], ("GO", "DOOR", "escape", 0)),
]


GUNNESS = [
    (9, [
        D("N"), ("GET", "CHAIR"), ("READ", "NOTE"),
        D("N"), ("GET", "BROOM"),
        D("S"), D("S"), D("S"),
        ("GET", "KEY"),
        D("N"), D("W"), D("S"), ("READ", "GRAFFITI"),
        D("N"), D("N"), ("WATCH", "TV"),
        D("S"), D("E"), D("E"), D("S"),
        ("OPEN", "CABINET"),
        ("GET", "FLASHLIGHT"), ("GET", "TAPE"), ("LIGHT", "FLASHLIGHT"),
        D("N"), D("N"),
        ("DROP", "CHAIR"), ("CLIMB", "CHAIR"),
        ("TAPE", "WIRES"),
        D("D"),
    ], ("PRESS", "BUTTON", 8, 13)),
    (8, [
        D("S"), ("GET", "PILL"),
        D("N"), D("W"), D("W"), ("GET", "ROPE"),
        D("E"), ("DROP", "PILL"), ("GET", "PIRANHA"),
        D("E"), D("S"), ("DROP", "PIRANHA"),
        D("E"), ("TIE", "ROPE"),
    ], ("CLIMB", "ROPE", 7, 18)),
    (7, [
        D("W"), ("GET", "GLUE"), ("GET", "STEP"),
        D("E"), D("S"), D("E"), D("E"),
        ("GET", "SHEET"),
        D("W"), D("W"), D("N"), D("N"),
        ("MAKE", "KEY"), ("GET", "KEY"),
        D("S"), D("E"),
        ("OPEN", "DOOR"), ("GO", "DOOR"), ("GLUE", "STEP"),
    ], ("CLIMB", "STAIRS", 6, 26)),
    (6, [
        D("N"), D("N"), ("GET", "GAS"),
        D("S"), D("S"), D("E"), ("GET", "BALLOON"),
        D("W"), D("S"), ("GET", "GUN"),
        D("N"), D("W"), D("W"),
        ("CLIMB", "LEDGE"), D("W"), ("CLIMB", "WINDOW"), ("GET", "DOLLAR"),
        D("W"), D("E"), ("CLIMB", "WINDOW"), D("E"), D("N"),
        ("READ", "SIGN"), ("PUT", "DOLLAR"), ("GET", "STRING"),
        ("INFLATE", "BALLOON"), ("TIE", "BALLOON"),
        D("S"), D("W"), ("CLIMB", "LEDGE"),
    ], ("JUMP", "", 5, 43)),
    (5, [
        D("W"), D("S"), ("GET", "NEEDLES"),
        D("N"), D("N"), ("GET", "YARN"),
        D("S"), D("E"), D("E"), D("S"),
        ("PRESS", "BUTTON"), ("KNIT", "CLOTHES"),
        D("N"), D("N"), ("GET", "KEY"),
        D("S"), D("W"), ("OPEN", "DOOR"), ("GO", "DOOR"),
    ], ("CLIMB", "STAIRS", 4, 45)),
    (4, [
        D("N"), ("PRESS", "BUTTON"),
        D("S"), D("S"),
        ("GET", "BOOK"), ("READ", "BOOK"),
        D("N"), D("E"), ("SWIM", ""), D("N"),
        ("GET", "UMBRELLA"), ("OPEN", "UMBRELLA"),
    ], ("JUMP", "", 3, 52)),
    (3, [
        D("N"), ("READ", "GRAFFITI"),
        D("S"), D("E"), D("E"), D("N"),
        ("GET", "FLUID"), ("GET", "SOLUTION"),
        D("S"), ("DRINK", "FLUID"), ("OPEN", "DOOR"), ("GO", "DOOR"),
        ("DRINK", "SOLUTION"),
    ], ("CLIMB", "SLIDE", 2, 58)),
    (2, [
        ("GET", "CUP"), ("GET", "WATER"),
        D("W"), ("POUR", "WATER"), ("CLIMB", "PLANT"),
        D("E"), ("GET", "FLUTE"), ("PLAY", "FLUTE"), ("CLIMB", "ROPE"),
    ], ("CLIMB", "STAIRS", 1, 63)),
    (1, [
        ("GET", "ROPE"), ("GET", "KEY"),
        D("E"), ("GET", "BOOK"), ("READ", "BOOK"),
        ("TIE", "ROPE"), ("THROW", "ROPE"), ("CLIMB", "ROPE"),
        ("OPEN", "DOOR"),
    ], ("GO", "DOOR", "escape", 0)),
]


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def expected_room(floor, room, verb, noun):
    """Where the player must be after one command, per the audit tables.

    Directional moves come from the audited exit table; verb moves come
    from VERB_MOVES; anything else leaves the player where they were.
    """
    verb = verb.upper()
    noun = noun.upper()
    if verb == "GO" and noun in ("N", "S", "E", "W", "U", "D"):
        table = ROOMS[floor]
        if room not in table:
            return None
        return table[room].get("exits", {}).get(noun)
    key = (floor, room, verb, noun)
    if key in VERB_MOVES:
        return VERB_MOVES[key]
    return room


def send(runner, verb, noun):
    """Run one command, swallowing the engine's inventory chatter."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return runner.send(verb, noun)


def run_route(label, sections):
    """Replay one published solution.  Returns a list of failure lines."""
    failures = []
    runner = GameRunner(floor=9)

    if runner.state.location != AUDITED_ARRIVALS[9]:
        failures.append("%s: game starts in room %s, audit says %s"
                        % (label, runner.state.location, AUDITED_ARRIVALS[9]))

    visited_floors = [runner.state.floor]

    for floor, steps, exit_step in sections:
        if runner.state.floor != floor:
            failures.append("%s: expected to be on floor %d, on floor %d"
                            % (label, floor, runner.state.floor))
            return failures

        for verb, noun in steps:
            before = runner.state.location
            text, transitioned, escaped = send(runner, verb, noun)
            where = "%s floor %d: %s %s" % (label, floor, verb, noun)
            if transitioned or escaped:
                failures.append("%s: unexpected transition" % where)
                return failures
            low = text.lower().strip()
            for marker in REFUSALS:
                if low.startswith(marker.lower()):
                    failures.append("%s: refused (%r)" % (where, text))
                    break
            want = expected_room(floor, before, verb, noun)
            if want is None:
                failures.append("%s: room %s is not on floor %d in the audit"
                                % (where, before, floor))
                return failures
            if runner.state.location != want:
                failures.append("%s: player is in room %s, audit says room %s"
                                % (where, runner.state.location, want))
                return failures

        # The floor's exit: the transition itself.
        verb, noun, target, landing = exit_step
        where = "%s floor %d: %s %s" % (label, floor, verb, noun)
        text, transitioned, escaped = send(runner, verb, noun)

        if target == "escape":
            if not escaped:
                failures.append("%s: did not escape the building (%r)"
                                % (where, text))
                return failures
            if not runner.escaped:
                failures.append("%s: runner did not record the escape" % where)
            if "escap" not in text.lower():
                failures.append("%s: escape text reads %r" % (where, text))
            continue

        if not transitioned:
            failures.append("%s: no transition (%r)" % (where, text))
            return failures
        marker = "TRANSITION:floor_%d:%d" % (target, landing)
        if text != marker:
            failures.append("%s: marker is %r, expected %r"
                            % (where, text, marker))
            return failures
        if runner.state.floor != target:
            failures.append("%s: landed on floor %s, expected %s"
                            % (where, runner.state.floor, target))
            return failures
        if runner.state.location != landing:
            failures.append("%s: landed in room %s, expected %s"
                            % (where, runner.state.location, landing))
            return failures
        if runner.state.location != AUDITED_ARRIVALS[target]:
            failures.append("%s: landed in room %s, audit arrival is %s"
                            % (where, runner.state.location,
                               AUDITED_ARRIVALS[target]))
            return failures
        visited_floors.append(runner.state.floor)

    expected_order = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    if visited_floors != expected_order:
        failures.append("%s: visited floors %s, expected %s"
                        % (label, visited_floors, expected_order))

    if not runner.escaped:
        failures.append("%s: the game did not end in an escape" % label)

    return failures


def test_francis_escapes():
    """Garry Francis' published solution escapes the building."""
    failures = run_route("Francis", FRANCIS)
    if failures:
        print("  FAIL Francis:")
        for line in failures:
            print("    " + line)
        return 1
    print("  PASS Francis escapes: floor 9 -> floor 1 -> street")
    return 0


def test_gunness_escapes():
    """Jacob Gunness' published solution escapes the building."""
    failures = run_route("Gunness", GUNNESS)
    if failures:
        print("  FAIL Gunness:")
        for line in failures:
            print("    " + line)
        return 1
    print("  PASS Gunness escapes: floor 9 -> floor 1 -> street")
    return 0


def test_arrival_contract():
    """The audited arrival rooms agree with the audit file."""
    import json

    audit_path = os.path.join(ROOT, "audit", "floors_1_5_verified.json")
    with open(audit_path) as fh:
        audit = json.load(fh)

    failures = []
    for floor in range(1, 6):
        want = audit[str(floor)]["entry"]
        if AUDITED_ARRIVALS[floor] != want:
            failures.append("floor %d arrival %s != audit entry %s"
                            % (floor, AUDITED_ARRIVALS[floor], want))
    if failures:
        print("  FAIL arrival contract:")
        for line in failures:
            print("    " + line)
        return 1
    print("  PASS arrival rooms match the audit (floors 1-5 from the "
          "audit file, 6-9 from the floor audits)")
    return 0


def test_repl_uses_the_same_dispatcher():
    """The REPL and the test drive the same dispatcher, not two copies."""
    with open(os.path.join(ROOT, "kidnapped.py")) as fh:
        source = fh.read()
    failures = []
    if "class GameRunner" not in source:
        failures.append("kidnapped.py has no GameRunner")
    if "runner.send(" not in source:
        failures.append("the REPL does not drive GameRunner.send()")
    if failures:
        print("  FAIL dispatcher sharing:")
        for line in failures:
            print("    " + line)
        return 1
    print("  PASS the REPL and the test share one dispatcher")
    return 0


def main():
    print("=" * 60)
    print("FULL-GAME ESCAPE TEST (real engine, real dispatcher)")
    print("=" * 60)

    failures = 0
    failures += test_arrival_contract()
    failures += test_repl_uses_the_same_dispatcher()
    print()
    failures += test_francis_escapes()
    failures += test_gunness_escapes()

    print()
    print("=" * 60)
    if failures:
        print("ESCAPE TEST: FAIL (%d problem(s))" % failures)
        print("=" * 60)
        return 1
    print("ESCAPE TEST: PASS - both published solutions escape the building")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
