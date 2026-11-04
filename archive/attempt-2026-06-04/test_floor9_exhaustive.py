#!/usr/bin/env python3
"""
Exhaustive navigation test for Floor 9.
Tests all reachable rooms, all items GET/DROP, and reports any issues.
"""
import sys
sys.path.insert(0, 'floors')

from floors.floor_9 import Floor9Engine, ROOMS

class SimpleState:
    def __init__(self):
        self.location = 1
        self.inventory = []
        self.floor = 9
        self.dark = False
        self.flashlight_on = False
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def exhaustive_navigation():
    """BFS/DFS to visit all reachable rooms and collect items."""
    state = SimpleState()
    engine = Floor9Engine(state)
    engine.on_enter()

    # Discover reachable rooms via BFS
    all_rooms = set(ROOMS.keys())
    visited = set()
    queue = [1]  # start at room 1

    while queue:
        rid = queue.pop(0)
        if rid in visited:
            continue
        visited.add(rid)

        # Get the room's exits
        exits = ROOMS[rid].get("exits", {})
        for d, target in exits.items():
            # Skip inter-floor transitions (strings like "floor_8")
            if isinstance(target, str):
                continue
            # Handle list destinations (e.g., {"N": [2, 10]})
            targets = target if isinstance(target, list) else [target]
            for t in targets:
                if t not in visited:
                    queue.append(t)

    unreachable = all_rooms - visited
    return visited, unreachable


def test_navigation_errors():
    """Try navigating from each room in every direction, checking for crashes."""
    state = SimpleState()
    engine = Floor9Engine(state)
    engine.on_enter()

    errors = []
    for rid in ROOMS.keys():
        state.location = rid
        state.floor = 9
        engine.state = state
        engine._key_on_ledge = True
        engine.cabinet_open = False
        engine.tape_used = False
        engine.elevator_fixed = False
        engine._room_items = {rid: list(r["items"]) for rid, r in ROOMS.items()}

        exits = ROOMS[rid].get("exits", {})
        for d in ["N", "S", "E", "W", "U", "D"]:
            try:
                result, done = engine.handle_command(d, "")
                # A string return is fine; None or exception is bad
                if result is None:
                    errors.append(f"Room {rid} dir {d}: returned None")
            except Exception as e:
                errors.append(f"Room {rid} dir {d}: EXCEPTION {type(e).__name__}: {e}")

    return errors


def test_item_get_drop():
    """Try getting and dropping every takeable item in each room."""
    state = SimpleState()
    engine = Floor9Engine(state)
    engine.on_enter()

    results = []

    # Reset state
    state.floor = 9
    engine._key_on_ledge = True
    engine.cabinet_open = False
    engine.tape_used = False
    engine.elevator_fixed = False
    engine._room_items = {rid: list(r["items"]) for rid, r in ROOMS.items()}

    # Items that CAN be taken (not scenery)
    takeable = {
        "FLASHLIGHT", "CHAIR", "BROOM",
        "LOCKED DOOR", "GRAFFITI ON WALL", "WIRES", "ADMISSION",
        "TAPE", "SMALL KEY", "KEY ON A KEY CHAIN", "PUSH BUTTON"
    }

    for rid, room in ROOMS.items():
        state.location = rid
        state.inventory = []
        engine.state = state
        engine._room_items = {r: list(ROOMS[r]["items"]) for r in ROOMS}
        engine._key_on_ledge = True
        engine.cabinet_open = False
        engine.tape_used = False
        engine.elevator_fixed = False

        for item in room.get("items", []):
            if item in ("GRAFFITI ON WALL", "ADMISSION", "LOCKED DOOR", "WIRES", "PUSH BUTTON", "TV SET", "CLOCK"):
                # These should NOT be takeable
                result, _ = engine.handle_command("GET", item)
                if "can't be taken" not in result.lower() and "can't" not in result.lower():
                    results.append(f"Room {rid}: {item} should NOT be takeable, got: {result}")
                continue

            # Try to GET the item
            result, _ = engine.handle_command("GET", item)
            if "no" in result.lower() and ("here" in result.lower() or item.lower() not in result.lower()):
                results.append(f"Room {rid}: GET {item} failed: {result}")
            else:
                # Try DROP
                drop_result, _ = engine.handle_command("DROP", item)
                if "not" in drop_result.lower() and "carrying" in drop_result.lower():
                    results.append(f"Room {rid}: DROP {item} failed: {drop_result}")

    return results


def main():
    print("=" * 60)
    print("FLOOR 9 EXHAUSTIVE NAVIGATION & ITEM TEST")
    print("=" * 60)

    # 1. Reachable rooms
    print("\n[1] REACHABLE ROOMS (BFS from room 1)")
    visited, unreachable = exhaustive_navigation()
    print(f"    Visited: {sorted(visited)}")
    if unreachable:
        print(f"    ❌ UNREACHABLE: {sorted(unreachable)}")
    else:
        print(f"    ✅ All {len(visited)} rooms reachable")

    # 2. Navigation errors
    print("\n[2] NAVIGATION STRESS TEST (all dirs from all rooms)")
    nav_errors = test_navigation_errors()
    if nav_errors:
        for e in nav_errors:
            print(f"    ❌ {e}")
    else:
        print(f"    ✅ No navigation errors")

    # 3. Item GET/DROP
    print("\n[3] ITEM GET/DROP TEST")
    item_errors = test_item_get_drop()
    if item_errors:
        for e in item_errors:
            print(f"    ❌ {e}")
    else:
        print(f"    ✅ All items GET/DROP correctly")

    # 4. Summary
    print("\n" + "=" * 60)
    total_errors = len(unreachable) + len(nav_errors) + len(item_errors)
    if total_errors == 0:
        print("✅ ALL TESTS PASSED — Floor 9 is fully navigable")
    else:
        print(f"❌ {total_errors} error(s) found:")
        if unreachable:
            print(f"   - {len(unreachable)} unreachable room(s)")
        if nav_errors:
            print(f"   - {len(nav_errors)} navigation error(s)")
        if item_errors:
            print(f"   - {len(item_errors)} item error(s)")
    print("=" * 60)


if __name__ == "__main__":
    main()
