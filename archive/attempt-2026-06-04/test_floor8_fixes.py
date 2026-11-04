#!/usr/bin/env python3
"""
Verification test for floor_8.py fixes.

Tests:
1. Bidirectional exits (no broken pairs)
2. Transitions actually fire (return True flag)
3. Room 21 cannot bypass the puzzle (no D=floor_7 from 21)
4. on_enter sets state.location = 21
5. USE BALLOON/HELIUM/TANK recognizes LIVE state
6. EXAMINE BALLOON recognizes LIVE state
7. Glue is consumed when used
8. Helium tank is consumed when used
"""
import sys
sys.path.insert(0, '.')

from floors.floor_8 import Floor8Engine, ROOMS


class SimpleState:
    def __init__(self):
        self.location = 1
        self.inventory = []
        self.floor = 8

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
        else:
            # Allow duplicates (state.add_item prints, but we don't care here)
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def assert_eq(label, actual, expected):
    if actual != expected:
        print(f"  ❌ {label}: got {actual!r}, expected {expected!r}")
        return False
    return True


def test_bidirectional():
    """1. All exits bidirectional."""
    print("\n[1] BIDIRECTIONAL EXIT CHECK")
    errors = []
    opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
    for rid, r in ROOMS.items():
        for d, t in r["exits"].items():
            if isinstance(t, str):
                continue  # inter-floor
            ro = opp[d]
            if ro not in ROOMS.get(t, {}).get("exits", {}):
                errors.append(f"Room {rid} → {d}={t}, but {t} has no {ro}")
            elif ROOMS[t]["exits"][ro] != rid:
                errors.append(f"Room {rid} → {d}={t}, but {t} → {ro}={ROOMS[t]['exits'][ro]}")
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        return False
    print(f"  ✅ All {len(ROOMS)} room pairs bidirectional")
    return True


def test_on_enter_sets_location():
    """4. on_enter sets state.location = 21."""
    print("\n[2] on_enter SETS LANDING ROOM")
    state = SimpleState()
    state.location = 999  # simulate arriving from floor 9 with bad location
    engine = Floor8Engine(state)
    engine.on_enter()
    ok = assert_eq("state.location after on_enter", state.location, 21)
    print(f"  {'✅' if ok else '❌'} state.location = {state.location}")
    return ok


def test_room_21_no_down_bypass():
    """3. Room 21 has no D=floor_7 (puzzle bypass)."""
    print("\n[3] ROOM 21 HAS NO BYPASS EXIT")
    r21 = ROOMS[21]
    exits = r21["exits"]
    ok = "D" not in exits or exits.get("D") != "floor_7"
    if not ok:
        print(f"  ❌ Room 21 has D=floor_7: {exits}")
    else:
        print(f"  ✅ Room 21 exits: {exits} (no D=floor_7)")
    return ok


def test_transitions_fire_down():
    """2a. DOWN from room 28 (with stairs fixed) returns (TRANSITION:..., True)."""
    print("\n[4] TRANSITION DOWN FIRES (with stairs_fixed)")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("SUPER GLUE")
    # Actually fix the step
    fix_result, _ = engine.handle_command("FIX", "STEP")
    assert engine.stairs_fixed, f"FIX STEP failed: {fix_result!r}"
    # Now try D
    result, transition = engine.handle_command("D", "")
    ok = transition is True and "TRANSITION:floor_7" in result
    if not ok:
        print(f"  ❌ D from 28 with fixed stairs: result={result!r}, transition={transition}")
    else:
        print(f"  ✅ result={result!r}, transition={transition}")
    return ok


def test_transitions_blocked_without_fix():
    """2b. DOWN from room 28 (without fix) blocks transition."""
    print("\n[5] TRANSITION BLOCKED (without stairs_fixed)")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    result, transition = engine.handle_command("D", "")
    ok = transition is False and "TRANSITION" not in result
    if not ok:
        print(f"  ❌ D from 28 without fix: result={result!r}, transition={transition}")
    else:
        print(f"  ✅ result={result!r}, transition={transition}")
    return ok


def test_transition_up_from_21():
    """2c. UP from room 21 returns transition."""
    print("\n[6] TRANSITION UP FROM ROOM 21")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 21
    result, transition = engine.handle_command("U", "")
    ok = transition is True and "TRANSITION:floor_9" in result
    if not ok:
        print(f"  ❌ U from 21: result={result!r}, transition={transition}")
    else:
        print(f"  ✅ result={result!r}, transition={transition}")
    return ok


def test_use_helium_after_inflation():
    """5a. USE HELIUM after inflation does not return the buggy 'no balloon to fill' message.
    The tank is now consumed after inflation, so 'no tank' is the correct response."""
    print("\n[7] USE HELIUM AFTER INFLATION (no buggy 'no balloon to fill')")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("TANK OF HELIUM GAS")
    state.add_item("LARGE DEFLATED BALLOON")
    result, _ = engine.handle_command("USE", "HELIUM")
    print(f"    After USE HELIUM: inventory={state.inventory}")
    # Try USE HELIUM again
    result, _ = engine.handle_command("USE", "HELIUM")
    # The original bug was "You don't have a balloon to fill." after inflation.
    # New correct behavior: tank is consumed, so "no tank" — both are valid, but
    # the bug message must NOT appear.
    buggy = "no balloon to fill" in result.lower()
    ok = not buggy
    if not ok:
        print(f"  ❌ USE HELIUM after inflation returned buggy message: {result!r}")
    else:
        print(f"  ✅ USE HELIUM after inflation: {result!r} (bug message absent)")
    return ok


def test_use_helium_balloon_after_inflation():
    """5b. USE HELIUM BALLOON (live) does not return the buggy 'no balloon to fill' message."""
    print("\n[8] USE 'HELIUM BALLOON' RECOGNIZES LIVE STATE")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("TANK OF HELIUM GAS")
    state.add_item("LARGE DEFLATED BALLOON")
    result, _ = engine.handle_command("USE", "HELIUM")
    # Now USE 'HELIUM BALLOON' (live). Tank is gone (consumed on inflate).
    result, _ = engine.handle_command("USE", "HELIUM BALLOON")
    # The original bug was "You don't have a balloon to fill." after inflation.
    # Must not appear.
    buggy = "no balloon to fill" in result.lower()
    ok = not buggy
    if not ok:
        print(f"  ❌ USE HELIUM BALLOON returned buggy message: {result!r}")
    else:
        print(f"  ✅ USE HELIUM BALLOON: {result!r} (bug message absent)")
    return ok


def test_examine_live_balloon():
    """6. EXAMINE BALLOON finds LIVE HELIUM BALLOON."""
    print("\n[9] EXAMINE BALLOON RECOGNIZES LIVE")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("TANK OF HELIUM GAS")
    state.add_item("LARGE DEFLATED BALLOON")
    engine.handle_command("USE", "HELIUM")
    # Now EXAMINE BALLOON
    result, _ = engine.handle_command("EXAMINE", "BALLOON")
    ok = "round" in result.lower() or "tugs" in result.lower()
    if not ok:
        print(f"  ❌ EXAMINE BALLOON (live): {result!r}")
    else:
        print(f"  ✅ EXAMINE BALLOON (live): {result!r}")
    return ok


def test_glue_consumed():
    """7. Glue is consumed when fixing step."""
    print("\n[10] GLUE CONSUMED ON FIX")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("SUPER GLUE")
    result, _ = engine.handle_command("FIX", "STEP")
    ok = "SUPER GLUE" not in state.inventory
    if not ok:
        print(f"  ❌ Glue still in inventory: {state.inventory}, result={result!r}")
    else:
        print(f"  ✅ Glue consumed. inventory={state.inventory}")
    return ok


def test_helium_consumed():
    """8. Helium tank is consumed on inflate."""
    print("\n[11] HELIUM TANK CONSUMED ON INFLATE")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    state.location = 28
    state.add_item("TANK OF HELIUM GAS")
    state.add_item("LARGE DEFLATED BALLOON")
    engine.handle_command("USE", "HELIUM")
    ok = "TANK OF HELIUM GAS" not in state.inventory
    if not ok:
        print(f"  ❌ Tank still in inventory: {state.inventory}")
    else:
        print(f"  ✅ Tank consumed. inventory={state.inventory}")
    return ok


def test_full_puzzle_path():
    """End-to-end: collect items, fix step, descend to floor 7."""
    print("\n[12] FULL PUZZLE PATH (collect → fix → descend)")
    state = SimpleState()
    engine = Floor8Engine(state)
    engine.on_enter()
    # Start in 21
    print(f"    Start: location={state.location}, inventory={state.inventory}")
    # N to 22
    r, _ = engine.handle_command("N", "")
    print(f"    After N: location={state.location}")
    assert state.location == 22, f"Expected 22, got {state.location}"
    # N to 24
    r, _ = engine.handle_command("N", "")
    assert state.location == 24
    # Get balloon
    r, _ = engine.handle_command("GET", "BALLOON")
    print(f"    After GET BALLOON: {r}, inv={state.inventory}")
    assert "LARGE DEFLATED BALLOON" in state.inventory
    # N to 28
    r, _ = engine.handle_command("N", "")
    assert state.location == 28
    # Get helium
    r, _ = engine.handle_command("GET", "HELIUM")
    print(f"    After GET HELIUM: {r}, inv={state.inventory}")
    assert "TANK OF HELIUM GAS" in state.inventory
    # S to 24
    r, _ = engine.handle_command("S", "")
    assert state.location == 24
    # S to 22
    r, _ = engine.handle_command("S", "")
    assert state.location == 22
    # E to 25
    r, _ = engine.handle_command("E", "")
    assert state.location == 25
    # Get glue
    r, _ = engine.handle_command("GET", "GLUE")
    print(f"    After GET GLUE: {r}, inv={state.inventory}")
    assert "SUPER GLUE" in state.inventory
    # W to 22
    r, _ = engine.handle_command("W", "")
    assert state.location == 22
    # N to 24
    r, _ = engine.handle_command("N", "")
    assert state.location == 24
    # N to 28
    r, _ = engine.handle_command("N", "")
    assert state.location == 28
    # Fix step
    r, _ = engine.handle_command("FIX", "STEP")
    print(f"    After FIX STEP: {r}")
    assert engine.stairs_fixed
    # D - should transition
    r, t = engine.handle_command("D", "")
    print(f"    After D: result={r!r}, transition={t}")
    ok = t is True and "TRANSITION:floor_7:31" in r
    if not ok:
        print(f"  ❌ D from 28 should transition to floor_7:31")
        return False
    print(f"  ✅ Full path works: collected items, fixed step, descended to floor 7")
    return True


def main():
    print("=" * 60)
    print("FLOOR 8 BUG-FIX VERIFICATION")
    print("=" * 60)
    tests = [
        test_bidirectional,
        test_on_enter_sets_location,
        test_room_21_no_down_bypass,
        test_transitions_fire_down,
        test_transitions_blocked_without_fix,
        test_transition_up_from_21,
        test_use_helium_after_inflation,
        test_use_helium_balloon_after_inflation,
        test_examine_live_balloon,
        test_glue_consumed,
        test_helium_consumed,
        test_full_puzzle_path,
    ]
    results = []
    for t in tests:
        results.append(t())

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"✅ ALL {total} TESTS PASSED — Floor 8 is fixed")
    else:
        print(f"❌ {total - passed} of {total} tests FAILED")
    print("=" * 60)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
