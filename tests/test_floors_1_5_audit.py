#!/usr/bin/env python3
"""
Floors 1-5 against the pixel-verified audit table.

Every expectation here comes from audit/floors_1_5_verified.json - the
machine-readable form of audit/FLOORS_1_5_GROUND_TRUTH.md, whose room
table and DATA item placement were read off the listing pixels.  The
floor modules are the thing under test, so this file never asks a
module what the answer is.

Checked per floor:
  * the room set, the room names and the exit tables
  * every room dict carries name/desc/exits/items
  * fixed scenery placement (FIXED_ITEMS) and movable placement
    (ITEM_ROOMS) against the audit's DATA placement
  * item aliases (the walkthroughs spell objects differently)
  * the entry room and the floor below
  * VERB_LINK_PAIRS is declared, so the map checker can see the
    handler transitions that the room table cannot express

Run:  python3 tests/test_floors_1_5_audit.py
"""

import importlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

with open(os.path.join(ROOT, "audit", "floors_1_5_verified.json")) as fh:
    AUDIT = json.load(fh)


def norm(value):
    """Room names differ only in trailing punctuation between the
    listing and the module; compare them on their substance."""
    return " ".join(str(value or "").split()).rstrip(".").upper()


errors = []

for floor in ("5", "4", "3", "2", "1"):
    mod = importlib.import_module("floors.floor_%s" % floor)
    data = AUDIT[floor]
    jrooms = {int(rid): entry for rid, entry in data["room"].items()}

    if set(mod.ROOMS) != set(jrooms):
        errors.append("floor %s: rooms %s != audit %s"
                      % (floor, sorted(mod.ROOMS), sorted(jrooms)))

    for rid in sorted(jrooms):
        name, desc, exits, items = jrooms[rid]
        room = mod.ROOMS.get(rid)
        if room is None:
            continue
        if norm(room.get("name")) != norm(name):
            errors.append("floor %s room %d: name %r != audit %r"
                          % (floor, rid, room.get("name"), name))
        module_exits = {k.upper(): v for k, v in room.get("exits", {}).items()}
        audit_exits = {k.upper(): v for k, v in exits.items()}
        if module_exits != audit_exits:
            errors.append("floor %s room %d: exits %r != audit %r"
                          % (floor, rid, module_exits, audit_exits))
        if list(room.get("items", [])) != list(items):
            errors.append("floor %s room %d: items %r != audit %r"
                          % (floor, rid, list(room.get("items", [])), list(items)))
        for key in ("name", "desc", "exits", "items"):
            if key not in room:
                errors.append("floor %s room %d: missing '%s'" % (floor, rid, key))

    if dict(mod.FIXED_ITEMS) != dict(data["fixed"]):
        errors.append("floor %s: FIXED_ITEMS %r != audit %r"
                      % (floor, mod.FIXED_ITEMS, data["fixed"]))
    if dict(mod.ITEM_ROOMS) != dict(data["movable"]):
        errors.append("floor %s: ITEM_ROOMS %r != audit %r"
                      % (floor, mod.ITEM_ROOMS, data["movable"]))
    if dict(mod.ITEM_ALIASES) != dict(data["aliases"]):
        errors.append("floor %s: ITEM_ALIASES %r != audit %r"
                      % (floor, mod.ITEM_ALIASES, data["aliases"]))
    if mod.ENTRY_ROOM != data["entry"]:
        errors.append("floor %s: ENTRY_ROOM %r != audit %r"
                      % (floor, mod.ENTRY_ROOM, data["entry"]))
    if (mod.NEXT_FLOOR_DOWN or None) != (data["nextdown"] or None):
        errors.append("floor %s: NEXT_FLOOR_DOWN %r != audit %r"
                      % (floor, mod.NEXT_FLOOR_DOWN, data["nextdown"]))
    if not getattr(mod, "VERB_LINK_PAIRS", None):
        errors.append("floor %s: no VERB_LINK_PAIRS declared" % floor)

if errors:
    print("FLOORS 1-5 AUDIT: FAIL")
    for error in errors:
        print("  - " + error)
    sys.exit(1)

print("FLOORS 1-5 AUDIT: PASS (rooms, exits, item placement and "
      "floor links match the verified audit table)")
