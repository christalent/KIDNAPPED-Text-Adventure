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


## Floors 1-5: rewritten and verified (2026-11-11)

`audit/FLOORS_1_5_GROUND_TRUTH.md` carries the pixel-verified room-to-floor
mapping for floors 1-5 (rooms 37-65), the per-floor item placement, and a
command-by-command replay of both published walkthroughs.

`floors/floor_1.py` .. `floors/floor_5.py` have been rewritten against that
file (commit 7a525d6): the old room set (66-75, ALLIGATOR, INDIAN ROPE) is
gone. Each floor declares `VERB_LINK_PAIRS` for the room pairs that a verb
action links rather than a compass exit, and `_here()` sees fixed scenery as
well as takeable items.

`tests/authoritative_tables.py` loads floors 1-5 straight out of
`audit/floors_1_5_verified.json`, so all 9 floors are source-validated
against an audit table. `tests/run_all.py`: 14/14 test files pass.

Still open on floors 1-5: the listing's handler code (pages 2-4) has not been
transcribed, so the puzzle state machines are reconstructed from the two
published walkthroughs and marked INFERRED in each module docstring.


## Full-game escape test (2026-11-11)

`tests/test_full_game_escape.py` replays BOTH published solutions - Francis
(`archive/solutions/sol_atari.txt`) and Gunness (`archive/solutions/
sol_gunness.txt`) - command for command, floor 9 down to the street.

It drives `kidnapped.GameRunner`, a REPL-free wrapper around the real
dispatcher that `main()` also uses, so the test and the game share one
transition path. Every room is checked against the pixel-verified tables in
`tests/authoritative_tables.py`, every floor transition against that floor's
audited arrival room.

The test found three real defects, all fixed:
- floor 9 did not accept `LIGHT FLASHLIGHT` (both walkthroughs use it)
- floor 1 matched a carried floor-8 `ROPE` before the room's own
  `LONG ROPE`, so `GET ROPE` grabbed the wrong rope
- the REPL and a test had no shared entry point

`tests/run_all.py`: 15/15 test files pass.
