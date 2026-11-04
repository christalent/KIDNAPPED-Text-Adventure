#!/usr/bin/env python3
"""
Regression tests for the CORRECTED Floor 9.

The old version of this file tested the OLD, WRONG floor 9 (rooms 1-17
with an elevator in room 1, a cabinet in room 1, a D exit from the
elevator to the maintenance room and rooms 13-17 misfiled on floor 9).
Every assertion here pins down one of the corrections the pixel audit
(FLOOR9_AUDIT_2026-11-03.md) forced:

  * no room 9 -> 10 exit (the elevator does not lead to the
    maintenance room; PRESS BUTTON goes down to floor 8)
  * no room 3 -> 4 "U" exit (the closet does not open onto the roof)
  * no room 4 -> 3 "D" exit
  * no room 10 -> 9 "U" exit
  * no room 11 -> 13/15 "E"/"W" exits (the crawlspace belongs to
    floor 9 alone)
  * room 12 ("ON A VERY NARROW LEDGE") does not exist
  * room 1 is a HALLWAY; the elevator is room 9
  * the CABINET is in room 10, the LONG BROOM is in room 3
  * the key must be fished down with the broom
  * the cabinet needs the key
  * the wires are live until 23:00
  * the elevator only moves once it is repaired
  * the crawlspace is reached by CLIMB CHAIR, not by walking

Run:  python3 tests/test_floor9_fixes.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from floors.floor_9 import Floor9Engine, ROOMS

import authoritative_tables


class SimpleState:
    """Minimal GameState-like object compatible with Floor9Engine."""

    def __init__(self, location=1):
        self.location = location
        self.inventory = []
        self.floor = 9
        self.dark = False
        self.flashlight_on = False
        self.turns = 0
        self.game_time = "10:00 PM"
        self.power_out = False
        self.alive = True
        self.game_over = False
        self.elevator_fixed = False

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh_engine(location=1):
    state = SimpleState(location=location)
    engine = Floor9Engine(state)
    engine.on_enter()
    state.location = location
    return state, engine


# ----------------------------------------------------------------------
# 1. The old wrong exits must be gone
# ----------------------------------------------------------------------

def test_no_exit_from_elevator_to_maintenance_room():
    """Room 9 (the elevator) has no D exit to room 10."""
    assert "D" not in ROOMS[9]["exits"], \
        f"Room 9 must not have a D exit, got {ROOMS[9]['exits']}"
    assert ROOMS[9]["exits"].get("D") != 10, \
        "Room 9 must not lead down to the maintenance room (room 10)"
    print("✅ room 9 has no D exit to room 10")


def test_no_wrong_vertical_exits():
    """Room 3 has no U exit, room 4 has no D exit, room 10 has no U exit."""
    assert "U" not in ROOMS[3]["exits"], \
        f"Room 3 (closet) must not have a U exit, got {ROOMS[3]['exits']}"
    assert "D" not in ROOMS[4]["exits"], \
        f"Room 4 must not have a D exit, got {ROOMS[4]['exits']}"
    assert "U" not in ROOMS[10]["exits"], \
        f"Room 10 (maintenance room) must not have a U exit, got {ROOMS[10]['exits']}"
    print("✅ no bogus U/D exits on rooms 3, 4 and 10")


def test_crawlspace_has_no_side_exits():
    """Room 11 (crawlspace) only leads back down to the elevator."""
    exits = ROOMS[11]["exits"]
    assert "E" not in exits, f"Room 11 must not have an E exit, got {exits}"
    assert "W" not in exits, f"Room 11 must not have a W exit, got {exits}"
    assert exits == {"D": 9}, f"Room 11's exits must be exactly D=9, got {exits}"
    print("✅ room 11 has no E/W exits into floor 8")


def test_no_room_12():
    """Room 12 ('ON A VERY NARROW LEDGE') must not exist on floor 9."""
    assert 12 not in ROOMS, "Room 12 must not exist on floor 9"
    assert 12 in authoritative_tables.FLOOR9_FORBIDDEN_ROOMS, \
        "the authoritative table should list 12 as forbidden"
    state, engine = fresh_engine()
    assert engine.get_room(12) is None, \
        "the engine must not be able to return a room 12"
    # and nothing may move the player into it
    for rid, room in ROOMS.items():
        for d, t in room["exits"].items():
            assert t != 12, f"Room {rid} has an exit to the forbidden room 12"
    state.location = 9
    result, _ = engine.handle_command("D", "D")
    assert state.location != 12, "the player must never land in room 12"
    print("✅ room 12 does not exist and cannot be entered")


# ----------------------------------------------------------------------
# 2. The right rooms hold the right things
# ----------------------------------------------------------------------

def test_room_1_is_a_hallway_not_the_elevator():
    """Room 1 is a HALLWAY; the elevator is room 9."""
    assert ROOMS[1]["name"] == "IN A HALLWAY", \
        f"Room 1 must be 'IN A HALLWAY', got {ROOMS[1]['name']!r}"
    assert "ELEVATOR" not in ROOMS[1]["name"].upper(), \
        "Room 1 must not be the elevator"
    assert ROOMS[9]["name"] == "IN AN ELEVATOR", \
        f"Room 9 must be 'IN AN ELEVATOR', got {ROOMS[9]['name']!r}"
    print("✅ room 1 is a hallway, room 9 is the elevator")


def test_cabinet_is_in_room_10():
    """The CABINET lives in the maintenance room (10), not in 1 or 2."""
    assert "CABINET" in ROOMS[10]["items"], \
        f"Room 10 must hold the CABINET, got {ROOMS[10]['items']}"
    assert "CABINET" not in ROOMS[1]["items"], \
        "The CABINET must not be in room 1"
    assert "CABINET" not in ROOMS[2]["items"], \
        "The CABINET must not be in room 2"
    print("✅ the CABINET is in room 10")


def test_broom_is_in_room_3():
    """The LONG BROOM lives in the closet (3), not in room 2."""
    assert "LONG BROOM" in ROOMS[3]["items"], \
        f"Room 3 must hold the LONG BROOM, got {ROOMS[3]['items']}"
    assert "LONG BROOM" not in ROOMS[2]["items"], \
        "The LONG BROOM must not be in room 2"
    print("✅ the LONG BROOM is in room 3")


# ----------------------------------------------------------------------
# 3. The puzzle mechanics
# ----------------------------------------------------------------------

def test_key_needs_the_broom():
    """GET KEY in room 7 is refused without the LONG BROOM."""
    state, engine = fresh_engine(location=7)
    result, _ = engine.handle_command("GET", "KEY")
    assert "KEY ON KEY CHAIN" not in state.inventory, \
        "GET KEY must be refused without the LONG BROOM"
    assert "reach" in result.lower() or "broom" in result.lower(), \
        f"Expected a refusal about reaching the key, got: {result}"
    print("✅ GET KEY refused without the LONG BROOM")

    state, engine = fresh_engine(location=7)
    state.add_item("LONG BROOM")
    result, _ = engine.handle_command("GET", "KEY")
    assert "KEY ON KEY CHAIN" in state.inventory, \
        f"GET KEY should succeed with the broom, got: {result}"
    print("✅ GET KEY succeeds with the LONG BROOM")


def test_cabinet_needs_the_key():
    """OPEN CABINET in room 10 is refused without the key and reveals
    the FLASHLIGHT and TAPE with it."""
    state, engine = fresh_engine(location=10)
    result, _ = engine.handle_command("OPEN", "CABINET")
    assert "FLASHLIGHT" not in result and "TAPE" not in result, \
        f"The cabinet must not open without the key, got: {result}"
    assert "locked" in result.lower() or "key" in result.lower(), \
        f"Expected a 'locked / need a key' message, got: {result}"
    assert not engine.cabinet_open, "the cabinet must stay closed"
    print("✅ OPEN CABINET refused without the key")

    state, engine = fresh_engine(location=10)
    state.add_item("KEY ON KEY CHAIN")
    result, _ = engine.handle_command("OPEN", "CABINET")
    assert engine.cabinet_open, "the cabinet should be open now"
    assert "FLASHLIGHT" in result and "TAPE" in result, \
        f"Opening the cabinet should reveal the FLASHLIGHT and TAPE, got: {result}"
    room10 = engine._room_items.get(10, [])
    assert "FLASHLIGHT" in room10 and "TAPE" in room10, \
        f"The FLASHLIGHT and TAPE should be in room 10, got {room10}"
    print("✅ OPEN CABINET reveals the FLASHLIGHT and TAPE with the key")


def test_wires_are_live_until_23_00():
    """The wires are live before 23:00 and dead afterwards."""
    state, engine = fresh_engine(location=11)
    state.add_item("TAPE")
    assert engine.wires_live, \
        f"wires should be live at {engine._current_time_str()}"
    result, _ = engine.handle_command("TAPE", "WIRES")
    assert not engine.elevator_fixed, \
        "taping live wires must not fix the elevator"
    assert "live" in result.lower(), \
        f"Expected a 'the wires are live' refusal, got: {result}"
    print(f"✅ TAPE WIRES refused while the wires are live "
          f"({engine._current_time_str()})")

    turns = 0
    while engine.wires_live and turns < 30:
        engine.handle_command("WAIT", "")
        turns += 1
    assert not engine.wires_live, \
        f"wires should be dead by now ({engine._current_time_str()})"
    print(f"✅ wires dead at {engine._current_time_str()} after {turns} waits")

    result, _ = engine.handle_command("TAPE", "WIRES")
    assert engine.elevator_fixed, \
        f"TAPE WIRES should repair the elevator, got: {result}"
    assert state.elevator_fixed, "state.elevator_fixed was not set"
    print("✅ TAPE WIRES succeeds after 23:00")


def test_button_only_works_after_the_repair():
    """PRESS BUTTON in room 9 is refused until the elevator is repaired."""
    state, engine = fresh_engine(location=9)
    result, transition = engine.handle_command("PRESS", "BUTTON")
    assert not transition, "PRESS BUTTON must not transition a dead elevator"
    assert "dead" in result.lower() or "repair" in result.lower() \
        or "fix" in result.lower(), \
        f"Expected a 'dead elevator' message, got: {result}"
    print("✅ PRESS BUTTON refused before the repair")

    # repair it the honest way: tape the wires once they are dead
    state, engine = fresh_engine(location=9)
    state.add_item("TAPE")
    state.add_item("CHAIR")
    engine.state.location = 11
    turns = 0
    while engine.wires_live and turns < 30:
        engine.handle_command("WAIT", "")
        turns += 1
    engine.handle_command("TAPE", "WIRES")
    assert engine.elevator_fixed, "the elevator should be repaired by now"
    engine.state.location = 9

    result, transition = engine.handle_command("PRESS", "BUTTON")
    assert transition, "PRESS BUTTON must transition once the elevator is fixed"
    assert result == "TRANSITION:floor_8:13", \
        f"unexpected transition marker: {result!r}"
    print("✅ PRESS BUTTON descends to floor 8 room 13 after the repair")


def test_climb_chair_needs_a_chair():
    """CLIMB CHAIR in room 9 is refused without a chair."""
    state, engine = fresh_engine(location=9)
    result, _ = engine.handle_command("CLIMB", "CHAIR")
    assert state.location == 9, \
        f"CLIMB CHAIR without a chair must not move the player, got {state.location}"
    assert "chair" in result.lower() or "reach" in result.lower(), \
        f"Expected a 'need a chair' message, got: {result}"
    print("✅ CLIMB CHAIR refused without a chair")

    # carried chair
    state, engine = fresh_engine(location=9)
    state.add_item("CHAIR")
    result, _ = engine.handle_command("CLIMB", "CHAIR")
    assert state.location == 11, \
        f"CLIMB CHAIR with a carried chair must reach room 11, got {state.location}"
    print("✅ CLIMB CHAIR with a carried chair reaches room 11")

    # chair dropped in the elevator
    state, engine = fresh_engine(location=9)
    state.add_item("CHAIR")
    engine.handle_command("DROP", "CHAIR")
    assert "CHAIR" in engine._room_items.get(9, []), \
        "the chair should be on the floor of room 9"
    result, _ = engine.handle_command("CLIMB", "CHAIR")
    assert state.location == 11, \
        f"CLIMB CHAIR with a dropped chair must reach room 11, got {state.location}"
    print("✅ CLIMB CHAIR with a dropped chair reaches room 11")


def test_verify_exits_pass():
    """The module's own bidirectional-exit check passes."""
    errors = Floor9Engine.verify_exits()
    assert not errors, f"Exit verification failed: {errors}"
    print("✅ all exits are bidirectionally consistent (verb link excepted)")


# ----------------------------------------------------------------------
# Main entry
# ----------------------------------------------------------------------

TESTS = [
    ("No elevator -> maintenance room exit", test_no_exit_from_elevator_to_maintenance_room),
    ("No bogus vertical exits", test_no_wrong_vertical_exits),
    ("Crawlspace has no side exits", test_crawlspace_has_no_side_exits),
    ("Room 12 does not exist", test_no_room_12),
    ("Room 1 is a hallway, not the elevator", test_room_1_is_a_hallway_not_the_elevator),
    ("CABINET is in room 10", test_cabinet_is_in_room_10),
    ("LONG BROOM is in room 3", test_broom_is_in_room_3),
    ("GET KEY needs the broom", test_key_needs_the_broom),
    ("OPEN CABINET needs the key", test_cabinet_needs_the_key),
    ("Wires live until 23:00", test_wires_are_live_until_23_00),
    ("PRESS BUTTON after the repair", test_button_only_works_after_the_repair),
    ("CLIMB CHAIR needs a chair", test_climb_chair_needs_a_chair),
    ("verify_exits", test_verify_exits_pass),
]


def main():
    print("=" * 60)
    print("FLOOR 9 CORRECTION REGRESSION TESTS")
    print("=" * 60)
    print()

    failures = []
    for name, fn in TESTS:
        try:
            fn()
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failures.append(name)
        except Exception as e:  # noqa: BLE001
            print(f"❌ {name}: unexpected {type(e).__name__}: {e}")
            failures.append(name)

    print()
    print("=" * 60)
    if failures:
        print(f"❌ {len(failures)} of {len(TESTS)} checks FAILED: {failures}")
        print("=" * 60)
        return 1
    print(f"✅ All {len(TESTS)} floor 9 correction checks passed")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
