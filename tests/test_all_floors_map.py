"""
All-floors map consistency tests.

What this catches that test_navigation.py misses:
  - Reachable-from-start (orphan rooms) — every room on the floor
    must be reachable from the floor's first room
  - Source mismatches — for floors 6-9 where PARSED_BASIC_SOURCE.txt
    has confirmed bidirectional pairs, every pair must actually exist
    as an exit between those two rooms
  - Unjustified extras — exits in ROOMS that have no source backing,
    even if they're internally consistent
  - Duplicate directions per room
  - Empty exit dicts

The existing test_navigation.py only checks "A→B has matching B→A";
it can't catch "A→B is a pair the source never authorized"
or "room X is unreachable from the start".
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib
from collections import deque, defaultdict

# Confirmed bidirectional pairs from PARSED_BASIC_SOURCE.txt,
# indexed by floor. Each entry: list of (room_a, room_b) pairs
# that the source explicitly confirms.
SOURCE_PAIRS = {
    9: [
        # From the BASIC PRINT statements
        (1, 2), (2, 3), (1, 7), (1, 8),
        (4, 5), (4, 6),
        (8, 9), (9, 11),
        (11, 13), (13, 16), (14, 15), (16, 17),
        # Synthesized in the port
        (1, 4), (3, 4), (8, 10), (9, 10),
        (11, 15), (13, 14), (14, 15),
    ],
    8: [
        (21, 22), (22, 24), (22, 25), (22, 27), (24, 28),
    ],
    7: [
        # Docstring in floor_7.py confirms:
        #   31<->32, 31<->33, 31<->38, 32<->36, 32<->37, 32<->39, 35<->38,
        #   36<->37, 37<->55, 38<->39, 55<->56
        (31, 32), (31, 33), (31, 38), (32, 36), (32, 37), (32, 39),
        (35, 38), (36, 37), (37, 55), (38, 39), (55, 56),
    ],
    6: [
        # Docstring in floor_6.py confirms the full linear chain
        # 41<->42, 42<->43, 43<->44, 44<->45, 45<->46, 46<->47, 47<->48, 48<->49
        (41, 42), (42, 43), (43, 44), (44, 45), (45, 46),
        (46, 47), (47, 48), (48, 49),
    ],
    # Floors 1-5 have no confirmed source pairs — structural tests only
}

OPP = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}


def test_floor(floor_num):
    """Return (issues_list, ascii_map_str) for one floor."""
    issues = []
    mod = importlib.import_module(f"floors.floor_{floor_num}")
    ROOMS = mod.ROOMS

    if not ROOMS:
        return [f"Floor {floor_num}: no ROOMS dict"], ""

    start_room = min(ROOMS.keys())
    edges = {rid: dict(r.get("exits", {})) for rid, r in ROOMS.items()}

    # 1. No empty exit dicts (dead-end rooms are allowed but should be intentional)
    # We warn rather than fail.
    dead_ends = [rid for rid, ex in edges.items() if not ex]
    if dead_ends:
        issues.append(f"  ⚠️  Dead-end rooms (no exits): {dead_ends}")

    # 2. Bidirectional consistency (skip inter-floor string markers)
    for rid, exits in edges.items():
        for d, t in exits.items():
            if isinstance(t, str):
                continue  # inter-floor marker
            if t not in edges:
                issues.append(f"  Room {rid}→{d}={t}: target missing")
                continue
            rev = OPP.get(d)
            if not rev:
                continue
            back = edges[t].get(rev)
            if back is None:
                issues.append(f"  Room {rid}→{d}={t}, but {t} has no {rev}")
            elif back != rid:
                issues.append(
                    f"  Room {rid}→{d}={t}, but {t}→{rev}={back} (expected {rid})"
                )

    # 3. Reachable from start
    visited = {start_room}
    queue = deque([start_room])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if isinstance(t, str) or t not in edges or t in visited:
                continue
            visited.add(t)
            queue.append(t)
    orphans = sorted(set(edges.keys()) - visited)
    if orphans:
        issues.append(f"  Orphan rooms (unreachable from {start_room}): {orphans}")

    # 4. No duplicate directions
    for rid, exits in edges.items():
        seen = defaultdict(list)
        for d, t in exits.items():
            seen[d].append(t)
        for d, ts in seen.items():
            if len(ts) > 1:
                issues.append(f"  Room {rid}: duplicate direction {d} → {ts}")

    # 5. Source-match (only for floors with source data)
    if floor_num in SOURCE_PAIRS:
        authorized = set()
        for a, b in SOURCE_PAIRS[floor_num]:
            authorized.add((a, b))
            authorized.add((b, a))
        for a, exits in edges.items():
            for d, b in exits.items():
                if isinstance(b, str):
                    continue
                if (a, b) not in authorized:
                    issues.append(
                        f"  Room {a}→{d}={b}: not in source's confirmed pairs"
                    )

    # 6. Sanity: every room has name and desc
    for rid, r in ROOMS.items():
        if not r.get("name"):
            issues.append(f"  Room {rid}: missing name")
        if not r.get("desc"):
            issues.append(f"  Room {rid}: missing desc")

    return issues, _render_map(edges, start_room, floor_num)


def _render_map(edges, start_room, floor_num):
    """BFS-place rooms and render an ASCII map."""
    pos = {start_room: (0, 0)}
    placed = {start_room}
    HSPACE, VSPACE = 6, 4

    queue = deque([start_room])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if isinstance(t, str) or t in placed:
                continue
            cx, cy = pos[cur]
            if d in ("N", "U"): cy -= VSPACE
            elif d in ("S", "D"): cy += VSPACE
            elif d == "E": cx += HSPACE
            elif d == "W": cx -= HSPACE
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
    width = (max_x - min_x) * 2 + 1
    height = max(ys) - min_y + 3

    grid = [[" "] * width for _ in range(height)]

    for rid, exits in edges.items():
        if rid not in pos:
            continue
        x1, y1 = pos[rid]
        cx1 = (x1 - min_x) * 2
        cy1 = y1 - min_y
        for d, t in exits.items():
            if isinstance(t, str) or t not in pos:
                continue
            x2, y2 = pos[t]
            cx2 = (x2 - min_x) * 2
            cy2 = y2 - min_y
            if cy1 == cy2:
                step = 1 if cx2 > cx1 else -1
                for x in range(cx1 + step, cx2, step):
                    if 0 <= cy1 < height and 0 <= x < width and grid[cy1][x] == " ":
                        grid[cy1][x] = "─"
            elif cx1 == cx2:
                step = 1 if cy2 > cy1 else -1
                for y in range(cy1 + step, cy2, step):
                    if 0 <= y < height and 0 <= cx1 < width and grid[y][cx1] == " ":
                        grid[y][cx1] = "│"

    for rid, (x, y) in pos.items():
        cx = (x - min_x) * 2
        cy = y - min_y
        label = f"{rid:>2} "
        for i, ch in enumerate(label):
            if 0 <= cy < height and 0 <= cx + i - 1 < width:
                grid[cy][cx + i - 1] = ch

    return f"\n--- Floor {floor_num} ---\n" + "\n".join(
        "".join(row).rstrip() for row in grid if any(c != " " for c in row)
    )


def main():
    print("=" * 60)
    print("ALL-FLOORS MAP CONSISTENCY")
    print("=" * 60)

    total_issues = 0
    for floor in range(9, 0, -1):
        issues, map_str = test_floor(floor)
        if not issues:
            print(f"\n✅ Floor {floor}: clean")
        else:
            total_issues += len(issues)
            print(f"\n❌ Floor {floor}: {len(issues)} issue(s)")
            for i in issues:
                print(i)
        print(map_str)

    print()
    print("=" * 60)
    if total_issues == 0:
        print("✅ All 9 floors pass map consistency")
    else:
        print(f"❌ {total_issues} total issues across floors")
    print("=" * 60)
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
