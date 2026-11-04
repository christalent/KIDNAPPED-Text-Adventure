# KIDNAPPED! — Archive: attempt-2026-06-04

This folder contains old/broken/superseded files from the KIDNAPPED! text adventure rebuild project, snapshotted on **2026-06-04**.

## Project State at Snapshot (2026-06-04)

- **All 9 floors working** — every floor module passes the bidirectional navigation test
- **Total rooms: 72** (16+6+10+9+9+8+5+5+4)
- **Main launcher:** `kidnapped.py` in repo root, supports `python3 kidnapped.py --floor N`
- **Floor status:**
  | Floor | Theme | Status |
  |-------|-------|--------|
  | 9 | Roof | ✅ Working (16 rooms, midnight blackout puzzle) |
  | 8 | Aquarium | ✅ Working (6 rooms, piranha/balloon) |
  | 7 | Bank Vault | ✅ Working (10 rooms, vault puzzle) |
  | 6 | Office | ✅ Working (9 rooms, balloon/gun) |
  | 5 | Mary Poppins | ✅ Working (9 rooms, knitting/umbrella) |
  | 4 | Jekyll/Hyde Lab | ✅ Working (8 rooms) |
  | 3 | Greenhouse | ✅ Working (5 rooms) |
  | 2 | Quicksand | ✅ Working (5 rooms) |
  | 1 | Ground — Escape | ✅ Working (4 rooms) |

- **Test suite:** `python3 tests/test_navigation.py` — **9 passed, 0 failed**
- **Key fix history:** this was the 4th attempt from scratch; the lesson was always to use the clean PDF source and verify bidirectional exits.

## What's in This Archive

| File / Folder | Why Archived |
|---------------|--------------|
| `v1_legacy/` | Original BASIC-to-Python port (single monolithic `kidnapped.py`, no `--floor` flag, no modular floors). Superseded by the current multi-floor architecture. **Notable: v1 did NOT have a `--floor` flag — the per-floor launch was added when the project was rebuilt.** |
| `play_floor9.py` | Old interactive test runner for Floor 9 (root-level). Functionality now lives in the main `kidnapped.py` launcher via `--floor 9`. |
| `test_floor8_fixes.py` | Root-level test for floor_8 fixes. Functionality was folded into `tests/test_floor7_floor6.py` and the main `tests/test_navigation.py` suite. |
| `test_floor9_exhaustive.py` | Root-level exhaustive Floor 9 test. Functionality was folded into `tests/test_floor9_fixes.py` and the main `tests/test_navigation.py` suite. |
| `kidnapped_basic_ocr.txt` | A second OCR pass over the original PDF. Superseded by the cleaner `KIDNAPPED_OCR.txt` (kept in the main repo) and the `PARSED_BASIC_SOURCE.txt` data file. |

## What Was Working vs Broken at Snapshot

**Working (kept in main repo):**
- All 9 floor modules
- `kidnapped.py` launcher with `--floor` flag
- `tests/test_navigation.py` (bidirectional exit checker — all 9 floors pass)
- `tests/test_floor5.py`, `tests/test_floor7_floor6.py`, `tests/test_floor9_fixes.py` (per-floor regression tests)

**Not Broken — Just Clutter (moved here):**
- The v1 legacy port
- Redundant OCR text
- Old ad-hoc test runners in the root directory

**Still Pending (not yet done as of 2026-06-04):**
- Full end-to-end playthrough to confirm all 9 floors can be cleared in sequence
- Polishing: room descriptions are functional but not always evocative
- Doc updates: this archive snapshot is part of that cleanup

## How to Recover

Everything here is preserved as-is. If you need to look at the old v1 port:
- `v1_legacy/kidnapped.py` is a single 105 KB file containing the whole game
- The other test files are reference implementations of specific Floor 8 / Floor 9 bug fixes

## See Also

- Main repo `README.md` — current state and how to run
- Main repo `SPEC.md` — architecture and design notes
- Main repo `PARSED_BASIC_SOURCE.txt` — clean parsed data used for the rebuild
- Main repo `GAME_ANALYSIS.txt` — analysis from the RetroGamesTroove review
