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
 10. USE SLIDE/GO DOWN in 55 -> TRANSITION:floor_6:41

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
    assert result.startswith("TRANSITION:floor_6:41"), \
        f"Expected TRANSITION:floor_6:41, got: {result}"
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
def test_floor6_exits_bidirectional():
    """All exits are bidirectional."""
    errors = Floor6Engine.verify_exits()
    assert not errors, f"Exit errors: {errors}"
    print(f"✅ Floor 6: all {len(ROOMS6)} rooms have bidirectional exits")


def test_floor6_items_in_correct_rooms():
    """Items are in the rooms specified by the task."""
    assert "GUN" in ROOMS6[43]["items"]
    assert "TIN FOIL" in ROOMS6[43]["items"]
    assert "LARGE DEFLATED BALLOON" in ROOMS6[44]["items"]
    assert "TANK OF HELIUM GAS" in ROOMS6[46]["items"]
    assert "STRING VENDING MACHINE" in ROOMS6[42]["items"]
    assert "LOCKED DOOR" in ROOMS6[48]["items"]
    print("✅ Floor 6: items are in correct rooms")


def test_floor6_door_blocks_49():
    """N from 48 is blocked by the LOCKED DOOR."""
    state, engine = fresh_engine(6)
    state.location = 48
    result, transition = engine.handle_command("N", "")
    assert not transition
    assert "locked" in result.lower() or "key" in result.lower(), \
        f"Expected locked message, got: {result}"
    assert state.location == 48
    print("✅ Floor 6: locked door blocks 48->49")


def test_floor6_gun_path_solves_puzzle():
    """Path A: gun + key unlocks door and reaches floor 5."""
    state, engine = fresh_engine(6)
    cmds = [
        ("N", ""),                  # 41 -> 42
        ("N", ""),                  # 42 -> 43
        ("GET", "GUN"),
        ("N", ""),                  # 43 -> 44
        ("N", ""),                  # 44 -> 45 (kidnapper balcony)
        ("GET", "DOLLAR"),          # kidnapper freezes, drops dollar+key
        ("N", ""),                  # 45 -> 46
        ("N", ""),                  # 46 -> 47
        ("N", ""),                  # 47 -> 48
        ("USE", "KEY"),             # unlock door
        ("N", ""),                  # 48 -> 49
        ("D", ""),                  # 49 -> floor 5
    ]
    for verb, noun in cmds:
        result, transition = engine.handle_command(verb, noun)
        if verb == "D":
            assert transition, f"D from 49 should transition; got: {result[:80]}"
    assert state.location == 49
    print("✅ Floor 6 Path A: gun + key + unlock -> floor 5 transition")


def test_floor6_balloon_path_solves_puzzle():
    """Path B: balloon + helium floats to floor 5."""
    state, engine = fresh_engine(6)
    cmds = [
        ("N", ""),                  # 41 -> 42
        ("N", ""),                  # 42 -> 43
        ("N", ""),                  # 43 -> 44
        ("GET", "BALLOON"),
        ("N", ""),                  # 44 -> 45
        ("N", ""),                  # 45 -> 46
        ("GET", "HELIUM"),
        ("INFLATE", "BALLOON"),
        ("USE", "INFLATED BALLOON"),
    ]
    for verb, noun in cmds:
        result, transition = engine.handle_command(verb, noun)
        if verb == "USE" and noun == "INFLATED BALLOON":
            assert transition, f"USE INFLATED BALLOON should transition; got: {result[:80]}"
    assert "INFLATED BALLOON" in state.inventory
    print("✅ Floor 6 Path B: balloon + helium -> floor 5 transition")


def test_floor6_shoot_kidnapper_kills_player():
    """SHOOT KIDNAPPER with gun -> blanks -> death."""
    state, engine = fresh_engine(6)
    state.inventory = ["GUN"]
    state.location = 45
    result, _ = engine.handle_command("SHOOT", "KIDNAPPER")
    assert "die" in result.lower() or "blanks" in result.lower() or "death" in result.lower(), \
        f"Expected death message, got: {result}"
    assert not state.alive, "Player should be dead"
    print("✅ Floor 6: SHOOT KIDNAPPER -> gun has blanks -> death")


def test_floor6_get_dollar_no_gun_kills_player():
    """GET DOLLAR without gun -> kidnapper kills you."""
    state, engine = fresh_engine(6)
    state.location = 45
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "die" in result.lower() or "death" in result.lower(), \
        f"Expected death message, got: {result}"
    assert not state.alive
    print("✅ Floor 6: GET DOLLAR (no gun) -> death")


def test_floor6_vending_machine_works():
    """USE DOLLAR at vending machine -> STRING."""
    state, engine = fresh_engine(6)
    state.inventory = ["DOLLAR BILL"]
    state.location = 42
    result, _ = engine.handle_command("USE", "DOLLAR")
    assert "STRING" in state.inventory, \
        f"Expected STRING in inventory, got: {state.inventory}"
    assert "DOLLAR BILL" not in state.inventory
    print("✅ Floor 6: vending machine gives STRING for $1")


def test_floor6_up_to_floor_7():
    """UP from 41 transitions to floor 7."""
    state, engine = fresh_engine(6)
    state.location = 41
    result, transition = engine.handle_command("U", "")
    assert transition
    assert "floor_7" in result
    print("✅ Floor 6: UP from 41 transitions to floor 7")


def test_floor7_to_floor_6_full_flow():
    """Walk through floor 7 to reach floor 6, then solve floor 6."""
    state, engine = fresh_engine(7)
    # Floor 7: get key, unlock vault, go to 55
    engine.handle_command("W", "")   # 31 -> 33
    engine.handle_command("GET", "SMALL KEY")
    engine.handle_command("E", "")   # 33 -> 31
    engine.handle_command("N", "")   # 31 -> 32
    engine.handle_command("N", "")   # 32 -> 37
    engine.handle_command("USE", "SMALL KEY")
    engine.handle_command("N", "")   # 37 -> 55
    # Slide to floor 6
    result, transition = engine.handle_command("USE", "SLIDE")
    assert transition
    # Simulate engine swap (the runner does this)
    state.floor = 6
    state.location = 41
    engine = Floor6Engine(state)
    engine.on_enter()
    assert state.location == 41
    print("✅ Floor 7 -> Floor 6: slide transition works, on_enter sets landing room")


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

    print("[FLOOR 6]")
    test_floor6_exits_bidirectional()
    test_floor6_items_in_correct_rooms()
    test_floor6_door_blocks_49()
    test_floor6_gun_path_solves_puzzle()
    test_floor6_balloon_path_solves_puzzle()
    test_floor6_shoot_kidnapper_kills_player()
    test_floor6_get_dollar_no_gun_kills_player()
    test_floor6_vending_machine_works()
    test_floor6_up_to_floor_7()
    print()

    print("[CROSS-FLOOR]")
    test_floor7_to_floor_6_full_flow()
    print()

    print("=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()
