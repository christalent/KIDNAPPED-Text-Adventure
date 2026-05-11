#!/usr/bin/env python3
"""
KIDNAPPED! - A Text Adventure
Based on the BASIC game by Peter Kirsch (1980)
Converted to Python by Lemmy

You awaken on the 9th floor of a strange building, the victim of a kidnapping.
The kidnapper is elsewhere, busy counting the ransom money. Your only job is to
escape from the building, floor by floor. You must beware of the kidnapper,
and stay alive. Many traps have been set, so be careful!

9 floors, 65+ locations. Each floor is independent - items don't carry over.
"""

import sys
import os

# Game state
class GameState:
    def __init__(self):
        # Current location
        self.location = 1  # Starting room
        self.floor = 9     # Start on floor 9 (top)

        # Flags for each floor
        self.time = -2     # Time counter (floor 9 only)
        self.dark = False  # Dark flag
        self.flashlight_on = False

        # Item flags
        self.cabinet_open = False
        self.flashlight_seen = False
        self.tape_used = False
        self.elevator_fixed = False

        # Player inventory
        self.inventory = []

        # Floor-specific flags will be reset each floor
        self.reset_floor_flags()

    def add_item(self, item):
        """Add an item to the player's inventory."""
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_item(self, item):
        """Remove an item from the player's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)

    def has_item(self, item):
        """Check if player has an item."""
        return item in self.inventory

    def reset_floor_flags(self):
        """Reset all flags when changing floors"""
        # Floor 9 flags
        self.key_taken = False
        self.cabinet_open = False
        self.flashlight_seen = False
        self.tape_used = False
        self.elevator_fixed = False

        # Floor 8 flags
        self.piranha_dead = False
        self.rope_taken = False
        self.rope_tied = False
        self.glue_taken = False
        self.balloon_inflated = False
        self.balloon_taken = False
        self.helium_taken = False

        # Floor 7 flags - VAULT (Bank Vault floor)
        self.vault_door_unlocked = False  # Steel vault door unlocked
        self.step_glued = False          # Loose step on bank floor fixed with glue
        self.small_key_taken = False     # Small key from key room taken
        self.vending_used = False        # Vending machine activated with tin foil
        self.tin_foil_taken = False      # Tin foil picked up
        self.solution_taken = False      # Solution/fluid picked up

        # Floor 6 flags - OFFICE
        self.floor6_balloon_inflated = False
        self.floor6_dollar_taken = False
        self.floor6_vending_paid = False
        self.floor6_string_tied = False
        self.floor6_jumped = False
        self.floor6_balloon_taken = False
        self.floor6_string_taken = False
        self.floor6_button_pressed = False

        # Floor 5 flags - Mary Poppins / Weird floor
        self.floor5_clothes_knitted = False
        self.floor5_small_key_taken = False
        self.floor5_door_unlocked = False
        self.floor5_umbrella_taken = False
        self.floor5_sponge_taken = False
        self.floor5_pool_dry = False

        # Floor 4 flags - Jekyll/Hyde Lab
        self.floor4_pool_drained = False
        self.floor4_umbrella_taken = False
        self.floor4_umbrella_opened = False
        self.floor4_jumped = False
        self.floor4_potion_taken = False
        self.jekyll_mode = False  # Jekyll/Hyde transformation flag

        # Floor 3 flags - Plant/Trap floor
        self.floor3_fluid_drunk = False   # Drank the mysterious fluid (transforms into plant)
        self.floor3_solution_drunk = False  # Drank the solution (alternative drink)
        self.floor3_door_opened = False    # Vine passage / door opened after plant transformation
        self.floor3_flute_taken = False    # Flute picked up
        self.floor3_flute_played = False    # Flute played to descend

        # Floor 2 flags - Quicksand/Piano floor
        self.floor2_rope_taken = False    # Picked up the rope
        self.floor2_rope_tied = False     # Rope tied to stake
        self.floor2_rope_stretched = False # Rope stretched across quicksand (can cross)
        self.floor2_piano_played = False   # Piano has been played
        self.floor2_piano_room_visited = False  # Visited the piano room

        # Floor 1 flags - Escape floor
        self.floor1_at_front_door = False  # At the front door area

# Rooms for each floor
FLOOR_ROOMS = {
    # Floor 9 - Roof level (rooms 1-20)
    9: {
        1: {"name": "ELEVATOR", "desc": "IN AN ELEVATOR.", "exits": {"S": 10}, "items": []},
        2: {"name": "ROOF", "desc": "ON THE ROOF.", "exits": {"N": 10}, "items": []},
        3: {"name": "CLOSET", "desc": "IN A CLOSET.", "exits": {"N": 10, "S": 2}, "items": []},
        4: {"name": "RESTROOM", "desc": "IN A RESTROOM.", "exits": {"S": 10}, "items": []},
        5: {"name": "LARGE ROOM", "desc": "IN A LARGE ROOM.", "exits": {"N": 10}, "items": []},
        6: {"name": "ELEVATOR SHAFT", "desc": "IN AN ELEVATOR SHAFT.", "exits": {"U": 1, "D": 10}, "items": []},
        7: {"name": "NARROW LEDGE", "desc": "ON A VERY NARROW LEDGE.", "exits": {"S": 10, "W": 11}, "items": ["KEY"]},
        8: {"name": "VISITOR'S LODGE", "desc": "IN A VISITOR'S LODGE.", "exits": {"W": 13}, "items": []},
        9: {"name": "CLOSET", "desc": "IN A CLOSET.", "exits": {"E": 13}, "items": []},
        10: {"name": "HALLWAY", "desc": "IN A HALLWAY.", "exits": {"W": 11, "E": 13, "N": 4, "S": 5}, "items": []},
        11: {"name": "MAIN ROOM", "desc": "IN A MAIN ROOM.", "exits": {"U": 6, "D": 12, "W": 14, "E": 13}, "items": []},
        12: {"name": "NARROW STAIRWAY", "desc": "IN A NARROW STAIRWAY.", "exits": {"D": 10}, "items": []},
        13: {"name": "CRAWLSPACE", "desc": "IN A CRAWLSPACE ON TOP OF THE ELEVATOR.", "exits": {"E": 11, "W": 8}, "items": ["LIVE WIRES"]},
        14: {"name": "STORAGE", "desc": "IN A SMALL STORAGE ROOM.", "exits": {"N": 13, "E": 11}, "items": []},

    },
    # Floor 8 - (placeholder - need full map)
    8: {
        16: {"name": "AQUARIUM ROOM", "desc": "YOU ARE IN A ROOM WITH A LARGE AQUARIUM.", "exits": {}, "items": []},
    },
    # Floor 7 - Vault floor
    7: {
        # Placeholder - full map needed
    },
    # Floor 6 - Office floor
    6: {
        # Placeholder - full map needed
    },
    # Floor 5 - Mary Poppins floor
    5: {
        # Placeholder
    },
    # Floor 4 - Jekyll/Hyde floor
    4: {
        # Placeholder
    },
    # Floor 3 - Plant/trap floor
    3: {
        # Placeholder
    },
    # Floor 2 - Quicksand/piano floor
    2: {
        # Placeholder
    },
    # Floor 1 - Ground floor (escape!)
    1: {
        # Placeholder
    }
}

class KidnappedGame:
    def __init__(self):
        self.state = GameState()
        self.running = True
        self.rooms = self.build_rooms()
        # Inventory is accessed via state.inventory (property below)
        self._player_inventory = []

    @property
    def player_inventory(self):
        """Redirect all inventory access to state.inventory for consistency."""
        return self.state.inventory

    @player_inventory.setter
    def player_inventory(self, value):
        """Setter redirects to state.inventory."""
        self.state.inventory = value

    def build_rooms(self):
        """Build complete room database"""
        rooms = {}

        # ============= FLOOR 9 - ROOF LEVEL =============
        rooms[1] = {"name": "ELEVATOR", "desc": "YOU ARE IN AN ELEVATOR.", "exits": {"S": 10}, "items": [], "floor": 9}
        rooms[2] = {"name": "ROOF", "desc": "YOU ARE ON THE ROOF.", "exits": {"N": 10}, "items": [], "floor": 9}
        rooms[3] = {"name": "CLOSET", "desc": "YOU ARE IN A CLOSET.", "exits": {"N": 10, "S": 2}, "items": [], "floor": 9}
        rooms[4] = {"name": "RESTROOM", "desc": "YOU ARE IN A RESTROOM.", "exits": {"S": 10}, "items": [], "floor": 9}
        rooms[5] = {"name": "LARGE ROOM", "desc": "YOU ARE IN A LARGE ROOM.", "exits": {"N": 10}, "items": [], "floor": 9}
        rooms[6] = {"name": "ELEVATOR SHAFT", "desc": "YOU ARE IN AN ELEVATOR SHAFT. THERE IS A CRAWLSPACE ABOVE THE ELEVATOR.", "exits": {"U": 1, "D": 10}, "items": [], "floor": 9}
        rooms[7] = {"name": "NARROW LEDGE", "desc": "YOU ARE ON A VERY NARROW LEDGE OUTSIDE THE WINDOW.", "exits": {"S": 10, "W": 11}, "items": ["KEY"], "floor": 9}
        rooms[8] = {"name": "VISITOR'S LODGE", "desc": "YOU ARE IN A VISITOR'S LODGE.", "exits": {"W": 13}, "items": [], "floor": 9}
        rooms[9] = {"name": "CLOSET", "desc": "YOU ARE IN A CLOSET.", "exits": {"E": 13}, "items": [], "floor": 9}
        rooms[10] = {"name": "HALLWAY", "desc": "YOU ARE IN A HALLWAY. THE ELEVATOR IS HERE.", "exits": {"W": 11, "E": 13, "N": 4, "S": 5}, "items": [], "floor": 9}
        rooms[11] = {"name": "MAIN ROOM", "desc": "YOU ARE IN A MAIN ROOM. THERE IS A BROOM HERE.", "exits": {"U": 6, "D": 12, "W": 14, "E": 13}, "items": ["BROOM"], "floor": 9}
        rooms[12] = {"name": "NARROW STAIRWAY", "desc": "YOU ARE IN A NARROW STAIRWAY.", "exits": {"D": 10}, "items": [], "floor": 9}
        rooms[13] = {"name": "CRAWLSPACE", "desc": "YOU ARE IN A CRAWLSPACE ON TOP OF THE ELEVATOR. THERE ARE LIVE ELECTRICAL WIRES HERE.", "exits": {"E": 11, "W": 8}, "items": ["WIRES"], "floor": 9}
        rooms[14] = {"name": "STORAGE", "desc": "YOU ARE IN A SMALL STORAGE ROOM. THERE IS A ROLL OF ELECTRIC TAPE HERE.", "exits": {"N": 13, "E": 11}, "items": ["TAPE"], "floor": 9}

        # ============= FLOOR 8 - AQUARIUM =============
        # Floor 8 has 9 rooms (21-29) with an aquarium/pool theme
        # The piranha pool blocks your path - you need to use rope or balloon to cross

        # Room 21: Elevator landing / Aquarium anteroom
        rooms[21] = {"name": "AQUARIUM ANTEROOM", "desc": "YOU ARE IN A SMALL ROOM AT THE TOP OF THE ELEVATOR. A DOORWAY TO THE NORTH LEADS INTO A LARGE ROOM.", "exits": {"N": 22, "U": 10}, "items": [], "floor": 8}

        # Room 22: Main aquarium room with piranhas and pool
        rooms[22] = {"name": "AQUARIUM", "desc": "YOU ARE IN A VAST ROOM WITH A LARGE INDOOR POOL. THE POOL SPANS THE ENTIRE ROOM, DIVIDING IT NORTH AND SOUTH. THE WATER IS MURKY AND DARK. YOU CAN SEE SOMETHING SHARP MOVING IN THE WATER... PIRANHAS!", "exits": {"S": 21, "N": 23}, "items": [], "floor": 8}

        # Room 23: South side of pool - need rope to cross north
        rooms[23] = {"name": "POOL SOUTH SIDE", "desc": "YOU ARE ON THE SOUTH SIDE OF THE HUGE AQUARIUM POOL. THE WATER IS RIGHT THERE, AND YOU CAN SEE THE PIRANHAS SWIMMING. TO THE NORTH IS THE AQUARIUM POOL ITSELF. THERE IS NO WAY TO CROSS THE POOL WITHOUT GOING THROUGH THE WATER - AND THAT WOULD BE SUICIDE!", "exits": {"N": 22, "S": 21}, "items": [], "floor": 8}

        # Room 24: North side of pool - storage area
        rooms[24] = {"name": "AQUARIUM STORAGE", "desc": "YOU ARE IN A STORAGE AREA ON THE NORTH SIDE OF THE AQUARIUM. THERE IS A LARGE DEFALTED BALLOON HERE, AND A TANK OF HELIUM GAS.", "exits": {"S": 25, "E": 22}, "items": ["BALLOON", "HELIUM"], "floor": 8}

        # Room 25: West corridor with rope
        rooms[25] = {"name": "WEST CORRIDOR", "desc": "YOU ARE IN A CORRIDOR ON THE WEST SIDE OF THE AQUARIUM. THERE IS A COIL OF ROPE ON THE FLOOR.", "exits": {"E": 24, "W": 26}, "items": ["ROPE"], "floor": 8}

        # Room 26: Small room with super glue
        rooms[26] = {"name": "SMALL ROOM", "desc": "YOU ARE IN A SMALL ROOM. THERE IS A JAR OF SUPER GLUE HERE.", "exits": {"E": 25}, "items": ["GLUE"], "floor": 8}

        # Room 27: East side of aquarium
        rooms[27] = {"name": "EAST CORRIDOR", "desc": "YOU ARE IN A CORRIDOR ON THE EAST SIDE OF THE AQUARIUM. THE POOL IS TO THE WEST.", "exits": {"W": 24}, "items": [], "floor": 8}

        # Room 28: Observation room - view of piranhas
        rooms[28] = {"name": "OBSERVATION ROOM", "desc": "YOU ARE IN A SMALL OBSERVATION ROOM WITH A GLASS WALL OVERLOOKING THE PIRANHA POOL. THE PIRANHAS ARE HUGE AND VERY ALERT. A SIGN ON THE WALL READS: 'DO NOT FEED THE FISH - THEY DON'T NEED TO BE FED.'", "exits": {"W": 27}, "items": [], "floor": 8}

        # Room 29: Stairway down to Floor 7
        rooms[29] = {"name": "STAIRS DOWN", "desc": "YOU ARE AT THE TOP OF A WOODEN STAIRWAY LEADING DOWN. THE STAIRS LOOK A LITTLE ROTTEN.", "exits": {"N": 27, "D": 31}, "items": [], "floor": 8}

        # ============= FLOOR 7 - VAULT =============
        # Vault structure: Rooms 31-39 + 55-57
        # Special action-based navigation (not standard N/S/E/W)
        # Key puzzle: Find small key (room 37) to unlock vault door (room 55)
        # Step hazard: The bank floor has a loose step - need GLUE from Floor 8
        # Vending machine: Use TIN FOIL at vending machine for payout

        # Room 31: Bank floor - entry from stairs down (from Floor 8)
        rooms[31] = {"name": "BANK FLOOR - ENTRY", "desc": "YOU ARE IN THE BANK FLOOR ENTRY AREA. AN ANCIENT MARBLE STAIRCASE LEADS DOWN FROM ABOVE. THERE IS A HEAVY DOOR TO THE EAST WITH 'VAULT' INSCRIBED ABOVE IT.", "exits": {"U": 29, "E": 32}, "items": [], "floor": 7}

        # Room 32: Vault corridor/anteroom
        rooms[32] = {"name": "VAULT ANTEROOM", "desc": "YOU ARE IN A CORRIDOR OUTSIDE THE VAULT. A SIGN ON THE WALL READS: 'VAULT DIAL: 32-55-57'. A STRING VENDING MACHINE HUMS IN THE CORNER. THERE ARE PASSAGES TO THE NORTH (KEY ROOM), SOUTH (CHEMICAL STORAGE), AND THE VAULT DOOR IS TO THE EAST.", "exits": {"W": 31, "N": 37, "S": 56, "E": 55}, "items": ["TIN FOIL"], "floor": 7}

        # Room 33: Side room with tin foil
        rooms[33] = {"name": "SIDE STORAGE", "desc": "YOU ARE IN A SMALL STORAGE AREA OFF THE CORRIDOR. THERE IS A ROLL OF TIN FOIL HERE.", "exits": {"E": 32}, "items": ["TIN FOIL"], "floor": 7}

        # Room 34: Vault mechanism room (combination room)
        rooms[34] = {"name": "VAULT MECHANISM ROOM", "desc": "YOU ARE IN A SMALL ROOM WITH GEARS AND LEVERS. A DIAL WITH NUMBERS 00-99 IS SET INTO THE WALL. A PLAQUE READS: 'AUTHORIZED PERSONNEL ONLY'.", "exits": {"S": 32}, "items": [], "floor": 7}

        # Room 35: Guard post / kidnapper room
        rooms[35] = {"name": "GUARD POST", "desc": "YOU ARE IN A SMALL GUARD POST. THE KIDNAPPER IS HERE, COUNTING HIS MONEY. HE LOOKS UP AND SEES YOU! HIS HAND REACHES FOR A GUN!", "exits": {"W": 32}, "items": [], "floor": 7}

        # Room 36: Manager's office
        rooms[36] = {"name": "MANAGER'S OFFICE", "desc": "YOU ARE IN A SMALL MANAGER'S OFFICE. FILING CABINETS LINE THE WALLS. A DESK WITH SCRATCHED PAPERS SITS IN THE CENTER.", "exits": {"S": 32}, "items": [], "floor": 7}

        # Room 37: Key room - the small key is here
        rooms[37] = {"name": "KEY ROOM", "desc": "YOU ARE IN A SMALL KEY ROOM. ON THE WALL IS A HOOK WITH A SMALL BRASS KEY. A SMALL SIGN READS: 'VAULT KEY'.", "exits": {"S": 32}, "items": ["SMALL KEY"], "floor": 7}

        # Room 38: Safe deposit boxes
        rooms[38] = {"name": "SAFE DEPOSIT BOXES", "desc": "YOU ARE IN A ROOM FILLED WITH SAFE DEPOSIT BOXES. EACH ONE IS STRONG STEEL, DENTED AND SCRATCHED FROM YEARS OF USE.", "exits": {"W": 37}, "items": [], "floor": 7}

        # Room 39: Old vault entrance (before the new one was built)
        rooms[39] = {"name": "OLD VAULT ENTRANCE", "desc": "YOU ARE AT AN OLD ABANDONED VAULT ENTRANCE. THE DOOR HAS BEEN SEALED SHUT. THE NEW VAULT IS THROUGH THE DOOR TO THE EAST.", "exits": {"E": 32}, "items": [], "floor": 7}

        # Room 55: The Vault - steel door, requires small key
        rooms[55] = {"name": "THE VAULT", "desc": "YOU ARE IN THE VAULT! SOLID STEEL WALLS SURROUND YOU. THE DOOR BEHIND YOU IS A MASSIVE STEEL PLATE. ON THE FAR WALL IS THE FAMOUS GOLD'S SLIDE - A FIREMAN'S POLE-LIKE SLIDE FOR QUICK EVACUATION OF GOLD BARS. A SIGN ON THE SLIDE READS: 'LEADS TO FLOOR 6'. THE DIAL ON THE DOOR SHOWS: 32-55-57.", "exits": {"W": 32}, "items": [], "floor": 7}

        # Room 56: Chemical storage - solution and fluid
        rooms[56] = {"name": "CHEMICAL STORAGE", "desc": "YOU ARE IN A CHEMICAL STORAGE ROOM. THERE ARE BOTTLES OF VARIOUS SOLUTIONS. LABELS READ: 'SOLUTION: ANTIMATTER', 'FLUID: INKPERSIBLE'. THE ODOR IS PUNGENT.", "exits": {"N": 32}, "items": ["SOLUTION", "FLUID"], "floor": 7}

        # Room 57: Gold's slide - escape from vault
        rooms[57] = {"name": "GOLD'S SLIDE", "desc": "YOU ARE AT THE TOP OF THE LEGENDARY GOLD'S SLIDE. A LONG, SHINY BRASS SLIDE COILS DOWN INTO DARKNESS. A SIGN READS: 'FLOOR 6 - EMERGENCY EXIT ONLY'. THE VAULT IS TO THE NORTH.", "exits": {"N": 55}, "items": [], "floor": 7}

        # ============= FLOOR 6 - OFFICE =============
        # Office floor layout:
        # Room 41: Entry from Gold's Slide
        # Room 42: Main corridor
        # Room 43: Side office with dollar bill
        # Room 44: Large office
        # Room 45: String vending machine room
        # Room 46: Craft room with yarn and knitting needles
        # Room 47: Large open room with pit - JUMP puzzle
        # Room 48: Secret room
        # Room 49: Corridor
        # Room 50: Stairs down to Floor 5

        # Room 41: Entry from Gold's Slide - OFFICE FLOOR
        rooms[41] = {"name": "OFFICE FLOOR", "desc": "YOU ARE ON THE OFFICE FLOOR. A LONG CORRIDOR STRETCHES TO THE NORTH AND EAST. DEBRIS FROM THE SLIDE IS SCATTERED ABOUT. SOMEONE WAS HERE RECENTLY.", "exits": {"N": 42, "E": 43}, "items": [], "floor": 6}

        # Room 42: Main corridor
        rooms[42] = {"name": "MAIN CORRIDOR", "desc": "YOU ARE IN THE MAIN CORRIDOR OF THE OFFICE FLOOR. FLUORESCENT LIGHTS HUMM ABOVE. DOORS LINE THE HALLWAY TO THE NORTH AND SOUTH. A SIGN ON THE WALL READS: 'PUSH BUTTON ON WALL'.", "exits": {"S": 41, "N": 44, "E": 45, "W": 46}, "items": [], "floor": 6}

        # Room 43: Side office with dollar bill
        rooms[43] = {"name": "SIDE OFFICE", "desc": "YOU ARE IN A SMALL SIDE OFFICE. PAPERS ARE STREWN ABOUT. ON THE DESK YOU SEE A SINGLE DOLLAR BILL. A WINDOW LOOKS OUT OVER THE CITY.", "exits": {"W": 41}, "items": ["DOLLAR"], "floor": 6}

        # Room 44: Large office
        rooms[44] = {"name": "LARGE OFFICE", "desc": "YOU ARE IN A LARGE OPEN-PLAN OFFICE. CUBICLES AND DESKS FILL THE SPACE. A PUSH BUTTON IS ON THE WALL NEAR THE EAST DOOR.", "exits": {"S": 42, "E": 45}, "items": [], "floor": 6}

        # Room 45: String vending machine room
        rooms[45] = {"name": "VENDING ROOM", "desc": "YOU ARE IN A SMALL ROOM WITH A STRING VENDING MACHINE. IT READS: 'INSERT $1 FOR STRING'. A COIN SLOT IS WAITING. THERE IS ALSO A SMALL BALLOON HERE, DEFLATED.", "exits": {"W": 44, "N": 47}, "items": ["BALLOON"], "floor": 6}

        # Room 46: Craft room with yarn and knitting needles
        rooms[46] = {"name": "CRAFT ROOM", "desc": "YOU ARE IN A SMALL ROOM THAT LOOKS LIKE A CRAFT AREA. THERE ARE SUPPLIES EVERYWHERE - CONSTRUCTION PAPER, GLUE STICKS, AND IN THE CORNER: A BALL OF YARN AND KNITTING NEEDLES. A SIGN ON THE WALL READS: 'SEXY YOUNG GIRL OFFICE WORKERS'.", "exits": {"E": 42}, "items": ["YARN", "KNITTING NEEDLES"], "floor": 6}

        # Room 47: Large open room with pit - the JUMP puzzle
        rooms[47] = {"name": "OPEN ATRIUM", "desc": "YOU ARE IN A LARGE OPEN AREA - AN ATRIUM THAT SPANS THE HEIGHT OF THE BUILDING. THE FLOOR HAS A DEEP PIT THAT BISECTS THE ROOM. THE FAR SIDE LOOKS DANGEROUS TO REACH. THERE IS NO WAY ACROSS EXCEPT TO JUMP - AND IT'S A LONG WAY DOWN TO THE FLOOR BELOW. A COIL OF STRING IS ATTACHED TO A HOOK ON THE WALL HERE.", "exits": {"S": 45, "N": 48}, "items": ["STRING"], "floor": 6}

        # Room 48: Secret room
        rooms[48] = {"name": "SECRET ROOM", "desc": "YOU ARE IN A HIDDEN ROOM BEHIND A FALSE WALL. IT'S DARK AND DINGY. OLD FILING CABINETS LINE THE WALLS. THIS WAS PROBABLY USED FOR SOMETHING ILLICIT. A SECRET PASSAGE LEADS EAST.", "exits": {"S": 47, "E": 49}, "items": [], "floor": 6}

        # Room 49: Corridor
        rooms[49] = {"name": "BACK CORRIDOR", "desc": "YOU ARE IN A BACK CORRIDOR. THE WALLS ARE PAINTED A DINGY BEIGE. THE STAIRWAY DOWN IS VISIBLE AT THE END OF THE HALL.", "exits": {"W": 48, "N": 50}, "items": [], "floor": 6}

        # Room 50: Stairs down to Floor 5
        rooms[50] = {"name": "STAIRS DOWN", "desc": "YOU ARE AT THE TOP OF A WOODEN STAIRWAY LEADING DOWN. THE STAIRS LOOK A LITTLE CREAKY BUT STURDY. A SIGN READS: 'STAIRS DOWN - FLOOR 5'.", "exits": {"S": 49, "D": 51}, "items": [], "floor": 6}

        # ============= FLOOR 5 - MARY POPPINS / WEIRD =============
        # Floor 5 has 10 rooms (62-71) with surreal Mary Poppins-style themes
        # (shifted from 51-60 to avoid overwriting Floor 7 vault rooms 55-57)
        # Items: umbrella, small key, sponge; yarn/knitting needles from Floor 6
        # Puzzles: knit clothes from yarn+needles, use small key to unlock door,
        #          use umbrella/sponge to handle pool, Hyde mode switch

        # Room 62: Entry / Main Hall of the Strange Floor (was 51)
        rooms[62] = {"name": "MAIN HALL", "desc": "YOU ARE IN THE MAIN HALL OF A VERY STRANGE FLOOR. THE WALLS ARE COVERED WITH COLORFUL MURALS OF CLOWNS AND MERRY-GO-ROUNDS. A GRAND STAIRCASE LEADING UP IS COVERED IN A MAGICAL RED CARPET. DOORS LINE THE HALLWAY. A SIGN READS: 'FLOOR 5 - WHERE DREAMS COME TRUE'.", "exits": {"N": 68, "E": 70, "S": 71, "W": 69, "U": 50}, "items": [], "floor": 5}

        # Room 63: Side room with small key (was 52)
        rooms[63] = {"name": "SMALL CHAMBER", "desc": "YOU ARE IN A SMALL, DINGY CHAMBER. DUSTY FURNITURE IS STACKED IN THE CORNER. ON A LITTLE HOOK ON THE WALL HANGS A SMALL BRASS KEY.", "exits": {"E": 62}, "items": ["SMALL KEY"], "floor": 5}

        # Room 64: Sitting room (was 53)
        rooms[64] = {"name": "SITTING ROOM", "desc": "YOU ARE IN A COZY SITTING ROOM. ARMCHAIRS AND SOFAS ARE ARRANGED AROUND A TINY COFFEE TABLE. A FIREPLACE IN THE CORNER IS WARM AND TOASTY.", "exits": {"N": 69, "E": 65}, "items": [], "floor": 5}

        # Room 65: Craft room - yarn and knitting needles (from Floor 6 player brings them) (was 54)
        rooms[65] = {"name": "CRAFT ROOM", "desc": "YOU ARE IN A QUAINT CRAFT ROOM. PILES OF FABRIC, THREAD, AND SEWING SUPPLIES ARE EVERYWHERE. THERE IS ALSO A BALL OF YARN AND KNITTING NEEDLES HERE - LEFT BY A VERY PARTICULAR SET OF TWINS.", "exits": {"W": 64}, "items": ["YARN", "KNITTING NEEDLES"], "floor": 5}

        # Room 66: Nursery - eerie child's playroom (was 55)
        rooms[66] = {"name": "NURSERY", "desc": "YOU ARE IN A CHILD'S NURSERY. A SMALL BED, A ROCKING HORSE, AND STACKS OF BOARD BOOKS FILL THE ROOM. THE CEILING IS PAINTED WITH STARS AND CRESCENT MOONS. IT'S SILENT - TOO SILENT.", "exits": {"S": 68}, "items": [], "floor": 5}

        # Room 67: Umbrella stand / coat room (was 56)
        rooms[67] = {"name": "COAT ROOM", "desc": "YOU ARE IN A SMALL COAT ROOM. THERE IS AN UMBRELLA STAND BY THE DOOR, AND SEVERAL UMBRELLAS OF VARIOUS COLORS ARE LEANING AGAINST THE WALL.", "exits": {"S": 70}, "items": ["UMBRELLA"], "floor": 5}

        # Room 68: Library - north of main hall (was 57)
        rooms[68] = {"name": "LIBRARY", "desc": "YOU ARE IN A MERRY LIBRARY FILLED WITH BOOKS OF ALL SIZES. THE SHELVES REACH FROM FLOOR TO CEILING. A LADDER ON RAILS LETS YOU REACH THE TOP SHELVES. A SIGN ON THE WALL READS: 'A BOOK A DAY KEEPS THE DOCTOR AWAY'.", "exits": {"S": 62, "W": 66}, "items": [], "floor": 5}

        # Room 69: Indoor pool / playroom - west of main hall, LOCKED DOOR (was 58)
        rooms[69] = {"name": "INDOOR POOL", "desc": "YOU ARE IN AN INDOOR POOL ROOM! THE WATER IS CALM AND CLEAR. A DIVING BOARD STANDS AT THE DEEP END. THE ROOM IS COVERED IN BRIGHT TILES SHAPED LIKE FISH AND SEASHELLS.", "exits": {"E": 62}, "items": [], "floor": 5}

        # Room 70: Shower room - east of main hall, stairs down (was 59)
        rooms[70] = {"name": "SHOWER ROOM", "desc": "YOU ARE IN AN ODD SHOWER ROOM. THE WALLS ARE LINED WITH COLORFUL TILES. THERE ARE SPRINKLERS IN THE CEILING THAT LOOK LIKE FLOWERS. THE FLOOR IS WET AND SLIPPERY. A DOOR TO THE NORTH LEADS TO THE COAT ROOM. STAIRS LEAD DOWN IN THE CORNER.", "exits": {"W": 62, "N": 67, "D": 72}, "items": [], "floor": 5}

        # Room 71: Laundry room - south of main hall (was 60)
        rooms[71] = {"name": "LAUNDRY ROOM", "desc": "YOU ARE IN A SMALL LAUNDRY ROOM. AN ANTIQUE WRINGER WASHER SITS IN THE CORNER, AND CLOTHESLINES HANG FROM THE CEILING. THERE IS A BASKET OF SPONGES NEAR THE SINK.", "exits": {"N": 62}, "items": ["SPONGE"], "floor": 5}

        # ============= FLOOR 4 - HYDE / LAB =============
        # Jekyll/Hyde floor - themes: potion transformation, pool drain, umbrella parachute
        # Room 72: Entry to lab floor from Floor 5 shower room
        rooms[72] = {"name": "LAB FLOOR", "desc": "YOU ARE IN DR. JEKYLL'S LABORATORY. ODD SMELLS AND STRANGE EQUIPMENT FILL THE ROOMS. BOTTLES OF COLORED LIQUIDS LINE THE SHELVES. A SIGN ON THE WALL READS: 'DR. JEKYLL'S RESEARCH LAB - FLOOR 4'. THERE ARE EXITS TO THE NORTH, EAST, AND WEST. STAIRS LEAD DOWN.", "exits": {"N": 73, "E": 74, "W": 75, "D": 0}, "items": ["YELLOW POTION"], "floor": 4}

        # Room 73: Potion storage / transformation chamber
        rooms[73] = {"name": "TRANSFORMATION CHAMBER", "desc": "YOU ARE IN A SMALL TRANSFORMATION CHAMBER. MIRRORS LINE THE WALLS. ON A TABLE YOU SEE A SIGN THAT READS: 'DRINK ONLY IN CASE OF EMERGENCY'. THE LAB IS TO THE SOUTH.", "exits": {"S": 72}, "items": [], "floor": 4}

        # Room 74: Pool room - pool full of toxic liquid
        rooms[74] = {"name": "POOL ROOM", "desc": "YOU ARE IN A LARGE ROOM WITH A SWIMMING POOL THAT SPANS THE ENTIRE SPACE. THE LIQUID IN THE POOL IS THICK AND GREEN - DEFINITELY NOT WATER! IT LOOKS DEADLY TO THE TOUCH. THE LAB IS TO THE WEST, AND STAIRS GO UP TO A HIGH DIVING BOARD.", "exits": {"W": 72, "U": 76}, "items": [], "floor": 4}

        # Room 75: Storage room with umbrella and drain controls
        rooms[75] = {"name": "STORAGE ROOM", "desc": "YOU ARE IN A STORAGE ROOM FILLED WITH OLD EQUIPMENT. THERE IS A LARGE PARASOL (UMBRELLA) IN THE CORNER, AND A CONTROL PANEL WITH A BIG RED BUTTON MARKED 'POOL DRAIN'. THE LAB IS TO THE EAST.", "exits": {"E": 72}, "items": ["UMBRELLA"], "floor": 4}

        # Room 76: High diving board / jump point
        rooms[76] = {"name": "DIVING BOARD", "desc": "YOU ARE ON A HIGH DIVING BOARD ABOVE THE POOL. IT'S A LONG WAY DOWN TO THE POOL BELOW - DEFINITELY TOO FAR TO SURVIVE A JUMP! BUT WAIT - YOU CAN SEE AN OPEN WINDOW AT THE END OF THE BUILDING. IF YOU HAD AN UMBRELLA AND COULD PARACHUTE SIDEWAYS...", "exits": {"D": 74}, "items": [], "floor": 4}

        # ============= FLOOR 3 - POOL / GREENHOUSE / VINE TRAP =============
        # Floor 3 theme: greenhouse with exotic plants, strange vines, plant-based puzzles
        # The mysterious fluid transforms you into a huge plant form to pass through vines

        # Room 77: Entry to Floor 3 from Floor 4 - POOL CHAMBER
        rooms[77] = {"name": "POOL CHAMBER", "desc": "YOU ARE IN A LARGE CHAMBER WITH A SWIMMING POOL. THE WATER IS CLEAR AND INVITING. STRANGE FISH SWIM IN THE POOL - THEY LOOK UNUSUAL, WITH TINY TENTACLES AND GLOWING SCALES. A SIGN ON THE WALL READS: 'AQUARIUM EXHIBIT - DO NOT FEED THE FISH'. THE GREENHOUSE IS TO THE EAST, AND STAIRS LEAD UP TO FLOOR 4.", "exits": {"U": 72, "E": 78}, "items": ["FLUID", "SOLUTION"], "floor": 3}

        # Room 78: Greenhouse - main area
        rooms[78] = {"name": "GREENHOUSE", "desc": "YOU ARE IN A GREENHOUSE FILLED WITH EXOTIC PLANTS. STRANGE VINES HANG FROM THE CEILING, SOME OF THEM MOVING SLIGHTLY ON THEIR OWN. THE AIR IS THICK AND HUMID, ALMOST TROPICAL. FLOWERS OF ALL COLORS BLOOM IN EVERY CORNER, AND THE SMELL IS ALMOST OVERPOWERING. THERE IS A PASSAGE TO THE NORTH BLOCKED BY THICK VINES, AND THE POOL CHAMBER IS TO THE WEST.", "exits": {"W": 77, "N": 79}, "items": [], "floor": 3}

        # Room 79: Vine Passage - blocked by vines until plant transformation
        rooms[79] = {"name": "VINE PASSAGE", "desc": "YOU ARE IN A NARROW PASSAGE COVERED IN THICK, TWISTING VINES. THEY BLOCK THE WAY NORTH COMPLETELY - YOU CANNOT PUSH THROUGH THEM IN YOUR NORMAL FORM. THE VINES SEEM TO BE ALIVE, MOVING SLIGHTLY WHEN YOU GET CLOSE. THE GREENHOUSE IS TO THE SOUTH.", "exits": {"S": 78, "N": 80}, "items": [], "floor": 3}

        # Room 80: Flute Alcove - the flute is here, use it to descend
        rooms[80] = {"name": "FLUTE ALCOVE", "desc": "YOU ARE IN A SMALL ALCOVE BEYOND THE VINES. ON A SMALL PEDESTAL THERE IS AN ANCIENT-LOOKING FLUTE. IT'S COVERED IN DUST, AS IF IT'S BEEN HERE FOR A VERY LONG TIME. THE VINE PASSAGE IS TO THE SOUTH. SOMEONE HAS SCRATCHED WORDS INTO THE WALL: 'FLUTE PLAYER COME DOWN TO THE FLOOR BELOW'.", "exits": {"S": 79, "D": 82}, "items": ["FLUTE"], "floor": 3}

        # Room 81: Plant Alcove - a small plant that hints at transformation
        rooms[81] = {"name": "PLANT ALCOVE", "desc": "YOU ARE IN A SMALL ALCOVE COVERED IN MOSS AND VINES. A SMALL, STRANGE-LOOKING PLANT SITS IN THE CORNER, ITS LEAVES AN UNUSUAL SHADE OF GREEN. IT ALMOST SEEMS TO BE WATCHING YOU. THE FLUTE ALCOVE IS TO THE WEST, AND A CREEPY CRAWLWAY LEADS NORTH INTO DARKNESS.", "exits": {"W": 80, "N": 83}, "items": ["SMALL PLANT"], "floor": 3}

        # ============= FLOOR 2 - QUICKSAND / PIANO =============
        # Floor 2 theme: quicksand bog, piano puzzle, rope crossing
        # The rope must be tied to stakes to cross the quicksand safely
        # The piano on the other side plays a crucial role in escaping

        # Room 81: QUICKSAND CHAMBER - the main puzzle room
        # This is where the player arrives after playing the flute on Floor 3
        rooms[81] = {"name": "QUICKSAND CHAMBER", "desc": "YOU ARE IN A DARK, DANK CHAMBER. A HUGE BOG OF QUICKSAND BLOCKS YOUR WAY EAST - YOU CAN SEE SAFETY ON THE OTHER SIDE, BUT THE SAND LOOKS DEADLY! ON THIS SIDE OF THE QUICKSAND, THERE IS A LARGE WOODEN STAKE DRIVEN INTO THE FLOOR. THROUGH A SMALL WINDOW, YOU CAN SEE A COILED ROPE ON THE FLOOR BELOW. THE LOUNGE IS TO THE NORTH, AND CRAWLWAYS LEAD WEST AND SOUTH.", "exits": {"N": 83, "W": 82, "S": 82}, "items": ["STAKE", "ROPE"], "floor": 2}

        # Room 82: Crawlway West - connects to Quicksand Chamber
        rooms[82] = {"name": "CRAWLWAY WEST", "desc": "YOU ARE IN A TIGHT CRAWLWAY. THE PASSAGE IS NARROW AND COBBWEB-COVERED. YOU CAN HEAR A STRANGE SOUND FROM SOMEWHERE TO THE EAST - IT SOUNDS LIKE... WHISPERS? OR MAYBE WIND? THE CRAWLWAY CONTINUES SOUTH, AND THE QUICKSAND CHAMBER IS TO THE EAST.", "exits": {"E": 81, "S": 83}, "items": [], "floor": 2}

        # Room 83: Lounge - a creepy lounge with old furniture
        rooms[83] = {"name": "OLD LOUNGE", "desc": "YOU ARE IN AN ABANDONED LOUNGE. DUSTY ARMCHAIRS AND OLD TABLES FILL THE ROOM. THE WALLPAPER IS PEELING AND MOULDY. A COLD DRAFT COMES FROM SOMEWHERE. THE QUICKSAND CHAMBER IS TO THE SOUTH, AND THE CRAWLWAY CONTINUES NORTH.", "exits": {"S": 81, "N": 84}, "items": [], "floor": 2}

        # Room 84: Piano Room - contains the piano and large rope
        rooms[84] = {"name": "PIANO ROOM", "desc": "YOU ARE IN A ROOM WITH A LARGE GRAND PIANO. THE PIANO IS DUSTY BUT OTHERWISE IN GOOD CONDITION. ITS BLACK AND WHITE KEYS GLIMMER IN THE dim LIGHT. ON THE FLOOR BESIDE IT LIES A LARGE COILED ROPE. THROUGH A WINDOW TO THE EAST, YOU CAN SEE THE FRONT ENTRANCE OF THE BUILDING - FREEDOM IS SO CLOSE! THE LOUNGE IS TO THE SOUTH, AND STAIRS LEAD DOWN TO THE FLOOR BELOW.", "exits": {"S": 83, "D": 91, "E": 85}, "items": ["PIANO", "LARGE ROPE"], "floor": 2}

        # Room 85: Corridor Hall - leads to the front door
        rooms[85] = {"name": "CORRIDOR HALL", "desc": "YOU ARE IN A LONG CORRIDOR. THE WALLS ARE LINED WITH OLD PHOTOGRAPHS OF SOLEMN-LOOKING PEOPLE. AT THE END OF THE CORRIDOR, YOU SEE IT - A LARGE FRONT DOOR! FREEDOM LIES JUST BEYOND! THE PIANO ROOM IS TO THE WEST, AND SMALL ROOMS LEAD NORTH AND SOUTH.", "exits": {"W": 84, "N": 86, "S": 87}, "items": [], "floor": 2}

        # Room 86: Small Room North
        rooms[86] = {"name": "SMALL ROOM", "desc": "YOU ARE IN A TINY ROOM. THE CEILING IS LOW AND THE AIR IS STALE. THERE'S NOTHING HERE BUT DUST AND SPIDERS. THE CORRIDOR IS TO THE SOUTH.", "exits": {"S": 85}, "items": [], "floor": 2}

        # Room 87: Small Room South  
        rooms[87] = {"name": "STORAGE ROOM", "desc": "YOU ARE IN A SMALL STORAGE ROOM. OLD BOXES AND BROKEN FURNITURE ARE STACKED AGAINST THE WALLS. ONE OF THE BOXES HAS 'PAPERS' WRITTEN ON IT IN FADED INK. THE CORRIDOR IS TO THE NORTH.", "exits": {"N": 85}, "items": [], "floor": 2}

        # ============= FLOOR 1 - GROUND FLOOR / ESCAPE =============
        # Floor 1 theme: the final floor - escape the building!
        # The front door is here - walk through it to win!

        # Room 91: Entrance Hall - where you arrive from Floor 2
        rooms[91] = {"name": "ENTRANCE HALL", "desc": "YOU ARE IN THE GRAND ENTRANCE HALL OF THE BUILDING. A LARGE CHANDELIER HANGS FROM THE CEILING, ITS CRYSTALS GLEAMING. MARBLE FLOORS REFLECT THE DIM LIGHT. THE FRONT DOOR IS RIGHT THERE - TO THE EAST! YOU CAN BARELY CONTAIN YOUR EXCITEMENT. THE CORRIDOR CONTINUES WEST.", "exits": {"E": 95, "W": 92}, "items": [], "floor": 1}

        # Room 92: Grand Corridor
        rooms[92] = {"name": "GRAND CORRIDOR", "desc": "YOU ARE IN A LONG, ORNATE CORRIDOR. PAINTINGS OF LANDSCAPES HANG ON THE WALLS. THE AIR FEELS FRESHER HERE - YOU CAN ALMOST SMELL THE OUTDOORS! THE ENTRANCE HALL IS TO THE EAST, AND THE FRONT DOOR IS JUST AHEAD TO THE NORTHEAST.", "exits": {"E": 91, "NE": 95}, "items": [], "floor": 1}

        # Room 95: FRONT DOOR - THE EXIT! Walking through here wins the game!
        rooms[95] = {"name": "FRONT DOOR", "desc": "YOU ARE STANDING BEFORE THE FRONT DOOR OF THE BUILDING. IT'S A massive WOODEN DOOR WITH A BRASS HANDEL. THROUGH THE WINDOWS NEXT TO IT, YOU CAN SEE SUNLIGHT - REAL, NATURAL SUNLIGHT! FREEDOM IS JUST ON THE OTHER SIDE OF THIS DOOR! WEST LEADS BACK TO THE ENTRANCE HALL.", "exits": {"W": 91}, "items": [], "floor": 1}

        return rooms

    def print_intro(self):
        """Print introduction"""
        print("=" * 60)
        print("KIDNAPPED!")
        print("=" * 60)
        print()
        print("BY PETER KIRSCH (1980)")
        print("PYTHON VERSION BY LEMMY")
        print()
        print("-" * 60)
        print("YOU AWAKEN ON THE 9TH FLOOR OF A STRANGE BUILDING,")
        print("OBVIOUSLY A KIDNAP VICTIM. YOU ARE ALIVE AT THE")
        print("PRESENT AND MUST ESCAPE FROM THE BUILDING, FLOOR BY FLOOR.")
        print("BEWARE THE KIDNAPPER! MANY TRAPS HAVE BEEN SET!")
        print("-" * 60)
        print()
        print("USE 1- OR 2-WORD COMMANDS LIKE: GET KEY, DROP LAMP")
        print("DIRECTIONS: N, S, E, W, U (UP), D (DOWN)")
        print("OTHER COMMANDS: LOOK, INVENTORY (OR I), QUIT")
        print()
        print("=" * 60)
        print()

    def print_status(self):
        """Print current status"""
        room = self.rooms.get(self.state.location, {"name": "UNKNOWN", "desc": "YOU ARE LOST!", "items": []})

        print(f"\n*** FLOOR {self.state.floor} ***")
        print(f"Location: {room['name']}")
        print(f"Exits: {', '.join(room['exits'].keys()) or 'NONE'}")
        print(f"Items here: {', '.join(room['items']) if room['items'] else 'NONE'}")
        print(f"Time: {self.state.time}")  # Floor 9 time tracking
        print()
        print(room['desc'])

        # Special descriptions based on location
        if self.state.floor == 9:
            self.print_floor9_extras()
        elif self.state.floor == 8:
            self.print_floor8_extras()
        elif self.state.floor == 7:
            self.print_floor7_extras()
        elif self.state.floor == 6:
            self.print_floor6_extras()
        elif self.state.floor == 5:
            self.print_floor5_extras()
        elif self.state.floor == 4:
            self.print_floor4_extras()
        elif self.state.floor == 3:
            self.print_floor3_extras()

    def print_floor8_extras(self):
        """Print floor 8 specific descriptions"""
        loc = self.state.location

        if loc == 22:
            if self.state.rope_tied:
                print("A ROPE IS STRETCHED ACROSS THE POOL, TIED TO A STAKE ON EACH SIDE.")
            elif self.state.balloon_inflated:
                print("A LARGE INFLATED BALLOON FLOATS ABOVE THE POOL, JUST WITHIN REACH.")
            else:
                print("THE PIRANHAS BARELY NOTICE YOU. ANY MOVEMENT IN THE WATER WOULD BE FATAL!")

        if loc == 23 and not self.state.rope_tied and not self.state.balloon_inflated:
            print("YOU NEED SOME WAY TO CROSS WITHOUT GETTING INTO THE WATER!")

        if loc == 24:
            if not self.state.balloon_inflated and "BALLOON" not in self.rooms[24].get("items", []) and not self.state.balloon_taken:
                print("THE HELIUM TANK IS HERE. YOU COULD INFLATE THE BALLOON WITH IT.")
            elif self.state.balloon_inflated:
                print("THE INFLATED BALLOON IS ATTACHED TO A STRING LEADING UPWARD.")

    def print_floor9_extras(self):
        """Print floor-specific descriptions"""
        loc = self.state.location

        if loc == 7 and not self.state.key_taken:
            print("THERE IS A KEY ON THE LEDGE, BUT YOUR ARM IS TOO SHORT TO REACH IT.")
            print("THERE IS A BROOM IN THE MAIN ROOM...")

        if loc == 13 and not self.state.tape_used:
            print("THE LIVE WIRES ARE DANGEROUS!")
            if self.state.time >= 12:
                print("IT'S PAST MIDNIGHT - THE POWER IS OFF!")

        if loc == 10 and self.state.tape_used and not self.state.elevator_fixed:
            print("THE ELEVATOR IS WAITING FOR REPAIRS...")

    def print_floor7_extras(self):
        """Print Floor 7 vault specific descriptions"""
        loc = self.state.location

        # Bank floor entry - loose step warning
        if loc == 31:
            if not self.state.step_glued:
                print("WARNING: ONE OF THE STEPS LOOKS VERY LOOSE!")
                print("IF YOU TRY TO PASS WITHOUT FIXING IT, YOU'LL FALL!")
            else:
                print("THE LOOSE STEP IS NOW SECURELY GLUED IN PLACE.")

        # Vault anteroom - vault door status
        if loc == 32:
            if self.state.vault_door_unlocked:
                print("THE VAULT DOOR IS OPEN. YOU CAN GO EAST TO ENTER.")
            else:
                print("THE VAULT DOOR IS LOCKED. YOU NEED A KEY.")

        # Key room
        if loc == 37 and not self.state.small_key_taken:
            print("A SMALL BRASS KEY HANGS ON A HOOK. IT LOOKS LIKE A VAULT KEY.")

        # The vault
        if loc == 55:
            if self.state.vault_door_unlocked:
                print("YOU ARE IN THE VAULT. THE GOLD'S SLIDE IS TO THE EAST.")
            else:
                print("THE VAULT DOOR IS LOCKED. THE DIAL SHOWS 32-55-57.")

        # Gold's slide room
        if loc == 57:
            print("YOU CAN GO DOWN THE SLIDE TO FLOOR 6!" if self.state.vault_door_unlocked else "THE VAULT DOOR BLOCKS THE SLIDE EXIT.")

    def print_floor6_extras(self):
        """Print Floor 6 office specific descriptions"""
        loc = self.state.location

        # Side office - dollar bill
        if loc == 43 and not self.state.floor6_dollar_taken:
            print("A SINGLE DOLLAR BILL SITS ON THE DESK, LEFT BY THE KIDNAPPER.")

        # Vending room - balloon and string vending machine
        if loc == 45:
            if not self.state.floor6_balloon_taken and not self.state.floor6_balloon_inflated:
                print("A DEFLATED BALLOON LIES ON THE FLOOR.")
            elif self.state.floor6_balloon_inflated and not self.state.floor6_string_tied:
                print("AN INFLATED BALLOON IS FLOATING NEAR THE CEILING!")
                print("YOU SHOULD FIND A WAY TO TIE IT DOWN.")
            elif self.state.floor6_string_tied:
                print("THE STRING IS SECURELY TIED TO THE BALLOON.")
            if not self.state.floor6_vending_paid:
                print("THE STRING VENDING MACHINE READS: 'INSERT $1 FOR STRING'.")
            else:
                print("THE STRING VENDING MACHINE IS EMPTY.")

        # Craft room - yarn and knitting needles
        if loc == 46 and not self.state.floor6_string_taken:
            print("THE YARN AND KNITTING NEEDLES LOOK LIKE THEY BELONG TO SOMEONE'S HOBBY PROJECT.")

        # Atrium - pit and jump puzzle
        if loc == 47:
            if self.state.floor6_jumped:
                print("YOU ALREADY JUMPED ACROSS THE PIT.")
            elif not self.state.floor6_balloon_inflated:
                print("A DEEP PIT BISECTS THE ROOM. THE FAR SIDE LOOKS TOO FAR TO JUMP.")
                print("YOU MIGHT NEED SOMETHING TO HELP YOU GET ACROSS.")
            elif not self.state.floor6_string_tied:
                print("THE INFLATED BALLOON WANTS TO FLOAT AWAY!")
                print("YOU SHOULD TIE IT DOWN WITH THE STRING!")
            else:
                print("THE BALLOON IS TIED WITH STRING. YOU COULD JUMP WITH IT!")

        # Stairs down
        if loc == 50:
            print("THE STAIRWAY LEADS DOWN TO FLOOR 5.")

    def print_floor5_extras(self):
        """Print Floor 5 Mary Poppins / Weird floor specific descriptions"""
        loc = self.state.location

        # Main hall
        if loc == 62:
            print("THE MURALS SEEM TO MOVE AS YOU WATCH...")

        # Small key room
        if loc == 63 and not self.state.floor5_small_key_taken:
            print("A SMALL BRASS KEY HANGS ON A HOOK ON THE WALL.")

        # Craft room - yarn and knitting needles
        if loc == 65:
            if not self.state.floor5_clothes_knitted:
                print("THE YARN AND KNITTING NEEDLES LOOK PERFECT FOR MAKING CLOTHES.")
                print("MAYBE YOU COULD KNIT SOMETHING USEFUL...")
            else:
                print("THE YARN HAS BEEN USED TO KNIT A NICE SET OF CLOTHES.")

        # Pool room - locked door
        if loc == 69:
            if not self.state.floor5_door_unlocked:
                print("A HEAVY DOOR ON THE NORTH WALL IS LOCKED.")
                print("A SMALL KEYHOLE IS VISIBLE.")
            else:
                print("THE DOOR TO THE NORTH IS UNLOCKED.")

        # Shower room - wet area
        if loc == 70:
            print("THE FLOOR IS VERY WET AND SLIPPERY.")
            print("THE SPRINKLERS IN THE CEILING LOOK LIKE THEY COULD TURN ON AT ANY MOMENT...")

        # Laundry room - sponge
        if loc == 71 and not self.state.floor5_sponge_taken:
            print("A SPONGE IN THE BASKET LOOKS USEFUL FOR CLEANING UP.")

    def print_floor4_extras(self):
        """Print Floor 4 Jekyll/Hyde Lab specific descriptions"""
        loc = self.state.location

        # Lab floor - Jekyll/Hyde mode
        if loc == 72:
            if self.state.jekyll_mode:
                print("YOU ARE IN HYDE MODE! YOUR MUSCLES ARE HUGE AND YOUR EYES ARE GREEN!")
                print("YOU FEEL INVINCIBLE!")
            else:
                print("A SIGN ON THE WALL READS: 'TRANSFORMATION SERUM - DRINK IN EMERGENCY'")

        # Pool room
        if loc == 74:
            if self.state.floor4_pool_drained:
                print("THE POOL IS NOW EMPTY. THE TOXIC GREEN LIQUID IS GONE.")
                print("THE HARD POOL FLOOR IS EXPOSED BELOW.")
            else:
                print("THE TOXIC GREEN LIQUID LOOKS DEADLY!")
                print("YOU DEFINITELY DON'T WANT TO FALL IN!")

        # Storage room - umbrella and drain
        if loc == 75:
            if not self.state.floor4_umbrella_taken:
                print("A LARGE PARASOL (UMBRELLA) STANDS IN THE CORNER.")
            if not self.state.floor4_pool_drained:
                print("THE 'POOL DRAIN' BUTTON AWAITS YOUR COMMAND.")
            else:
                print("THE POOL DRAIN BUTTON HAS BEEN USED.")

        # Diving board - umbrella parachute
        if loc == 76:
            if self.state.floor4_umbrella_opened:
                print("YOUR UMBRELLA IS OPEN AND READY!")
                print("YOU CAN JUMP NOW TO USE IT AS A PARACHUTE!")
            elif "UMBRELLA" in self.player_inventory or self.state.floor4_umbrella_taken:
                print("YOU HAVE AN UMBRELLA BUT HAVEN'T OPENED IT YET.")
                print("YOU SHOULD 'USE UMBRELLA' TO OPEN IT FIRST.")
            else:
                print("YOU NEED AN UMBRELLA TO SURVIVE THIS JUMP!")

    def print_floor3_extras(self):
        """Print Floor 3 Plant/Trap specific descriptions"""
        loc = self.state.location

        # Pool chamber - fluid/solution available
        if loc == 77:
            if self.state.floor3_fluid_drunk or self.state.floor3_solution_drunk:
                print("YOUR PLANT-LIKE BODY TINGLES WITH NATURAL ENERGY.")
                print("YOU COULD BREAK THROUGH THICK VINES NOW!")
            else:
                if "FLUID" in self.rooms[77].get("items", []) or "SOLUTION" in self.rooms[77].get("items", []):
                    print("BOTTLES OF MYSTERIOUS FLUID AND SOLUTION SIT BY THE POOL'S EDGE.")
                    print("THE LABELS READ: 'CAUTION: DO NOT DRINK'.")
                print("THE STRANGE FISH SWIM CURIOUSLY, THEIR TENTACLES WAVING.")

        # Greenhouse - vines block north
        if loc == 78:
            if self.state.floor3_fluid_drunk or self.state.floor3_solution_drunk:
                print("THE VINES TO THE NORTH SEEM THINNER NOW...")
                print("YOUR PLANT FORM MIGHT BE ABLE TO BREAK THROUGH!")
            else:
                print("THICK VINES BLOCK THE NORTH PASSAGE.")
                print("THEY'RE TOO STRONG TO PUSH THROUGH IN YOUR CURRENT FORM.")
                print("SOMETHING MIGHT HELP YOU CHANGE YOUR FORM...")

        # Vine passage
        if loc == 79:
            if self.state.floor3_fluid_drunk or self.state.floor3_solution_drunk:
                print("YOUR PLANT-LIKE BODY ALLOWS YOU TO PASS THROUGH THE VINES!")
            else:
                print("THE VINES ARE IMPENETRABLE IN YOUR NORMAL FORM.")

        # Flute alcove
        if loc == 80:
            if "FLUTE" in self.player_inventory:
                print("YOU HAVE THE FLUTE. YOU COULD PLAY IT TO DESCEND...")
                print("TRY: PLAY FLUTE, USE FLUTE, or just GO DOWN")
            elif self.state.floor3_flute_played:
                print("YOU'VE ALREADY PLAYED THE FLUTE TO DESCEND.")
            else:
                print("THE FLUTE AWAITS ON THE PEDESTAL.")

    def do_look(self):
        """Look around"""
        self.print_status()

    def do_inventory(self):
        """Show inventory"""
        print("YOU ARE CARRYING:")
        if self.player_inventory:
            for item in self.player_inventory:
                print(f"  {item}")
        else:
            print("  NOTHING")

    def do_go(self, direction):
        """Move in a direction"""
        direction = direction.upper()
        if direction not in ["N", "S", "E", "W", "U", "D", "NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"]:
            print("INVALID DIRECTION")
            return

        # Convert full words to letters
        dir_map = {"N": "N", "S": "S", "E": "E", "W": "W", "U": "U", "D": "D",
                   "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W", "UP": "U", "DOWN": "D"}
        direction = dir_map.get(direction, direction)

        # Special transitions - checked BEFORE normal exits (some use phantom exits)
        # Elevator in room 1 goes down to Floor 8 (no D exit in room data)
        if self.state.floor == 9 and direction == "D" and self.state.location == 1:
            if not self.state.elevator_fixed:
                print("THE ELEVATOR ISN'T WORKING!")
                return
            else:
                print("YOU TAKE THE ELEVATOR DOWN ONE FLOOR...")
                self.state.floor = 8
                self.state.reset_floor_flags()
                self.state.location = 21  # Floor 8 start
                self.print_status()
                return

        room = self.rooms.get(self.state.location, {"exits": {}})
        exits = room.get("exits", {})

        if direction in exits:
            new_loc = exits[direction]

            # Floor 8 piranha pool crossing check
            if self.state.floor == 8:
                # Trying to cross the piranha pool from south side (23) to north (22)
                if self.state.location == 23 and direction == "N":
                    if self.state.rope_tied:
                        print("YOU CLING TO THE ROPE AND PULL YOURSELF ACROSS!")
                    elif self.state.balloon_inflated:
                        print("YOU HOLD ONTO THE BALLOON AND FLOAT ACROSS!")
                    else:
                        print("YOU WADE INTO THE WATER TO CROSS...")
                        print("THE PIRANHAS ATTACK!")
                        print("THOUSANDS OF RAZOR-SHARP TEETH TEAR AT YOUR FLESH!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return
                # Trying to enter the aquarium pool (22) from north side (24) going EAST
                if self.state.location == 24 and direction == "E":
                    if self.state.rope_tied:
                        print("YOU CLING TO THE ROPE AND PULL YOURSELF ACROSS!")
                    elif self.state.balloon_inflated:
                        print("YOU HOLD ONTO THE BALLOON AND FLOAT ACROSS!")
                    elif self.state.piranha_dead:
                        print("YOU WALK ACROSS THE POOL FLOOR. THE PIRANHAS ARE ALL ASLEEP.")
                    else:
                        print("YOU WADE INTO THE WATER TO CROSS...")
                        print("THE PIRANHAS ATTACK!")
                        print("THOUSANDS OF RAZOR-SHARP TEETH TEAR AT YOUR FLESH!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return
                # Down from room 29 goes to Floor 7
                if self.state.location == 29 and direction == "D":
                    print("YOU DESCEND THE STAIRWAY TO FLOOR 7...")
                    self.state.floor = 7
                    self.state.reset_floor_flags()
                    self.state.location = 31  # Floor 7 start
                    self.print_status()
                    return

            # Floor 7: Vault special navigation
            if self.state.floor == 7:
                loc = self.state.location

                # Room 31: Bank floor - loose step hazard
                if loc == 31 and direction == "E":
                    if not self.state.step_glued:
                        print("YOU TRY TO GO THROUGH THE DOORWAY...")
                        print("YOUR FOOT HITS A LOOSE STEP!")
                        print("THE STEP IS MISSING! YOU FALL THROUGH THE FLOOR!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return

                # Room 32: Going EAST to vault - check if door is unlocked
                if loc == 32 and direction == "E":
                    if not self.state.vault_door_unlocked:
                        print("THE VAULT DOOR IS LOCKED. YOU NEED TO UNLOCK IT FIRST.")
                        return

            # Floor 6: Office floor special navigation
            if self.state.floor == 6:
                loc = self.state.location

                # Room 47: JUMP puzzle - trying to go NORTH to secret room
                if loc == 47 and direction == "N":
                    if self.state.floor6_jumped:
                        print("YOU'VE ALREADY JUMPED ACROSS THE PIT.")
                        # Allow through since already jumped
                    elif not self.state.floor6_balloon_inflated:
                        print("YOU TRY TO JUMP ACROSS THE PIT...")
                        print("YOU LEAP! BUT YOU CAN'T MAKE IT!")
                        print("YOU FALL INTO THE PIT!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return
                    elif not self.state.floor6_string_tied:
                        print("YOU TRY TO JUMP ACROSS WITH THE BALLOON...")
                        print("BUT THE BALLOON GETS AWAY FROM YOU!")
                        print("WITHOUT BEING TIED DOWN, THE BALLOON FLOATS AWAY!")
                        print("YOU FALL INTO THE PIT!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return
                    else:
                        print("YOU HOLD TIGHT TO THE BALLOON AND STRING!")
                        print("THE BALLOON LIFTS YOU LIGHTLY ACROSS THE PIT!")
                        print("YOU LAND SAFELY ON THE OTHER SIDE!")
                        self.state.floor6_jumped = True
                        self.state.location = new_loc
                        self.print_status()
                        return

                # Down from room 50 goes to Floor 5
                if loc == 50 and direction == "D":
                    print("YOU DESCEND THE STAIRWAY TO FLOOR 5...")
                    self.state.floor = 5
                    self.state.reset_floor_flags()
                    self.state.location = 62  # Floor 5 start (room 62 = MAIN HALL)
                    self.print_status()
                    return

            # Floor 5: Mary Poppins / Weird floor
            if self.state.floor == 5:
                loc = self.state.location

                # Room 69: Indoor pool - locked door to sitting room (64)
                # Need small key to go NORTH from pool to sitting room
                if loc == 69 and direction == "N":
                    if not self.state.floor5_door_unlocked:
                        print("A HEAVY DOOR BLOCKS YOUR WAY. IT'S LOCKED.")
                        print("YOU NEED A KEY TO OPEN IT.")
                        return

                # Room 64: Sitting room - locked door to pool (69)
                if loc == 64 and direction == "S":
                    if not self.state.floor5_door_unlocked:
                        print("A HEAVY DOOR BLOCKS YOUR WAY. IT'S LOCKED.")
                        print("YOU NEED A KEY TO OPEN IT.")
                        return

                # Down from room 70 (shower room) goes to Floor 4 (room 72)
                if loc == 70 and direction == "D":
                    print("YOU DESCEND THE STAIRWAY TO FLOOR 4...")
                    self.state.floor = 4
                    self.state.reset_floor_flags()
                    self.state.location = 72  # Floor 4 start (LAB FLOOR)
                    self.print_status()
                    return

            # Floor 4: Jekyll/Hyde Lab
            if self.state.floor == 4:
                loc = self.state.location

                # Room 76: Jump from diving board with umbrella (parachute)
                if loc == 76 and direction == "D":
                    if not self.state.floor4_umbrella_opened:
                        print("YOU JUMP OFF THE DIVING BOARD!")
                        print("AAAAAAAAGH!")
                        print("YOU FALL ALL THE WAY DOWN INTO THE TOXIC POOL!")
                        print("THE GREEN LIQUID DISSOLVES YOUR BODY!")
                        print("YOU HAVE DIED A TERRIBLE DEATH.")
                        self.running = False
                        return
                    else:
                        print("YOU OPEN THE UMBRELLA WIDE!")
                        print("THE PARASOL CATCHES THE AIR LIKE A PARACHUTE!")
                        print("YOU GLIDE SIDEWAYS THROUGH THE WINDOW!")
                        print("YOU LAND SAFELY ON THE FLOOR BELOW!")
                        self.state.floor4_jumped = True
                        self.state.floor = 3
                        self.state.reset_floor_flags()
                        self.state.location = 77  # Floor 3 start (POOL CHAMBER)
                        self.print_status()
                        return

                # Down from room 72 (lab floor) goes to Floor 3
                if loc == 72 and direction == "D":
                    if self.state.location == 72:
                        print("YOU DESCEND TO FLOOR 3...")
                        self.state.floor = 3
                        self.state.reset_floor_flags()
                        self.state.location = 77  # Floor 3 start (POOL CHAMBER)
                        self.print_status()
                        return

            # Floor 3: Plant/Trap floor - vine passage and flute
            if self.state.floor == 3:
                loc = self.state.location
                
                # Room 78 (GREENHOUSE): North to room 79 blocked by vines unless plant form
                if loc == 78 and direction == "N":
                    if not (self.state.floor3_fluid_drunk or self.state.floor3_solution_drunk):
                        print("THICK VINES BLOCK YOUR PATH!")
                        print("YOU TRY TO PUSH THROUGH, BUT THE VINES ARE TOO STRONG!")
                        print("IN YOUR NORMAL FORM, YOU CANNOT PASS.")
                        print("MAYBE IF YOU WERE... DIFFERENT... YOU COULD BREAK THROUGH...")
                        return
                    else:
                        print("YOUR PLANT-LIKE FORM ALLOWS YOU TO PUSH THROUGH THE VINES!")
                        print("YOUR ROOTS AND VINE-LIKE ARMS INTERTWINE WITH THE BARRIER...")
                        print("AND YOU BREAK THROUGH TO THE OTHER SIDE!")
                
                # Room 80 (FLUTE ALCOVE): Down with flute to Floor 2
                if loc == 80 and direction == "D":
                    if "FLUTE" not in self.player_inventory and not self.state.floor3_flute_taken:
                        print("YOU CAN'T GO DOWN WITHOUT FINDING SOMETHING TO HELP YOU DESCEND...")
                        print("PERHAPS YOU NEED TO FIND OR USE SOMETHING FIRST.")
                        return
                    if self.state.floor3_flute_played:
                        print("YOU ALREADY PLAYED THE FLUTE TO DESCEND.")
                        return
                    print("YOU PUT THE FLUTE TO YOUR LIPS AND PLAY A HAUNTING MELODY...")
                    print("THE NOTES ECHO THROUGH THE BUILDING...")
                    print("SUDDENLY, THE FLOOR BENEATH YOU GIVES WAY!")
                    print("A MAGICAL STAIRWAY REVEALS ITSELF!")
                    print("YOU DESCEND THE STAIRS TO FLOOR 2...")
                    self.state.floor3_flute_played = True
                    self.state.floor = 2
                    self.state.reset_floor_flags()
                    self.state.location = 81  # Floor 2 start (QUICKSAND CHAMBER)
                    self.print_status()
                    return

            # Floor 2: Quicksand / Piano floor
            if self.state.floor == 2:
                loc = self.state.location
                
                # Room 81 (QUICKSAND CHAMBER): East is blocked by quicksand unless rope is stretched
                if loc == 81 and direction == "E":
                    if not self.state.floor2_rope_stretched:
                        print("YOU WALK EAST TOWARD THE QUICKSAND...")
                        print("THE SAND LOOKS DEADLY - SOFT AND TREACHEROUS!")
                        print("WITHOUT A WAY TO CROSS, YOU CANNOT GO EAST!")
                        print("MAYBE IF YOU HAD A ROPE AND SOMETHING TO TIE IT TO...")
                        return
                    else:
                        print("YOU GRIP THE ROPE TIGHTLY AND STEP ONTO THE QUICKSAND...")
                        print("YOUR FEET SINK SLIGHTLY, BUT THE ROPE HOLDS YOU SAFE!")
                        print("YOU CAREFULLY MAKE YOUR WAY ACROSS THE QUICKSAND!")
                
                # Down from room 84 (PIANO ROOM) goes to Floor 1
                if loc == 84 and direction == "D":
                    print("YOU DESCEND THE STAIRS TO THE GROUND FLOOR...")
                    self.state.floor = 1
                    self.state.reset_floor_flags()
                    self.state.location = 91  # Floor 1 start (ENTRANCE HALL)
                    self.print_status()
                    return

            # Floor 1: Ground floor - ESCAPE!
            if self.state.floor == 1:
                loc = self.state.location
                
                # Room 91 or 92: East or Northeast to room 95 (FRONT DOOR)
                if loc in [91, 92] and direction in ["E", "NE"]:
                    new_loc = 95  # Force to FRONT DOOR
                
                # Room 95 (FRONT DOOR): Going EAST through the door wins the game!
                if loc == 95 and direction == "E":
                    print("========================================")
                    print("YOU PUSH OPEN THE FRONT DOOR!")
                    print("FRESH AIR RUSHES IN! SUNLIGHT BLINDES YOU!")
                    print("YOU STUMBLE OUT INTO THE REAL WORLD!")
                    print("========================================")
                    print()
                    print("CONGRATULATIONS! YOU'VE MADE IT!")
                    print("YOU ESCAPED THE BUILDING!")
                    print("YOU ARE FREE!")
                    print()
                    self.running = False  # Game won!
                    return

            self.state.location = new_loc
            self.print_status()
        else:
            print("YOU CAN'T GO THAT WAY.")

    def do_get(self, item):
        """Pick up an item"""
        if not item:
            print("GET WHAT?")
            return

        item = item.upper()
        room = self.rooms.get(self.state.location, {"items": []})

        if item in room.get("items", []):
            # Special case: KEY on ledge - need BROOM in inventory
            if item == "KEY" and self.state.location == 7:
                if "BROOM" not in self.player_inventory:
                    print("YOUR ARM IS TOO SHORT TO REACH IT!")
                    print("YOU NEED SOMETHING LONG TO PUSH IT TOWARD YOU...")
                    return
                else:
                    print("YOU USE THE BROOM TO KNOCK THE KEY OFF THE LEDGE!")
                    room["items"].remove(item)
                    self.player_inventory.append(item)
                    self.state.key_taken = True
                    return

            room["items"].remove(item)
            self.player_inventory.append(item)
            print(f"YOU TAKE THE {item}.")

            # Set flag when picking up BROOM
            if item == "BROOM":
                self.state.has_broom = True

            # Floor 8 specific item tracking
            elif item == "ROPE":
                self.state.rope_taken = True
            elif item == "GLUE":
                self.state.glue_taken = True
            elif item == "HELIUM":
                self.state.helium_taken = True
            elif item == "BALLOON":
                self.state.balloon_taken = True
            elif item == "WIRES":
                pass  # Wires don't need special handling
            # Floor 7 vault items
            elif item == "SMALL KEY":
                self.state.small_key_taken = True
            elif item == "TIN FOIL":
                self.state.tin_foil_taken = True
            elif item == "SOLUTION" or item == "FLUID":
                self.state.solution_taken = True
            # Floor 6 office items
            elif item == "DOLLAR":
                self.state.floor6_dollar_taken = True
            elif item == "BALLOON":
                self.state.floor6_balloon_taken = True
            elif item == "STRING":
                self.state.floor6_string_taken = True
            # Floor 5 Mary Poppins / Weird floor items
            elif item == "SMALL KEY":
                self.state.floor5_small_key_taken = True
            elif item == "UMBRELLA":
                self.state.floor5_umbrella_taken = True
            elif item == "SPONGE":
                self.state.floor5_sponge_taken = True
            # Floor 4 Jekyll/Hyde Lab items
            elif item == "YELLOW POTION":
                self.state.floor4_potion_taken = True
            elif item == "UMBRELLA":
                self.state.floor4_umbrella_taken = True
            # Floor 3 Plant/Trap items
            elif item == "FLUTE":
                self.state.floor3_flute_taken = True
            elif item == "FLUID":
                pass  # Floor 3 fluid - used for plant transformation
            elif item == "SOLUTION":
                pass  # Floor 3 solution - used for plant transformation
            # Floor 2 Quicksand/Piano items
            elif item == "ROPE" or item == "LARGE ROPE":
                self.state.floor2_rope_taken = True
            elif item == "PIANO":
                print("YOU CAN'T TAKE THE PIANO! IT'S HUGE AND FIXED TO THE FLOOR!")
                # Put it back
                room["items"].append(item)
                self.player_inventory.remove(item)
            elif item == "STAKE":
                print("YOU CAN'T TAKE THE STAKE! IT'S DRIVEN DEEP INTO THE FLOOR!")
                # Put it back
                room["items"].append(item)
                self.player_inventory.remove(item)
            else:
                pass  # Item picked up, inventory updated
        else:
            print(f"THERE IS NO {item} HERE.")

    def do_drop(self, item):
        """Drop an item"""
        if not item:
            print("DROP WHAT?")
            return
        item = item.upper()
        if item in self.player_inventory:
            self.player_inventory.remove(item)
            room = self.rooms.get(self.state.location)
            if room and "items" in room:
                room["items"].append(item)
            print(f"YOU DROP THE {item}.")
        else:
            print(f"YOU DON'T HAVE A {item}.")

    def process_command(self, cmd):
        """Process a player command"""
        if not cmd:
            return

        # Increment time on Floor 9 (time represents hours, 0-23)
        if self.state.floor == 9 and self.state.time < 24:
            self.state.time += 1

        cmd = cmd.upper().strip()
        words = cmd.split()

        if len(words) == 0:
            return

        verb = words[0]
        obj = " ".join(words[1:]) if len(words) > 1 else ""

        # Direction shortcuts
        if verb in ["N", "S", "E", "W", "U", "D"]:
            self.do_go(verb)
        elif verb in ["NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN"]:
            self.do_go(verb)
        elif verb == "GO" or verb == "WALK":
            if obj.upper() in ["SLIDE", "VAULT"]:
                if obj.upper() == "SLIDE":
                    self.do_slide()
                else:
                    self.do_vault()
            else:
                self.do_go(obj)
        elif verb == "LOOK" or verb == "L":
            self.do_look()
        elif verb == "INVENTORY" or verb == "I":
            self.do_inventory()
        elif verb == "GET" or verb == "TAKE" or verb == "GRAB":
            self.do_get(obj)
        elif verb == "DROP" or verb == "PUT":
            self.do_drop(obj)
        elif verb == "TIE" or (verb == "TIE" and obj):
            self.do_tie(obj)
        elif verb == "INFLATE":
            self.do_inflate(obj)
        elif verb == "USE" and obj:
            self.do_use(obj)
        elif verb == "CROSS" or verb == "SWIM":
            self.do_cross()
        # Floor 7 vault special commands
        elif verb == "VAULT" or verb == "OPEN VAULT" or verb == "UNLOCK DOOR" or (verb == "UNLOCK" and "DOOR" in obj.upper()) or (verb == "OPEN" and "DOOR" in obj.upper()):
            self.do_vault()
        elif verb == "USE KEY" or (verb == "USE" and "KEY" in obj.upper()):
            self.do_use_key()
        elif verb == "GLUE STEP" or (verb == "GLUE" and "STEP" in obj.upper()):
            self.do_glue_step()
        elif verb == "SLIDE" or verb == "GO SLIDE" or (verb == "GO" and "SLIDE" in obj.upper()):
            self.do_slide()
        elif verb == "READ SIGN" or (verb == "READ" and "SIGN" in obj.upper()):
            self.do_read_sign()
        elif verb == "VENDING" or verb == "USE VENDING" or (verb == "USE" and "VENDING" in obj.upper()) or (verb == "INSERT" and "TIN" in obj.upper()):
            self.do_vending()
        # Floor 6 office commands
        elif verb == "PAY" or verb == "USE DOLLAR" or (verb == "INSERT" and "DOLLAR" in obj.upper()):
            self.do_pay_vending()
        elif verb == "PRESS BUTTON" or verb == "PUSH BUTTON" or (verb == "PRESS" and "BUTTON" in obj.upper()) or (verb == "PUSH" and "BUTTON" in obj.upper()):
            self.do_press_button()
        elif verb == "JUMP" or verb == "LEAP":
            self.do_jump()
        # Floor 5 Mary Poppins / Weird floor commands
        elif verb == "KNIT" or verb == "KNITTING" or verb == "KNIT CLOTHES":
            self.do_knit()
        elif verb == "UNLOCK DOOR" or verb == "UNLOCK" or verb == "USE KEY" or (verb == "USE" and "KEY" in obj.upper()) or (verb == "OPEN" and "DOOR" in obj.upper()):
            # Floor-specific: Floor 5 has a locked door in pool/sitting room
            if self.state.floor == 5:
                self.do_floor5_unlock()
            else:
                self.do_use_key()
        elif verb == "DRINK" or verb == "USE BOTTLE" or verb == "DRINK POTION":
            self.do_drink()
        elif verb == "USE UMBRELLA" or verb == "UMBRELLA" or (verb == "USE" and "UMBRELLA" in obj.upper()):
            self.do_use_umbrella()
        elif verb == "USE SPONGE" or verb == "SPONGE" or (verb == "USE" and "SPONGE" in obj.upper()):
            self.do_use_sponge()
        elif verb == "DRAIN" or verb == "DRAIN POOL" or verb == "USE DRAIN" or (verb == "USE" and "BUTTON" in obj.upper()) or verb == "PRESS BUTTON" or verb == "PUSH BUTTON":
            # Floor 4: Drain the pool
            if self.state.floor == 4:
                self.do_drain()
            else:
                self.do_press_button()
        # Floor 3 Plant/Trap floor commands
        elif verb == "PLAY FLUTE" or verb == "USE FLUTE" or verb == "FLUTE" or (verb == "USE" and "FLUTE" in obj.upper()) or (verb == "PLAY" and "FLUTE" in obj.upper()):
            self.do_play_flute()
        # Floor 2 Piano commands
        elif verb == "PLAY PIANO" or verb == "USE PIANO" or verb == "PIANO" or (verb == "USE" and "PIANO" in obj.upper()) or (verb == "PLAY" and "PIANO" in obj.upper()):
            self.do_play_piano()
        elif verb == "QUIT" or verb == "Q" or verb == "BYE":
            print("THANKS FOR PLAYING!")
            self.running = False
        elif verb == "HELP" or verb == "?":
            self.do_help()
        else:
            print(f"I DON'T UNDERSTAND '{cmd}'")
            print("TYPE 'HELP' FOR COMMANDS.")

    def do_tie(self, obj):
        """Tie something (rope)"""
        if not obj:
            print("TIE WHAT?")
            return
        obj = obj.upper()

        if self.state.floor == 8:
            if "ROPE" in obj:
                if self.state.location not in [23, 25]:
                    print("YOU CAN'T TIE THE ROPE HERE.")
                    return
                if self.state.rope_tied:
                    print("THE ROPE IS ALREADY STRETCHED ACROSS THE POOL.")
                    return
                if not self.state.rope_taken:
                    print("YOU DON'T HAVE THE ROPE!")
                    return
                print("YOU STRETCH THE ROPE ACROSS THE POOL, TIED SECURELY TO STAKE ON EACH SIDE.")
                print("THE PIRANHAS LOOK UP, DISAPPOINTED.")
                self.state.rope_tied = True
            else:
                print(f"YOU CAN'T TIE THE {obj}.")
        elif self.state.floor == 6:
            if "STRING" in obj or "BALLOON" in obj:
                self.do_tie_string()
            else:
                print(f"YOU CAN'T TIE THE {obj} HERE.")
        elif self.state.floor == 2:
            if "ROPE" in obj:
                if self.state.location != 81:
                    print("YOU CAN'T TIE THE ROPE HERE.")
                    print("YOU NEED TO FIND THE QUICKSAND BOG AND A STAKE TO TIE IT TO.")
                    return
                if self.state.floor2_rope_stretched:
                    print("THE ROPE IS ALREADY STRETCHED ACROSS THE QUICKSAND!")
                    return
                if "ROPE" not in self.player_inventory and "LARGE ROPE" not in self.player_inventory:
                    print("YOU DON'T HAVE THE ROPE!")
                    print("YOU NEED TO FIND A ROPE FIRST.")
                    return
                print("YOU TIE THE ROPE SECURELY TO THE LARGE WOODEN STAKE!")
                print("YOU STRETCH THE OTHER END TOWARD THE OTHER SIDE...")
                print("THE ROPE IS NOW STRETCHED ACROSS THE QUICKSAND!")
                print("YOU CAN NOW CROSS SAFELY BY HOLDING THE ROPE!")
                self.state.floor2_rope_stretched = True
                self.state.floor2_rope_tied = True
                # Remove rope from inventory
                if "ROPE" in self.player_inventory:
                    self.player_inventory.remove("ROPE")
                if "LARGE ROPE" in self.player_inventory:
                    self.player_inventory.remove("LARGE ROPE")
                self.player_inventory.append("ROPE (STRETCHED)")
            else:
                print(f"YOU CAN'T TIE THE {obj} HERE.")
        else:
            print("THERE'S NOTHING TO TIE HERE.")

    def do_inflate(self, obj):
        """Inflate something (balloon)"""
        if not obj:
            print("INFLATE WHAT?")
            return
        obj = obj.upper()

        if self.state.floor == 8:
            if "BALLOON" in obj:
                if self.state.balloon_inflated:
                    print("THE BALLOON IS ALREADY INFLATED.")
                    return
                if not self.state.balloon_taken:
                    print("YOU DON'T HAVE THE BALLOON!")
                    return
                if not self.state.helium_taken:
                    print("YOU NEED HELIUM TO INFLATE THE BALLOON.")
                    return
                print("YOU CONNECT THE HELIUM TANK TO THE BALLOON AND FILL IT WITH GAS.")
                print("THE BALLOON EXPANDS, FLOATING GENTLY UPWARD!")
                print("IT SEEMS STRONG ENOUGH TO HOLD YOUR WEIGHT IF YOU HOLD ONTO IT.")
                self.state.balloon_inflated = True
            else:
                print(f"YOU CAN'T INFLATE THE {obj}.")
        elif self.state.floor == 6:
            if "BALLOON" in obj:
                self.do_press_button()
            else:
                print(f"YOU CAN'T INFLATE THE {obj}.")
        else:
            print("THERE'S NOTHING HERE TO INFLATE.")

    def do_use(self, obj):
        """Use an item"""
        if not obj:
            print("USE WHAT?")
            return
        obj = obj.upper()

        if self.state.floor == 8:
            if "PILL" in obj or "SLEEPING" in obj:
                if self.state.location == 22 or self.state.location == 23:
                    if self.state.piranha_dead:
                        print("THE PIRANHAS ARE ALREADY DEAD.")
                    else:
                        print("YOU THROW THE SLEEPING PILL INTO THE WATER...")
                        print("THE PIRANHAS GOBBLE IT UP!")
                        print("AFTER A FEW MOMENTS, THEY ALL FALL ASLEEP AND SINK TO THE BOTTOM.")
                        print("THE POOL IS NOW SAFE TO CROSS!")
                        self.state.piranha_dead = True
                        self.state.rope_tied = True  # Now safe to cross
                else:
                    print("THERE'S NO POINT USING THAT HERE.")
            elif "GLUE" in obj:
                if self.state.rope_taken and self.state.location == 25:
                    print("YOU APPLY THE SUPER GLUE TO THE ROPE ENDS.")
                    print("THIS WILL HELP SECURE THE KNOTS.")
                else:
                    print("YOU CAN'T USE THAT HERE.")
            else:
                print(f"YOU CAN'T USE THE {obj}.")
        elif self.state.floor == 6:
            if "DOLLAR" in obj:
                self.do_pay_vending()
            elif "BUTTON" in obj:
                self.do_press_button()
            elif "STRING" in obj or "BALLOON" in obj:
                if "BALLOON" in obj:
                    self.do_press_button()
                else:
                    print("USE THE STRING TO DO WHAT?")
            else:
                print(f"YOU CAN'T USE THE {obj} HERE.")
        elif self.state.floor == 9:
            # Floor 9: TAPE on WIRES fixes the elevator
            if "TAPE" in obj or "WIRES" in obj:
                if "TAPE" not in self.player_inventory:
                    print("YOU DON'T HAVE ANY TAPE.")
                elif self.state.location != 13:
                    print("THERE ARE NO WIRES HERE TO TAP.")
                elif self.state.tape_used:
                    print("THE WIRES ARE ALREADY TAPED.")
                elif self.state.time < 12:
                    print("YOU TOUCH THE LIVE WIRES...")
                    print("ZAP! YOU'RE ELECTROCUTED!")
                    self.state.dead = True
                    self.running = False
                else:
                    print("YOU WRAP THE ELECTRIC TAPE AROUND THE LIVE WIRES...")
                    print("SPARK! THE WIRES ARE NOW SAFELY INSULATED.")
                    print("THE ELEVATOR IS NOW FIXED!")
                    self.state.tape_used = True
                    self.state.elevator_fixed = True
            elif "BROOM" in obj:
                if self.state.location == 7 and "KEY" in self.rooms[7].get("items", []):
                    if "BROOM" not in self.player_inventory:
                        print("YOU DON'T HAVE THE BROOM.")
                    else:
                        print("YOU USE THE BROOM TO KNOCK THE KEY OFF THE LEDGE!")
                        self.state.key_taken = True
                else:
                    print("THERE'S NO USE FOR THE BROOM HERE.")
            elif "FIX" in obj or "REPAIR" in obj or "ELEVATOR" in obj:
                if self.state.elevator_fixed:
                    print("THE ELEVATOR IS ALREADY FIXED!")
                elif not self.state.tape_used:
                    print("THE ELEVATOR ISN'T WORKING. THE WIRES NEED TO BE FIXED FIRST.")
                else:
                    print("THE ELEVATOR IS NOW WORKING!")
                    self.state.elevator_fixed = True
            else:
                print("YOU CAN'T USE THAT HERE.")
        else:
            print("YOU CAN'T USE THAT HERE.")

    def do_cross(self):
        """Cross the piranha pool on Floor 8"""
        if self.state.floor != 8:
            print("THERE'S NOTHING TO CROSS HERE.")
            return

        if self.state.location not in [22, 23, 24]:
            print("YOU CAN'T CROSS FROM HERE.")
            return

        if self.state.rope_tied:
            print("YOU CLING TO THE ROPE AND PULL YOURSELF ACROSS!")
            # Move to the other side
            if self.state.location == 23:
                self.state.location = 24
            else:
                self.state.location = 23
            self.print_status()
        elif self.state.balloon_inflated:
            print("YOU HOLD ONTO THE BALLOON AND FLOAT ACROSS!")
            if self.state.location == 23:
                self.state.location = 24
            else:
                self.state.location = 23
            self.print_status()
        elif self.state.piranha_dead:
            print("YOU WALK ACROSS THE POOL FLOOR. THE PIRANHAS ARE ALL ASLEEP.")
            if self.state.location == 23:
                self.state.location = 24
            else:
                self.state.location = 23
            self.print_status()
        else:
            print("YOU WADE INTO THE WATER TO CROSS...")
            print("THE PIRANHAS ATTACK!")
            print("THOUSANDS OF RAZOR-SHARP TEETH TEAR AT YOUR FLESH!")
            print("YOU HAVE DIED A TERRIBLE DEATH.")
            self.running = False

    # ============= FLOOR 7 VAULT COMMANDS =============

    def do_vault(self):
        """Try to open/unlock the vault door"""
        if self.state.floor != 7:
            print("THERE'S NO VAULT HERE.")
            return

        loc = self.state.location

        # Can only unlock vault door from rooms 32 or 55
        if loc not in [32, 55]:
            print("THERE'S NO VAULT DOOR HERE.")
            return

        if self.state.vault_door_unlocked:
            print("THE VAULT DOOR IS ALREADY UNLOCKED.")
            return

        # Check if player has the small key
        if "SMALL KEY" in self.player_inventory or self.state.small_key_taken:
            print("YOU INSERT THE SMALL KEY INTO THE VAULT DOOR LOCK...")
            print("*CLICK!* *WHIRRRR*")
            print("THE VAULT DOOR UNLOCKS WITH A HEAVY CLUNK!")
            print("THE VAULT IS NOW ACCESSIBLE!")
            self.state.vault_door_unlocked = True
        else:
            print("THE VAULT DOOR IS LOCKED. YOU NEED A KEY TO OPEN IT.")
            print("THE SMALL BRASS KEY IN THE KEY ROOM MIGHT WORK...")

    def do_use_key(self):
        """Use the small key on the vault door"""
        if self.state.floor != 7:
            print("THERE'S NOTHING TO USE THE KEY ON HERE.")
            return

        if self.state.vault_door_unlocked:
            print("THE VAULT DOOR IS ALREADY UNLOCKED.")
            return

        if "SMALL KEY" not in self.player_inventory and not self.state.small_key_taken:
            print("YOU DON'T HAVE THE VAULT KEY!")
            return

        print("YOU INSERT THE SMALL KEY INTO THE VAULT DOOR LOCK...")
        print("*CLICK!* *WHIRRRR*")
        print("THE VAULT DOOR UNLOCKS WITH A HEAVY CLUNK!")
        self.state.vault_door_unlocked = True

    def do_glue_step(self):
        """Glue the loose step on the bank floor"""
        if self.state.floor != 7:
            print("THERE'S NO LOOSE STEP HERE.")
            return

        if self.state.location != 31:
            print("THERE'S NO LOOSE STEP HERE.")
            return

        if self.state.step_glued:
            print("THE STEP IS ALREADY SECURED WITH GLUE.")
            return

        if "GLUE" not in self.player_inventory and not self.state.glue_taken:
            print("YOU DON'T HAVE ANY GLUE!")
            print("YOU NEED SOMETHING TO SECURE THE LOOSE STEP.")
            return

        print("YOU APPLY THE SUPER GLUE TO THE LOOSE STEP...")
        print("THE STEP IS NOW SECURELY FASTENED IN PLACE!")
        print("YOU CAN NOW PASS SAFELY.")
        self.state.step_glued = True

    def do_slide(self):
        """Use the gold's slide to escape the vault"""
        if self.state.floor != 7:
            print("THERE'S NO SLIDE HERE.")
            return

        # From vault (55), going to the slide platform
        if self.state.location == 55:
            print("YOU CLIMB INTO THE GOLD'S SLIDE...")
            print("WHOOOOOOSH!")
            print("YOU SLIDE DOWN THE LONG, COILING BRASS TUBE...")
            print("AND LAND AT THE BOTTOM - FLOOR 6!")
            self.state.floor = 6
            self.state.reset_floor_flags()
            self.state.location = 41  # Floor 6 start
            self.print_status()
            return

        # From slide room (57)
        if self.state.location == 57:
            print("YOU GO DOWN THE GOLD'S SLIDE...")
            print("WHOOOOOOSH!")
            print("YOU SLIDE DOWN TO FLOOR 6!")
            self.state.floor = 6
            self.state.reset_floor_flags()
            self.state.location = 41
            self.print_status()
            return

        print("THERE'S NO SLIDE HERE.")

    def do_read_sign(self):
        """Read the vault dial sign"""
        if self.state.floor != 7:
            print("THERE'S NO SIGN HERE TO READ.")
            return

        if self.state.location in [32, 55]:
            print("THE SIGN READS: 'VAULT DIAL: 32-55-57'")
            print("THESE NUMBERS MIGHT BE IMPORTANT FOR THE VAULT COMBINATION...")
        else:
            print("THERE'S NO SIGN TO READ HERE.")

    def do_vending(self):
        """Use the vending machine with tin foil"""
        if self.state.floor != 7:
            print("THERE'S NO VENDING MACHINE HERE.")
            return

        if self.state.location != 32:
            print("THERE'S NO VENDING MACHINE HERE.")
            return

        if self.state.vending_used:
            print("THE VENDING MACHINE HAS ALREADY BEEN USED.")
            return

        if "TIN FOIL" not in self.player_inventory and not self.state.tin_foil_taken:
            print("YOU NEED SOMETHING TO PUT IN THE VENDING MACHINE.")
            return

        print("YOU CRUMPLE UP THE TIN FOIL AND INSERT IT INTO THE VENDING MACHINE...")
        print("CLUNK! CLUNK! CLUNK!")
        print("SOME KIND OF COIN POPS OUT OF THE COIN SLOT!")
        print("IT LOOKS LIKE A VERY OLD COIN - PROBABLY WORTH $1.00")
        self.state.vending_used = True

    # ============= FLOOR 6 OFFICE COMMANDS =============

    def do_pay_vending(self):
        """Pay the string vending machine on Floor 6"""
        if self.state.floor != 6:
            print("THERE'S NO STRING VENDING MACHINE HERE.")
            return

        if self.state.location != 45:
            print("THERE'S NO STRING VENDING MACHINE HERE.")
            return

        if self.state.floor6_vending_paid:
            print("THE STRING VENDING MACHINE HAS ALREADY DISPENSED.")
            return

        if "DOLLAR" not in self.player_inventory:
            print("YOU NEED A DOLLAR TO USE THE STRING VENDING MACHINE.")
            print("MAYBE YOU CAN FIND ONE SOMEWHERE ON THIS FLOOR...")
            return

        print("YOU INSERT THE DOLLAR BILL INTO THE STRING VENDING MACHINE...")
        print("CLUNK! CLUNK! CLUNK!")
        print("A LONG COIL OF STRING POPS OUT OF THE MACHINE!")
        print("YOU TAKE THE STRING.")
        self.state.floor6_vending_paid = True
        self.state.floor6_string_taken = True
        if "STRING" not in self.player_inventory:
            self.player_inventory.append("STRING")
        # Remove dollar from inventory
        if "DOLLAR" in self.player_inventory:
            self.player_inventory.remove("DOLLAR")

    def do_press_button(self):
        """Press the button on the wall (inflates balloon)"""
        if self.state.floor != 6:
            print("THERE'S NO BUTTON HERE.")
            return

        if self.state.location not in [42, 44]:
            print("THERE'S NO BUTTON HERE.")
            return

        if self.state.floor6_button_pressed:
            print("THE BUTTON HAS ALREADY BEEN PRESSED.")
            return

        if "BALLOON" not in self.player_inventory and not self.state.floor6_balloon_taken:
            print("YOU PRESS THE BUTTON...")
            print("A MECHANISM CLICKS, BUT NOTHING HAPPENS.")
            print("THE BUTTON SEEMS TO BE WAITING FOR A BALLOON TO BE PLACED NEARBY.")
            return

        if self.state.floor6_balloon_inflated:
            print("THE BALLOON IS ALREADY INFLATED.")
            return

        print("YOU PRESS THE BUTTON ON THE WALL...")
        print("*CLICK* *HISS* *WHIRRRR*")
        print("A MECHANISM ACTIVATES!")
        print("SOME KIND OF PNEUMATIC SYSTEM BEGINS TO INFLATE THE BALLOON!")
        print("THE BALLOON EXPANDS, FLOATING GENTLY UPWARD!")
        print("IT'S A HELIUM BALLOON - IT WANTS TO FLY AWAY!")
        self.state.floor6_button_pressed = True
        self.state.floor6_balloon_inflated = True

    def do_tie_string(self):
        """Tie the string to the balloon"""
        if self.state.floor != 6:
            print("THERE'S NOTHING TO TIE HERE.")
            return

        if self.state.location != 47:
            print("YOU SHOULD FIND A SAFE PLACE TO TIE THE STRING FIRST.")
            return

        if self.state.floor6_string_tied:
            print("THE STRING IS ALREADY TIED TO THE BALLOON.")
            return

        if not self.state.floor6_balloon_inflated:
            print("YOU CAN'T TIE STRING TO A DEFLATED BALLOON!")
            return

        if "STRING" not in self.player_inventory and not self.state.floor6_string_taken:
            print("YOU DON'T HAVE ANY STRING!")
            return

        print("YOU TIE THE STRING SECURELY TO THE BALLOON.")
        print("THE BALLOON IS NOW ANCHORED BY THE STRING.")
        print("YOU CAN HOLD ONTO THE STRING TO HELP YOU JUMP!")
        self.state.floor6_string_tied = True

    def do_jump(self):
        """Jump across the pit on Floor 6"""
        if self.state.floor != 6:
            print("THERE'S NOTHING TO JUMP OVER HERE.")
            return

        if self.state.location != 47:
            print("YOU CAN'T JUMP FROM HERE.")
            return

        if self.state.floor6_jumped:
            print("YOU'VE ALREADY JUMPED ACROSS THE PIT.")
            return

        if not self.state.floor6_balloon_inflated:
            print("YOU TRY TO JUMP ACROSS THE PIT...")
            print("YOU LEAP! BUT YOU CAN'T MAKE IT!")
            print("YOU FALL INTO THE PIT!")
            print("YOU HAVE DIED A TERRIBLE DEATH.")
            self.running = False
            return

        if not self.state.floor6_string_tied:
            print("YOU TRY TO JUMP ACROSS WITH THE BALLOON...")
            print("BUT THE BALLOON GETS AWAY FROM YOU!")
            print("WITHOUT BEING TIED DOWN, THE BALLOON FLOATS AWAY!")
            print("YOU FALL INTO THE PIT!")
            print("YOU HAVE DIED A TERRIBLE DEATH.")
            self.running = False
            return

        print("YOU HOLD TIGHT TO THE BALLOON AND STRING!")
        print("THE BALLOON LIFTS YOU LIGHTLY ACROSS THE PIT!")
        print("YOU LAND SAFELY ON THE OTHER SIDE!")
        self.state.floor6_jumped = True
        self.state.location = 48
        self.print_status()

    # ============= FLOOR 5 MARY POPPINS / WEIRD COMMANDS =============

    def do_knit(self):
        """Knit clothes using yarn and knitting needles"""
        if self.state.floor != 5:
            print("THERE'S NOTHING TO KNIT HERE.")
            return

        if self.state.location != 65:
            print("YOU SHOULD GO TO THE CRAFT ROOM TO KNIT.")
            return

        if self.state.floor5_clothes_knitted:
            print("YOU'VE ALREADY KNIT CLOTHES TODAY!")
            return

        # Check if player has both yarn and knitting needles
        has_yarn = "YARN" in self.player_inventory
        has_needles = "KNITTING NEEDLES" in self.player_inventory

        if not has_yarn and not has_needles:
            print("YOU DON'T HAVE ANY YARN OR KNITTING NEEDLES!")
            print("YOU NEED BOTH TO KNIT CLOTHES.")
            return

        if not has_yarn:
            print("YOU DON'T HAVE ANY YARN!")
            print("YOU NEED YARN TO KNIT CLOTHES.")
            return

        if not has_needles:
            print("YOU DON'T HAVE ANY KNITTING NEEDLES!")
            print("YOU NEED KNITTING NEEDLES TO KNIT CLOTHES.")
            return

        print("YOU SIT DOWN AND BEGIN TO KNIT...")
        print("CLICKITY-CLACKETY-CLICK...")
        print("AFTER SOME TIME, YOU'VE KNIT A LOVELY SET OF CLOTHES!")
        print("A NICE WARM SWEATER AND COMFY PANTS!")
        print("YOU FEEL VERY PROUD OF YOURSELF.")
        self.state.floor5_clothes_knitted = True
        # Remove yarn and needles from inventory (used up)
        if "YARN" in self.player_inventory:
            self.player_inventory.remove("YARN")
        if "KNITTING NEEDLES" in self.player_inventory:
            self.player_inventory.remove("KNITTING NEEDLES")
        self.player_inventory.append("KNIT CLOTHES")

    def do_floor5_unlock(self):
        """Unlock the locked door in the pool room on Floor 5"""
        if self.state.floor != 5:
            print("THERE'S NO LOCKED DOOR HERE TO UNLOCK.")
            return

        # Check if player is in pool room (58) or sitting room (53)
        if self.state.location not in [64, 69]:
            print("THERE'S NO LOCKED DOOR HERE.")
            return

        if self.state.floor5_door_unlocked:
            print("THE DOOR IS ALREADY UNLOCKED.")
            return

        if "SMALL KEY" not in self.player_inventory and not self.state.floor5_small_key_taken:
            print("YOU DON'T HAVE A KEY!")
            print("YOU NEED A SMALL KEY TO UNLOCK THIS DOOR.")
            return

        print("YOU INSERT THE SMALL KEY INTO THE LOCK...")
        print("*CLICK!* *WHIRRRR*")
        print("THE DOOR UNLOCKS WITH A SATISFYING CLICK!")
        self.state.floor5_door_unlocked = True

    def do_drink(self):
        """Drink a potion - transforms into Hyde on certain floors"""
        # Floor 4: Jekyll/Hyde transformation in the lab
        if self.state.floor == 4:
            if self.state.location not in [72, 73]:
                print("THERE'S NOTHING HERE TO DRINK.")
                return

            if "YELLOW POTION" not in self.player_inventory:
                print("YOU DON'T HAVE ANY POTION TO DRINK!")
                return

            if self.state.jekyll_mode:
                print("YOU ALREADY DRANK THE POTION AND BECAME HYDE!")
                return

            print("YOU DRINK THE YELLOW POTION...")
            print("A STRANGE SENSATION OVERTAKES YOU...")
            print("YOUR BODY BEGINS TO CHANGE!")
            print("YOUR MUSCLES GROW, YOUR EYES TURN GREEN...")
            print("YOU'VE CHANGED INTO HYDE! YOU ARE VERY STRONG!")
            self.state.jekyll_mode = True
            self.state.hyde_mode = True
            # Remove potion from inventory
            if "YELLOW POTION" in self.player_inventory:
                self.player_inventory.remove("YELLOW POTION")
            return

        # Floor 3: Plant transformation - drink the mysterious fluid to become a huge plant
        if self.state.floor == 3 and self.state.location in [77, 78]:
            if self.state.floor3_fluid_drunk or self.state.floor3_solution_drunk:
                print("YOU'VE ALREADY DRUNK THE MYSTERIOUS FLUID!")
                print("YOUR BODY IS ALREADY CHANGED...")
                print("YOU ARE A HUGE, STRANGE PLANT!")
                return

            # Check if player has FLUID or SOLUTION
            has_fluid = "FLUID" in self.player_inventory
            has_solution = "SOLUTION" in self.player_inventory

            if not has_fluid and not has_solution:
                print("YOU LOOK AROUND FOR SOMETHING TO DRINK...")
                print("YOU DON'T SEE ANYTHING SAFE TO DRINK HERE.")
                print("PERHAPS THE POOL CHAMBER HAS SOMETHING...")
                return

            if has_fluid:
                print("YOU DRINK THE MYSTERIOUS FLUID...")
                print("A STRANGE SENSATION OVERTAKES YOUR BODY!")
                print("YOUR LIMBS BEGIN TO STRETCH AND TWIST...")
                print("YOUR SKIN TURNS GREEN AND ROUGH...")
                print("VINES GROW FROM YOUR ARMS AND LEGS!")
                print("YOU'VE BECOME A HUGE, PLANT-LIKE CREATURE!")
                print("YOU CAN NOW BREAK THROUGH THICK VINES!")
                self.state.floor3_fluid_drunk = True
                self.player_inventory.remove("FLUID")
            elif has_solution:
                print("YOU DRINK THE STRANGE SOLUTION...")
                print("A STRANGE SENSATION OVERTAKES YOUR BODY!")
                print("YOUR LIMBS BEGIN TO STRETCH AND TWIST...")
                print("YOUR SKIN TURNS GREEN AND ROUGH...")
                print("VINES GROW FROM YOUR ARMS AND LEGS!")
                print("YOU'VE BECOME A HUGE, PLANT-LIKE CREATURE!")
                print("YOU CAN NOW BREAK THROUGH THICK VINES!")
                self.state.floor3_solution_drunk = True
                self.player_inventory.remove("SOLUTION")
            return
        elif self.state.floor == 5:
            print("YOU LOOK AROUND FOR SOMETHING TO DRINK...")
            print("THERE'S NOTHING HERE THAT LOOKS SAFE TO DRINK.")
        else:
            print("THERE'S NOTHING HERE TO DRINK.")

    def do_use_umbrella(self):
        """Use the umbrella - Floor 5 shower/petit, Floor 4 parachute"""
        # Floor 4: Umbrella as parachute on diving board
        if self.state.floor == 4:
            if "UMBRELLA" not in self.player_inventory and not self.state.floor4_umbrella_taken:
                print("YOU DON'T HAVE AN UMBRELLA!")
                return

            if self.state.location != 76:
                print("YOU OPEN AND CLOSE THE UMBRELLA, BUT THERE'S NO USE FOR IT HERE.")
                return

            if self.state.floor4_umbrella_opened:
                print("THE UMBRELLA IS ALREADY OPEN!")
                print("YOU CAN NOW JUMP TO USE IT AS A PARACHUTE!")
                return

            print("YOU OPEN THE UMBRELLA WIDE!")
            print("IT EXPANDS INTO A LARGE PARASOL!")
            print("IF YOU JUMP NOW, IT SHOULD ACT LIKE A PARACHUTE!")
            self.state.floor4_umbrella_opened = True
            return

        # Floor 5: Umbrella protects from sprinklers in shower room
        if self.state.floor != 5:
            print("THERE'S NO UMBRELLA TO USE HERE.")
            return

        if "UMBRELLA" not in self.player_inventory and not self.state.floor5_umbrella_taken:
            print("YOU DON'T HAVE AN UMBRELLA!")
            return

        if self.state.location == 70:
            # In shower room - umbrella protects from sprinklers
            print("YOU OPEN THE UMBRELLA OVER YOUR HEAD.")
            print("THE SPRINKLERS TURN ON! (BLOOM!)")
            print("BUT YOU STAY DRY UNDER YOUR UMBRELLA!")
            print("WATER DRIPS OFF THE EDGES LIKE A WATERFALL.")
        elif self.state.location == 69:
            # In pool room - umbrella floats!
            print("YOU OPEN THE UMBRELLA AND HOLD IT ABOVE THE POOL...")
            print("THE UMBRELLA CATCHES THE AIR AND BEGINS TO LIFT!")
            print("IT'S LIKE A MAGIC CARPET! ALMOST...")
        else:
            print("YOU OPEN AND CLOSE THE UMBRELLA, BUT THERE'S NO USE FOR IT HERE.")

    def do_use_sponge(self):
        """Use the sponge on Floor 5"""
        if self.state.floor != 5:
            print("THERE'S NO SPONGE TO USE HERE.")
            return

        if "SPONGE" not in self.player_inventory and not self.state.floor5_sponge_taken:
            print("YOU DON'T HAVE A SPONGE!")
            return

        if self.state.location == 70:
            # In shower room - sponge cleans up water
            print("YOU USE THE SPONGE TO MOP UP THE WET FLOOR.")
            print("THE SPONGE SOAKS UP ALL THE WATER!")
            print("THE FLOOR IS NOW SAFE TO WALK ON.")
        elif self.state.location == 71:
            # In laundry room
            print("YOU SQUEEZE THE SPONGE OVER THE SINK...")
            print("WATER DRIPS OUT. IT'S NICE AND SQUEAKY.")
        else:
            print("YOU SQUEEZE THE SPONGE BUT THERE'S NO USE FOR IT HERE.")

    def do_drain(self):
        """Drain the pool on Floor 4"""
        if self.state.floor != 4:
            print("THERE'S NO DRAIN HERE.")
            return

        if self.state.location != 75:
            print("THERE'S NO DRAIN CONTROL HERE.")
            return

        if self.state.floor4_pool_drained:
            print("THE POOL IS ALREADY DRAINED.")
            return

        print("YOU PRESS THE BIG RED 'POOL DRAIN' BUTTON!")
        print("*GRIND...GRIND...WHOOOOSH*")
        print("THE TOXIC GREEN LIQUID DRAINS OUT OF THE POOL!")
        print("BELOW YOU CAN SEE THE HARD POOL FLOOR.")
        print("THE POOL IS NOW EMPTY AND SAFE!")
        self.state.floor4_pool_drained = True

    def do_play_flute(self):
        """Play the flute on Floor 3 to descend to Floor 2"""
        if self.state.floor != 3:
            print("THERE'S NO FLUTE TO PLAY HERE.")
            return

        if self.state.location != 80:
            print("YOU CAN'T PLAY THE FLUTE HERE.")
            return

        if "FLUTE" not in self.player_inventory and not self.state.floor3_flute_taken:
            print("YOU DON'T HAVE THE FLUTE!")
            print("THE FLUTE IS ON THE PEDESTAL IN THE ALCOVE.")
            return

        if self.state.floor3_flute_played:
            print("YOU'VE ALREADY PLAYED THE FLUTE TO DESCEND.")
            return

        print("YOU PUT THE FLUTE TO YOUR LIPS AND PLAY A HAUNTING MELODY...")
        print("THE NOTES ECHO THROUGH THE BUILDING...")
        print("SUDDENLY, THE FLOOR BENEATH YOU GIVES WAY!")
        print("A MAGICAL STAIRWAY REVEALS ITSELF!")
        print("YOU DESCEND THE STAIRS TO FLOOR 2...")
        self.state.floor3_flute_played = True
        self.state.floor = 2
        self.state.reset_floor_flags()
        self.state.location = 81  # Floor 2 start (QUICKSAND CHAMBER)
        self.print_status()

    def do_play_piano(self):
        """Play the piano on Floor 2"""
        if self.state.floor != 2:
            print("THERE'S NO PIANO HERE.")
            return

        if self.state.location != 84:
            print("YOU CAN'T PLAY THE PIANO HERE.")
            print("THE PIANO IS IN THE PIANO ROOM ON THE OTHER SIDE OF THE QUICKSAND.")
            return

        if self.state.floor2_piano_played:
            print("YOU'VE ALREADY PLAYED THE PIANO.")
            print("THE BEAUTIFUL MELODY STILL HANGS IN THE AIR...")
            return

        print("YOU SIT DOWN AT THE GRAND PIANO AND PLAY A BEAUTIFUL MELODY...")
        print("DOH RE MI FAH SO LA TI DOH...")
        print("THE NOTES RING OUT THROUGH THE OLD BUILDING!")
        print("AS THE LAST NOTE FADES, YOU HEAR A CLICKING SOUND FROM SOMEWHERE...")
        print("SOMETHING HAS UNLOCKED!")
        print()
        print("A SECRET PASSAGEWAY HAS OPENED IN THE WALL!")
        print("STAIRS LEAD DOWN TO THE FLOOR BELOW - THE GROUND FLOOR!")
        self.state.floor2_piano_played = True
        # Update the piano room exits to show the new stairs down
        self.rooms[84]["exits"]["D"] = 91
        print()
        print("YOU CAN NOW GO DOWN THE STAIRS TO THE GROUND FLOOR!")

    def do_help(self):
        """Show help"""
        print("\n=== COMMANDS ===")
        print("LOOK (L) - Describe your surroundings")
        print("N/S/E/W/U/D - Move in a direction")
        print("GET <ITEM> - Pick up an item")
        print("DROP <ITEM> - Drop an item")
        print("INVENTORY (I) - See what you're carrying")
        print("TIE <ITEM> - Tie something (e.g., TIE ROPE)")
        print("INFLATE <ITEM> - Inflate something (e.g., INFLATE BALLOON)")
        print("USE <ITEM> - Use an item")
        print("CROSS - Cross a gap/pool (Floor 8)")
        print("UNLOCK DOOR / VAULT - Unlock the vault door (Floor 7)")
        print("GLUE STEP - Glue a loose step (Floor 7)")
        print("SLIDE - Use the gold's slide (Floor 7)")
        print("READ SIGN - Read the vault dial sign (Floor 7)")
        print("PAY - Pay the string vending machine (Floor 6)")
        print("PRESS BUTTON / PUSH BUTTON - Press button on wall (Floor 6)")
        print("JUMP - Jump across a gap (Floor 6)")
        print("KNIT - Knit clothes with yarn and needles (Floor 5)")
        print("UNLOCK DOOR - Unlock a locked door (Floor 5)")
        print("DRINK - Drink a potion (Floor 4 - Hyde mode!)")
        print("USE UMBRELLA - Use an umbrella (Floor 4: parachute, Floor 5: shower)")
        print("USE SPONGE - Use a sponge (Floor 5)")
        print("DRAIN - Drain the pool (Floor 4)")
        print("PLAY FLUTE / USE FLUTE - Play the flute to descend (Floor 3)")
        print("PLAY PIANO / USE PIANO - Play the piano (Floor 2)")
        print("QUIT - End the game")
        print("HELP - Show this message")
        print()

    def game_loop(self):
        """Main game loop"""
        self.print_intro()
        self.print_status()

        while self.running:
            try:
                cmd = input("\nWHAT DO YOU WANT TO DO? ").strip()
                if cmd:
                    self.process_command(cmd)
            except (EOFError, KeyboardInterrupt):
                print("\n\nTHANKS FOR PLAYING!")
                break

        # Player died
        if not self.running and self.state.floor > 0:
            print("\n" + "=" * 50)
            print("GAME OVER")
            print(f"You reached Floor {self.state.floor}")
            print("=" * 50)
            retry = input("\nTRY AGAIN? (Y/N) ").strip().upper()
            if retry == "Y":
                # Reset game
                self.state = GameState()
                self.player_inventory = []
                self.running = True
                self.rooms = self.build_rooms()
                self.print_status()
            else:
                print("THANKS FOR PLAYING!")

def main():
    game = KidnappedGame()
    game.game_loop()

if __name__ == "__main__":
    main()
