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

## Audited Room Layout -- Floors 9 and 8 (source-verified 2026-11-03)
Replaces the old "Correct Floor 9 Room Layout" block, which was hand-patched
from the corrupted OCR layer (see FLOOR9_GROUND_TRUTH.md -- the invented
reciprocal `E=14`/`W=11` pairs made the bad map look symmetric).

### Floor 9 -- rooms 1-11
```
Room 1:  IN A HALLWAY                               W=4 N=2 E=8 S=7           
Room 2:  IN AN OFFICE                               N=3 S=1                     PAPER NOTE, DESK, CHAIR
Room 3:  IN A CLOSET                                S=2                         LONG BROOM
Room 4:  IN A HALLWAY                               N=5 E=1 S=6               
Room 5:  IN AN OFFICE                               S=4                         TV SET, CLOCK
Room 6:  IN A RESTROOM                              N=4                         GRAFFITI ON WALL
Room 7:  IN AN OFFICE                               N=1                         OPEN WINDOW, KEY ON KEY CHAIN
Room 8:  IN A HALLWAY                               W=1 N=9 S=10              
Room 9:  IN AN ELEVATOR                             S=8                         TRAP DOOR IN CEILING, DOWN BUTTON
Room 10:  IN A MAINTENANCE ROOM                     N=8                         CABINET, FLASHLIGHT, TAPE
Room 11:  IN A CRAWLSPACE ON TOP OF THE ELEVATOR    D=9                         ENDS OF 2 LIVE WIRES
```

### Floor 8 -- rooms 13-17
```
Room 13:  IN A HALLWAY                              W=14 S=16                 
Room 14:  IN A VISITORS LOUNGE                      W=15 E=13                   AQUARIUM
Room 15:  IN A CLOSET                               E=14                        ROPE
Room 16:  IN AN OFFICE                              N=13 E=17                   SLEEPING PILL
Room 17:  IN AN OFFICE                              W=16                        OPEN WINDOW, DESK
```

## Audited Items -- Floors 9 and 8
```
Floor 9:
  Room  2: PAPER NOTE (take), DESK (fixed), CHAIR (take)
  Room  3: LONG BROOM (take)          <- source DATA: "LONG BROOM",3
  Room  5: TV SET (fixed), CLOCK (fixed)
  Room  6: GRAFFITI ON WALL (fixed)    <- reads 'WATCH OUT FOR LIVE ONES'
  Room  7: OPEN WINDOW (fixed), KEY ON KEY CHAIN (take, created in code)
  Room  9: TRAP DOOR IN CEILING (fixed), DOWN BUTTON (fixed)
  Room 10: CABINET (fixed, opens to reveal FLASHLIGHT), TAPE (take)
  Room 11: ENDS OF 2 'LIVE' WIRES (fixed)
Floor 8:
  Room 14: AQUARIUM (fixed)            <- source DATA: "AQUARIUM",-14
  Room 15: ROPE (take)
  Room 16: SLEEPING PILL (take)
  Room 17: OPEN WINDOW (fixed), DESK (fixed)
```

Corrected source DATA rows and the OCR-vs-pixels evidence:
`KIDNAPPED_SOURCE_CORRECTED.txt`, `OCR_CORRECTIONS_2026-11-04.md`.

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
