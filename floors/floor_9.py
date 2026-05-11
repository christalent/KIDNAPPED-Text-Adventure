"""
KIDNAPPED! - Floor 9: The Roof
Starting floor — must escape down through the building.
All exits verified bidirectional.
"""

FLOOR_NUMBER = 9
NEXT_FLOOR_DOWN = 8

# --------------------------------------------------------------------
# Room map (verified bidirectional):
#  1: N=2, S=7, E=8
#  2: S=1, N=3
#  3: S=2 (dead end)
#  4: W=5, S=6
#  5: E=4
#  6: N=4 (dead end)
#  7: N=1 (dead end)
#  8: N=9, W=1, S=10
#  9: S=8, U=11, D=10
# 10: N=8, U=9
# 11: D=9, E=13, W=15
# 13: W=11, S=16, E=14
# 14: W=13
# 15: E=11, W=17
# 16: N=13, E=17
# 17: W=16, E=15
# --------------------------------------------------------------------
ROOMS = {
    1: {"name": "IN AN ELEVATOR", "desc": "You stand inside an old elevator car. The walls are scratched and graffitied. The elevator is dead. A small cabinet is mounted on the wall.", "exits": {"N": 2, "S": 7, "E": 8}, "items": []},
    2: {"name": "IN AN OFFICE", "desc": "A dusty office. Papers scattered. A portable FLASHLIGHT sits on a filing cabinet.", "exits": {"N": 3, "S": 1}, "items": ["FLASHLIGHT"]},
    3: {"name": "IN A CLOSET", "desc": "A cramped supply closet. A sturdy wooden CHAIR has been left behind.", "exits": {"S": 2}, "items": ["CHAIR"]},
    4: {"name": "ON THE ROOF", "desc": "On the flat roof. Night wind cuts through your clothes. A battered BROOM leans against a ventilation unit.", "exits": {"W": 5, "S": 6}, "items": ["BROOM"]},
    5: {"name": "IN A LARGE ROOM", "desc": "A large room. A broken TV SET, a dead CLOCK on the wall (midnight), a LOCKED DOOR barred shut.", "exits": {"E": 4}, "items": ["TV SET", "CLOCK", "LOCKED DOOR"]},
    6: {"name": "IN A RESTROOM", "desc": "A foul-smelling restroom. Someone scratched GRAFFITI into the wall.", "exits": {"N": 4}, "items": ["GRAFFITI ON WALL"]},
    7: {"name": "IN AN OFFICE", "desc": "A small executive office. Through the window, a KEY rests on the ledge outside.", "exits": {"N": 1}, "items": [], "special_desc": "A KEY ON A KEY CHAIN rests on the ledge."},
    8: {"name": "IN AN ELEVATOR", "desc": "Another dead elevator car. The doors are jammed.", "exits": {"N": 9, "W": 1, "S": 10}, "items": []},
    9: {"name": "IN AN ELEVATOR", "desc": "A third dead elevator car. A PUSH BUTTON is on the wall.", "exits": {"S": 8, "U": 11, "D": 10}, "items": ["PUSH BUTTON"]},
    10: {"name": "IN THE CRAWLSPACE ABOVE THE ELEVATOR", "desc": "A tight crawlspace above the shaft. Pipes and conduits. Very dark.", "exits": {"N": 8, "U": 9}, "items": []},
    11: {"name": "IN AN ELEVATOR SHAFT", "desc": "Inside the elevator shaft. Twisted, sparking WIRES hang from a junction box. A sign reads 'ADMISSION.'", "exits": {"D": 9, "E": 13, "W": 15}, "items": ["WIRES", "ADMISSION"]},
    13: {"name": "IN A VISITOR'S LOUNGE", "desc": "A dingy lounge. Worn couches. A SMALL KEY is hooked on a frame.", "exits": {"W": 11, "S": 16, "E": 14}, "items": ["SMALL KEY"]},
    14: {"name": "IN A SMALL ROOM", "desc": "A small, bare room. Nothing of interest.", "exits": {"W": 13}, "items": []},
    15: {"name": "IN A CLOSET", "desc": "A storage closet. A roll of ELECTRIC TAPE sits on a shelf.", "exits": {"E": 11, "W": 17}, "items": ["TAPE"]},
    16: {"name": "IN A SMALL ROOM", "desc": "An old nursery — a baby's crib with rusted bars.", "exits": {"N": 13, "E": 17}, "items": []},
    17: {"name": "IN A STORAGE ROOM", "desc": "A cramped storage room. Old boxes and cobwebs.", "exits": {"W": 16, "E": 15}, "items": []},
}


class Floor9Engine:
    def __init__(self, state):
        self.state = state
        self.key_taken = False
        self.cabinet_open = False
        self.tape_used = False
        self.elevator_fixed = False
        self._key_on_ledge = True
        self._room_items = {rid: list(r["items"]) for rid, r in ROOMS.items()}

    def get_room(self, rid):
        if rid not in ROOMS:
            return None
        r = dict(ROOMS[rid])
        r["id"] = rid
        r["items"] = list(self._room_items.get(rid, []))
        return r

    def on_enter(self):
        self.state.floor = FLOOR_NUMBER
        self.state.location = 1
        self.state.dark = False
        self.state.flashlight_on = False
        self.__init__(self.state)

    def handle_command(self, verb, noun):
        verb = verb.upper()
        noun = noun.upper().strip()
        if verb in ("TAKE", "GRAB", "PICK"):
            verb = "GET"
        if verb in ("PUT", "PLACE"):
            verb = "DROP"
        loc = self.state.location

        if verb in ("N", "NORTH") or (verb == "GO" and noun in ("N", "NORTH")):
            return self._go("N"), False
        if verb in ("S", "SOUTH") or (verb == "GO" and noun in ("S", "SOUTH")):
            return self._go("S"), False
        if verb in ("E", "EAST") or (verb == "GO" and noun in ("E", "EAST")):
            return self._go("E"), False
        if verb in ("W", "WEST") or (verb == "GO" and noun in ("W", "WEST")):
            return self._go("W"), False
        if verb in ("U", "UP") or (verb == "GO" and noun in ("U", "UP")):
            return self._go("U"), False
        if verb in ("D", "DOWN") or (verb == "GO" and noun in ("D", "DOWN")):
            return self._go_down()

        if verb in ("LOOK", "L"):
            return self._look(), False
        if verb == "GET":
            return self._get(noun), False
        if verb == "DROP":
            return self._drop(noun), False
        if verb in ("USE", "APPLY", "TAPE"):
            return self._use(noun), False
        if verb in ("OPEN", "UNLOCK"):
            return self._open(noun), False
        if verb in ("EXAMINE", "READ", "X", "CHECK"):
            return self._examine(noun), False
        if verb in ("PUSH", "PRESS"):
            return self._push(noun)
        if verb in ("FIX", "REPAIR"):
            return self._use("TAPE"), False
        return "You can't do that.", False

    def _go(self, d):
        r = self.get_room(self.state.location)
        if d not in r["exits"]:
            return "You can't go that way."
        self.state.location = r["exits"][d]
        return self._look()

    def _go_down(self):
        loc = self.state.location
        r = self.get_room(loc)
        if "D" not in r["exits"]:
            return "You can't go that way.", False
        if self.elevator_fixed:
            self.state.floor = NEXT_FLOOR_DOWN
            return "The elevator groans and descends. Ding! Floor 8.\n\nA damp, fishy smell...", True
        return "The elevator is dead — the wires need to be repaired first.", False

    def _look(self):
        loc = self.state.location
        r = self.get_room(loc)
        lines = [f"**{r['name']}**", r["desc"]]
        if loc == 7 and self._key_on_ledge:
            lines.append(r.get("special_desc", ""))
        items = self._room_items.get(loc, [])
        if items:
            lines.append(f"Things: {', '.join(items)}.")
        lines.append(f"Exits: {', '.join(r['exits'].keys())}.")
        return "\n".join(lines)

    def _get(self, noun):
        loc = self.state.location
        nm = {"FLASHLIGHT": "FLASHLIGHT", "CHAIR": "CHAIR", "BROOM": "BROOM",
              "TV": "TV SET", "TV SET": "TV SET", "CLOCK": "CLOCK",
              "LOCKED DOOR": "LOCKED DOOR", "DOOR": "LOCKED DOOR",
              "GRAFFITI": "GRAFFITI ON WALL", "GRAFFITI ON WALL": "GRAFFITI ON WALL",
              "WIRES": "WIRES", "LIVE WIRES": "WIRES", "ADMISSION": "ADMISSION",
              "TAPE": "TAPE", "ELECTRIC TAPE": "TAPE",
              "SMALL KEY": "SMALL KEY", "KEY": "SMALL KEY",
              "KEY ON KEY CHAIN": "KEY ON A KEY CHAIN", "KEY ON A KEY CHAIN": "KEY ON A KEY CHAIN",
              "PUSH BUTTON": "PUSH BUTTON", "BUTTON": "PUSH BUTTON"}
        t = nm.get(noun)
        if not t:
            return f"No '{noun}' here."
        if noun in ("KEY", "KEY ON KEY CHAIN", "KEY ON A KEY CHAIN") and loc == 7:
            if not self._key_on_ledge:
                return "The key is gone."
            self._key_on_ledge = False
            self.state.add_item("KEY ON A KEY CHAIN")
            return "You reach out the window and snag the key chain!"
        items = self._room_items.get(loc, [])
        if t not in items:
            return f"No {t} here."
        if t in ("GRAFFITI ON WALL", "ADMISSION", "LOCKED DOOR", "WIRES", "PUSH BUTTON"):
            return f"The {t} can't be taken."
        items.remove(t)
        self.state.add_item(t)
        return f"You take the {t}."

    def _drop(self, noun):
        inv = self.state.inventory
        nm = {"FLASHLIGHT": "FLASHLIGHT", "CHAIR": "CHAIR", "BROOM": "BROOM",
              "TAPE": "TAPE", "SMALL KEY": "SMALL KEY", "KEY": "SMALL KEY",
              "KEY ON A KEY CHAIN": "KEY ON A KEY CHAIN"}
        t = nm.get(noun)
        if not t or t not in inv:
            return f"You're not carrying a {noun}."
        self.state.remove_item(t)
        self._room_items.setdefault(self.state.location, []).append(t)
        return f"You drop the {t}."

    def _use(self, noun):
        loc = self.state.location
        inv = self.state.inventory
        if noun in ("TAPE", "ELECTRIC TAPE", "WIRES", "WIRE", "TAPE ON WIRES"):
            if "TAPE" not in inv:
                return "You don't have tape."
            if loc != 11:
                return "No wires to tape here."
            if self.tape_used:
                return "Already taped."
            self.tape_used = True
            self.elevator_fixed = True
            return "You wrap tape around the wires. Sparks stop. The elevator is FIXED!"
        if noun in ("KEY", "SMALL KEY", "KEY ON A KEY CHAIN"):
            if loc == 1 and "KEY ON A KEY CHAIN" in inv:
                if not self.cabinet_open:
                    self.cabinet_open = True
                    self._room_items[1].append("FLASHLIGHT")
                    return "You unlock the cabinet. A FLASHLIGHT inside!"
            return "Nothing to unlock here."
        if noun in ("FLASHLIGHT", "LIGHT"):
            if "FLASHLIGHT" not in inv:
                return "No flashlight."
            self.state.flashlight_on = True
            return "Click. Light cuts the darkness."
        return f"Can't use the {noun}."

    def _open(self, noun):
        loc = self.state.location
        if noun == "CABINET":
            if loc != 1:
                return "No cabinet here."
            if self.cabinet_open:
                return "Already open."
            if "KEY ON A KEY CHAIN" not in self.state.inventory:
                return "Locked. Need a key."
            self.cabinet_open = True
            self._room_items[1].append("FLASHLIGHT")
            return "You unlock. A FLASHLIGHT inside!"
        if noun == "LOCKED DOOR" and loc == 5:
            return "Barred shut."
        return "Can't open that."

    def _examine(self, noun):
        loc = self.state.location
        if noun in ("GRAFFITI", "GRAFFITI ON WALL") and loc == 6:
            return "'MATCH WIT FOR LIVE WIRES.'"
        if noun in ("WIRES", "LIVE WIRES") and loc == 11:
            return "Live wires, sparking. Need tape." if not self.tape_used else "Wires taped, fixed."
        if noun in ("ADMISSION", "SIGN") and loc == 11:
            return "'ADMISSION: $1.00.' Old prices."
        if noun == "CLOCK" and loc == 5:
            return "Frozen at midnight."
        if noun in ("TV", "TV SET") and loc == 5:
            return "Cracked screen. Dead."
        if noun in ("KEY", "KEY ON KEY CHAIN") and loc == 7 and self._key_on_ledge:
            return "A key on a key chain on the ledge outside."
        if noun == "CABINET" and loc == 1:
            return "Small metal cabinet." + (" Open." if self.cabinet_open else " Locked.")
        if noun == "BROOM" and loc == 4:
            return "Battered broom."
        if noun in ("PUSH BUTTON", "BUTTON") and loc == 9:
            return "Controls the elevator."
        return f"You examine the {noun}."

    def _push(self, noun):
        if noun in ("BUTTON", "PUSH BUTTON"):
            return self._go_down()
        return "Can't push that."

    @staticmethod
    def verify_exits():
        errors = []
        opp = {"N": "S", "S": "N", "E": "W", "W": "E", "U": "D", "D": "U"}
        for rid, r in ROOMS.items():
            for d, t in r["exits"].items():
                ro = opp[d]
                if ro not in ROOMS.get(t, {}).get("exits", {}):
                    errors.append(f"Room {rid} → {d}={t}, but {t} has no {ro}")
                elif ROOMS[t]["exits"][ro] != rid:
                    errors.append(f"Room {rid} → {d}={t}, but {t} → {ro}={ROOMS[t]['exits'][ro]}")
        return errors


if __name__ == "__main__":
    e = Floor9Engine.verify_exits()
    if e:
        print(f"❌ {len(e)} errors:")
        for x in e:
            print(f"  {x}")
    else:
        print(f"✅ All exits bidirectional ({len(ROOMS)} rooms)")
