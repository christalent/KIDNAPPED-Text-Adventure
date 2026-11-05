#!/usr/bin/env python3
"""
KIDNAPPED! — Main Game Engine
A Python port of the classic text adventure by Peter Kirsch (1980).
Manages floor transitions, global state, and command routing.
"""

import sys
import importlib
import argparse


class GameState:
    def __init__(self, floor=9):
        self.location = 1
        self.inventory = []
        self.floor = floor
        self.game_over = False
        self.alive = True
        self.pm_scared = False

    def add_item(self, item):
        self.inventory.append(item)
        print(f"  → You now have: {item}")

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def show_inventory(self):
        if not self.inventory:
            print("You're carrying nothing.")
        else:
            print("You are carrying:")
            for item in self.inventory:
                print(f"  - {item}")


def load_floor_engine(floor_num):
    """Import and return the floor engine for the given floor number."""
    try:
        module = importlib.import_module(f"floors.floor_{floor_num}")
        engine_class_name = f"Floor{floor_num}Engine"
        engine_class = getattr(module, engine_class_name)
        return engine_class
    except (ImportError, AttributeError) as e:
        print(f"Error loading floor {floor_num}: {e}")
        return None


def get_floor_name(floor_num):
    """Return the theme name for a floor number."""
    themes = {
        9: "The Roof",
        8: "The Aquarium",
        7: "The Bank Vault",
        6: "The Office",
        5: "Weird (Mary Poppins)",
        4: "Jekyll/Hyde Lab",
        3: "The Greenhouse",
        2: "The Quicksand",
        1: "Ground Floor — ESCAPE!",
    }
    return themes.get(floor_num, f"Floor {floor_num}")


def show_help():
    print("Commands:")
    print("  N/S/E/W/U/D  — Move (North/South/East/West/Up/Down)")
    print("  LOOK         — Look around the current room")
    print("  GET <item>   — Pick up an item")
    print("  DROP <item>  — Drop an item")
    print("  USE <item>   — Use an item")
    print("  OPEN <thing> — Open something")
    print("  EXAMINE <x>  — Examine something")
    print("  PUSH <x>     — Push a button or switch")
    print("  I / INV      — Show inventory")
    print("  HELP         — Show this help")
    print("  QUIT         — Quit the game")


def ensure_valid_location(engine, state):
    """Some floors' on_enter() leaves state.location outside their own room table.

    A direct '--floor N' start then lands the player nowhere. Pick the floor's
    own arrival room (or its lowest room) instead.
    """
    mod = sys.modules.get(type(engine).__module__)
    rooms = getattr(mod, "ROOMS", None) if mod else None
    if not rooms:
        return
    if getattr(state, "location", None) in rooms:
        return
    special = getattr(mod, "SPECIAL_ROOMS", {}) or {}
    candidates = [e["landing_room"] for e in special.values()
                   if isinstance(e, dict) and "landing_room" in e]
    candidates.append(min(rooms))
    for cand in candidates:
        if cand in rooms:
            state.location = cand
            return


def main():
    parser = argparse.ArgumentParser(description="KIDNAPPED! text adventure")
    parser.add_argument("--floor", type=int, default=9,
                        help="Starting floor (1-9, default: 9)")
    args = parser.parse_args()

    print("=" * 60)
    print("KIDNAPPED!")
    print("A text adventure by Peter Kirsch (1980)")
    print("Python port by Lemmy (AI assistant)")
    print("=" * 60)
    print()
    print("You wake up in a strange building. You must escape.")
    print("Floor by floor, room by room — find the exits!")
    print("Type HELP for commands.")
    print()

    state = GameState(floor=args.floor)
    engine_class = load_floor_engine(state.floor)
    if not engine_class:
        print(f"FATAL: Could not load starting floor {state.floor}!")
        return

    engine = engine_class(state)
    engine.on_enter()
    ensure_valid_location(engine, state)

    print(f"\n=== Floor {state.floor}: {get_floor_name(state.floor)} ===\n")

    result, transition = engine.handle_command("LOOK", "")
    print(result)

    while not state.game_over:
        print()
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not cmd:
            continue

        parts = cmd.upper().split()
        verb = parts[0]
        noun = " ".join(parts[1:]) if len(parts) > 1 else ""

        # Parse direction shortcuts
        if verb in ("N", "S", "E", "W", "U", "D"):
            noun = verb
            verb = "GO"

        # Built-in commands
        if verb in ("QUIT", "Q", "EXIT"):
            print("Goodbye!")
            break
        if verb in ("HELP", "H", "?"):
            show_help()
            continue
        if verb in ("INV", "INVENTORY", "I"):
            state.show_inventory()
            continue

        # Pass to floor engine
        _res = engine.handle_command(verb, noun)
        if _res is None:
            # Floors 1-4 return bare None for unhandled verbs.
            result, transition = "You can't do that here.", False
        else:
            result, transition = _res
        if not (isinstance(result, str) and result.startswith("TRANSITION:")):
            print(result)

        # Handle floor transition
        if transition:
            target_floor = None
            landing_room = None
            if isinstance(result, str) and result.startswith("TRANSITION:floor_"):
                try:
                    _pf, _pr = result[len("TRANSITION:"):].split(":", 1)
                    target_floor = int(_pf.split("_")[1])
                    landing_room = int(_pr)
                except (ValueError, IndexError):
                    target_floor = None
            next_floor = target_floor if target_floor is not None else state.floor - 1
            if next_floor < 1:
                print("\n" + "=" * 60)
                print("CONGRATULATIONS! You escaped the building!")
                print("=" * 60)
                state.game_over = True
                break

            _word = "Descending to" if next_floor < state.floor else "Ascending to"
            print(f"\n=== {_word} Floor {next_floor}... ===\n")
            state.floor = next_floor

            engine_class = load_floor_engine(state.floor)
            if not engine_class:
                print(f"FATAL: Floor {next_floor} not implemented yet!")
                state.game_over = True
                break

            if landing_room is not None:
                state.location = landing_room

            engine = engine_class(state)
            engine.on_enter()
            ensure_valid_location(engine, state)
            print(f"\n=== Floor {state.floor}: {get_floor_name(state.floor)} ===\n")
            result, _ = engine.handle_command("LOOK", "")
            print(result)

    print("\nThanks for playing KIDNAPPED!")


if __name__ == "__main__":
    main()
