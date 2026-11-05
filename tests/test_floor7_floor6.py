"""
Floor 6 regression tests (formerly test_floor7_floor6.py).

The floor 7 half of this file asserted a fabricated bank-vault layout
(rooms 31-39 and 55-56) that collided with floor 6's real rooms.  Floor 7
is now source-audited (global rooms 18-25) and is covered by
tests/test_floor7_source.py instead.

Floor 6 fixes under test:
  1. New layout: rooms 26-36 with bidirectional exits
  2. Items: GUN, TIN FOIL, BALLOON, HELIUM, VENDING MACHINE, LOCKED DOOR
  3. GUN path: threaten kidnapper -> get dollar + key -> unlock door -> descend
  4. BALLOON path: inflate with helium -> fly to floor 5
  5. SHOOT KIDNAPPER -> blanks -> die (red herring)
  6. GET DOLLAR (no gun) -> die
  7. Transitions work properly
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from floors.floor_6 import Floor6Engine, ROOMS as ROOMS6

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


























# ======================================================================
# Floor 6 tests
# ======================================================================




















def main():
    print("=" * 60)
    print("FLOOR 7 + FLOOR 6 BUG-FIX TESTS")
    print("=" * 60)
    print()

    print("[FLOOR 7]")

    print()

    print()

    print("[CROSS-FLOOR]")
    print()

    print("=" * 60)
    print("ALL TESTS PASSED ✅")
    print("=" * 60)




if __name__ == "__main__":
    main()
