"""
Floor 6 tests - the office complex, the ledges and the vault.

Every expectation here is traceable to the pixel read of the original
listing recorded in ``audit/FLOOR6_PIXEL_NOTES.md`` or to one of the two
published walkthroughs in ``archive/solutions/``.

The two walkthrough replays are the strongest checks in the file: if the
room table, the verb transitions or the puzzle state machine is wrong,
one of them will not finish.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from floors.floor_6 import (  # noqa: E402
    FIXED_ITEMS,
    FLOOR_NUMBER,
    ROOMS,
    SPECIAL_ROOMS,
    Floor6Engine,
)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from authoritative_tables import (  # noqa: E402
        FLOOR6_FORBIDDEN_ROOMS,
        FLOOR6_ITEMS,
        FLOOR6_ROOMS,
    )
except ImportError:  # pragma: no cover - tests/ is not a package
    from tests.authoritative_tables import (  # noqa: E402
        FLOOR6_FORBIDDEN_ROOMS,
        FLOOR6_ITEMS,
        FLOOR6_ROOMS,
    )


class FakeState:
    """Minimal stand-in for the game's GameState."""

    def __init__(self, location=26):
        self.location = location
        self.floor = FLOOR_NUMBER
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def make_engine(location=26):
    state = FakeState(location)
    engine = Floor6Engine(state)
    engine.on_enter()
    state.location = location
    return engine


def run(engine, commands):
    """Run a list of (verb, noun) pairs, returning the list of results."""
    out = []
    for verb, noun in commands:
        result = engine.handle_command(verb, noun)
        out.append(result)
    return out


def parse(command):
    parts = command.strip().split()
    if not parts:
        return ("", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[0], " ".join(parts[1:]))


def test_room_table_matches_authoritative_table():
    assert set(ROOMS) == set(FLOOR6_ROOMS), (
        "floor_6.py rooms %s != authoritative %s"
        % (sorted(ROOMS), sorted(FLOOR6_ROOMS))
    )
    for rid, expect in FLOOR6_ROOMS.items():
        got = ROOMS[rid]
        assert got["name"] == expect["name"], rid
        assert got["exits"] == expect["exits"], rid
        assert sorted(got["items"]) == sorted(expect["items"]), rid


def test_floor6_owns_exactly_rooms_26_to_36():
    assert set(ROOMS) == set(range(26, 37))
    for bad in FLOOR6_FORBIDDEN_ROOMS:
        assert bad not in ROOMS, bad


def test_item_table_matches_room_table():
    derived = {}
    for rid, r in ROOMS.items():
        if r["items"]:
            derived[rid] = sorted(r["items"])
    assert derived == {k: sorted(v) for k, v in FLOOR6_ITEMS.items()}


def test_arrival_room_is_26():
    engine = make_engine()
    assert engine.state.location == 26
    assert ROOMS[26]["name"] == "IN A HALLWAY"


def test_special_rooms_targets_floor_5():
    assert "floor_5" in SPECIAL_ROOMS
    assert SPECIAL_ROOMS["floor_5"]["target"] == "floor_5"
    # UNRESOLVED until floor 5 is audited: the landing room is a
    # placeholder and must not silently point at a stale floor-5 room.
    assert isinstance(SPECIAL_ROOMS["floor_5"]["landing_room"], int)


def test_every_command_returns_a_two_tuple():
    engine = make_engine()
    for verb, noun in [("LOOK", ""), ("N", ""), ("GET", "GUN"),
                       ("JUMP", ""), ("INFLATE", "BALLOON"),
                       ("TIE", "STRING"), ("BOGUS", "THING")]:
        result = engine.handle_command(verb, noun)
        assert isinstance(result, tuple), (verb, noun, result)
        assert len(result) == 2, (verb, noun, result)
        assert isinstance(result[0], str), (verb, noun, result)
        assert isinstance(result[1], bool), (verb, noun, result)


def test_helium_tank_balloon_and_gun_are_where_the_data_says():
    engine = make_engine()
    engine.state.location = 28
    text, _ = engine.handle_command("GET", "TANK OF HELIUM GAS")
    assert "TANK OF HELIUM GAS" in engine.state.inventory
    engine.state.location = 29
    engine.handle_command("GET", "BALLOON")
    assert "LARGE DEFLATED BALLOON" in engine.state.inventory
    engine.state.location = 30
    engine.handle_command("GET", "GUN")
    assert "GUN" in engine.state.inventory


def test_scenery_cannot_be_taken():
    engine = make_engine()
    engine.state.location = 32
    text, _ = engine.handle_command("GET", "SIGN")
    assert "can't be taken" in text
    assert "SIGN ON WALL" not in engine.state.inventory
    engine.state.location = 33
    text, _ = engine.handle_command("GET", "WINDOW")
    assert "can't be taken" in text
    assert "OPEN WINDOW" not in engine.state.inventory


def test_ledge_and_window_verb_transitions():
    engine = make_engine()
    # 33 --CLIMB LEDGE--> 34
    engine.state.location = 33
    engine.handle_command("CLIMB", "LEDGE")
    assert engine.state.location == 34
    # 34 --CLIMB WINDOW--> 33
    engine.state.location = 34
    engine.handle_command("CLIMB", "WINDOW")
    assert engine.state.location == 33
    # 36 --CLIMB WINDOW--> 35 (the vault)
    engine.state.location = 36
    engine.handle_command("CLIMB", "WINDOW")
    assert engine.state.location == 35
    # 35 --CLIMB LEDGE--> 36
    engine.state.location = 35
    engine.handle_command("CLIMB", "LEDGE")
    assert engine.state.location == 36
    # GO LEDGE / GO WINDOW are the same verbs
    engine.state.location = 33
    engine.handle_command("GO", "LEDGE")
    assert engine.state.location == 34
    engine.state.location = 36
    engine.handle_command("GO", "WINDOW")
    assert engine.state.location == 35


def test_sign_and_string_purchase():
    engine = make_engine()
    engine.state.location = 32
    text, _ = engine.handle_command("READ", "SIGN")
    assert "STRING COSTS $1.00" in text
    # No money yet
    text, _ = engine.handle_command("PUT", "DOLLAR")
    assert "don't have any money" in text
    engine.state.add_item("DOLLAR")
    text, _ = engine.handle_command("PUT", "DOLLAR")
    assert "long string" in text.lower()
    assert "LONG STRING" in engine._room_items[32]
    text, _ = engine.handle_command("GET", "STRING")
    assert "LONG STRING" in engine.state.inventory


def test_inflate_and_tie_need_the_right_things():
    engine = make_engine()
    engine.state.location = 29
    engine.handle_command("GET", "BALLOON")
    text, _ = engine.handle_command("INFLATE", "BALLOON")
    assert "need something to inflate" in text
    engine.state.location = 28
    engine.handle_command("GET", "TANK OF HELIUM GAS")
    text, _ = engine.handle_command("INFLATE", "BALLOON")
    assert "LARGE INFLATED BALLOON" in engine.state.inventory
    text, _ = engine.handle_command("TIE", "BALLOON")
    assert "need a string" in text
    engine.state.add_item("LONG STRING")
    text, _ = engine.handle_command("TIE", "BALLOON")
    assert "INFLATED BALLOON WITH STRING" in engine.state.inventory


def test_jump_from_ledge_34_transitions_to_floor_5():
    engine = make_engine()
    engine.state.location = 34
    text, transition = engine.handle_command("JUMP", "")
    assert transition is True
    # The marker must be the whole result: the dispatcher parses a
    # result only when it starts with "TRANSITION:floor_N:room".
    assert text.startswith("TRANSITION:floor_5:"), text
    assert text == "TRANSITION:floor_5:43", text


def test_gun_in_the_vault_is_a_dead_end():
    engine = make_engine()
    engine.state.location = 35
    engine.state.add_item("GUN")
    text, _ = engine.handle_command("USE", "GUN")
    assert "BLANKS" in text


def test_gunness_walkthrough_replays():
    """Jacob Gunness (CASA Solution Archive, Sept 2004), floor 6 verbatim."""
    engine = make_engine()
    commands = [
        "N", "N", "GET GAS", "S", "S", "E", "GET BALLOON", "W", "S",
        "GET GUN", "N", "W", "W", "CLIMB LEDGE", "W", "CLIMB WINDOW",
        "GET DOLLAR", "W", "E", "CLIMB WINDOW", "E", "N", "READ SIGN",
        "PUT DOLLAR", "GET STRING", "INFLATE BALLOON", "TIE BALLOON",
        "S", "W", "CLIMB LEDGE", "JUMP",
    ]
    results = run(engine, [parse(c) for c in commands])
    last_text, last_transition = results[-1]
    assert last_transition is True, results
    assert last_text == "TRANSITION:floor_5:43", last_text
    # The gun was picked up on the way.
    assert "GUN" in engine.state.inventory
    # The balloon ended up tied to the string.
    assert "INFLATED BALLOON WITH STRING" in engine.state.inventory


def test_atari_walkthrough_replays():
    """Garry Francis (minimal Atari solution), floor 6 verbatim."""
    engine = make_engine()
    commands = [
        "S", "GET GUN", "N", "E", "GET LARGE DEFLATED BALLOON", "W",
        "N", "N", "GET TANK OF HELIUM GAS", "INFLATE BALLOON", "S", "S",
        "W", "W", "GO LEDGE", "W", "GO WINDOW", "GET DOLLAR", "W", "E",
        "GO WINDOW", "E", "N", "PAY DOLLAR", "GET LONG STRING",
        "TIE STRING", "S", "W", "GO LEDGE", "JUMP",
    ]
    results = run(engine, [parse(c) for c in commands])
    last_text, last_transition = results[-1]
    assert last_transition is True, results
    assert last_text == "TRANSITION:floor_5:43", last_text
    assert "INFLATED BALLOON WITH STRING" in engine.state.inventory


def test_tie_string_uses_the_long_string_alias():
    engine = make_engine()
    engine.state.location = 29
    engine.handle_command("GET", "BALLOON")
    engine.state.location = 28
    engine.handle_command("GET", "GAS")
    engine.handle_command("INFLATE", "BALLOON")
    engine.state.add_item("LONG STRING")
    text, _ = engine.handle_command("TIE", "STRING")
    assert "INFLATED BALLOON WITH STRING" in engine.state.inventory


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(list(globals().items())):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS %s" % name)
            except Exception as exc:  # noqa: BLE001
                failures += 1
                print("FAIL %s: %s" % (name, exc))
    print("FAILURES: %d" % failures)
    sys.exit(1 if failures else 0)
