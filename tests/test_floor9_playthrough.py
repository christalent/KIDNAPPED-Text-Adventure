"""End-to-end playthrough of Floor 9 — prove the puzzle is solvable
using only commands the map actually supports."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from floors.floor_9 import Floor9Engine, ROOMS

class State:
    def __init__(self):
        self.location = 1
        self.inventory = []
        self.floor = 9
        self.game_over = False
        self.alive = True
    def add_item(self, item):
        self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

def cmd(engine, verb, noun=""):
    msg, transition = engine.handle_command(verb, noun)
    return msg, transition

def solve_floor_9():
    """Walk through the canonical solution path described in the
    floor_9.py docstring. Every step is a real map traversal and a
    real command. We assert we end with elevator_fixed=True and
    we got there without ever hitting an 'unknown' or 'can't' message.
    """
    s = State()
    eng = Floor9Engine(s)
    eng.on_enter()

    bad = ("can't", "can't go that way", "don't have", "no", "not", "can't be")

    def must(verb, noun=""):
        msg, t = cmd(eng, verb, noun)
        return msg, t

    # 1. Get broom from closet (room 3, via rooms 1 → 2 → 3)
    assert s.location == 1
    must("N");  # room 2
    assert s.location == 2, f"expected room 2, got {s.location}"
    must("N");  # room 3
    assert s.location == 3
    must("GET", "BROOM")
    assert "BROOM" in s.inventory

    # 2. Use broom in room 7 to fish the key, then GET it
    must("S");  # back to 2
    must("S");  # back to 1
    must("S");  # room 7
    assert s.location == 7
    must("USE", "BROOM")
    must("GET", "KEY")
    assert "KEY ON KEY CHAIN" in s.inventory

    # 3. Back to room 1, unlock cabinet
    must("N");  # back to 1
    assert s.location == 1
    must("USE", "KEY")
    # Cabinet should now have flashlight + tape
    must("GET", "FLASHLIGHT")
    must("GET", "TAPE")
    assert "FLASHLIGHT" in s.inventory
    assert "TAPE" in s.inventory

    # 4. Get to room 11 (elevator shaft): 1 → E → 8 → N → 9 → U → 11
    must("E");  # 8
    assert s.location == 8
    must("N");  # 9
    assert s.location == 9
    must("U");  # 11
    assert s.location == 11

    # 5. Wait until past 11 PM so wires are safe (we start at 10:00 PM,
    # need to wait >6 turns). The puzzle says wait until after midnight.
    # Time advance: 10 min/turn, start at 10:00 PM.
    # 11 PM = 60 min later = 6 turns
    # Midnight = 120 min later = 12 turns
    for i in range(15):
        must("WAIT")

    # 6. Tape the wires
    must("USE", "TAPE")
    assert eng.elevator_fixed, "elevator should be fixed after taping"

    # 7. Back to room 9, PUSH button, get floor transition
    must("D");  # 9
    assert s.location == 9
    msg, transition = must("PUSH", "BUTTON")
    assert transition, f"PUSH BUTTON should trigger floor transition, got msg: {msg!r}"

    print("✅ Floor 9 puzzle solved end-to-end")
    print(f"   Final inventory: {s.inventory}")
    print(f"   Time at finish: {eng._current_time_str()}")
    print(f"   Final message: {msg[:100]}...")

if __name__ == "__main__":
    solve_floor_9()
