# KIDNAPPED! — Text Adventure

A Python port of the classic **KIDNAPPED!** text adventure game by Peter Kirsch (1980), published in SoftSide Magazine.

## Original Game
- **Platform:** TRS-80 / S-80 (16K machines)
- **Author:** Peter Kirsch, 1980
- **Rooms:** 65 rooms across 9 floors (source numbering 1-65)
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

## Floor Status (2026-11-04)

All 9 floors are playable and pass bidirectional navigation tests, but only floors 9
and 8 have been audited against the scanned source. Floors 7-1 still carry stale room
numbering and are being rewritten floor-by-floor (floor 6 is next).

| Floor | Theme | Rooms | Status |
|-------|-------|-------|--------|
| 9 | Roof — elevator & midnight blackout | 11 | ✅ Audited vs source 2026-11-03 |
| 8 | Aquarium — piranhas & balloon | 5 | ✅ Audited vs source 2026-11-03 |
| 7 | Bank Vault — combination locks | 10 | ⚠️ Stale room IDs — rewrite next |
| 6 | Office — balloon/vending puzzles | 9 | ⚠️ Stale room IDs — rewrite next |
| 5 | Weird (Mary Poppins) — knitting, umbrellas | 9 | ⚠️ Stale room IDs |
| 4 | Jekyll/Hyde Lab — transformation | 8 | ⚠️ Stale room IDs |
| 3 | Greenhouse — plants and traps | 5 | ⚠️ Stale room IDs |
| 2 | Quicksand — piano puzzle | 5 | ⚠️ Stale room IDs |
| 1 | Ground — escape! | 4 | ⚠️ Stale room IDs |

**Source: 65 rooms** (global room numbers 1-65). This port currently ships 66 room entries,
because floors 7-1 are still on stale room numbering; floors 9 and 8 match the source
exactly (rooms 1-11 and 13-17). The count lands on 65 as floors 7-1 are rewritten.

## Project Structure

```
kidnapped-text-adventure/
├── kidnapped.py              # Main launcher (engine + REPL) — supports --floor N
├── KIDNAPPED_SOURCE_CORRECTED.txt  # Source-corrected DATA rows (2026-11-04)
├── OCR_CORRECTIONS_2026-11-04.md  # OCR-vs-pixels correction log
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
