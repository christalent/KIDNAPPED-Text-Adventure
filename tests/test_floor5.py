#!/usr/bin/env python3
"""
Tests for KIDNAPPED! Floor 5 (The Fire and the Knitting).

Floor 5 covers:
  1. The eight audited rooms (37-44) load, with the room table the
     pixel audit recorded.
  2. Entry: room 43 (also floor_6's landing room).
  3. Exit:  room 44 GO STAIRS -> floor_4:45.
  4. SEXY, YOUNG GIRL OFFICE WORKERS (37), PUSH BUTTON ON WALL (42),
     LOCKED DOOR (43) and STAIRS (44) are fixed scenery - they cannot
     be taken.
  5. SMALL KEY (37), BALL OF YARN (39) and KNITTING NEEDLES (40) are
     takeable and sit where the listing puts them.
  6. PRESS BUTTON in 42 douses the fire and costs you your clothes;
     it works only once.
  7. The fire blocks N from 41 until the button has been pressed.
  8. KNIT CLOTHES needs both the needles and the yarn.
  9. The stairs refuse a player who is not dressed.
 10. OPEN DOOR in 43 needs the SMALL KEY; GO DOOR then reaches room 44.
 11. Fixed scenery counts as "here" for verbs - the _here() defect that
     broke PRESS/OPEN/GO on floors 1-5.

End-to-end reference run: see ``run_reference``.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "floors"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from floors.floor_5 import (Floor5Engine, ROOMS, FIXED_ITEMS, ITEM_ROOMS,
                             FLOOR_NUMBER, NEXT_FLOOR_DOWN, ENTRY_ROOM,
                             VERB_LINK_PAIRS)


class SimpleState:
    """Minimal GameState-like object compatible with Floor5Engine."""
    def __init__(self, location=43, floor=5):
        self.location = location
        self.inventory = []
        self.floor = floor
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def fresh_engine(location=43):
    state = SimpleState(location=location)
    engine = Floor5Engine(state)
    engine.on_enter()
    return state, engine


def cmd(engine, verb, noun=""):
    """Run one command; return (text, transition)."""
    return engine.handle_command(verb, noun)


# --- 1. module loads ------------------------------------------------
def test_module_loads():
    assert FLOOR_NUMBER == 5, FLOOR_NUMBER
    assert NEXT_FLOOR_DOWN == 4, NEXT_FLOOR_DOWN
    assert ENTRY_ROOM == 43, ENTRY_ROOM
    assert VERB_LINK_PAIRS, "floor 5 must declare its verb-linked rooms"
    print("  ok: module constants")


# --- 2. room table --------------------------------------------------
EXPECTED_ROOMS = {
    37: ("AN OFFICE", {"S": 41}),
    38: ("A HALLWAY", {"E": 43, "N": 39, "S": 40}),
    39: ("AN OFFICE", {"S": 38}),
    40: ("AN OFFICE", {"N": 38}),
    41: ("A HALLWAY", {"W": 43, "N": 37, "S": 42}),
    42: ("AN OFFICE", {"N": 41}),
    43: ("A HALLWAY", {"W": 38, "E": 41}),
    44: ("A STAIRCASE", {}),
}


def test_room_table():
    assert set(ROOMS) == set(EXPECTED_ROOMS), sorted(ROOMS)
    for rid, (name, exits) in EXPECTED_ROOMS.items():
        room = ROOMS[rid]
        assert room["name"].upper() == name, (rid, room["name"])
        assert room["exits"] == exits, (rid, room["exits"])
        assert room["desc"], rid
    print("  ok: room table 37-44")


def test_exits_bidirectional_except_verb_links():
    links = {tuple(p) for p in VERB_LINK_PAIRS}
    rev = {"N": "S", "S": "N", "E": "W", "W": "E"}
    for rid, room in ROOMS.items():
        for direction, target in room["exits"].items():
            if (rid, target) in links:
                continue
            back = ROOMS[target]["exits"].get(rev[direction])
            assert back == rid, (rid, direction, target, back)
    print("  ok: exits bidirectional except verb links")


# --- 3. entry / exit ------------------------------------------------
def test_entry_room():
    state, engine = fresh_engine(location=999)
    assert state.location == 43, state.location
    assert state.floor == 5, state.floor
    print("  ok: entry room 43")


def test_stairs_exit_to_floor_4():
    state, engine = fresh_engine(location=44)
    engine.flags["clothed"] = True
    text, transition = cmd(engine, "GO", "STAIRS")
    assert transition is True, text
    assert text == "TRANSITION:floor_4:45", text
    text, transition = cmd(engine, "CLIMB", "STAIRS")
    assert transition is True, text
    assert text == "TRANSITION:floor_4:45", text
    print("  ok: room 44 GO/CLIMB STAIRS -> floor_4:45")


# --- 4. fixed scenery ------------------------------------------------
def test_fixed_items_cannot_be_taken():
    assert FIXED_ITEMS == {
        "SEXY, YOUNG GIRL OFFICE WORKERS": 37,
        "PUSH BUTTON ON WALL": 42,
        "LOCKED DOOR": 43,
        "STAIRS": 44,
    }, FIXED_ITEMS
    state, engine = fresh_engine(location=37)
    text, _ = cmd(engine, "GET", "SEXY")
    assert "fixed in place" in text, text
    assert "SEXY, YOUNG GIRL OFFICE WORKERS" not in state.inventory
    state, engine = fresh_engine(location=42)
    text, _ = cmd(engine, "GET", "BUTTON")
    assert not text.startswith("You pick up"), text
    assert "PUSH BUTTON ON WALL" not in state.inventory
    print("  ok: fixed scenery cannot be taken")


# --- 5. takeable items ----------------------------------------------
def test_takeable_items_in_correct_rooms():
    assert ITEM_ROOMS == {
        "SMALL KEY": 37,
        "BALL OF YARN": 39,
        "KNITTING NEEDLES": 40,
    }, ITEM_ROOMS
    for item, room in ITEM_ROOMS.items():
        state, engine = fresh_engine(location=room)
        text, _ = cmd(engine, "GET", item)
        assert text.startswith("You pick up"), (item, text)
        assert item in state.inventory, (item, state.inventory)
    print("  ok: takeable items sit where the listing puts them")


# --- 6. the button ---------------------------------------------------
def test_button_douses_fire_and_is_one_time():
    state, engine = fresh_engine(location=42)
    text, _ = cmd(engine, "PRESS", "BUTTON")
    assert "sprinklers" in text.lower(), text
    assert engine.flags.get("doused") is True
    assert engine.flags.get("soaked") is True
    assert "clothed" not in engine.flags
    text, _ = cmd(engine, "PRESS", "BUTTON")
    assert "already" in text.lower(), text
    print("  ok: button douses fire once and costs your clothes")


def test_button_only_in_room_42():
    state, engine = fresh_engine(location=43)
    text, _ = cmd(engine, "PRESS", "BUTTON")
    assert "no button" in text.lower(), text
    assert engine.flags.get("doused") is None
    print("  ok: no button outside room 42")


# --- 7. the fire blocks the north ------------------------------------
def test_fire_blocks_north_until_doused():
    state, engine = fresh_engine(location=41)
    text, _ = cmd(engine, "N")
    assert "fire" in text.lower(), text
    assert state.location == 41, state.location
    state, engine = fresh_engine(location=42)
    cmd(engine, "PRESS", "BUTTON")
    state.location = 41
    text, _ = cmd(engine, "N")
    assert state.location == 37, (state.location, text)
    print("  ok: fire blocks N from 41 until the button is pressed")


# --- 8. knitting ------------------------------------------------------
def test_knit_needs_needles_and_yarn():
    state, engine = fresh_engine(location=39)
    text, _ = cmd(engine, "KNIT", "CLOTHES")
    assert "knit" in text.lower(), text
    state.inventory.append("KNITTING NEEDLES")
    text, _ = cmd(engine, "KNIT", "CLOTHES")
    assert "yarn" in text.lower(), text
    state.inventory.append("BALL OF YARN")
    text, _ = cmd(engine, "KNIT", "CLOTHES")
    assert engine.flags.get("clothed") is True, text
    print("  ok: knitting needs needles and yarn")


# --- 9. the stairs refuse a naked player -----------------------------
def test_stairs_refuse_undressed_player():
    state, engine = fresh_engine(location=44)
    text, transition = cmd(engine, "CLIMB", "STAIRS")
    assert transition is False, text
    assert "clothes" in text.lower(), text
    print("  ok: stairs refuse an undressed player")


# --- 10. the locked door ---------------------------------------------
def test_locked_door_needs_key():
    state, engine = fresh_engine(location=43)
    text, _ = cmd(engine, "OPEN", "DOOR")
    assert "key" in text.lower(), text
    assert engine.flags.get("door_open") is None
    state.inventory.append("SMALL KEY")
    text, _ = cmd(engine, "OPEN", "DOOR")
    assert engine.flags.get("door_open") is True, text
    text, transition = cmd(engine, "GO", "DOOR")
    assert state.location == 44, (state.location, text)
    print("  ok: locked door needs the small key")


# --- 11. fixed scenery counts as "here" ------------------------------
def test_here_sees_fixed_scenery():
    state, engine = fresh_engine(location=42)
    assert engine._here("PUSH BUTTON ON WALL") is True
    assert engine._here("LOCKED DOOR") is False
    state, engine = fresh_engine(location=43)
    assert engine._here("LOCKED DOOR") is True
    assert engine._here("PUSH BUTTON ON WALL") is False
    print("  ok: _here() sees fixed scenery")


# --- 12. state stays per instance -------------------------------------
def test_state_is_per_instance():
    state, engine = fresh_engine(location=37)
    cmd(engine, "GET", "SMALL KEY")
    assert "SMALL KEY" in state.inventory
    other_state, other_engine = fresh_engine(location=37)
    assert "SMALL KEY" not in other_state.inventory
    assert "SMALL KEY" in other_engine._room_items[37]
    assert "SMALL KEY" not in ROOMS[37]["items"]
    print("  ok: item state is per engine instance")


# --- 13. the two published routes --------------------------------------
FRANCIS = [
    ("E", ""), ("S", ""), ("PRESS", "BUTTON"), ("N", ""), ("W", ""),
    ("W", ""), ("S", ""), ("GET", "KNITTING NEEDLES"), ("N", ""), ("N", ""),
    ("GET", "BALL OF YARN"), ("KNIT", "CLOTHES"), ("S", ""), ("E", ""),
    ("E", ""), ("N", ""), ("GET", "SMALL KEY"), ("S", ""), ("W", ""),
    ("OPEN", "DOOR"), ("GO", "DOOR"), ("GO", "STAIRS"),
]
GUNNESS = [
    ("W", ""), ("S", ""), ("GET", "NEEDLES"), ("N", ""), ("N", ""),
    ("GET", "YARN"), ("S", ""), ("E", ""), ("E", ""), ("S", ""),
    ("PRESS", "BUTTON"), ("KNIT", "CLOTHES"), ("N", ""), ("N", ""),
    ("GET", "KEY"), ("S", ""), ("W", ""), ("OPEN", "DOOR"),
    ("GO", "DOOR"), ("CLIMB", "STAIRS"),
]


def run_route(route):
    """Replay a published route; stop when it transitions to floor 4.

    Francis ends with GO STAIRS and Gunness with CLIMB STAIRS, so the
    transition itself is the stop condition, not the verb.
    """
    state, engine = fresh_engine(location=43)
    for verb, noun in route:
        text, transition = cmd(engine, verb, noun)
        if transition:
            assert text == "TRANSITION:floor_4:45", (verb, noun, text)
            return state, engine
    raise AssertionError("route never reached the stairs")


def test_both_published_routes_reach_floor_4():
    for name, route in (("Francis", FRANCIS), ("Gunness", GUNNESS)):
        state, engine = run_route(route)
        assert engine.flags.get("doused") is True, name
        assert engine.flags.get("door_open") is True, name
        assert engine.flags.get("clothed") is True, name
    print("  ok: Francis and Gunness both reach floor 4")


def run_reference(state, engine, verbose=True):
    """Replay Francis route verb by verb, printing each step."""
    for verb, noun in FRANCIS:
        text, transition = cmd(engine, verb, noun)
        if verbose:
            print("  > %s %s" % (verb, noun))
            print("    %s" % text.replace("\n", " "))
            if transition:
                print("    [transition]")
        if transition:
            break


def test_reference_full_puzzle():
    state, engine = fresh_engine(location=43)
    run_reference(state, engine, verbose=False)
    print("  ok: reference puzzle run")


def main():
    print("=" * 60)
    print("KIDNAPPED! Floor 5 - The Fire and the Knitting")
    print("=" * 60)

    print("[Module]")
    test_module_loads()
    print()

    print("[Rooms]")
    test_room_table()
    test_exits_bidirectional_except_verb_links()
    test_entry_room()
    test_stairs_exit_to_floor_4()
    print()

    print("[Items]")
    test_fixed_items_cannot_be_taken()
    test_takeable_items_in_correct_rooms()
    print()

    print("[Puzzle mechanics]")
    test_button_douses_fire_and_is_one_time()
    test_button_only_in_room_42()
    test_fire_blocks_north_until_doused()
    test_knit_needs_needles_and_yarn()
    test_stairs_refuse_undressed_player()
    test_locked_door_needs_key()
    test_here_sees_fixed_scenery()
    print()

    print("[State management]")
    test_state_is_per_instance()
    print()

    print("[End-to-end reference run]")
    test_both_published_routes_reach_floor_4()
    test_reference_full_puzzle()
    print()

    print("=" * 60)
    print("REFERENCE COMMAND SEQUENCE (verbose)")
    print("=" * 60)
    state, engine = fresh_engine(location=43)
    run_reference(state, engine, verbose=True)
    print()

    print("=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
