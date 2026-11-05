#!/usr/bin/env python3
"""Floor 8 tests: the authoritative room table and the published route.

The floor 8 table below is the pixel-derived one from
FLOOR9_AUDIT_2026-11-03.md - the ground truth for this floor:

    13  IN A HALLWAY          W->14  S->16
    14  IN A VISITORS LOUNGE  W->15  E->13      AQUARIUM
    15  IN A CLOSET           E->14               ROPE
    16  IN AN OFFICE          N->13  E->17       SLEEPING PILL
    17  IN AN OFFICE          W->16               OPEN WINDOW, DESK

Room 13 is the arrival room (floor 9's PRESS BUTTON lands here).

The published walkthrough route (audit replay, exact):

    S(16) GET PILL . N(13) . W(14) . W(15) GET ROPE . E(14)
    DROP PILL GET PIRANHA . E(13) . S(16) DROP PIRANHA . E(17)
    TIE ROPE CLIMB ROPE  -> floor 7

Run standalone:  python3 tests/test_floor8.py
Exit code 0 = all tests passed, 1 = at least one failure.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from floors.floor_8 import Floor8Engine, ROOMS, SPECIAL_ROOMS  # noqa: E402

try:
    from authoritative_tables import FLOOR8_ROOMS
except Exception:  # pragma: no cover - the table module must exist
    FLOOR8_ROOMS = None

# ---------------------------------------------------------------------------
# The authoritative floor 8 table, exactly as the audit establishes it.
# ---------------------------------------------------------------------------
EXPECTED = {
    13: {
        "name": "IN A HALLWAY",
        "exits": {"W": 14, "S": 16},
        "items": [],
    },
    14: {
        "name": "IN A VISITORS LOUNGE",
        "exits": {"W": 15, "E": 13},
        "items": ["AQUARIUM"],
    },
    15: {
        "name": "IN A CLOSET",
        "exits": {"E": 14},
        "items": ["ROPE"],
    },
    16: {
        "name": "IN AN OFFICE",
        "exits": {"N": 13, "E": 17},
        "items": ["SLEEPING PILL"],
    },
    17: {
        "name": "IN AN OFFICE",
        "exits": {"W": 16},
        "items": ["OPEN WINDOW", "DESK"],
    },
}

# The room set the previous (wrong) floor 8 module used.
OLD_ROOMS = {21, 22, 24, 25, 27, 28}
OLD_NAMES = (
    "ELEVATOR LANDING",
    "PIRANHA POOL",
    "AQUARIUM STORAGE",
    "MAINTENANCE CORRIDOR",
    "POOL VIEWING GALLERY",
    "STAIRS DOWN",
)

# The published walkthrough route, one command per step, with the room the
# player must be standing in afterwards.
ROUTE = [
    ("S", "", 16),
    ("GET", "PILL", 16),
    ("N", "", 13),
    ("W", "", 14),
    ("W", "", 15),
    ("GET", "ROPE", 15),
    ("E", "", 14),
    ("DROP", "PILL", 14),
    ("GET", "PIRANHA", 14),
    ("E", "", 13),
    ("S", "", 16),
    ("DROP", "PIRANHA", 16),
    ("E", "", 17),
    ("TIE", "ROPE", 17),
    ("CLIMB", "ROPE", 18),
]


# ---------------------------------------------------------------------------
# Test double - the same shape the other floor tests use.
# ---------------------------------------------------------------------------
class FakeState:
    def __init__(self):
        self.location = 13
        self.inventory = []
        self.floor = 8
        self.alive = True
        self.game_over = False

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh_engine():
    state = FakeState()
    engine = Floor8Engine(state)
    engine.on_enter()
    return engine, state


# ---------------------------------------------------------------------------
# Table normalisation helpers (the authoritative table may spell exits
# and items in slightly different shapes).
# ---------------------------------------------------------------------------
def _norm_exits(exits):
    if isinstance(exits, dict):
        return {str(k).upper(): int(v) for k, v in exits.items()}
    out = {}
    for pair in exits or []:
        if isinstance(pair, (tuple, list)) and len(pair) == 2:
            out[str(pair[0]).upper()] = int(pair[1])
    return out


def _norm_items(items):
    if items is None:
        return []
    if isinstance(items, str):
        items = [i.strip() for i in items.split(",") if i.strip()]
    return sorted(str(i) for i in items)


def _norm_entry(entry):
    if isinstance(entry, dict):
        name = entry.get("name", "")
        exits = entry.get("exits", {})
        items = entry.get("items", [])
    elif isinstance(entry, (tuple, list)):
        name = entry[0]
        exits = entry[1] if len(entry) > 1 else {}
        items = entry[2] if len(entry) > 2 else []
    else:
        raise AssertionError(f"unrecognised table entry: {entry!r}")
    return str(name), _norm_exits(exits), _norm_items(items)


def _norm_table(table):
    return {int(k): v for k, v in table.items()}


def _compare_tables(actual, expected, label):
    actual = _norm_table(actual)
    expected = _norm_table(expected)
    assert set(actual) == set(expected), (
        f"{label}: room ids differ: {sorted(actual)} != {sorted(expected)}"
    )
    for rid in sorted(expected):
        an, ax, ai = _norm_entry(actual[rid])
        en, ex, ei = _norm_entry(expected[rid])
        assert an == en, f"{label} room {rid}: name {an!r} != {en!r}"
        assert ax == ex, f"{label} room {rid}: exits {ax} != {ex}"
        assert ai == ei, f"{label} room {rid}: items {ai} != {ei}"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_room_table_matches_the_audit():
    """The module's room table is exactly the audited floor 8 table."""
    _compare_tables(ROOMS, EXPECTED, "floor_8.ROOMS vs the audit table")


def test_room_table_matches_authoritative_tables():
    """...and it agrees with tests/authoritative_tables.py."""
    assert FLOOR8_ROOMS is not None, (
        "tests/authoritative_tables.py must export FLOOR8_ROOMS")
    _compare_tables(ROOMS, FLOOR8_ROOMS, "floor_8.ROOMS vs FLOOR8_ROOMS")
    _compare_tables(FLOOR8_ROOMS, EXPECTED, "FLOOR8_ROOMS vs the audit table")


def test_old_rooms_are_gone():
    """The invented rooms 21,22,24,25,27,28 and their names are gone."""
    assert not (OLD_ROOMS & set(ROOMS)), (
        f"old floor 8 rooms still present: {sorted(OLD_ROOMS & set(ROOMS))}")
    blob = " ".join(
        f"{r.get('name', '')} {r.get('desc', '')}" for r in ROOMS.values()
    ).upper()
    for name in OLD_NAMES:
        assert name not in blob, f"old floor 8 room name still present: {name}"
    assert SPECIAL_ROOMS.get("floor_9") is None, (
        "floor 8 must not link up to floor 9 - the descent is one way")
    assert SPECIAL_ROOMS.get("floor_7") is not None, (
        "floor 8 must declare its floor 7 link")


def test_arrival_room_is_13():
    """on_enter() puts the player in room 13 (IN A HALLWAY)."""
    engine, state = fresh_engine()
    assert state.location == 13, f"arrival room is {state.location}, not 13"
    room = engine.get_current_room()
    assert room is not None, "the arrival room must exist"
    assert room["name"] == "IN A HALLWAY"


def test_published_route():
    """The published walkthrough route replays exactly on floor 8."""
    engine, state = fresh_engine()
    last = None

    for verb, noun, expected_room in ROUTE:
        text, transition = engine.handle_command(verb, noun)
        assert isinstance(text, str), f"{verb} {noun} returned no text"
        assert isinstance(transition, bool), f"{verb} {noun} returned no flag"
        if expected_room == 18:
            # The rope crossing: the marker names floor 7 and the player
            # is left in floor 7's landing room.
            assert transition is True, (
                f"{verb} {noun} must be a transition")
            assert text.startswith("TRANSITION:floor_7"), (
                f"{verb} {noun} must return a floor 7 marker, got {text!r}")
        else:
            assert transition is False, (
                f"{verb} {noun} must not be a transition (got {text!r})")
        assert state.location == expected_room, (
            f"after '{verb} {noun}' the player is in room "
            f"{state.location}, expected {expected_room}")
        last = (verb, noun, text, transition)

    # The steps themselves, asserted against the walkthrough.
    assert "PIRANHA" not in state.inventory, (
        "DROP PIRANHA must take the piranha off the player")
    assert last[0] == "CLIMB" and last[1] == "ROPE"


def test_published_route_puzzle_steps():
    """The aquarium / piranha / rope puzzle behaves as published."""
    engine, state = fresh_engine()

    engine.handle_command("S", "")            # 16
    engine.handle_command("GET", "PILL")
    assert "SLEEPING PILL" in state.inventory, "GET PILL must yield the pill"

    engine.handle_command("N", "")            # 13
    engine.handle_command("W", "")            # 14, the aquarium
    assert state.location == 14, "W from 13 must reach the lounge (14)"

    engine.handle_command("W", "")            # 15, the closet
    engine.handle_command("GET", "ROPE")
    assert "ROPE" in state.inventory, "GET ROPE must yield the rope"

    engine.handle_command("E", "")            # 14
    assert state.location == 14, "E from 15 must return to the lounge (14)"

    engine.handle_command("DROP", "PILL")
    assert "SLEEPING PILL" not in state.inventory, (
        "the pill goes into the tank, not back into your pocket")

    engine.handle_command("GET", "PIRANHA")
    assert "PIRANHA" in state.inventory, (
        "GET PIRANHA must work once the pill is in the tank")

    engine.handle_command("E", "")            # 13
    engine.handle_command("S", "")            # 16
    assert state.location == 16, "S from 13 must reach the office (16)"
    engine.handle_command("DROP", "PIRANHA")
    assert "PIRANHA" not in state.inventory, (
        "DROP PIRANHA must take the piranha off the player")

    engine.handle_command("E", "")            # 17
    assert state.location == 17, "E from 16 must reach the second office (17)"


def test_piranha_needs_the_pill():
    """The tank yields a piranha only after the sleeping pill is dropped."""
    engine, state = fresh_engine()
    engine.handle_command("S", "")          # 16
    engine.handle_command("GET", "PILL")
    engine.handle_command("N", "")          # 13
    engine.handle_command("W", "")          # 14, the aquarium
    text, _ = engine.handle_command("GET", "PIRANHA")
    assert "PIRANHA" not in state.inventory, (
        "the piranha cannot be taken before it is asleep")

    engine.handle_command("DROP", "PILL")
    text, _ = engine.handle_command("GET", "PIRANHA")
    assert "PIRANHA" in state.inventory, (
        "the piranha must be takeable once the pill is in the tank")

    # The pill itself is gone for good.
    text, _ = engine.handle_command("GET", "SLEEPING PILL")
    assert "SLEEPING PILL" not in state.inventory, (
        "the pill must not be recoverable from the tank")


def test_rope_crossing_is_a_verb_transition():
    """Room 17 has no directional exit to floor 7 - the rope is a verb."""
    for rid, room in ROOMS.items():
        for direction, target in room["exits"].items():
            assert isinstance(target, int), (
                f"room {rid} exit {direction} points off-floor ({target!r}); "
                "floor crossings must be verbs, not exits")
    assert "U" not in ROOMS[17]["exits"], (
        "room 17 must not have an up-exit to floor 9 - one way down only")
    assert "D" not in ROOMS[17]["exits"], (
        "room 17 must not have a down-exit - the rope is a verb")

    engine, state = fresh_engine()
    engine.handle_command("S", "")              # 16
    engine.handle_command("GET", "PILL")
    engine.handle_command("N", "")              # 13
    engine.handle_command("W", "")              # 14
    engine.handle_command("W", "")              # 15
    engine.handle_command("GET", "ROPE")
    engine.handle_command("E", "")              # 14
    engine.handle_command("E", "")              # 13
    engine.handle_command("S", "")              # 16
    engine.handle_command("E", "")              # 17
    assert state.location == 17

    text, transition = engine.handle_command("CLIMB", "ROPE")
    assert transition is False, "CLIMB ROPE before TIE ROPE must not descend"
    text, transition = engine.handle_command("TIE", "ROPE")
    assert transition is False, "TIE ROPE must not descend by itself"

    for verb, noun in (("CLIMB", "ROPE"), ("GO", "ROPE"), ("USE", "ROPE"),
                       ("CLIMB", "THE ROPE")):
        engine.state.location = 17          # re-enter the office each time
        text, transition = engine.handle_command(verb, noun)
        assert transition is True, f"{verb} {noun} must descend to floor 7"
        assert text.startswith("TRANSITION:floor_7"), (
            f"{verb} {noun} must return a floor 7 marker, got {text!r}")


def test_every_command_returns_a_tuple():
    """Every command path returns (text, transition) so the dispatcher
    can unpack it."""
    engine, state = fresh_engine()
    for verb, noun in (
        ("LOOK", ""), ("INVENTORY", ""), ("EXAMINE", "AQUARIUM"),
        ("GET", "PILL"), ("DROP", "PILL"), ("USE", "ROPE"), ("OPEN", "DESK"),
        ("TIE", "ROPE"), ("CLIMB", "ROPE"), ("GO", "W"), ("N", ""),
        ("FLIBBERTIGIBBET", ""), ("GET", ""),
    ):
        result = engine.handle_command(verb, noun)
        assert isinstance(result, tuple), f"{verb} {noun} returned {result!r}"
        assert len(result) == 2, f"{verb} {noun} returned {result!r}"
        text, transition = result
        assert isinstance(text, str), f"{verb} {noun} returned {result!r}"
        assert isinstance(transition, bool), f"{verb} {noun} returned {result!r}"


def main():
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    failures = []
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except AssertionError as exc:
            failures.append((name, str(exc)))
            print(f"FAIL  {name}: {exc}")
        except Exception as exc:  # pragma: no cover
            failures.append((name, repr(exc)))
            print(f"ERROR {name}: {exc!r}")
    print(f"\n{len(tests) - len(failures)}/{len(tests)} floor 8 tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
