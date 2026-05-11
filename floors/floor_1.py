"""
Floor 1: Ground — Escape!
Entry from Floor 2 via the stairwell (Room 91).
Goal: Navigate the final floor and ESCAPE through the front door!

Key rooms from BASIC source:
- Room 91: Entry from Floor 2
- Room 58: A BURGLAR'S MASK BLOCKS YOUR WAY EAST.
  HE HAS THE REMAINS OF THE KIDNAPPER IN HIS MOUTH.
  YOU CATCH A GLIMPSE OF A STAIRCASE PAST THE ALLIGATOR.
- Room 59: THERE IS A TRAP DOOR ABOVE YOU.
- Room 61: A HUGE BOG OF QUICKSAND BLOCKS YOUR WAY EAST.
  THE FRONT ENTRANCE IS THERE, WALK TO SAFETY.
  THERE IS A LARGE PIANO ON THE OTHER SIDE AND A TOO STAKE ON THIS SIDE.

WIN: Walking through the FRONT DOOR (Room 95) wins the game!
"""

FLOOR_NUMBER = 1

# --------------------------------------------------------------------
# Room definitions for Floor 1 (rooms 91-99, ground floor)
# --------------------------------------------------------------------
ROOMS = {
    # ---- Room 91: Entry from Floor 2 ----
    91: {
        "name": "ENTRANCE HALL",
        "desc": (
            "You stand in the grand entrance hall of the building. "
            "A crystal chandelier glitters overhead, casting fractured "
            "light across the marble floors. The air is cool and smells "
            "of old stone. To the EAST, you can see an ornate corridor "
            "leading deeper into the floor — and through a gap in the "
            "curtains, you catch a glimpse of SUNLIGHT. "
            "To the WEST, the corridor continues. "
            "A grand staircase leads UP — back to Floor 2."
        ),
        "exits": {"E": 92, "W": 92, "U": "floor_2"},
        "items": [],
    },

    # ---- Room 92: Grand Corridor ----
    92: {
        "name": "GRAND CORRIDOR",
        "desc": (
            "You are in a long, ornate corridor. Faded portraits of "
            "solemn-faced dignitaries line the walls. The air feels "
            "fresher here — you can almost smell the outdoors! "
            "To the EAST, a doorway leads into a side chamber. "
            "To the NORTH, a narrow passage disappears into shadow. "
            "The entrance hall is back to the WEST."
        ),
        "exits": {"W": 91, "E": 58, "N": 59},
        "items": [],
    },

    # ---- Room 58: The Alligator Chamber ----
    # From BASIC: "A BURGLAR'S MASK BLOCKS YOUR WAY EAST.
    # HE HAS THE REMAINS OF THE KIDNAPPER IN HIS MOUTH.
    # YOU CATCH A GLIMPSE OF A STAIRCASE PAST THE ALLIGATOR."
    58: {
        "name": "ALLIGATOR CHAMBER",
        "desc": (
            "You are in a dim, stone-walled chamber. "
            "A massive ALLIGATOR blocks your path — its eyes lock onto you "
            "with predatory focus. In its mouth are the REMAINS of the "
            "KIDNAPPER. A BURGLAR'S MASK dangles from one of its teeth. "
            "Through the gloom to the EAST, you glimpse a stairway "
            "leading DOWN — almost like an exit. "
            "The corridor is to the WEST."
        ),
        "exits": {"W": 92, "E": 95},
        "items": [],
    },

    # ---- Room 59: Trap Door Room ----
    # From BASIC: "THERE IS A TRAP DOOR ABOVE YOU."
    59: {
        "name": "TRAP DOOR ROOM",
        "desc": (
            "You are in a small, dusty antechamber. "
            "A heavy TRAP DOOR is set into the ceiling above you — "
            "it leads UP to Floor 2. "
            "The corridor lies to the SOUTH."
        ),
        "exits": {"S": 92, "U": "floor_2"},
        "items": [],
    },

    # ---- Room 95: FRONT DOOR — THE EXIT! ----
    95: {
        "name": "FRONT DOOR",
        "desc": (
            "You are standing before the massive FRONT DOOR of the building. "
            "Sunlight streams through the windows beside it — real, warm, "
            "natural sunlight! Freedom is inches away! "
            "Through the glass panels you can see the outside world: "
            "blue sky, green grass, open air. "
            "The door handle is right there. "
            "The corridor is back to the WEST."
        ),
        "exits": {"W": 58},
        "items": [],
    },
}


# --------------------------------------------------------------------
# Special room targets (cross-floor navigation)
# --------------------------------------------------------------------
SPECIAL_ROOMS = {
    # UP from Entrance Hall or Trap Door Room → Floor 2 (stairwell)
    "floor_2": {"target": "floor_2", "landing_room": 84},
}


# --------------------------------------------------------------------
# Floor 1 Engine
# --------------------------------------------------------------------
class Floor1Engine:
    """Engine for Floor 1 — Ground floor, the final escape!"""

    NEXT_FLOOR_DOWN = None  # No floor below — this is it!

    def __init__(self, state):
        self.state = state
        # Per-floor flags (reset each visit)
        self.alligator_dealt_with = False  # Have you dealt with the alligator?
        self.trap_door_opened = False

        # Room items (mutable per-floor copy)
        self._room_items = {}
        for rid, rdata in ROOMS.items():
            self._room_items[rid] = list(rdata["items"])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_room(self, room_id):
        """Return room data dict for the given room_id."""
        if room_id not in ROOMS:
            return None
        return ROOMS[room_id]

    def on_enter(self):
        """Called when player first arrives on Floor 1."""
        self._room_items = {}
        for rid, rdata in ROOMS.items():
            self._room_items[rid] = list(rdata["items"])
        self.alligator_dealt_with = False
        self.trap_door_opened = False

    def on_leave(self):
        """Called when player leaves Floor 1."""
        pass

    def check_win(self):
        """Returns True if the player has escaped (reached the front door
        and gone EAST through it)."""
        # Win is triggered by going EAST from room 95 (the front door)
        # This is handled in handle_command / _do_move
        return getattr(self.state, "_floor1_won", False)

    # ------------------------------------------------------------------
    # Command handling
    # ------------------------------------------------------------------
    def handle_command(self, verb, noun):
        loc = self.state.location

        # ---- LOOK ----
        if verb == "LOOK":
            return self._describe_room(loc)

        # ---- INVENTORY ----
        if verb in ("INVENTORY", "I"):
            return self._do_inventory()

        # ---- GET / TAKE ----
        if verb in ("GET", "TAKE", "GRAB"):
            return self._do_get(noun, loc)

        # ---- DROP ----
        if verb == "DROP":
            return self._do_drop(noun, loc)

        # ---- USE ----
        if verb == "USE":
            return self._do_use(noun, loc)

        # ---- OPEN ----
        if verb == "OPEN":
            return self._do_open(noun, loc)

        # ---- GO / DIRECTION ----
        if verb in (
            "NORTH", "SOUTH", "EAST", "WEST",
            "UP", "DOWN",
            "N", "S", "E", "W", "U", "D",
            "GO", "ENTER",
        ):
            return self._do_move(verb, noun, loc)

        # ---- SHOOT / KILL / ATTACK ----
        if verb in ("SHOOT", "KILL", "ATTACK", "STAB", "HIT"):
            return self._do_attack(noun, loc)

        # ---- THROW ----
        if verb == "THROW":
            return self._do_throw(noun, loc)

        return None  # Fall through to engine

    # ------------------------------------------------------------------
    # Room description
    # ------------------------------------------------------------------
    def _describe_room(self, room_id):
        room = ROOMS.get(room_id)
        if not room:
            return "You are in a dark void."

        lines = [f"== {room['name']} ==", "", room["desc"]]

        # Special: Alligator chamber description changes after dealing with it
        if room_id == 58:
            if self.alligator_dealt_with:
                lines.append("")
                lines.append(
                    "The alligator lies still — it won't be bothering anyone again."
                )

        # Special: Front door — urgency!
        if room_id == 95:
            lines.append("")
            lines.append(
                "This is it. Freedom is RIGHT THERE. "
                "Go EAST to push through the door and ESCAPE!"
            )

        # Items in the room
        items = self._room_items.get(room_id, [])
        if items:
            lines.append("")
            lines.append("You see:")
            for item in items:
                lines.append(f"  {item}")

        # Exits
        exits = room.get("exits", {})
        exit_dirs = list(exits.keys())
        if exit_dirs:
            dir_names = {
                "N": "NORTH", "S": "SOUTH",
                "E": "EAST", "W": "WEST",
                "U": "UP", "D": "DOWN",
            }
            exit_strs = [dir_names.get(d, d) for d in exit_dirs]
            lines.append("")
            lines.append(f"Exits: {', '.join(exit_strs)}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    def _do_move(self, verb, noun, loc):
        # Normalize direction
        dir_map = {
            "N": "N", "NORTH": "N",
            "S": "S", "SOUTH": "S",
            "E": "E", "EAST": "E",
            "W": "W", "WEST": "W",
            "U": "U", "UP": "U",
            "D": "D", "DOWN": "D",
        }
        if verb.upper() == "GO" or verb.upper() == "ENTER":
            direction = noun.upper().strip() if noun else None
        else:
            direction = verb.upper()

        direction = dir_map.get(direction, direction)

        if not direction:
            return "Go where?"

        room = ROOMS.get(loc)
        if not room:
            return "You are nowhere."

        # ---- Special: Room 95 (Front Door) — going EAST wins! ----
        # Check this BEFORE looking up the exit, since room 95 has no EAST exit
        if loc == 95 and direction == "E":
            self.state._floor1_won = True
            return "WIN"

        exits = room.get("exits", {})
        next_target = exits.get(direction)

        if next_target is None:
            return f"You can't go {direction} from here."

        # ---- Special: UP → Floor 2 ----
        if next_target == "floor_2":
            return f"TRANSITION:floor_2:{SPECIAL_ROOMS['floor_2']['landing_room']}"

        # ---- Alligator Chamber (Room 58) — going EAST blocked by alligator ----
        if loc == 58 and direction == "E":
            if not self.alligator_dealt_with:
                return (
                    "The ALLIGATOR lunges at you before you can make it through "
                    "the doorway! Its massive jaws snap shut — you are DEAD!\n\n"
                    "The kidnapper's pet got you just feet from freedom. "
                    "So close... yet so far.\n\n"
                    "Your body is never recovered."
                )
            else:
                # Alligator is dealt with — safe passage
                self.state.location = next_target
                return self._describe_room(next_target)

        # ---- Entrance Hall (Room 91) — EAST blocked by burglar's mask until alligator dealt with ----
        if loc == 91 and direction == "E":
            if not self.alligator_dealt_with:
                return (
                    "A BURGLAR'S MASK blocks your path! "
                    "Beyond it, the alligator waits. "
                    "You need to deal with the alligator first before "
                    "you can pass through."
                )
            else:
                self.state.location = next_target
                return self._describe_room(next_target)

        # Normal room-to-room movement
        self.state.location = next_target
        return self._describe_room(next_target)

    # ------------------------------------------------------------------
    # GET / TAKE
    # ------------------------------------------------------------------
    def _do_get(self, noun, loc):
        if not noun:
            return "Take what?"

        target = noun.upper().strip()

        room_items = self._room_items.get(loc, [])
        for item in list(room_items):
            if target.lower() in item.lower() or item.lower() in target.lower():
                room_items.remove(item)
                self._room_items[loc] = room_items
                self.state.inventory.append(item)
                return f"You take the {item}."

        return "You don't see that here."

    # ------------------------------------------------------------------
    # DROP
    # ------------------------------------------------------------------
    def _do_drop(self, noun, loc):
        if not noun:
            return "Drop what?"

        target = noun.upper().strip()

        for item in list(self.state.inventory):
            if target.lower() in item.lower() or item.lower() in target.lower():
                self.state.inventory.remove(item)
                if loc not in self._room_items:
                    self._room_items[loc] = []
                self._room_items[loc].append(item)
                return f"You drop the {item}."

        return "You're not carrying that."

    # ------------------------------------------------------------------
    # USE
    # ------------------------------------------------------------------
    def _do_use(self, noun, loc):
        if not noun:
            return "Use what?"

        target = noun.upper().strip()

        # ---- Use GUN on ALLIGATOR ----
        if ("GUN" in target or "PISTOL" in target) and loc == 58:
            if "GUN" in self.state.inventory:
                return (
                    "You draw the GUN and fire at the alligator! "
                    "The shot echoes through the chamber. "
                    "The alligator thrashes violently and then goes limp. "
                    "The burglar's mask falls from its teeth to the floor."
                )
            else:
                return "You don't have a gun."

        # ---- Use ROPE ----
        if "ROPE" in target and loc == 58:
            if "ROPE" in self.state.inventory:
                return (
                    "You try to lasso the alligator with the rope, "
                    "but it's too quick! The beast snaps at you. "
                    "You'll need something more decisive — like a GUN."
                )
            else:
                return "You don't have a rope."

        return None  # Fall through

    # ------------------------------------------------------------------
    # OPEN (trap door)
    # ------------------------------------------------------------------
    def _do_open(self, noun, loc):
        if not noun:
            return "Open what?"

        target = noun.upper().strip()

        if ("TRAP" in target or "DOOR" in target) and loc == 59:
            self.trap_door_opened = True
            return (
                "You push open the heavy TRAP DOOR in the ceiling. "
                "Dusty air rushes down from above. "
                "You can go UP to Floor 2 from here."
            )

        return None  # Fall through

    # ------------------------------------------------------------------
    # ATTACK / SHOOT
    # ------------------------------------------------------------------
    def _do_attack(self, noun, loc):
        if not noun:
            return "Attack what?"

        target = noun.upper().strip()

        # ---- Attack/Kill ALLIGATOR ----
        if (
            ("ALLIGATOR" in target or "GATOR" in target or "CROC" in target)
            and loc == 58
        ):
            if "GUN" in self.state.inventory:
                self.alligator_dealt_with = True
                return (
                    "You draw the GUN and fire! The shot hits true. "
                    "The alligator thrashes wildly, then goes still. "
                    "The burglar's mask falls from its cold, dead jaws "
                    "to the stone floor with a CLUNK.\n\n"
                    "The way EAST is now clear! Freedom awaits!"
                )
            else:
                return (
                    "You have nothing to fight the alligator with! "
                    "Its hide is too thick for fists or kicks. "
                    "You need a WEAPON — like a GUN."
                )

        # ---- Attack burglar's mask ----
        if "MASK" in target or "BURGLAR" in target:
            if loc == 58:
                return (
                    "The burglar's mask is just a mask — "
                    "it's the ALLIGATOR wearing it that's the problem. "
                    "You need to deal with the alligator itself."
                )

        return None  # Fall through

    # ------------------------------------------------------------------
    # THROW
    # ------------------------------------------------------------------
    def _do_throw(self, noun, loc):
        if not noun:
            return "Throw what?"

        target = noun.upper().strip()

        # ---- Throw GUN at alligator ----
        if "GUN" in target and loc == 58:
            return (
                "You hurl the gun at the alligator. "
                "It bounces off the beast's snout harmlessly. "
                "The alligator looks mildly annoyed. "
                "You need to shoot it, not throw things at it."
            )

        # ---- Throw anything at alligator ----
        if loc == 58:
            return (
                "You throw the item at the alligator. "
                "The beast doesn't even flinch. "
                "It watches you with cold, predatory eyes."
            )

        return None  # Fall through

    # ------------------------------------------------------------------
    # INVENTORY
    # ------------------------------------------------------------------
    def _do_inventory(self):
        if not self.state.inventory:
            return "You are carrying nothing."
        lines = ["You are carrying:"]
        for item in self.state.inventory:
            lines.append(f"  {item}")
        return "\n".join(lines)
