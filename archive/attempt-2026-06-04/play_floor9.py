#!/usr/bin/env python3
"""Interactive test runner for Floor 9."""

import sys
sys.path.insert(0, 'floors')

from floors.floor_9 import Floor9Engine

class SimpleState:
    def __init__(self):
        self.location = 1
        self.inventory = []
        self.floor = 9
    def add_item(self, item): self.inventory.append(item)
    def remove_item(self, item):
        if item in self.inventory: self.inventory.remove(item)

def main():
    state = SimpleState()
    engine = Floor9Engine(state)
    engine.on_enter()

    print("=" * 60)
    print("KIDNAPPED! - Floor 9 (Interactive Test)")
    print("=" * 60)
    print("Commands: N/S/E/W/U/D, LOOK, GET <item>, DROP <item>,")
    print("         USE <item>, EXAMINE <item>, INVENTORY (or I), QUIT")
    print()
    print("(Type commands, one per line. Empty line to quit.)")
    print()

    # Show starting room
    result, _ = engine.handle_command("LOOK", "")
    print(result)
    print()

    # Read commands one at a time from stdin (works with pipes or interactive)
    line_num = 0
    while True:
        line_num += 1
        cmd = sys.stdin.readline()
        if not cmd:  # EOF
            break
        cmd = cmd.strip()

        if not cmd:
            break
        if cmd.upper() in ("QUIT", "Q", "EXIT"):
            print("Goodbye!")
            break

        # Parse command
        parts = cmd.upper().split()
        verb = parts[0]
        noun = " ".join(parts[1:]) if len(parts) > 1 else ""

        # Direction shortcuts: N/S/E/W/U/D alone → GO <dir>
        if verb in ("N", "S", "E", "W", "U", "D"):
            noun = verb
            verb = "GO"

        result, done = engine.handle_command(verb, noun)

        if result:
            print(result)

        if isinstance(result, str) and result.startswith("TRANSITION:"):
            print("\n" + "=" * 60)
            print("FLOOR TRANSITION:", result)
            print("=" * 60)

        print()

if __name__ == "__main__":
    main()
