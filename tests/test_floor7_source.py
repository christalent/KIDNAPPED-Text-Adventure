#!/usr/bin/env python3
"""
Floor 7 source-regression tests.

Every expectation in this file comes from the printed BASIC listing
(listing lines 28-35 for the room table, line 2010 for the DATA rows,
lines 900 and 930 for the handlers), not from the previous implementation
of floors/floor_7.py - which was a fabrication that collided with floor 6.

Run:  python3 tests/test_floor7_source.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from floors.floor_7 import Floor7Engine, ROOMS, VERB_LINK_PAIRS, SPECIAL_ROOMS


class SimpleState:
    """Minimal GameState stand-in."""

    def __init__(self, location=18, floor=7):
        self.location = location
        self.inventory = []
        self.floor = floor
        self.alive = True
        self.game_over = False

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh(location=18):
    """Build an engine standing in `location`.

    on_enter() is what puts the player in the arrival room (18), so for
    any other room the location is restored afterwards.
    """
    state = SimpleState(location)
    engine = Floor7Engine(state)
    engine.on_enter()
    state.location = location
    return state, engine


# ======================================================================
# Room table - listing lines 28-35
# ======================================================================
def test_room_set_is_18_to_25():
    assert set(ROOMS) == set(range(18, 26)), sorted(ROOMS)


def test_room_exits_match_source():
    expected = {
        18: {"W": 20, "N": 19, "E": 24, "S": 21},
        19: {"S": 18},
        20: {"E": 18},
        21: {"N": 18, "E": 22},
        22: {"W": 21, "E": 23},
        23: {"W": 22},
        24: {"W": 18},
        25: {"W": 24},
    }
    for rid, exits in expected.items():
        assert ROOMS[rid]["exits"] == exits, (rid, ROOMS[rid]["exits"], exits)


def test_room_names_match_source():
    expected = {
        18: "IN A HALLWAY",
        19: "IN AN OFFICE",
        20: "IN A TOOL CRIB",
        21: "IN A HALLWAY",
        22: "IN AN OFFICE",
        23: "IN A SMALL STORAGE ROOM",
        24: "IN A HALLWAY",
        25: "IN A NARROW STAIRWAY",
    }
    for rid, name in expected.items():
        assert ROOMS[rid]["name"] == name, (rid, ROOMS[rid]["name"], name)


def test_items_match_source_data():
    assert ROOMS[19]["fixed_items"] == ["KEY MAKING MACHINE"]
    assert ROOMS[20]["items"] == ["SUPER GLUE", "WOODEN STAIR STEP"]
    assert ROOMS[23]["items"] == ["THICK COPPER SHEET"]
    assert ROOMS[24]["fixed_items"] == ["LOCKED DOOR"]
    assert ROOMS[25]["fixed_items"] == ["WOODEN STAIRS"]


def test_exits_are_consistent():
    assert Floor7Engine.verify_exits() == [], Floor7Engine.verify_exits()


def test_door_is_a_verb_link_not_an_exit():
    assert (24, 25) in VERB_LINK_PAIRS and (25, 24) in VERB_LINK_PAIRS
    assert "E" not in ROOMS[24]["exits"]
    assert 25 not in ROOMS[24]["exits"].values()


def test_arrival_room_is_18():
    state, engine = fresh()
    assert state.location == 18
    assert state.floor == 7


def test_down_transition_targets_floor_6_room_26():
    assert SPECIAL_ROOMS["floor_6"]["landing_room"] == 26


# ======================================================================
# Handler 900 - MAKE KEY (listing line 900)
# ======================================================================
def test_make_key_requires_the_copper_sheet():
    state, engine = fresh(19)
    result, _ = engine.handle_command("MAKE", "KEY")
    assert "CRUDE KEY" not in state.inventory
    assert "CRUDE KEY" not in engine.room_items[19]
    assert "copper" in result.lower(), result


def test_make_key_creates_crude_key_in_room_19():
    state, engine = fresh(19)
    state.add_item("THICK COPPER SHEET")
    result, _ = engine.handle_command("MAKE", "KEY")
    assert "CRUDE KEY" in engine.room_items[19], result
    result, _ = engine.handle_command("GET", "CRUDE KEY")
    assert "CRUDE KEY" in state.inventory


def test_make_key_only_at_the_machine():
    state, engine = fresh(18)
    state.add_item("THICK COPPER SHEET")
    result, _ = engine.handle_command("MAKE", "KEY")
    assert "CRUDE KEY" not in state.inventory
    assert "machine" in result.lower(), result


# ======================================================================
# The locked door and the stairway
# ======================================================================
def test_locked_door_needs_a_key():
    state, engine = fresh(24)
    result, _ = engine.handle_command("GO", "DOOR")
    assert state.location == 24
    assert "locked" in result.lower(), result
    result, _ = engine.handle_command("OPEN", "DOOR")
    assert "key" in result.lower(), result


def test_crude_key_opens_the_door():
    state, engine = fresh(24)
    state.add_item("CRUDE KEY")
    result, _ = engine.handle_command("OPEN", "DOOR")
    assert engine.door_unlocked
    result, transition = engine.handle_command("GO", "DOOR")
    assert state.location == 25
    assert transition is False


def test_stairs_need_the_step_glued():
    state, engine = fresh(25)
    result, transition = engine.handle_command("GO", "STAIRS")
    assert transition is False
    assert "step" in result.lower(), result


def test_glue_step_needs_glue_and_step():
    state, engine = fresh(25)
    result, _ = engine.handle_command("GLUE", "STEP")
    assert "glue" in result.lower(), result
    state.add_item("SUPER GLUE")
    result, _ = engine.handle_command("GLUE", "STEP")
    assert "step" in result.lower(), result
    state.add_item("WOODEN STAIR STEP")
    result, _ = engine.handle_command("GLUE", "STEP")
    assert result == "STAIR'S FIXED", result
    assert engine.stairs_fixed
    assert "WOODEN STAIR STEP" not in state.inventory


def test_glue_step_only_in_the_stairway():
    state, engine = fresh(20)
    state.add_item("SUPER GLUE")
    state.add_item("WOODEN STAIR STEP")
    result, _ = engine.handle_command("GLUE", "STEP")
    assert not engine.stairs_fixed
    assert "glue" in result.lower(), result


def test_fixed_stairs_descend_to_floor_6():
    state, engine = fresh(25)
    state.add_item("SUPER GLUE")
    state.add_item("WOODEN STAIR STEP")
    engine.handle_command("GLUE", "STEP")
    result, transition = engine.handle_command("GO", "STAIRS")
    assert transition is True
    assert result == "TRANSITION:floor_6:26", result


# ======================================================================
# The published walkthrough route, move for move
# ======================================================================
def test_walkthrough_route_replays():
    state, engine = fresh(18)

    def go(direction):
        result, transition = engine.handle_command(direction, "")
        assert not transition
        return result

    go("S")
    assert state.location == 21
    go("E")
    assert state.location == 22
    go("E")
    assert state.location == 23
    engine.handle_command("GET", "THICK COPPER SHEET")
    go("W")
    go("W")
    go("N")
    go("N")
    assert state.location == 19
    engine.handle_command("MAKE", "KEY")
    engine.handle_command("GET", "CRUDE KEY")
    assert "CRUDE KEY" in state.inventory
    go("S")
    go("W")
    assert state.location == 20
    engine.handle_command("GET", "SUPER GLUE")
    engine.handle_command("GET", "WOODEN STAIR STEP")
    go("E")
    go("E")
    assert state.location == 24
    engine.handle_command("OPEN", "DOOR")
    result, transition = engine.handle_command("GO", "DOOR")
    assert state.location == 25
    engine.handle_command("GLUE", "STEP")
    result, transition = engine.handle_command("GO", "STAIRS")
    assert transition is True
    assert result == "TRANSITION:floor_6:26"


def main():
    tests = [(name, fn) for name, fn in sorted(globals().items())
             if name.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS {0}".format(name))
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print("FAIL {0}: {1}".format(name, exc))
    print("\n{0}/{1} Floor 7 source tests passed".format(len(tests) - failed, len(tests)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
