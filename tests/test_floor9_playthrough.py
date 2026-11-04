"""
End-to-end playthrough of Floor 9 - prove the puzzle is solvable using
only commands the authoritative map actually supports.

Route (one command per step, the location asserted after each step):

    N -> 2            GET CHAIR
    READ NOTE
    N -> 3            GET BROOM        (the item is the LONG BROOM)
    S -> 2, S -> 1, S -> 7
    GET KEY           (needs the broom)
    N -> 1, W -> 4, S -> 6
    READ GRAFFITI
    N -> 4, N -> 5
    WATCH TV
    S -> 4, E -> 1, E -> 8, S -> 10
    OPEN CABINET      (needs the key)
    GET FLASHLIGHT, GET TAPE
    N -> 8, N -> 9
    PRESS BUTTON      (must fail - elevator not repaired yet)
    DROP CHAIR
    CLIMB CHAIR -> 11 (verb transition, not a directional exit)
    TAPE WIRES        (must succeed once the clock is past 23:00)
    D -> 9
    PRESS BUTTON      -> ("TRANSITION:floor_8:13", True)

Two side scenarios cover the refusals that the linear route cannot
show, because the linear route is too long to hit them:

  * GET KEY without the LONG BROOM is refused (the key is out of
    reach on the ledge outside the window in room 7).
  * TAPE WIRES while the wires are still live is refused; the wires
    only go dead when the in-game clock reaches 23:00.

NOTE on ordering: the engine starts the clock at 10:00 PM and advances
it 10 minutes per command, so the wires die 6 commands in.  The real
route to the crawlspace takes ~29 commands, which means the linear
route always arrives in room 11 *after* 23:00.  The live-wire refusal
is therefore checked in its own scenario (fresh engine, TAPE in hand,
placed in room 11 at 10:00 PM), not by pretending the linear route is
shorter than it is.

Run:  python3 tests/test_floor9_playthrough.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from floors.floor_9 import Floor9Engine, ROOMS


class State:
    """Minimal GameState stand-in compatible with Floor9Engine."""

    def __init__(self, location=1):
        self.location = location
        self.inventory = []
        self.floor = 9
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


def fresh_engine(location=1):
    state = State(location=location)
    engine = Floor9Engine(state)
    engine.on_enter()
    state.location = location
    return state, engine


def cmd(engine, verb, noun=""):
    """Run one command; return (message, transition)."""
    return engine.handle_command(verb, noun)


def solve_floor_9():
    """The real solution route, one command per step."""
    state, engine = fresh_engine()
    assert state.location == 1, f"expected to start in room 1, got {state.location}"

    def go(verb, noun="", expect=None, note=""):
        msg, transition = cmd(engine, verb, noun)
        if expect is not None:
            assert state.location == expect, (
                f"after '{verb} {noun}'{note}: expected room {expect}, "
                f"got {state.location}")
        return msg, transition

    # --- room 2: the chair and the note -----------------------------
    go("N", expect=2)
    go("GET", "CHAIR", note=" in room 2")
    assert "CHAIR" in state.inventory, \
        f"CHAIR not picked up, inventory={state.inventory}"

    msg, _ = go("READ", "NOTE", note=" in room 2")
    assert "note" in msg.lower(), f"READ NOTE did not mention the note: {msg!r}"

    # --- room 3: the broom -------------------------------------------
    go("N", expect=3)
    go("GET", "BROOM", note=" in room 3")
    assert "LONG BROOM" in state.inventory, \
        f"LONG BROOM not picked up, inventory={state.inventory}"

    # --- room 7: fish the key out of the window ----------------------
    go("S", expect=2)
    go("S", expect=1)
    go("S", expect=7)
    msg, _ = go("GET", "KEY", note=" in room 7")
    assert "KEY ON KEY CHAIN" in state.inventory, \
        f"GET KEY did not yield the key with the broom: {msg!r}"

    # --- room 6: the graffiti ----------------------------------------
    go("N", expect=1)
    go("W", expect=4)
    go("S", expect=6)
    msg, _ = go("READ", "GRAFFITI", note=" in room 6")
    assert "MATCH" in msg.upper(), \
        f"READ GRAFFITI did not show the graffiti: {msg!r}"

    # --- room 5: the television --------------------------------------
    go("N", expect=4)
    go("N", expect=5)
    msg, _ = go("WATCH", "TV", note=" in room 5")
    assert msg.strip(), "WATCH TV produced no output"

    # --- room 10: the cabinet ----------------------------------------
    go("S", expect=4)
    go("E", expect=1)
    go("E", expect=8)
    go("S", expect=10)
    msg, _ = go("OPEN", "CABINET", note=" in room 10")
    assert "FLASHLIGHT" in msg and "TAPE" in msg, \
        f"OPEN CABINET did not reveal the flashlight and tape: {msg!r}"
    go("GET", "FLASHLIGHT", note=" in room 10")
    go("GET", "TAPE", note=" in room 10")
    assert "FLASHLIGHT" in state.inventory, "no flashlight"
    assert "TAPE" in state.inventory, "no tape"

    # --- room 9: the elevator ----------------------------------------
    go("N", expect=8)
    go("N", expect=9)

    msg, transition = go("PRESS", "BUTTON", note=" in room 9")
    assert not transition, \
        f"PRESS BUTTON must fail before the repair, got transition={transition!r}"
    assert not engine.elevator_fixed, \
        "elevator must not be fixed before the wires are taped"
    assert "dead" in msg.lower() or "repair" in msg.lower() or "fix" in msg.lower(), \
        f"PRESS BUTTON gave no 'dead elevator' message: {msg!r}"

    # --- climb to the crawlspace -------------------------------------
    go("DROP", "CHAIR", note=" in room 9")
    assert "CHAIR" not in state.inventory, "the chair is still carried"
    assert "CHAIR" in engine._room_items.get(9, []), \
        f"the chair is not in room 9: {engine._room_items.get(9)}"

    go("CLIMB", "CHAIR", expect=11, note=" (verb transition)")

    # --- tape the wires ----------------------------------------------
    # The linear route is long enough that the clock is already past
    # 23:00 by the time we get here; if it is not yet, the tape must
    # be refused and we have to wait the wires out first.
    if engine.wires_live:
        msg, _ = go("TAPE", "WIRES", note=" in room 11")
        assert "live" in msg.lower(), \
            f"taping live wires should be refused: {msg!r}"
        assert not engine.elevator_fixed, \
            "elevator must not be fixed while the wires are live"
        while engine.wires_live:
            go("WAIT")
    else:
        assert engine._current_time_str(), "no clock reading"

    msg, _ = go("TAPE", "WIRES", note=" in room 11")
    assert engine.elevator_fixed, \
        f"TAPE WIRES did not repair the elevator: {msg!r}"
    assert state.elevator_fixed, "state.elevator_fixed was not set"

    # --- back down and ride the elevator ------------------------------
    go("D", expect=9, note=" (down from the crawlspace)")
    msg, transition = go("PRESS", "BUTTON", note=" in room 9")
    assert transition, "PRESS BUTTON must transition once the elevator is fixed"
    assert msg == "TRANSITION:floor_8:13", \
        f"unexpected transition marker: {msg!r}"

    # --- ending state -------------------------------------------------
    assert "CHAIR" in engine._room_items.get(9, []), \
        "the chair must be left standing in room 9 (the elevator)"
    assert engine.elevator_fixed is True, "engine.elevator_fixed must be True"
    assert state.location == 9, f"expected to be in room 9, got {state.location}"

    print("✅ Floor 9 puzzle solved end-to-end")
    print(f"   Final inventory: {state.inventory}")
    print(f"   Room 9 items: {engine._room_items.get(9)}")
    print(f"   Time at finish: {engine._current_time_str()}")
    print(f"   Final transition: {msg!r} (transition={transition})")
    return engine


def scenario_get_key_needs_broom():
    """GET KEY in room 7 is refused without the LONG BROOM, and works
    with it. The linear route cannot show the refusal (it has the
    broom already), so it gets its own scenario."""
    # without the broom
    state, engine = fresh_engine(location=7)
    msg, _ = cmd(engine, "GET", "KEY")
    assert "KEY ON KEY CHAIN" not in state.inventory, \
        "GET KEY must not succeed without the broom"
    assert "reach" in msg.lower() or "broom" in msg.lower() or "long" in msg.lower(), \
        f"expected a refusal mentioning reach/broom, got: {msg!r}"
    print("   ✅ GET KEY refused without the LONG BROOM")

    # with the broom
    state, engine = fresh_engine(location=7)
    state.add_item("LONG BROOM")
    msg, _ = cmd(engine, "GET", "KEY")
    assert "KEY ON KEY CHAIN" in state.inventory, \
        f"GET KEY should succeed with the broom: {msg!r}"
    print("   ✅ GET KEY succeeds with the LONG BROOM")


def scenario_live_wires_refuse_tape():
    """TAPE WIRES is refused while the wires are live and works once the
    clock has reached 23:00."""
    state, engine = fresh_engine(location=11)
    state.add_item("TAPE")

    assert engine.wires_live, \
        f"wires should be live at {engine._current_time_str()}"
    msg, _ = cmd(engine, "TAPE", "WIRES")
    assert "live" in msg.lower(), \
        f"taping live wires should be refused, got: {msg!r}"
    assert not engine.elevator_fixed, \
        "elevator must not be fixed while the wires are live"
    print(f"   ✅ TAPE WIRES refused at {engine._current_time_str()} (wires live)")

    # wait the wires out: 10:00 PM + 6 turns = 23:00
    turns = 0
    while engine.wires_live and turns < 20:
        cmd(engine, "WAIT")
        turns += 1
    assert not engine.wires_live, \
        f"wires should be dead by now ({engine._current_time_str()})"
    print(f"   ✅ wires dead at {engine._current_time_str()} after {turns} waits")

    msg, _ = cmd(engine, "TAPE", "WIRES")
    assert engine.elevator_fixed, \
        f"TAPE WIRES should repair the elevator: {msg!r}"
    print("   ✅ TAPE WIRES succeeds after 23:00")


def main():
    print("=" * 60)
    print("FLOOR 9 END-TO-END PLAYTHROUGH")
    print("=" * 60)
    print()

    print("[scenario] GET KEY needs the broom")
    scenario_get_key_needs_broom()
    print()

    print("[scenario] live wires refuse the tape")
    scenario_live_wires_refuse_tape()
    print()

    print("[route] the real solution route")
    solve_floor_9()
    print()

    print("=" * 60)
    print("ALL FLOOR 9 PLAYTHROUGH CHECKS PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
