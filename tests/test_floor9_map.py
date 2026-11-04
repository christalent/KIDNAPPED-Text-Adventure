"""
Map consistency tests for Floor 9.

Ground truth: the pixel-derived audit
    FLOOR9_AUDIT_2026-11-03.md
transcribed into
    tests/authoritative_tables.py  (FLOOR9_ROOMS)

This file deliberately does NOT use a hand-written CONFIRMED_PAIRS list.
The old version of this test compared floors/floor_9.py against a
table that had been guessed by the same author - it graded a guess
against itself and happily passed a wrong room set (it still believed
in rooms 13-17 and in an exit from the elevator to the maintenance
room).

What is checked here:
  1. the exact set of room ids is {1..11}
  2. every room's exits, item list and name equal the authoritative table
  3. floors/floor_9.py declares VERB_LINK_PAIRS == {(9,11),(11,9)}
  4. the 9 -> 11 link is a VERB link, not a directional exit: room 9
     has no "U" exit and room 11's only exit is D=9
  5. rooms 12-17 do not exist on floor 9
  6. structural sanity: no duplicate directions, no orphan rooms
     (verb links count as extra edges), every room has a name/desc
  7. an ASCII map of the directional grid, with the off-grid
     crawlspace (room 11) listed as an annotation

Run:  python3 tests/test_floor9_map.py
"""

import sys, os

# tests/ is not a package - put it on sys.path so we can import the
# authoritative tables from the same directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib
from collections import deque, defaultdict

import authoritative_tables

mod = importlib.import_module("floors.floor_9")
ROOMS = mod.ROOMS

AUTHORITATIVE = authoritative_tables.FLOOR9_ROOMS
FORBIDDEN = authoritative_tables.FLOOR9_FORBIDDEN_ROOMS
EXPECTED_ROOM_IDS = set(range(1, 12))

OPP = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}


def _build_edges():
    """Return dict: room_id -> {direction: target} from ROOMS."""
    return {rid: dict(r["exits"]) for rid, r in ROOMS.items()}


def test_room_id_set():
    """Floor 9 must contain exactly rooms 1..11."""
    errors = []
    ids = set(ROOMS.keys())
    missing = sorted(EXPECTED_ROOM_IDS - ids)
    extra = sorted(ids - EXPECTED_ROOM_IDS)
    if missing:
        errors.append(f"missing authoritative rooms: {missing}")
    if extra:
        errors.append(f"unexpected rooms: {extra} "
                      f"(floor 9 is rooms 1-11 only)")
    return errors


def test_forbidden_rooms_absent():
    """Rooms 12-17 were misfiled on floor 9 by the old port."""
    errors = []
    present = sorted(set(ROOMS.keys()) & FORBIDDEN)
    if present:
        errors.append(f"forbidden rooms present on floor 9: {present} "
                      f"(12 is a verb-only special room; 13-17 belong to floor 8)")
    return errors


def test_matches_authoritative_table():
    """Every room's exits, items and name must equal the authoritative table."""
    errors = []
    for rid in sorted(EXPECTED_ROOM_IDS):
        if rid not in ROOMS:
            continue
        module = ROOMS[rid]
        truth = AUTHORITATIVE[rid]
        if module.get("name") != truth["name"]:
            errors.append(f"Room {rid}: name {module.get('name')!r} != "
                          f"authoritative {truth['name']!r}")
        if module.get("exits") != truth["exits"]:
            errors.append(f"Room {rid}: exits {module.get('exits')!r} != "
                          f"authoritative {truth['exits']!r}")
        if list(module.get("items", [])) != list(truth["items"]):
            errors.append(f"Room {rid}: items {list(module.get('items', []))!r} != "
                          f"authoritative {list(truth['items'])!r}")
    return errors


def test_verb_link_pairs_declared():
    """The module must document the deliberate one-way verb transition."""
    errors = []
    declared = getattr(mod, "VERB_LINK_PAIRS", None)
    if declared is None:
        errors.append("floors/floor_9.py does not declare VERB_LINK_PAIRS")
        return errors
    declared = {tuple(p) for p in declared}
    if declared != {(9, 11), (11, 9)}:
        errors.append(f"VERB_LINK_PAIRS is {sorted(declared)}, "
                      f"expected [(9, 11), (11, 9)]")
    return errors


def test_up_link_is_not_directional():
    """9 -> 11 is CLIMB CHAIR, not a directional exit."""
    errors = []
    if "U" in ROOMS.get(9, {}).get("exits", {}):
        errors.append(f"Room 9 must not have a directional 'U' exit "
                      f"(the up-link is the CLIMB CHAIR verb transition), "
                      f"got {ROOMS[9]['exits']}")
    room11_exits = ROOMS.get(11, {}).get("exits", {})
    if room11_exits != {"D": 9}:
        errors.append(f"Room 11's only exit must be D=9, got {room11_exits}")
    return errors


def test_bidirectional_pairs():
    """Every directional exit must have a matching reverse exit, except
    the documented verb-linked pair."""
    edges = _build_edges()
    verb_links = {tuple(p) for p in getattr(mod, "VERB_LINK_PAIRS", set())}
    errors = []
    for rid, exits in edges.items():
        for d, t in exits.items():
            if t not in edges:
                errors.append(f"Room {rid}->{d}={t}: target room {t} missing")
                continue
            if (rid, t) in verb_links:
                continue
            rev = OPP[d]
            back = edges[t].get(rev)
            if back is None:
                errors.append(f"Room {rid}->{d}={t}, but {t} has no {rev} exit")
            elif back != rid:
                errors.append(
                    f"Room {rid}->{d}={t}, but {t}->{rev}={back} (expected {rid})"
                )
    return errors


def test_no_duplicate_directions():
    """A room cannot have two exits in the same direction."""
    errors = []
    for rid, r in ROOMS.items():
        exits = r["exits"]
        seen = defaultdict(list)
        for d, t in exits.items():
            seen[d].append(t)
        for d, ts in seen.items():
            if len(ts) > 1:
                errors.append(f"Room {rid} has {len(ts)} exits in direction {d}: {ts}")
    return errors


def test_reachability_from_start():
    """Every room must be reachable from room 1, counting verb links as
    extra edges (the crawlspace 11 is reached by CLIMB CHAIR)."""
    edges = _build_edges()
    adj = {rid: set() for rid in edges}
    for rid, exits in edges.items():
        for d, t in exits.items():
            if t in edges:
                adj[rid].add(t)
    for a, b in {tuple(p) for p in getattr(mod, "VERB_LINK_PAIRS", set())}:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)

    visited = {1}
    queue = deque([1])
    while queue:
        cur = queue.popleft()
        for t in adj.get(cur, ()):
            if t not in visited:
                visited.add(t)
                queue.append(t)
    return sorted(set(edges.keys()) - visited)


def test_rooms_have_names_and_descriptions():
    """Sanity: every room has a non-empty name, desc, exits and items."""
    errors = []
    for rid, r in ROOMS.items():
        if not r.get("name", "").strip():
            errors.append(f"Room {rid}: missing name")
        if not r.get("desc", "").strip():
            errors.append(f"Room {rid}: missing desc")
        if not isinstance(r.get("exits"), dict):
            errors.append(f"Room {rid}: exits is not a dict")
        if not isinstance(r.get("items"), (list, tuple)):
            errors.append(f"Room {rid}: items is not a list")
    return errors


def render_ascii_map():
    """ASCII layout of floor 9's DIRECTIONAL grid, plus an annotation
    for the verb-linked crawlspace.

    Room 11 (the crawlspace) is off the directional grid: the only way
    up to it is the CLIMB CHAIR verb transition, so it cannot be placed
    by walking the compass exits. It is listed separately instead of
    crashing the renderer.
    """
    edges = _build_edges()
    verb_links = {tuple(p) for p in getattr(mod, "VERB_LINK_PAIRS", set())}

    HSPACE = 6
    VSPACE = 4
    pos = {1: (0, 0)}
    placed = {1}

    queue = deque([1])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if t in placed:
                continue
            cx, cy = pos[cur]
            if d in ("N", "U"):
                cy -= VSPACE
            elif d in ("S", "D"):
                cy += VSPACE
            elif d == "E":
                cx += HSPACE
            elif d == "W":
                cx -= HSPACE
            attempts = 0
            while any(p == (cx, cy) for rid, p in pos.items() if rid != cur):
                cy += 1
                attempts += 1
                if attempts > 10:
                    break
            pos[t] = (cx, cy)
            placed.add(t)
            queue.append(t)

    if not pos:
        return ""

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs) - 4, max(xs) + 4
    min_y = min(ys) - 2
    width = (max_x - min_x) * 2
    height = max(ys) - min_y

    grid = [[" "] * (width + 1) for _ in range(height + 1)]

    for rid, exits in edges.items():
        if rid not in pos:
            continue
        x1, y1 = pos[rid]
        cx1 = (x1 - min_x) * 2
        cy1 = y1 - min_y
        for d, t in exits.items():
            if t not in pos:
                continue
            x2, y2 = pos[t]
            cx2 = (x2 - min_x) * 2
            cy2 = y2 - min_y
            if cy1 == cy2:
                step = 1 if cx2 > cx1 else -1
                for x in range(cx1 + step, cx2, step):
                    if 0 <= cy1 < len(grid) and 0 <= x < len(grid[0]):
                        if grid[cy1][x] == " ":
                            grid[cy1][x] = "-"
            elif cx1 == cx2:
                step = 1 if cy2 > cy1 else -1
                for y in range(cy1 + step, cy2, step):
                    if 0 <= y < len(grid) and 0 <= cx1 < len(grid[0]):
                        if grid[y][cx1] == " ":
                            grid[y][cx1] = "|"

    for rid, (x, y) in pos.items():
        cx = (x - min_x) * 2
        cy = y - min_y
        label = f"{rid:>2} "
        for i, ch in enumerate(label):
            if 0 <= cy < len(grid) and 0 <= cx + i - 1 < len(grid[0]):
                grid[cy][cx + i - 1] = ch

    art = "\n".join("".join(row).rstrip() for row in grid if any(c != " " for c in row))

    # Rooms that are not on the directional grid (verb-linked only).
    off_grid = sorted(rid for rid in edges if rid not in pos)
    annotations = []
    for rid in off_grid:
        name = ROOMS[rid].get("name", "?")
        annotations.append(f"  [off-grid] room {rid}: {name} "
                           f"(reached by verb, exits {edges[rid]})")
    for a, b in sorted(verb_links):
        annotations.append(f"  [verb link] {a} <-> {b}")

    if annotations:
        return art + "\n" + "\n".join(annotations)
    return art


def main():
    print("=" * 60)
    print("FLOOR 9 MAP CONSISTENCY TESTS")
    print("=" * 60)
    print("Ground truth: tests/authoritative_tables.py (FLOOR9_ROOMS), "
          "transcribed from FLOOR9_AUDIT_2026-11-03.md")
    print()

    all_errors = []
    for name, fn in [
        ("Room ids are exactly 1..11", test_room_id_set),
        ("Rooms 12-17 absent", test_forbidden_rooms_absent),
        ("Matches authoritative table", test_matches_authoritative_table),
        ("VERB_LINK_PAIRS declared", test_verb_link_pairs_declared),
        ("9->11 is a verb link, not an exit", test_up_link_is_not_directional),
        ("Bidirectional pairs", test_bidirectional_pairs),
        ("No duplicate directions", test_no_duplicate_directions),
        ("Rooms have names/descs", test_rooms_have_names_and_descriptions),
    ]:
        result = fn()
        if isinstance(result, list) and not result:
            print(f"  ✅ {name}: pass")
        elif isinstance(result, list):
            print(f"  ❌ {name}: {len(result)} issue(s)")
            for e in result:
                print(f"     - {e}")
            all_errors.extend([(name, e) for e in result])
        else:
            # reachability returns a list of orphans
            if not result:
                print("  ✅ Reachable from start: pass")
            else:
                print(f"  ❌ Reachable from start: unreachable rooms {result}")
                all_errors.append(("Reachable from start", f"orphans: {result}"))

    print()
    print("=" * 60)
    print("ASCII MAP (Floor 9, from room 1)")
    print("=" * 60)
    print(render_ascii_map())
    print()

    if all_errors:
        print(f"\n❌ {len(all_errors)} issues found")
        return 1
    else:
        print("\n✅ Map matches the authoritative floor 9 table")
        return 0


if __name__ == "__main__":
    sys.exit(main())
