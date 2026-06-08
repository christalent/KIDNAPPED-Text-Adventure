# KIDNAPPED! — Text Adventure

A Python port of the classic **KIDNAPPED!** text adventure game by Peter Kirsch (1980), published in SoftSide Magazine.

## Original Game
- **Platform:** TRS-80 / S-80 (16K machines)
- **Author:** Peter Kirsch, 1980
- **Locations:** 65+ rooms across 9 floors
- **Objective:** Escape a 9-story building as a kidnapping victim, floor by floor

## This Port
- **Language:** Python 3
- **Author:** Lemmy (AI assistant)
- **Based on:** Clean PDF source + parsed BASIC data
- **Architecture:** Modular — one Python file per floor in `floors/`, driven by a central `kidnapped.py` engine

## How to Play

```bash
# Start at floor 9 (the default — start of the game)
python3 kidnapped.py

# Start at a specific floor (1-9) for testing
python3 kidnapped.py --floor 5
```

Use 1-2 word commands like `LOOK`, `GET KEY`, `OPEN DOOR`, `N`, `S`, `E`, `W`, `U`, `D`, `INVENTORY` (or `I`), `HELP`, `QUIT`.

## Floor Status (2026-06-04)

All 9 floors implemented and passing bidirectional navigation tests.

| Floor | Theme | Rooms | Status |
|-------|-------|-------|--------|
| 9 | Roof — elevator & midnight blackout | 16 | ✅ Working |
| 8 | Aquarium — piranhas & balloon | 6 | ✅ Working |
| 7 | Bank Vault — combination locks | 10 | ✅ Working |
| 6 | Office — balloon/vending puzzles | 9 | ✅ Working |
| 5 | Weird (Mary Poppins) — knitting, umbrellas | 9 | ✅ Working |
| 4 | Jekyll/Hyde Lab — transformation | 8 | ✅ Working |
| 3 | Greenhouse — plants and traps | 5 | ✅ Working |
| 2 | Quicksand — piano puzzle | 5 | ✅ Working |
| 1 | Ground — escape! | 4 | ✅ Working |

**Total: 72 rooms** (vs the original's 65 — slight differences from hand-rebuilding with bidirectional exit verification).

## Project Structure

```
kidnapped-text-adventure/
├── kidnapped.py              # Main launcher (engine + REPL) — supports --floor N
├── floors/                   # One module per floor
│   ├── floor_1.py            # Ground floor
│   ├── floor_2.py            # Quicksand
│   ├── floor_3.py            # Greenhouse
│   ├── floor_4.py            # Jekyll/Hyde
│   ├── floor_5.py            # Mary Poppins
│   ├── floor_6.py            # Office
│   ├── floor_7.py            # Bank Vault
│   ├── floor_8.py            # Aquarium
│   └── floor_9.py            # Roof
├── tests/                    # Test suite
│   ├── test_navigation.py    # Bidirectional exit verification (all floors)
│   ├── test_floor5.py        # Per-floor regression tests
│   ├── test_floor7_floor6.py
│   └── test_floor9_fixes.py
├── SPEC.md                   # Architecture & design notes
├── PARSED_BASIC_SOURCE.txt   # Clean parsed room/item data (from PDF)
├── KIDNAPPED.BAS             # Reconstructed BASIC source
├── KIDNAPPED_OCR.txt         # OCR text from original PDF
├── KIDNAPPED_Original.pdf    # Original game PDF (SoftSide Dec 1980)
├── GAME_ANALYSIS.txt         # Review + player notes
├── README.md                 # This file
└── archive/
    └── attempt-2026-06-04/   # Old/broken attempts — see archive README
```

## Tests

```bash
# Verify all floors have correct bidirectional exits
python3 tests/test_navigation.py

# Per-floor regression tests
python3 tests/test_floor5.py
python3 tests/test_floor7_floor6.py
python3 tests/test_floor9_fixes.py

# Map consistency (new — catches what test_navigation.py misses)
python3 tests/test_floor9_map.py        # floor 9 deep map check
python3 tests/test_all_floors_map.py    # all 9 floors + ASCII render
python3 tests/test_floor9_playthrough.py # end-to-end puzzle solve
```

Current test results: **9/9 floors pass map consistency** (bidirectional,
reachable from start, no orphan rooms, matches source where the source
is authoritative), and Floor 9 is verified end-to-end solvable.

## Build Notes

- **No external dependencies** — pure Python 3 stdlib
- Python 3.8+ recommended (uses `argparse`, `importlib`)
- Each floor module is self-contained and importable on its own (the test suite relies on this)

## Archive

Older work and superseded files are in [`archive/attempt-2026-06-04/`](archive/attempt-2026-06-04/). See its README for details on what was archived and why.

## License
Original game © Peter Kirsch, 1980. This port is for personal/historical preservation purposes.
