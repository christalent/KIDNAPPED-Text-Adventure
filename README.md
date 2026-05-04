# KIDNAPPED! — Text Adventure

A Python port of the classic **KIDNAPPED!** text adventure game by Peter Kirsch (1980), published in SoftSide Magazine.

## Original Game
- **Platform:** TRS-80 / S-80 (16K machines)
- **Author:** Peter Kirsch, 1980
- **Locations:** 65 rooms across 9 floors
- **Objective:** Escape a 9-story building as a kidnapping victim, floor by floor

## This Port
- **Language:** Python 3
- **Author:** Lemmy (AI assistant)
- **Based on:** BASIC source transcription + OCR from original PDF

## How to Play
```bash
python3 kidnapped.py
```

Use 1-2 word commands like `GET KEY`, `OPEN DOOR`, `N`, `S`, `E`, `W`, `U`, `D` to navigate and interact.

## Floor Overview
| Floor | Theme |
|-------|-------|
| 9 | Roof — starting floor, elevator puzzles |
| 8 | Aquarium — piranha pool |
| 7 | Bank Vault — combination locks |
| 6 | Office — balloon/vending puzzles |
| 5 | Weird (Mary Poppins) — knitting, umbrellas |
| 4 | Jekyll/Hyde Lab — transformation, diving board |
| 3 | Greenhouse — plants and traps |
| 2 | Quicksand — piano puzzle |
| 1 | Ground — escape! |

## Files
- `kidnapped.py` — Python game (play this)
- `KIDNAPPED.BAS` — Original BASIC source
- `kidnapped_basic_ocr.txt` — OCR text from original PDF

## License
Original game © Peter Kirsch, 1980. This port is for personal/historical preservation purposes.
