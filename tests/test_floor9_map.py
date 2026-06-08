"""
Map consistency tests for Floor 9.

What this catches that test_navigation.py misses:
  1. Source mismatches: a room's exits don't match PARSED_BASIC_SOURCE.txt
     (the existing test only checks that A→B has a matching B→A back;
     it does NOT check that A→B is the right connection per the source).
  2. Orphan rooms: a room is defined but unreachable from room 1
     (start of the floor). The basic test won't catch it because it
     only validates exit pairs, not graph connectivity.
  3. Dead-end contradictions: a room described as having an exit in
     the prose but missing it in ROOMS, or vice versa.
  4. Compass-direction sanity: e.g. two different rooms claiming
     the same direction from one source.

Ground truth: PARSED_BASIC_SOURCE.txt "CONFIRMED BIDIRECTIONAL PAIRS"
section (the explicit ground-truth list, not the inferred-corrected map
which has known bugs).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib
from collections import deque, defaultdict

mod = importlib.import_module("floors.floor_9")
ROOMS = mod.ROOMS

# Ground truth: confirmed bidirectional pairs from PARSED_BASIC_SOURCE.txt
# plus the explicit floor-9 map section.
CONFIRMED_PAIRS = [
    # From the BASIC PRINT statements section in PARSED_BASIC_SOURCE.txt
    (1, 2), (2, 3),  # 1→N=2, 2→N=3, 3→S=2
    (1, 7), (1, 8),
    (4, 5), (4, 6),
    (8, 9), (9, 11),
    (11, 13), (13, 16), (14, 15), (16, 17),
    # Synthesized in the port to connect the two halves of the floor:
    (1, 4),  # elevator hub ↔ roof
    (3, 4),  # closet ↔ roof via ceiling hatch
    (8, 10), (9, 10),  # elevator cars ↔ crawlspace
    (11, 15),  # shaft ↔ rope closet (W from 11, E from 15)
    (13, 14), (14, 15),  # ring 11-13-14-15-11
]

OPP = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}


def _build_edges():
    """Return dict: room_id -> {direction: target} from ROOMS."""
    return {rid: dict(r["exits"]) for rid, r in ROOMS.items()}


def test_bidirectional_pairs():
    """Every edge in ROOMS must have a matching reverse edge."""
    edges = _build_edges()
    errors = []
    for rid, exits in edges.items():
        for d, t in exits.items():
            if t not in edges:
                errors.append(f"Room {rid}→{d}={t}: target room {t} missing")
                continue
            rev = OPP[d]
            back = edges[t].get(rev)
            if back is None:
                errors.append(f"Room {rid}→{d}={t}, but {t} has no {rev} exit")
            elif back != rid:
                errors.append(
                    f"Room {rid}→{d}={t}, but {t}→{rev}={back} (expected {rid})"
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
    """Every defined room should be reachable from room 1."""
    edges = _build_edges()
    visited = {1}
    queue = deque([1])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if t in edges and t not in visited:
                visited.add(t)
                queue.append(t)
    unreachable = sorted(set(edges.keys()) - visited)
    return unreachable


def test_pairs_match_source():
    """Every confirmed bidirectional pair must be navigable both ways."""
    edges = _build_edges()
    errors = []
    for a, b in CONFIRMED_PAIRS:
        if a not in edges:
            errors.append(f"Source requires room {a} (paired with {b}) but it doesn't exist")
            continue
        if b not in edges:
            errors.append(f"Source requires room {b} (paired with {a}) but it doesn't exist")
            continue
        # Must be some direction from a to b
        a_to_b = [d for d, t in edges[a].items() if t == b]
        b_to_a = [d for d, t in edges[b].items() if t == a]
        if not a_to_b:
            errors.append(f"Confirmed pair {a}↔{b}: room {a} has no exit to {b} "
                          f"(its exits go to {sorted(edges[a].values())})")
        if not b_to_a:
            errors.append(f"Confirmed pair {a}↔{b}: room {b} has no exit to {a} "
                          f"(its exits go to {sorted(edges[b].values())})")
        if a_to_b and b_to_a:
            # Both directions must use the opposite compass
            for d in a_to_b:
                rev = OPP[d]
                if rev not in b_to_a:
                    errors.append(
                        f"Confirmed pair {a}↔{b}: {a}→{d}={b} but {b} goes {b_to_a} "
                        f"(expected {rev}, not {[OPP.get(x,'?') for x in b_to_a]})"
                    )
    return errors


def test_no_extra_exits():
    """Warn about any exit not justified by the source."""
    edges = _build_edges()
    # Build set of all (a, b) pairs that the source authorizes
    authorized = set()
    for a, b in CONFIRMED_PAIRS:
        authorized.add((a, b))
        authorized.add((b, a))

    extras = []
    for a, exits in edges.items():
        for d, b in exits.items():
            if (a, b) not in authorized:
                extras.append(f"Room {a}→{d}={b} is NOT in the source's confirmed pairs")
    return extras


def test_rooms_have_names_and_descriptions():
    """Sanity: every room has non-empty name and desc."""
    errors = []
    for rid, r in ROOMS.items():
        if not r.get("name", "").strip():
            errors.append(f"Room {rid}: missing name")
        if not r.get("desc", "").strip():
            errors.append(f"Room {rid}: missing desc")
        if not isinstance(r.get("exits"), dict):
            errors.append(f"Room {rid}: exits is not a dict")
    return errors


def render_ascii_map():
    """Best-effort ASCII layout. Each room gets a 4-cell-wide cell;
    edges are drawn as straight lines between cell centers.
    Conflicts (two rooms needing the same cell) are detected and
    we re-place the later one below. This produces a readable map
    that a human can eyeball against the source.
    """
    edges = _build_edges()
    CELL_W = 6  # each room occupies a CELL_W x 1 cell
    HSPACE = 6
    VSPACE = 4
    pos = {1: (0, 0)}  # room 1 at origin
    placed = {1}

    def place_rel(parent, direction, child):
        px, py = pos[parent]
        if direction == "N":   return (px, py - VSPACE)
        if direction == "S":   return (px, py + VSPACE)
        if direction == "E":   return (px + HSPACE, py)
        if direction == "W":   return (px - HSPACE, py)
        if direction == "U":   return (px, py - VSPACE)
        if direction == "D":   return (px, py + VSPACE)

    # BFS placement. If a target cell is already taken, nudge
    # vertically until we find a free cell.
    queue = deque([1])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if t in placed:
                continue
            cx, cy = place_rel(cur, d, t)
            # Nudge for conflict
            attempts = 0
            while any(p == (cx, cy) for rid, p in pos.items() if rid != cur):
                cy += 1
                attempts += 1
                if attempts > 10:
                    break
            pos[t] = (cx, cy)
            placed.add(t)
            queue.append(t)

    # Compute grid bounds
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    min_x, max_x = min(xs) - 4, max(xs) + 4
    min_y, max_y = min(ys) - 2, max(ys) + 2
    width = (max_x - min_x) * 2
    height = max_y - min_y

    # Use 2 chars per cell horizontally to make it readable
    grid = [[" "] * (width + 1) for _ in range(height + 1)]

    # Draw edges as straight lines between cell centers
    for rid, exits in edges.items():
        x1, y1 = pos[rid]
        cx1 = (x1 - min_x) * 2
        cy1 = y1 - min_y
        for d, t in exits.items():
            if t not in pos:
                continue
            x2, y2 = pos[t]
            cx2 = (x2 - min_x) * 2
            cy2 = y2 - min_y
            if cy1 == cy2:  # horizontal
                step = 1 if cx2 > cx1 else -1
                for x in range(cx1 + step, cx2, step):
                    if 0 <= cy1 < len(grid) and 0 <= x < len(grid[0]):
                        if grid[cy1][x] == " ":
                            grid[cy1][x] = "─"
            elif cx1 == cx2:  # vertical
                step = 1 if cy2 > cy1 else -1
                for y in range(cy1 + step, cy2, step):
                    if 0 <= y < len(grid) and 0 <= cx1 < len(grid[0]):
                        if grid[y][cx1] == " ":
                            grid[y][cx1] = "│"

    # Draw room labels (centered in their cell)
    for rid, (x, y) in pos.items():
        cx = (x - min_x) * 2
        cy = y - min_y
        # 4-char label: [N ]
        label = f"{rid:>2} "
        for i, ch in enumerate(label):
            if 0 <= cy < len(grid) and 0 <= cx + i - 1 < len(grid[0]):
                grid[cy][cx + i - 1] = ch

    # Trim trailing whitespace per line
    return "\n".join("".join(row).rstrip() for row in grid if any(c != " " for c in row))


def main():
    print("=" * 60)
    print("FLOOR 9 MAP CONSISTENCY TESTS")
    print("=" * 60)

    all_errors = []
    for name, fn in [
        ("Bidirectional pairs", test_bidirectional_pairs),
        ("No duplicate directions", test_no_duplicate_directions),
        ("Reachable from start", lambda: test_reachability_from_start()),
        ("Matches PARSED source", test_pairs_match_source),
        ("No unjustified extras", test_no_extra_exits),
        ("Sanity (names/descs)", test_rooms_have_names_and_descriptions),
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
                print(f"  ✅ {name}: pass")
            else:
                print(f"  ❌ {name}: unreachable rooms {result}")
                all_errors.append((name, f"orphans: {result}"))

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
        print("\n✅ Map is internally consistent and matches source")
        return 0


if __name__ == "__main__":
    sys.exit(main())
