# KIDNAPPED! — Parallel Rebuild Spec

## Game Overview
- **Original:** Peter Kirsch, 1980 (SoftSide Magazine)
- **Platform:** TRS-80 / S-80 (16K machines)
- **Rooms:** 65 locations across 9 floors
- **Objective:** Escape a 9-story building as a kidnapping victim, floor by floor
- **Items:** Each floor is independent — no item carryover between floors

## ⚠️ CRITICAL: Use Clean PDF Source
The original OCR'd text is GARBLED. Use these sources instead:
1. **KIDNAPPED_Original.pdf** — clean PDF (SoftSide Vol 3 No 03)
2. **PARSED_BASIC_SOURCE.txt** — parsed room/item data from clean PDF
3. **GAME_ANALYSIS.txt** — game analysis from RetroGamesTroove review

## Architecture
Each floor is a **separate Python module** in `floors/` directory.
A central `engine.py` handles command parsing, floor transitions, win/lose conditions.

## CRITICAL: Bidirectional Navigation Rule
Every exit MUST be symmetric:
- If Room A has `N=B`, then Room B MUST have `S=A`
- If Room A has `E=B`, then Room B MUST have `W=A`
- Run `tests/test_navigation.py` to verify ALL floors pass before considering done
- This was the PRIMARY source of bugs in all prior rebuild attempts

## KEY PUZZLE: Floor 9 Midnight Blackout
From the RetroGamesTroove review (verified by player Chris):
> "The exposed wires providing power to the elevator are 'hot' — you're going to need to coordinate your repairs with a building blackout that occurs at midnight."

The TIME variable (TI) controls this:
- Line 830: `IF TI<23` — wires are LIVE until after 11 PM
- Player must WAIT until after midnight to safely tape wires
- The CLOCK in room 5 is frozen at midnight

## Correct Floor 9 Room Layout (from BASIC)
```
Room 1:  N=2, E=8, S=7      (elevator hub)
Room 2:  N=3, S=1           (office, FLASHLIGHT here)
Room 3:  S=2                 (closet, CHAIR)
Room 4:  W=5, E=1, S=6      (roof)
Room 5:  E=4                 (large room, TV/CLOCK/LOCKED DOOR)
Room 6:  N=4                 (restroom, GRAFFITI)
Room 7:  N=1                 (office, KEY on ledge)
Room 8:  N=9, W=1, S=10    (elevator)
Room 9:  S=8, U=11, D=10   (elevator, PUSH BUTTON)
Room 10: N=8, U=9           (crawlspace)
Room 11: D=9, E=13, W=15   (shaft, LIVE WIRES)
Room 13: W=11, S=16, E=14  (visitor lounge)
Room 14: W=15, E=13         (small room)
Room 15: E=14, W=11         (closet, TAPE)
Room 16: N=13, E=17         (nursery)
Room 17: W=16                (storage)
```

## Correct Floor 9 Items (from BASIC DATA)
```
Room 2:  PAPER NOTE, CHAIR (takeable)
Room 3:  LONG BROOM (takeable)
Room 5:  TV SET, CLOCK, LOCKED DOOR (fixed)
Room 6:  GRAFFITI ON WALL (fixed)
Room 7:  OPEN WINDOW (fixed) — KEY on ledge outside
Room 9:  TRAP DOOR, PUSH BUTTON (fixed)
Room 10: CABINET (fixed) — opens to reveal FLASHLIGHT
Room 11: LIVE WIRES, ADMISSION (fixed)
Room 15: ROPE (takeable)
Room 16: SLEEPING PILL (takeable)
Room 19: KEY ON KEY CHAIN (takeable)
Room 20: SUPER GLUE, WOODEN STAIR STEP (takeable)
```

## Floor Themes & Difficulty
| Floor | Theme | Key Puzzles | Difficulty |
|-------|-------|-------------|------------|
| 9 | Roof | Midnight blackout, elevator repair | Moderate |
| 8 | Aquarium | Piranhas, balloon, gun | Moderate |
| 7 | Bank Vault | Burglar, dollar, vault | **HARDEST** |
| 6 | Office | Knitting, office girls | Moderate |
| 5 | Mary Poppins | Absurdist, umbrella | Moderate |
| 4 | Jekyll/Hyde | Transformation, potion | Moderate |
| 3 | Greenhouse | Plants, flute | Moderate |
| 2 | Quicksand | Piano, rope | Hard |
| 1 | Ground | Escape! | Easy |

## Test Suite
Always run `python3 tests/test_navigation.py` to verify bidirectional exits.
All floors must pass before considering a floor complete.

## File Inventory
```
KIDNAPPED_Original.pdf   — Clean source PDF (use this!)
PARSED_BASIC_SOURCE.txt   — Parsed room/item data from clean PDF
GAME_ANALYSIS.txt        — Game analysis from review + player memory
SPEC.md                   — This file
floors/floor_9.py        — Floor 9 (verified bidirectional)
floors/floor_7.py        — Floor 7 (has bidir errors)
floors/floor_1.py        — Floor 1 (has bidir errors)
v1_legacy/              — Archived original Python port
tests/test_navigation.py  — Bidirectional exit test suite
```

## History
This is Chris's 4th attempt from scratch to rebuild this game. Key lessons learned:
- OCR is unreliable for this BASIC source — always use clean PDF
- Bidirectional exit verification is MANDATORY per floor
- The midnight blackout puzzle is the key Floor 9 mechanic
- Parallel Lemmy approach had Token Plan concurrency limits (2-3 max)
