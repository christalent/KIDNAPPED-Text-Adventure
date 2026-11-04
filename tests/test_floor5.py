#!/usr/bin/env python3
"""
Tests for KIDNAPPED! Floor 5 (Mary Poppins / weird floor).

Floor 5 fixes:
  1. All 9 rooms (51-59) load and have bidirectional exits.
  2. Entry: room 51 U -> floor_6:26
  3. Exit:  room 59 D -> floor_4:61
  4. SIGN ON WALL is fixed (cannot be taken).
  5. GRAFFITI ON WALL is fixed.
  6. PUSH BUTTON is fixed; pressing it ONCE dispenses a REVERSIBLE PIE
     into the player's inventory.
  7. JUMP PLATFORM is fixed.
  8. SUPER CALIFRAGILISTIC MACHINE is fixed.
  9. PUSH BUTTON is one-time (no pie on the second press).
 10. The REVERSIBLE PIE, used in room 57, REVERSES the machine and
     disables the magical barrier blocking the umbrella vault.
 11. N from 58 to 59 is blocked until machine_activated.
 12. JUMP at the platform in 58 with machine_activated=True moves
     the player into the umbrella vault (room 59).
 13. The MAGIC UMBRELLA in 59 can be GET'd and triggers a flag.
 14. D from 59 transitions to floor_4:61 (the landing room on floor 4).
 15. EXAMINE works for SIGN, PIE, MACHINE, GRAFFITI, JUMP PLATFORM.

End-to-end reference run: see ``run_reference``.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "floors"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from floors.floor_5 import Floor5Engine, ROOMS, FIXED_ITEMS, FLOOR_NUMBER, NEXT_FLOOR_DOWN


class SimpleState:
    """Minimal GameState-like object compatible with Floor5Engine."""
    def __init__(self, location=51, floor=5):
        self.location = location
        self.inventory = []
        self.floor = floor
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh_engine(location=51):
    state = SimpleState(location=location)
    engine = Floor5Engine(state)
    engine.on_enter()
    # on_enter() resets the location to the floor's landing room (51).
    # Override the location for tests that need a non-landing starting point.
    state.location = location
    return state, engine


# ----------------------------------------------------------------------
# Module-level sanity
# ----------------------------------------------------------------------
def test_module_loads():
    """Floor 5 module imports cleanly."""
    import floors.floor_5 as f5
    assert f5.FLOOR_NUMBER == 5
    assert f5.NEXT_FLOOR_DOWN == 4
    assert len(f5.ROOMS) == 9
    print("✅ Floor 5 module loads; FLOOR_NUMBER=5, NEXT_FLOOR_DOWN=4, 9 rooms")


def test_room_numbers():
    """Floor 5 should have rooms 51 through 59."""
    assert sorted(ROOMS.keys()) == [51, 52, 53, 54, 55, 56, 57, 58, 59], \
        f"Expected rooms 51-59, got: {sorted(ROOMS.keys())}"
    print("✅ Floor 5 has rooms 51-59 (no duplicates, no gaps)")


def test_rooms_have_names_and_descs():
    """Every room has a name and a non-empty description."""
    for rid, r in ROOMS.items():
        assert "name" in r and r["name"], f"Room {rid} missing name"
        assert "desc" in r and r["desc"], f"Room {rid} missing desc"
        assert "exits" in r, f"Room {rid} missing exits"
    print("✅ All rooms have name, desc, exits")


# ----------------------------------------------------------------------
# Exits / transitions
# ----------------------------------------------------------------------
def test_exits_bidirectional():
    """All numeric exits are bidirectional (verify_exits passes)."""
    errors = Floor5Engine.verify_exits()
    assert not errors, f"Bidirectional exit errors: {errors}"
    print(f"✅ All {len(ROOMS)} rooms have bidirectional numeric exits")


def test_entry_51_up_to_floor6():
    """Room 51 U exit should transition to floor_6 landing room 26."""
    r51 = ROOMS[51]
    assert "U" in r51["exits"], "Room 51 missing U exit"
    assert r51["exits"]["U"] == "floor_6", \
        f"Room 51 U must be 'floor_6', got {r51['exits']['U']}"
    print("✅ Room 51 U exit = floor_6")


def test_entry_51_up_actually_transitions():
    """U from 51 returns TRANSITION:floor_6:26 with transition=True."""
    state, engine = fresh_engine(location=51)
    result, transition = engine.handle_command("U", "")
    assert transition, "U from 51 should set transition=True"
    assert result == "TRANSITION:floor_6:26", \
        f"Expected TRANSITION:floor_6:26, got {result}"
    print("✅ U from 51 emits TRANSITION:floor_6:26 with transition=True")


def test_exit_59_down_to_floor4():
    """Room 59 D exit should transition to floor_4 landing room 61."""
    r59 = ROOMS[59]
    assert "D" in r59["exits"], "Room 59 missing D exit"
    assert r59["exits"]["D"] == "floor_4", \
        f"Room 59 D must be 'floor_4', got {r59['exits']['D']}"
    print("✅ Room 59 D exit = floor_4")


def test_exit_59_down_actually_transitions():
    """D from 59 returns TRANSITION:floor_4:61 with transition=True."""
    state, engine = fresh_engine(location=59)
    result, transition = engine.handle_command("D", "")
    assert transition, "D from 59 should set transition=True"
    assert result == "TRANSITION:floor_4:61", \
        f"Expected TRANSITION:floor_4:61, got {result}"
    print("✅ D from 59 emits TRANSITION:floor_4:61 with transition=True")


def test_walk_full_path_51_to_59():
    """Walking N/E/E/E/E/N/JUMP reaches 59 (puzzle path)."""
    state, engine = fresh_engine(location=51)
    # Walk to jump chamber
    engine.handle_command("N", "")  # 52
    assert state.location == 52
    engine.handle_command("E", "")  # 54
    assert state.location == 54
    engine.handle_command("N", "")  # 56
    assert state.location == 56
    engine.handle_command("E", "")  # 57
    assert state.location == 57
    engine.handle_command("N", "")  # 58
    assert state.location == 58
    # Activate machine by giving it the pie (skip pie step in this test)
    engine.machine_activated = True
    # JUMP should move us to 59
    engine.handle_command("JUMP", "")
    assert state.location == 59, f"Expected 59, got {state.location}"
    print("✅ Walking 51→52→54→56→57→58→JUMP reaches 59")


# ----------------------------------------------------------------------
# Items in correct rooms
# ----------------------------------------------------------------------
def test_items_in_correct_rooms():
    """Items are in the rooms specified by the task."""
    assert "SMALL UMBRELLA" in ROOMS[55]["items"], "Room 55 must have SMALL UMBRELLA"
    assert "MAGIC UMBRELLA" in ROOMS[59]["items"], "Room 59 must have MAGIC UMBRELLA"
    assert "PUSH BUTTON" in ROOMS[56]["items"], "Room 56 must have PUSH BUTTON"
    assert "JUMP PLATFORM" in ROOMS[58]["items"], "Room 58 must have JUMP PLATFORM"
    assert "SIGN ON WALL" in ROOMS[52]["items"], "Room 52 must have SIGN"
    assert "GRAFFITI ON WALL" in ROOMS[53]["items"], "Room 53 must have GRAFFITI"
    assert "SUPER CALIFRAGILISTIC MACHINE" in ROOMS[57]["items"], \
        "Room 57 must have the machine"
    print("✅ Items present in correct rooms (SIGN, GRAFFITI, UMBRELLAs, BUTTON, PLATFORM, MACHINE)")


# ----------------------------------------------------------------------
# Fixed items cannot be taken
# ----------------------------------------------------------------------
def test_fixed_items_cannot_be_taken():
    """SIGN, GRAFFITI, PUSH BUTTON, JUMP PLATFORM, MACHINE are scenery."""
    state, engine = fresh_engine(location=52)
    result, _ = engine.handle_command("GET", "SIGN")
    assert "can't take" in result.lower(), f"Expected 'can't take' for SIGN, got: {result}"

    state, engine = fresh_engine(location=53)
    result, _ = engine.handle_command("GET", "GRAFFITI")
    assert "can't take" in result.lower(), f"Expected 'can't take' for GRAFFITI, got: {result}"

    state, engine = fresh_engine(location=56)
    result, _ = engine.handle_command("GET", "BUTTON")
    assert "can't take" in result.lower(), f"Expected 'can't take' for BUTTON, got: {result}"

    state, engine = fresh_engine(location=58)
    result, _ = engine.handle_command("GET", "PLATFORM")
    assert "can't take" in result.lower(), f"Expected 'can't take' for PLATFORM, got: {result}"

    state, engine = fresh_engine(location=57)
    result, _ = engine.handle_command("GET", "MACHINE")
    assert "can't take" in result.lower(), f"Expected 'can't take' for MACHINE, got: {result}"
    print("✅ All fixed items (SIGN, GRAFFITI, BUTTON, PLATFORM, MACHINE) cannot be taken")


def test_takeable_items_can_be_taken():
    """SMALL UMBRELLA and MAGIC UMBRELLA are takeable."""
    state, engine = fresh_engine(location=55)
    result, _ = engine.handle_command("GET", "UMBRELLA")
    assert "SMALL UMBRELLA" in state.inventory, f"Expected SMALL UMBRELLA, got: {state.inventory}, {result}"
    assert "take" in result.lower()

    state, engine = fresh_engine(location=59)
    engine.machine_activated = True  # N/JUMP works
    result, _ = engine.handle_command("GET", "UMBRELLA")
    assert "MAGIC UMBRELLA" in state.inventory, f"Expected MAGIC UMBRELLA, got: {state.inventory}, {result}"
    assert engine.umbrella_found
    print("✅ SMALL UMBRELLA (55) and MAGIC UMBRELLA (59) are takeable")


# ----------------------------------------------------------------------
# PUSH BUTTON (pie dispenser)
# ----------------------------------------------------------------------
def test_push_button_dispenses_pie():
    """Pressing PUSH BUTTON adds REVERSIBLE PIE to inventory."""
    state, engine = fresh_engine(location=56)
    assert "REVERSIBLE PIE" not in state.inventory
    result, _ = engine.handle_command("PUSH", "BUTTON")
    assert "REVERSIBLE PIE" in state.inventory, \
        f"Expected REVERSIBLE PIE in inventory, got: {state.inventory}"
    assert engine.pie_taken
    print("✅ PUSH BUTTON adds REVERSIBLE PIE to inventory")


def test_push_button_one_time():
    """PUSH BUTTON can only be pressed once (no second pie)."""
    state, engine = fresh_engine(location=56)
    engine.handle_command("PUSH", "BUTTON")
    assert "REVERSIBLE PIE" in state.inventory
    inv_len = len(state.inventory)
    result, _ = engine.handle_command("PUSH", "BUTTON")
    assert len(state.inventory) == inv_len, \
        f"Inventory should not grow on second press, got: {state.inventory}"
    assert "closed" in result.lower() or "nothing" in result.lower(), \
        f"Expected 'closed' or 'nothing' on second press, got: {result}"
    print("✅ PUSH BUTTON is one-time (no second pie)")


# ----------------------------------------------------------------------
# Puzzle: pie → machine → umbrella vault
# ----------------------------------------------------------------------
def test_use_pie_elsewhere_fails():
    """Using the pie outside room 57 does nothing."""
    state, engine = fresh_engine(location=58)
    state.add_item("REVERSIBLE PIE")
    result, _ = engine.handle_command("USE", "PIE")
    assert not engine.machine_activated, "Machine should NOT be activated outside 57"
    assert "REVERSIBLE PIE" in state.inventory, "Pie should NOT be consumed outside 57"
    print("✅ USE PIE outside room 57 is a no-op (pie retained)")


def test_use_pie_in_57_activates_machine():
    """Using the pie in room 57 activates the machine (consumes the pie)."""
    state, engine = fresh_engine(location=57)
    state.add_item("REVERSIBLE PIE")
    result, _ = engine.handle_command("USE", "PIE")
    assert engine.machine_activated, "Machine should be activated after USE PIE in 57"
    assert "REVERSIBLE PIE" not in state.inventory, "Pie should be consumed"
    assert engine.pie_used, "pie_used flag should be set"
    print("✅ USE PIE in 57 activates machine (consumes pie)")


def test_n_58_blocked_without_machine():
    """N from 58 is blocked by the magical barrier until machine activated."""
    state, engine = fresh_engine(location=58)
    result, _ = engine.handle_command("N", "")
    assert state.location == 58, f"Should still be in 58, got {state.location}"
    assert "barrier" in result.lower(), f"Expected barrier message, got: {result}"
    print("✅ N from 58 blocked without machine activation")


def test_n_58_unlocked_with_machine():
    """N from 58 works once the machine is activated."""
    state, engine = fresh_engine(location=58)
    engine.machine_activated = True
    result, _ = engine.handle_command("N", "")
    assert state.location == 59, f"Expected 59, got {state.location}"
    print("✅ N from 58 works with machine activated")


def test_jump_58_fails_without_machine():
    """JUMP at 58 is flavor text only without the machine."""
    state, engine = fresh_engine(location=58)
    result, _ = engine.handle_command("JUMP", "")
    assert state.location == 58, f"Should still be in 58, got {state.location}"
    assert "barrier" in result.lower(), f"Expected barrier mention, got: {result}"
    print("✅ JUMP at 58 without machine: flavor text, no movement")


def test_jump_58_succeeds_with_machine():
    """JUMP at 58 with machine activated launches player into 59."""
    state, engine = fresh_engine(location=58)
    engine.machine_activated = True
    result, _ = engine.handle_command("JUMP", "")
    assert state.location == 59, f"Expected 59, got {state.location}"
    assert "UMBRELLA" in result.upper(), f"Expected umbrella mention, got: {result[:80]}"
    print("✅ JUMP at 58 with machine activated launches to 59")


def test_jump_other_rooms_fails():
    """JUMP only works in room 58 (the jump chamber)."""
    for loc in (51, 52, 53, 54, 55, 56, 57, 59):
        state, engine = fresh_engine(location=loc)
        result, _ = engine.handle_command("JUMP", "")
        assert state.location == loc, \
            f"JUMP from {loc} should not move player, but went to {state.location}"
    print("✅ JUMP only works in room 58")


# ----------------------------------------------------------------------
# EXAMINE
# ----------------------------------------------------------------------
def test_examine_sign():
    """EXAMINE SIGN in 52 mentions 'MOST REVERSIBLE' as a hint."""
    state, engine = fresh_engine(location=52)
    result, _ = engine.handle_command("EXAMINE", "SIGN")
    assert "MOST REVERSIBLE" in result.upper() or "REVERSIBLE" in result.upper(), \
        f"Expected REVERSIBLE hint, got: {result}"
    print("✅ EXAMINE SIGN gives REVERSIBLE hint")


def test_examine_pie_in_inventory():
    """EXAMINE PIE in inventory shows the label."""
    state, engine = fresh_engine(location=58)
    state.add_item("REVERSIBLE PIE")
    result, _ = engine.handle_command("EXAMINE", "PIE")
    assert "REVERSIBLE PIE" in result.upper() or "reversing" in result.lower(), \
        f"Expected pie description, got: {result}"
    print("✅ EXAMINE PIE in inventory shows label")


def test_examine_machine():
    """EXAMINE MACHINE in 57 hints at the pie."""
    state, engine = fresh_engine(location=57)
    result, _ = engine.handle_command("EXAMINE", "MACHINE")
    assert "SUPER CALIFRAGILISTIC" in result.upper(), \
        f"Expected machine description, got: {result}"
    print("✅ EXAMINE MACHINE gives machine description")


# ----------------------------------------------------------------------
# on_enter resets state
# ----------------------------------------------------------------------
def test_on_enter_resets_state():
    """Calling on_enter() resets all puzzle flags and location.

    Inventory is intentionally NOT cleared - items carry across floors
    so the player can use acquired items later (e.g. MAGIC UMBRELLA on
    floor 4).
    """
    state, engine = fresh_engine(location=59)
    state.add_item("REVERSIBLE PIE")
    engine.machine_activated = True
    engine.pie_taken = True
    engine.pie_used = True
    engine.umbrella_found = True
    # Manually corrupt the location
    state.location = 99
    engine.on_enter()
    assert state.location == 51, f"on_enter should reset location to 51, got {state.location}"
    assert not engine.machine_activated
    assert not engine.pie_taken
    assert not engine.pie_used
    assert not engine.umbrella_found
    # Inventory should carry across floors (intentional design)
    assert "REVERSIBLE PIE" in state.inventory, \
        f"Inventory should be preserved across floors, got: {state.inventory}"
    print("✅ on_enter() resets location and puzzle flags; inventory persists")


# ----------------------------------------------------------------------
# Reference run: complete the puzzle
# ----------------------------------------------------------------------
REFERENCE_COMMANDS = [
    "look",
    "n",
    "examine sign",
    "e",
    "n",
    "push button",
    "e",
    "use pie",
    "n",
    "jump",
    "get umbrella",
    "d",
]


def run_reference(state, engine, verbose=True):
    """Run the reference puzzle-solving command sequence."""
    log = []
    for cmd in REFERENCE_COMMANDS:
        parts = cmd.upper().split()
        verb = parts[0]
        noun = " ".join(parts[1:]) if len(parts) > 1 else ""
        # Direction shortcut normalization (matches kidnapped.py)
        if verb in ("N", "S", "E", "W", "U", "D"):
            noun = verb
            verb = "GO"
        result, transition = engine.handle_command(verb, noun)
        log.append((cmd, result, transition))
        if verbose:
            print(f"> {cmd}")
            print(f"  -> {result[:90]}{'...' if len(result)>90 else ''}")
            if transition:
                print(f"  [TRANSITION! -> {result}]")
            print()
    return log


def test_reference_full_puzzle():
    """Full end-to-end puzzle run reaches 59 with MAGIC UMBRELLA and transitions to floor 4."""
    state, engine = fresh_engine(location=51)
    log = run_reference(state, engine, verbose=False)
    # Final state checks
    assert "MAGIC UMBRELLA" in state.inventory, \
        f"Final inventory should contain MAGIC UMBRELLA, got: {state.inventory}"
    assert engine.umbrella_found, "umbrella_found flag should be set"
    # The last command ('d') should have triggered a transition to floor_4
    last_cmd, last_result, last_transition = log[-1]
    assert last_cmd == "d"
    assert last_transition, f"D from 59 should transition, got result={last_result}"
    assert "floor_4" in last_result
    assert ":61" in last_result
    print("✅ Full reference puzzle run: reaches 59, gets MAGIC UMBRELLA, transitions to floor_4:61")


# ----------------------------------------------------------------------
# Main entry
# ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print("FLOOR 5 PUZZLE / BUG-FIX TESTS")
    print("=" * 60)
    print()

    print("[Module]")
    test_module_loads()
    test_room_numbers()
    test_rooms_have_names_and_descs()
    print()

    print("[Exits & transitions]")
    test_exits_bidirectional()
    test_entry_51_up_to_floor6()
    test_entry_51_up_actually_transitions()
    test_exit_59_down_to_floor4()
    test_exit_59_down_actually_transitions()
    test_walk_full_path_51_to_59()
    print()

    print("[Items & room placement]")
    test_items_in_correct_rooms()
    test_fixed_items_cannot_be_taken()
    test_takeable_items_can_be_taken()
    print()

    print("[PUSH BUTTON]")
    test_push_button_dispenses_pie()
    test_push_button_one_time()
    print()

    print("[Puzzle mechanics]")
    test_use_pie_elsewhere_fails()
    test_use_pie_in_57_activates_machine()
    test_n_58_blocked_without_machine()
    test_n_58_unlocked_with_machine()
    test_jump_58_fails_without_machine()
    test_jump_58_succeeds_with_machine()
    test_jump_other_rooms_fails()
    print()

    print("[EXAMINE]")
    test_examine_sign()
    test_examine_pie_in_inventory()
    test_examine_machine()
    print()

    print("[State management]")
    test_on_enter_resets_state()
    print()

    print("[End-to-end reference run]")
    test_reference_full_puzzle()
    print()

    print("=" * 60)
    print("REFERENCE COMMAND SEQUENCE (verbose)")
    print("=" * 60)
    state, engine = fresh_engine(location=51)
    run_reference(state, engine, verbose=True)
    print()
    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
