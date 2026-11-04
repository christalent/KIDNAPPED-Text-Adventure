"""
All-floors map consistency tests.

NON-CIRCULAR BY DESIGN
----------------------
This file used to compare every floor against a hand-written
SOURCE_PAIRS table that had been guessed by the same person who wrote
the floors - i.e. it graded a guess against itself and could never
catch a wrong room set.

Now:

  * Floors whose room tables have been pixel-audited are compared
    against the authoritative table in tests/authoritative_tables.py
    (transcribed from FLOOR9_AUDIT_2026-11-03.md).
  * Floors that have NOT been audited yet print
    "NOT YET AUDITED - source validation skipped" and are only checked
    structurally. Their source comparison is deliberately skipped
    rather than done against a guess.

Structural checks (valid for every floor, audited or not):
  a) every exit target exists as a room on the same floor
     (string targets are inter-floor transition markers and are skipped)
  b) directional exits are bidirectional, EXCEPT for documented verb
     links - e.g. floor 9's CLIMB CHAIR between the elevator (9) and
     the crawlspace (11) is a verb transition, not a directional exit.
     A floor module may declare VERB_LINK_PAIRS to document this.
  c) no orphan rooms - every room is reachable from the floor's entry
     room when verb links are treated as extra edges
  d) every room dict has name/desc/exits/items keys
  e) no duplicate directions per room (a room cannot have two exits
     to the north)

Run:  python3 tests/test_all_floors_map.py
"""

import sys, os

# tests/ is not a package: put it on the path so authoritative_tables
# can be imported, and the repo root so floors.* can be imported.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import importlib
from collections import deque, defaultdict

import authoritative_tables

# ---------------------------------------------------------------------
# Which floors may be compared against an authoritative table?
#
# authoritative_tables.UNAUDITED_FLOORS lists the floors whose room
# tables are still guesses. A floor is source-validated only if it has
# an authoritative table AND is not on the unaudited list.
#
# Floor 8 is audited too: floors/floor_8.py now carries the
# authoritative 13-17 table, so it is compared here like floor 9.
# ---------------------------------------------------------------------
VALIDATED_FLOORS = {
    f for f in authoritative_tables.AUDITED_ROOMS
    if f not in authoritative_tables.UNAUDITED_FLOORS
}

OPP = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}


class _DummyState:
    """Minimal GameState stand-in used to ask a floor engine where it
    puts the player when you enter the floor."""

    def __init__(self):
        self.location = None
        self.inventory = []
        self.floor = 0
        self.dark = False
        self.flashlight_on = False
        self.turns = 0
        self.game_time = "10:00 PM"
        self.power_out = False
        self.alive = True
        self.game_over = False

    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)


def _entry_room(mod, floor_num, rooms):
    """Return (entry_room, how_we_know).

    The floor's own on_enter() arrival room is authoritative. Floors
    whose on_enter() does not move the player (they inherit the
    location from the game state) fall back to the lowest room id on
    the floor, which is the landing room for those floors.
    """
    cls = getattr(mod, f"Floor{floor_num}Engine", None)
    if cls is not None:
        state = _DummyState()
        try:
            engine = cls(state)
            engine.on_enter()
            if state.location in rooms:
                return state.location, "on_enter() arrival room"
        except Exception:
            pass
    return min(rooms.keys()), "lowest room id (on_enter does not move the player)"


def _verb_links(mod):
    """Documented verb-linked room pairs, if the floor declares them."""
    pairs = getattr(mod, "VERB_LINK_PAIRS", None)
    if not pairs:
        return set()
    return {tuple(p) for p in pairs}


def check_structure(floor_num):
    """Structural checks that hold for any floor, audited or not.

    Returns (errors, warnings, notes).
    """
    errors = []
    warnings = []
    notes = []

    mod = importlib.import_module(f"floors.floor_{floor_num}")
    ROOMS = getattr(mod, "ROOMS", None)
    if not ROOMS:
        return ([f"Floor {floor_num}: no ROOMS dict"], warnings, notes)

    verb_links = _verb_links(mod)
    if verb_links:
        notes.append(f"verb links: {sorted(verb_links)}")

    edges = {}
    for rid, r in ROOMS.items():
        edges[rid] = {d: t for d, t in r.get("exits", {}).items()}

    entry, how = _entry_room(mod, floor_num, ROOMS)
    notes.append(f"entry room: {entry} ({how})")

    # (a) every exit target exists on this floor
    inter_floor = []
    for rid, exits in edges.items():
        for d, t in exits.items():
            if isinstance(t, str):
                inter_floor.append((rid, d, t))
                continue
            if t not in edges:
                errors.append(f"Room {rid}->{d}={t}: target room does not exist")
    if inter_floor:
        notes.append(f"inter-floor exits: {len(inter_floor)} "
                     f"(e.g. {inter_floor[0]})")

    # (b) directional exits are bidirectional, except verb links
    for rid, exits in edges.items():
        for d, t in exits.items():
            if isinstance(t, str) or t not in edges:
                continue
            if (rid, t) in verb_links:
                continue  # deliberate one-way verb transition
            rev = OPP.get(d)
            if not rev:
                continue
            back = edges[t].get(rev)
            if back is None:
                errors.append(f"Room {rid}->{d}={t}, but {t} has no {rev} exit")
            elif back != rid:
                errors.append(f"Room {rid}->{d}={t}, but {t}->{rev}={back} "
                              f"(expected {rid})")

    # (c) no orphan rooms - reachable from the entry room, counting
    #     verb links as extra (undirected) edges
    adj = {rid: set() for rid in edges}
    for rid, exits in edges.items():
        for d, t in exits.items():
            if isinstance(t, str) or t not in edges:
                continue
            adj[rid].add(t)
    for a, b in verb_links:
        if a in adj and b in adj:
            adj[a].add(b)
            adj[b].add(a)

    visited = {entry}
    queue = deque([entry])
    while queue:
        cur = queue.popleft()
        for t in adj.get(cur, ()):
            if t not in visited:
                visited.add(t)
                queue.append(t)
    orphans = sorted(set(edges.keys()) - visited)
    if orphans:
        errors.append(f"Orphan rooms (unreachable from {entry}): {orphans}")

    # (d) every room dict has the four required keys
    for rid, r in ROOMS.items():
        for key in ("name", "desc", "exits", "items"):
            if key not in r:
                errors.append(f"Room {rid}: missing '{key}' key")
        if not r.get("name"):
            errors.append(f"Room {rid}: empty name")
        if not r.get("desc"):
            errors.append(f"Room {rid}: empty desc")
        if not isinstance(r.get("exits"), dict):
            errors.append(f"Room {rid}: exits is not a dict")
        if not isinstance(r.get("items"), (list, tuple)):
            errors.append(f"Room {rid}: items is not a list")

    # (e) no duplicate directions
    for rid, exits in edges.items():
        seen = defaultdict(list)
        for d, t in exits.items():
            seen[d].append(t)
        for d, ts in seen.items():
            if len(ts) > 1:
                errors.append(f"Room {rid}: duplicate direction {d} -> {ts}")

    dead_ends = [rid for rid, ex in edges.items() if not ex]
    if dead_ends:
        warnings.append(f"Dead-end rooms (no exits): {dead_ends}")

    return errors, warnings, notes


def check_against_authoritative(floor_num):
    """Compare a floor module with its authoritative room table.

    Returns a list of error strings (empty when the floor matches).
    """
    errors = []
    mod = importlib.import_module(f"floors.floor_{floor_num}")
    ROOMS = mod.ROOMS
    table = authoritative_tables.AUDITED_ROOMS[floor_num]

    # exact room id set
    module_ids = set(ROOMS.keys())
    table_ids = set(table.keys())
    if module_ids != table_ids:
        missing = sorted(table_ids - module_ids)
        extra = sorted(module_ids - table_ids)
        if missing:
            errors.append(f"floor {floor_num}: missing authoritative rooms {missing}")
        if extra:
            errors.append(f"floor {floor_num}: unexpected rooms {extra}")

    # per-room name / exits / items
    for rid in sorted(module_ids & table_ids):
        m = ROOMS[rid]
        t = table[rid]
        if m.get("name") != t["name"]:
            errors.append(f"Room {rid}: name {m.get('name')!r} != "
                          f"authoritative {t['name']!r}")
        if m.get("exits") != t["exits"]:
            errors.append(f"Room {rid}: exits {m.get('exits')!r} != "
                          f"authoritative {t['exits']!r}")
        if list(m.get("items", [])) != list(t["items"]):
            errors.append(f"Room {rid}: items {list(m.get('items', []))!r} != "
                          f"authoritative {list(t['items'])!r}")

    # flattened exit triples must agree as well
    module_pairs = authoritative_tables.source_pairs(
        {rid: {"exits": r.get("exits", {})} for rid, r in ROOMS.items()})
    table_pairs = authoritative_tables.source_pairs(table)
    if module_pairs != table_pairs:
        errors.append(f"floor {floor_num}: exit triples differ from the "
                      f"authoritative table "
                      f"(extra: {sorted(module_pairs - table_pairs)}, "
                      f"missing: {sorted(table_pairs - module_pairs)})")

    # rooms the audit proved must not exist
    if floor_num == 9:
        forbidden = authoritative_tables.FLOOR9_FORBIDDEN_ROOMS
        present = sorted(set(ROOMS.keys()) & forbidden)
        if present:
            errors.append(f"floor 9: forbidden rooms present: {present} "
                          f"(the audit proved they are not on floor 9)")

    return errors


def _render_map(edges, start_room, floor_num, verb_links=()):
    """BFS-place rooms and render an ASCII map.

    Rooms that are only reachable through a verb link (e.g. floor 9's
    crawlspace 11) are off the directional grid; they are listed as an
    annotation instead of blowing up the renderer.
    """
    pos = {start_room: (0, 0)}
    placed = {start_room}
    HSPACE, VSPACE = 6, 4

    queue = deque([start_room])
    while queue:
        cur = queue.popleft()
        for d, t in edges[cur].items():
            if isinstance(t, str) or t not in edges or t in placed:
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
                        grid[cy1][x] = "-"
            elif cx1 == cx2:
                step = 1 if cy2 > cy1 else -1
                for y in range(cy1 + step, cy2, step):
                    if 0 <= y < height and 0 <= cx1 < width and grid[y][cx1] == " ":
                        grid[y][cx1] = "|"

    for rid, (x, y) in pos.items():
        cx = (x - min_x) * 2
        cy = y - min_y
        label = f"{rid:>2} "
        for i, ch in enumerate(label):
            if 0 <= cy < height and 0 <= cx + i - 1 < width:
                grid[cy][cx + i - 1] = ch

    art = "\n".join("".join(row).rstrip() for row in grid if any(c != " " for c in row))

    off_grid = [rid for rid in edges if rid not in pos]
    extra = []
    if off_grid:
        for rid in sorted(off_grid):
            extra.append(f"  off-grid (verb-linked) room {rid}: {edges[rid]}")
    for a, b in sorted(set(verb_links)):
        extra.append(f"  verb link {a} <-> {b}")

    return f"\n--- Floor {floor_num} ---\n" + art + ("\n" + "\n".join(extra) if extra else "")


def main():
    print("=" * 60)
    print("ALL-FLOORS MAP CONSISTENCY")
    print("=" * 60)
    print(f"Audited floors (validated against tests/authoritative_tables.py): "
          f"{sorted(VALIDATED_FLOORS)}")
    print(f"Not yet audited (source validation skipped): "
          f"{sorted(authoritative_tables.UNAUDITED_FLOORS)}")

    total_issues = 0
    for floor in range(9, 0, -1):
        errors, warnings, notes = check_structure(floor)
        mod = importlib.import_module(f"floors.floor_{floor}")
        verb_links = _verb_links(mod)
        ROOMS = mod.ROOMS
        edges = {rid: dict(r.get("exits", {})) for rid, r in ROOMS.items()}
        entry, _how = _entry_room(mod, floor, ROOMS)

        print()
        print(f"--- Floor {floor} ---")
        for note in notes:
            print(f"  · {note}")

        if floor in VALIDATED_FLOORS:
            src_errors = check_against_authoritative(floor)
            if src_errors:
                total_issues += len(src_errors)
                print(f"  ❌ source validation vs authoritative table: "
                      f"{len(src_errors)} issue(s)")
                for e in src_errors:
                    print(f"     - {e}")
            else:
                print("  ✅ source validation: matches the authoritative table")
        else:
            print("  ⏭ NOT YET AUDITED - source validation skipped "
                  "(no hand-written table to compare against)")

        if errors:
            total_issues += len(errors)
            print(f"  ❌ structural checks: {len(errors)} issue(s)")
            for e in errors:
                print(f"     - {e}")
        else:
            print("  ✅ structural checks: pass "
                  "(targets exist, bidirectional except verb links, "
                  "no orphans, all keys present)")

        for w in warnings:
            print(f"  ⚠️  {w}")

        print(_render_map(edges, entry, floor, verb_links))

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
