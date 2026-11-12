# kidnapped-text-adventure

**Purpose:** Python text adventure game (kidnap-themed).
**Status:** dormant
**Last touched:** 2026-07-09

## Structure
- Python source for a terminal text adventure
- tests/test_navigation.py - basic navigation tests
- README.md - how to play

## Notes
- Hobby project, structural inventory only.


## Floors 1-5: mapping verified (2026-11-08)

`audit/FLOORS_1_5_GROUND_TRUTH.md` now carries the pixel-verified room-to-floor
mapping for floors 1-5 (rooms 37-65), the per-floor item placement, and a
command-by-command replay of both published walkthroughs. The room map in
`floors/floor_1.py` .. `floors/floor_5.py` is still the old, wrong one (rooms
66-75, ALLIGATOR, INDIAN ROPE) and is being rewritten against this file.
