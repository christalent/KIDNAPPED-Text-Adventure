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
        result, transition = engine.handle_command(verb, noun)
        print(result)

        # Handle floor transition
        if transition:
            next_floor = state.floor - 1
            if next_floor < 1:
                print("\n" + "=" * 60)
                print("CONGRATULATIONS! You escaped the building!")
                print("=" * 60)
                state.game_over = True
                break

            print(f"\n=== Descending to Floor {next_floor}... ===\n")
            state.floor = next_floor

            engine_class = load_floor_engine(state.floor)
            if not engine_class:
                print(f"FATAL: Floor {next_floor} not implemented yet!")
                state.game_over = True
                break

            engine = engine_class(state)
            engine.on_enter()
            print(f"\n=== Floor {state.floor}: {get_floor_name(state.floor)} ===\n")
            result, _ = engine.handle_command("LOOK", "")
            print(result)

    print("\nThanks for playing KIDNAPPED!")


if __name__ == "__main__":
    main()
