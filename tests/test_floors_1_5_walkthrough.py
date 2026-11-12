#!/usr/bin/env python3
"""
Command-for-command replay of BOTH published solutions through floors 5-1.

This is the proof that the floors 1-5 rewrite is PLAYABLE, not merely
internally consistent.  Every command below is copied from the published
walkthroughs in archive/solutions/ (sol_atari.txt = Garry Francis,
sol_gunness.txt = Jacob Gunness), and the room expected after each
command is taken from the pixel-verified audit table
(audit/floors_1_5_verified.json) - never from the floor modules.

The two solutions take different routes through the same rooms and both
must land on the right object at every step:

  Francis (floor 5): E, S, PRESS BUTTON, N, W, W, S, GET KNITTING
      NEEDLES, N, N, GET BALL OF YARN, KNIT CLOTHES, S, E, E, N, GET
      SMALL KEY, S, W, OPEN DOOR, GO DOOR, GO STAIRS
  Gunness (floor 5): W, S, GET NEEDLES, N, N, GET YARN, S, E, E, S,
      PRESS BUTTON, KNIT CLOTHES, N, N, GET KEY, S, W, OPEN DOOR, GO
      DOOR, CLIMB STAIRS

Run:  python3 tests/test_floors_1_5_walkthrough.py
"""

import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

with open(os.path.join(ROOT, "audit", "floors_1_5_verified.json")) as fh:
    AUDIT = json.load(fh)

# Landing room per floor, straight from the audit table.
ENTRY = {int(f): d["entry"] for f, d in AUDIT.items()}


class State:
    """Minimal GameState stand-in compatible with the floor engines."""

    def __init__(self, location, floor):
        self.location = location
        self.inventory = []
        self.floor = floor
        self.alive = True
        self.game_over = False
        self.dark = False
        self.flashlight_on = False
        self.turns = 0
        self.game_time = "10:00 PM"
        self.power_out = False
        self.elevator_fixed = False

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def make_engine(floor, inventory=()):
    mod = importlib.import_module("floors.floor_%d" % floor)
    cls = getattr(mod, "Floor%dEngine" % floor)
    state = State(ENTRY[floor], floor)
    state.inventory = list(inventory)
    engine = cls(state)
    engine.on_enter()
    state.location = ENTRY[floor]
    return state, engine


def run_route(label, route):
    """Replay one published solution.

    Each step is (verb, noun, expect) where expect is one of:
      ("room", n)        - the player must be in room n afterwards
      ("trans", f, r)    - the command must emit TRANSITION:floor_f:r
      ("escape",)        - the command must end the game
    """
    failures = []
    floor = 5
    state, engine = make_engine(floor)

    for index, (verb, noun, expect) in enumerate(route, start=1):
        message, transition = engine.handle_command(verb, noun)
        kind = expect[0]

        if kind == "room":
            if state.location != expect[1]:
                failures.append(
                    "step %d (%s %s): expected room %d, got %d - %s"
                    % (index, verb, noun, expect[1], state.location, message))
        elif kind == "trans":
            target = "TRANSITION:floor_%d:%d" % (expect[1], expect[2])
            if message != target:
                failures.append(
                    "step %d (%s %s): expected %s, got %r"
                    % (index, verb, noun, target, message))
            elif not transition:
                failures.append(
                    "step %d (%s %s): transition flag not set" % (index, verb, noun))
            else:
                carried = list(state.inventory)
                floor = expect[1]
                state, engine = make_engine(floor, carried)
                state.location = expect[2]
        elif kind == "escape":
            if "escaped" not in message.lower():
                failures.append(
                    "step %d (%s %s): expected the escape, got %r"
                    % (index, verb, noun, message))
            elif not transition:
                failures.append(
                    "step %d (%s %s): escape did not end the game" % (index, verb, noun))

    return failures


# ---------------------------------------------------------------------
# Garry Francis (Atari) solution, floors 5 -> 1.
# ---------------------------------------------------------------------
FRANCIS = [
    # --- floor 5 -------------------------------------------------------
    ("E", "", ("room", 41)),
    ("S", "", ("room", 42)),
    ("PRESS", "BUTTON", ("room", 42)),
    ("N", "", ("room", 41)),
    ("W", "", ("room", 43)),
    ("W", "", ("room", 38)),
    ("S", "", ("room", 40)),
    ("GET", "KNITTING NEEDLES", ("room", 40)),
    ("N", "", ("room", 38)),
    ("N", "", ("room", 39)),
    ("GET", "BALL OF YARN", ("room", 39)),
    ("KNIT", "CLOTHES", ("room", 39)),
    ("S", "", ("room", 38)),
    ("E", "", ("room", 43)),
    ("E", "", ("room", 41)),
    ("N", "", ("room", 37)),
    ("GET", "SMALL KEY", ("room", 37)),
    ("S", "", ("room", 41)),
    ("W", "", ("room", 43)),
    ("OPEN", "DOOR", ("room", 43)),
    ("GO", "DOOR", ("room", 44)),
    ("GO", "STAIRS", ("trans", 4, 45)),
    # --- floor 4 -------------------------------------------------------
    ("N", "", ("room", 46)),
    ("PRESS", "BUTTON", ("room", 46)),
    ("S", "", ("room", 45)),
    ("S", "", ("room", 47)),
    ("GET", "BOOK", ("room", 47)),
    ("READ", "BOOK", ("room", 47)),
    ("N", "", ("room", 45)),
    ("E", "", ("room", 48)),
    ("SWIM", "", ("room", 49)),
    ("N", "", ("room", 50)),
    ("GET", "MARY POPPIN'S UMBRELLA", ("room", 50)),
    ("OPEN", "UMBRELLA", ("room", 50)),
    ("S", "", ("room", 49)),
    ("E", "", ("room", 51)),
    ("JUMP", "", ("trans", 3, 52)),
    # --- floor 3 -------------------------------------------------------
    ("E", "", ("room", 54)),
    ("E", "", ("room", 55)),
    ("N", "", ("room", 56)),
    ("GET", "JAR OF FLUID", ("room", 56)),
    ("DRINK", "FLUID", ("room", 56)),
    ("GET", "VIAL OF YELLOW SOLUTION", ("room", 56)),
    ("S", "", ("room", 55)),
    ("OPEN", "DOOR", ("room", 55)),
    ("DRINK", "SOLUTION", ("room", 55)),
    ("GO", "DOOR", ("room", 57)),
    ("GO", "SLIDE", ("trans", 2, 58)),
    # --- floor 2 -------------------------------------------------------
    ("GET", "PAPER CUP", ("room", 58)),
    ("GET", "WATER", ("room", 58)),
    ("W", "", ("room", 59)),
    ("POUR", "WATER", ("room", 59)),
    ("GO", "PLANT", ("room", 60)),
    ("E", "", ("room", 61)),
    ("GET", "FLUTE", ("room", 61)),
    ("PLAY", "FLUTE", ("room", 61)),
    ("GO", "ROPE", ("room", 62)),
    ("GO", "STAIRS", ("trans", 1, 63)),
    # --- floor 1 -------------------------------------------------------
    ("GET", "KEY", ("room", 63)),
    ("GET", "LONG ROPE", ("room", 63)),
    ("E", "", ("room", 64)),
    ("GET", "BOOK", ("room", 64)),
    ("READ", "BOOK", ("room", 64)),
    ("TIE", "ROPE", ("room", 64)),
    ("THROW", "ROPE", ("room", 64)),
    ("GO", "ROPE", ("room", 65)),
    ("OPEN", "DOOR", ("room", 65)),
    ("GO", "DOOR", ("escape",)),
]

# ---------------------------------------------------------------------
# Jacob Gunness solution, floors 5 -> 1.
# ---------------------------------------------------------------------
GUNNESS = [
    # --- floor 5 -------------------------------------------------------
    ("W", "", ("room", 38)),
    ("S", "", ("room", 40)),
    ("GET", "NEEDLES", ("room", 40)),
    ("N", "", ("room", 38)),
    ("N", "", ("room", 39)),
    ("GET", "YARN", ("room", 39)),
    ("S", "", ("room", 38)),
    ("E", "", ("room", 43)),
    ("E", "", ("room", 41)),
    ("S", "", ("room", 42)),
    ("PRESS", "BUTTON", ("room", 42)),
    ("KNIT", "CLOTHES", ("room", 42)),
    ("N", "", ("room", 41)),
    ("N", "", ("room", 37)),
    ("GET", "KEY", ("room", 37)),
    ("S", "", ("room", 41)),
    ("W", "", ("room", 43)),
    ("OPEN", "DOOR", ("room", 43)),
    ("GO", "DOOR", ("room", 44)),
    ("CLIMB", "STAIRS", ("trans", 4, 45)),
    # --- floor 4 -------------------------------------------------------
    ("N", "", ("room", 46)),
    ("PRESS", "BUTTON", ("room", 46)),
    ("S", "", ("room", 45)),
    ("S", "", ("room", 47)),
    ("GET", "BOOK", ("room", 47)),
    ("READ", "BOOK", ("room", 47)),
    ("N", "", ("room", 45)),
    ("E", "", ("room", 48)),
    ("SWIM", "", ("room", 49)),
    ("N", "", ("room", 50)),
    ("GET", "UMBRELLA", ("room", 50)),
    ("OPEN", "UMBRELLA", ("room", 50)),
    ("JUMP", "", ("trans", 3, 52)),
    # --- floor 3 -------------------------------------------------------
    ("N", "", ("room", 53)),
    ("READ", "GRAFFITI", ("room", 53)),
    ("S", "", ("room", 52)),
    ("E", "", ("room", 54)),
    ("E", "", ("room", 55)),
    ("N", "", ("room", 56)),
    ("GET", "FLUID", ("room", 56)),
    ("GET", "SOLUTION", ("room", 56)),
    ("S", "", ("room", 55)),
    ("DRINK", "FLUID", ("room", 55)),
    ("OPEN", "DOOR", ("room", 55)),
    ("GO", "DOOR", ("room", 57)),
    ("DRINK", "SOLUTION", ("room", 57)),
    ("CLIMB", "SLIDE", ("trans", 2, 58)),
    # --- floor 2 -------------------------------------------------------
    ("GET", "CUP", ("room", 58)),
    ("GET", "WATER", ("room", 58)),
    ("W", "", ("room", 59)),
    ("POUR", "WATER", ("room", 59)),
    ("CLIMB", "PLANT", ("room", 60)),
    ("E", "", ("room", 61)),
    ("GET", "FLUTE", ("room", 61)),
    ("PLAY", "FLUTE", ("room", 61)),
    ("CLIMB", "ROPE", ("room", 62)),
    ("CLIMB", "STAIRS", ("trans", 1, 63)),
    # --- floor 1 -------------------------------------------------------
    ("GET", "ROPE", ("room", 63)),
    ("GET", "KEY", ("room", 63)),
    ("E", "", ("room", 64)),
    ("GET", "BOOK", ("room", 64)),
    ("READ", "BOOK", ("room", 64)),
    ("TIE", "ROPE", ("room", 64)),
    ("THROW", "ROPE", ("room", 64)),
    ("CLIMB", "ROPE", ("room", 65)),
    ("OPEN", "DOOR", ("room", 65)),
    ("GO", "DOOR", ("escape",)),
]


def main():
    failures = []
    for label, route in (("Francis", FRANCIS), ("Gunness", GUNNESS)):
        route_failures = run_route(label, route)
        if route_failures:
            failures.append("%s solution:" % label)
            failures.extend("    " + f for f in route_failures)
        else:
            print("PASS  %s solution replays command for command (floor 5 -> escape)"
                  % label)

    if failures:
        print("\nWALKTHROUGH REPLAY: FAIL")
        for line in failures:
            print(line)
        return 1
    print("\nWALKTHROUGH REPLAY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
