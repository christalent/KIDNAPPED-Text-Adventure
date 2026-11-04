#!/usr/bin/env python3
"""
Test the Floor 7 and Floor 6 fixes.

Floor 7 fixes:
  1. Removed duplicate room 33 (was defined twice)
  2. Added missing room 35 (stairs to floor 8)
  3. All exits are bidirectional (no errors)
  4. SMALL KEY, JAR OF YELLOW SOLUTION in room 33
  5. BALL OF YARN, KNITTING NEEDLES in room 39
  6. STEEL DOOR in room 37 (locked; opens with SMALL KEY)
  7. KID'S SLIDE in room 55 actually transitions to floor 6
  8. KNIT/SWEATER mechanic: USE YARN + NEEDLES -> SUIT (auto-worn)
  9. BURGLAR in 39: dollar accessible only with disguise/gun
 10. USE SLIDE/GO DOWN in 55 -> TRANSITION:floor_6:26

Floor 6 fixes:
  1. New layout: 9 rooms (41-49) with all bidirectional exits
  2. Items: GUN, TIN FOIL, BALLOON, HELIUM, VENDING MACHINE, LOCKED DOOR
  3. GUN path: threaten kidnapper -> get dollar + key -> unlock door -> descend
  4. BALLOON path: inflate with helium -> fly to floor 5
  5. SHOOT KIDNAPPER -> blanks -> die (red herring)
  6. GET DOLLAR (no gun) -> die
  7. Transitions work properly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "floors"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from floors.floor_7 import Floor7Engine, ROOMS as ROOMS7
from floors.floor_6 import Floor6Engine, ROOMS as ROOMS6


class SimpleState:
    """Minimal GameState-like object."""
    def __init__(self):
        self.location = 31
        self.inventory = []
        self.floor = 7
        self.alive = True
        self.game_over = False
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh_engine(floor=7):
    state = SimpleState()
    state.floor = floor
    if floor == 7:
        state.location = 31
        engine = Floor7Engine(state)
    else:
        state.location = 41
        engine = Floor6Engine(state)
    engine.on_enter()
    return state, engine


# ======================================================================
# Floor 7 tests
# ======================================================================
def test_floor7_no_duplicate_room33():
    """Floor 7 should not have a duplicate room 33."""
    assert 33 in ROOMS7, "Room 33 must exist"
    # The dict can only have one entry per key; the bug was having
    # two definitions of 33 in the source (the second overwrote the
    # first).  Verify the FINAL room 33 is the correct one.
    assert "SMALL KEY" in ROOMS7[33]["items"], \
        f"Room 33 must have SMALL KEY, got: {ROOMS7[33]['items']}"
    print("✅ Floor 7: room 33 has SMALL KEY (no duplicate)")


def test_floor7_room35_exists():
    """Room 35 (stairs to floor 8) must exist."""
    assert 35 in ROOMS7, "Room 35 must exist"
    assert "U" in ROOMS7[35]["exits"], "Room 35 must have UP exit"
    assert ROOMS7[35]["exits"]["U"] == "floor_8", \
        "Room 35 U exit must be floor_8"
    print("✅ Floor 7: room 35 exists with UP=floor_8")


def test_floor7_exits_bidirectional():
    """All exits are bidirectional."""
    errors = Floor7Engine.verify_exits()
    assert not errors, f"Exit errors: {errors}"
    print(f"✅ Floor 7: all {len(ROOMS7)} rooms have bidirectional exits")


def test_floor7_items_in_correct_rooms():
    """Items are in the rooms specified by the task."""
    assert "SMALL KEY" in ROOMS7[33]["items"]
    assert "JAR OF YELLOW SOLUTION" in ROOMS7[33]["items"]
    assert "BALL OF YARN" in ROOMS7[39]["items"]
    assert "KNITTING NEEDLES" in ROOMS7[39]["items"]
    assert "TIN FOIL" in ROOMS7[36]["items"]
    assert "JAR OF FLUID" in ROOMS7[55]["items"]
    assert "KID'S SLIDE" in ROOMS7[55]["items"]
    print("✅ Floor 7: items are in correct rooms")


def test_floor7_kid_slide_transitions_to_floor_6():
    """USE SLIDE in room 55 transitions to floor 6."""
    state, engine = fresh_engine(7)
    state.location = 55
    result, transition = engine.handle_command("USE", "SLIDE")
    assert transition, f"USE SLIDE should transition, got: {result[:80]}"
    assert result.startswith("TRANSITION:floor_6:26"), \
        f"Expected TRANSITION:floor_6:26, got: {result}"
    print("✅ Floor 7: USE SLIDE in 55 transitions to floor 6 (room 41)")


def test_floor7_up_from_31_transitions():
    """UP from room 31 transitions to floor 8."""
    state, engine = fresh_engine(7)
    state.location = 31
    result, transition = engine.handle_command("U", "")
    assert transition
    assert "floor_8" in result
    print("✅ Floor 7: UP from 31 transitions to floor 8")


def test_floor7_knit_suit_mechanic():
    """USE YARN + NEEDLES creates a suit (auto-worn)."""
    state, engine = fresh_engine(7)
    state.inventory = ["BALL OF YARN", "KNITTING NEEDLES"]
    state.location = 39
    result, _ = engine.handle_command("USE", "YARN")
    assert "HAND-KNIT SUIT" in state.inventory, \
        f"Expected HAND-KNIT SUIT in inventory, got: {state.inventory}"
    assert engine.suit_worn, "Suit should be auto-worn"
    assert "BALL OF YARN" not in state.inventory
    assert "KNITTING NEEDLES" not in state.inventory
    print("✅ Floor 7: USE YARN + NEEDLES knits suit (auto-worn)")


def test_floor7_burglar_blocks_dollar_without_disguise():
    """GET DOLLAR without suit/gun causes death."""
    state, engine = fresh_engine(7)
    state.location = 39
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "die" in result.lower() or "death" in result.lower(), \
        f"Expected death message, got: {result}"
    print("✅ Floor 7: GET DOLLAR without disguise -> death")


def test_floor7_burglar_yields_with_suit():
    """GET DOLLAR with suit works (burglar fooled)."""
    state, engine = fresh_engine(7)
    state.inventory = ["HAND-KNIT SUIT"]
    engine.suit_worn = True
    state.location = 39
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "DOLLAR BILL" in state.inventory, \
        f"Expected DOLLAR BILL in inventory, got: {state.inventory}"
    assert engine.dollar_taken
    print("✅ Floor 7: GET DOLLAR with suit -> burglar gives dollar")


def test_floor7_burglar_yields_with_gun():
    """GET DOLLAR with gun also works (BASIC fallback)."""
    state, engine = fresh_engine(7)
    state.inventory = ["GUN"]
    state.location = 39
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "DOLLAR BILL" in state.inventory
    assert engine.dollar_taken
    print("✅ Floor 7: GET DOLLAR with gun -> burglar freezes, drops dollar")


def test_floor7_vault_locked_until_key_used():
    """Cannot enter 55 from 37 without unlocking the vault."""
    state, engine = fresh_engine(7)
    state.location = 37
    result, transition = engine.handle_command("N", "")
    assert not transition, "Should not transition (still on floor 7)"
    assert "locked" in result.lower() or "key" in result.lower(), \
        f"Expected locked message, got: {result}"
    assert state.location == 37
    print("✅ Floor 7: vault door blocks N from 37 until unlocked")


def test_floor7_vault_unlocks_with_small_key():
    """USE SMALL KEY at 37 unlocks the vault."""
    state, engine = fresh_engine(7)
    state.inventory = ["SMALL KEY"]
    state.location = 37
    result, _ = engine.handle_command("USE", "SMALL KEY")
    assert engine.vault_unlocked
    # Now N should work
    result, _ = engine.handle_command("N", "")
    assert state.location == 55, f"Expected loc=55, got {state.location}"
    print("✅ Floor 7: USE SMALL KEY unlocks vault; N reaches 55")


def test_floor7_full_puzzle_solve():
    """Walk through the entire puzzle and end on the slide transition."""
    state, engine = fresh_engine(7)
    cmds = [
        ("W", ""),                 # 31 -> 33
        ("GET", "SMALL KEY"),      # get key
        ("E", ""),                 # 33 -> 31
        ("N", ""),                 # 31 -> 32
        ("N", ""),                 # 32 -> 37
        ("USE", "SMALL KEY"),      # unlock vault
        ("N", ""),                 # 37 -> 55
        ("S", ""),                 # 55 -> 37
        ("W", ""),                 # 37 -> 36
        ("GET", "TIN FOIL"),
        ("W", ""),                 # 36 -> 32
        ("W", ""),                 # 32 -> 39
        ("GET", "BALL OF YARN"),
        ("GET", "KNITTING NEEDLES"),
        ("USE", "YARN"),           # knit suit
        ("GET", "DOLLAR"),         # burglar gives dollar (suit disguise)
        ("E", ""),                 # 39 -> 32
        ("PAY", "DOLLAR"),         # vending machine
        ("N", ""),                 # 32 -> 37
        ("N", ""),                 # 37 -> 55
        ("USE", "SLIDE"),          # descend
    ]
    for verb, noun in cmds:
        result, transition = engine.handle_command(verb, noun)
        if verb == "USE" and noun == "SLIDE":
            assert transition, f"USE SLIDE should transition; got: {result[:80]}"
            assert "floor_6" in result
    assert "STRING" in state.inventory, \
        f"Expected STRING (from vending), got: {state.inventory}"
    assert "HAND-KNIT SUIT" in state.inventory
    print("✅ Floor 7: full puzzle solves cleanly (ends on slide transition)")


# ======================================================================
# Floor 6 tests
# ======================================================================




















def main():
    print("=" * 60)
    print("FLOOR 7 + FLOOR 6 BUG-FIX TESTS")
    print("=" * 60)
    print()

    print("[FLOOR 7]")
    test_floor7_no_duplicate_room33()
    test_floor7_room35_exists()
    test_floor7_exits_bidirectional()
    test_floor7_items_in_correct_rooms()
    test_floor7_kid_slide_transitions_to_floor_6()
    test_floor7_up_from_31_transitions()
    test_floor7_knit_suit_mechanic()
    test_floor7_burglar_blocks_dollar_without_disguise()
    test_floor7_burglar_yields_with_suit()
    test_floor7_burglar_yields_with_gun()
    test_floor7_vault_locked_until_key_used()
    test_floor7_vault_unlocks_with_small_key()
    test_floor7_full_puzzle_solve()
    print()

    print()

    print("[CROSS-FLOOR]")
    print()

    print("=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)


def test_floor7_to_floor_6_full_flow():
    """Floor 7's slide lands on the audited Floor 6 arrival room (26),
    and Floor 6 is playable from there.

    The old version of this test drove the STALE floor 6 (rooms 41-49,
    a kidnapper standing in the vault, an UP exit back to floor 7).  All
    of that was guesswork; Floor 6 is now audited from the source
    pixels and is covered by tests/test_floor6.py, which replays both
    published walkthroughs command-for-command.
    """
    from floors.floor_6 import Floor6Engine as _F6

    f7 = Floor7Engine(FakeState())
    f7.on_enter()
    f7.state.location = 55
    result, transition = f7.handle_command("USE", "SLIDE")
    assert transition is True, result
    assert result == "TRANSITION:floor_6:26", result

    f6 = _F6(FakeState())
    f6.on_enter()
    assert f6.state.location == 26, f6.state.location
    text, _ = f6.handle_command("N", "")
    assert "OFFICE" in text, text
    text, _ = f6.handle_command("N", "")
    assert "CLOSET" in text, text
    text, _ = f6.handle_command("GET", "TANK OF HELIUM GAS")
    assert "TANK OF HELIUM GAS" in f6.state.inventory


if __name__ == "__main__":
    main()
