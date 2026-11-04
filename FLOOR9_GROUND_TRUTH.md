# FLOOR 9 GROUND TRUTH — from the scanned source, not from the OCR layer

STATUS: pixel-verified 2026-11-03 by direct reads of 300-500dpi crops of
`KIDNAPPED_Original.pdf`. NOT yet cross-checked against the M3.1-Flash delegation.

## Why this document exists

The PDF's embedded text layer (pdftotext) is OCR-damaged in a SPECIFIC, systematic
way: the digit **4 is rendered as 1**. Every hand-parsed map we inherited was built
from that damaged layer, so all of them carry the corruption.

Proof (OCR text layer vs. actual pixels):

| listing line | OCR text layer | actual pixels |
|---|---|---|
| 23 | `W=11` | `W=14` |
| 25 | `E=11` | `E=14` |
| 28 | `E=21` | `E=24` |

Worse: `SPEC.md`'s "Correct Floor 9 Room Layout" is NOT a correction. Someone
hand-patched the corrupted `11`s into reciprocal-looking pairs (giving room 13 an
invented `E=14`, room 15 an invented `W=11`) so the bad numbers would LOOK
symmetric. That is where the mapping work went in circles for months.

## Room-number to line-number mapping

Listing line 10 is:

    IF A=66 THEN 600 ELSE IF DT=1 THEN 320 ELSE ON A GOTO 11,12,13,...,75

`A` is the player's room number; `ON A GOTO` dispatches to the room's description
line. The destinations run 11..75 for A=1..65, so:

    **listing line = room number + 10**

The direction values (N=/E=/S=/W=/U=/D=) are ROOM NUMBERS, not line numbers.
Verified independently: 17 of 18 edges close perfectly as a symmetric pair set
under this mapping (1<->4, 1<->2, 1<->8, 1<->7, 2<->3, 4<->5, 4<->6, 8<->9,
8<->10, 13<->14, 13<->16, 14<->15, 16<->17, 18<->19, 18<->20, 18<->21).

Floor membership is NOT encoded in the description lines. It comes from room-number
ranges plus the special-case code at listing line ~1000 (the elevator).

## Floor 9 room table — PIXEL-VERIFIED

Rooms 1-20 (listing lines 11-30). Description text is often a variable (J$ / N$)
whose literal value is set elsewhere.

| room | line | description | N | E | S | W | U | D |
|---|---|---|---|---|---|---|---|---|
| 1 | 11 | `J$` | 2 | 8 | 7 | 4 | | |
| 2 | 12 | `N$` | 3 | | 1 | | | |
| 3 | 13 | "IN A CLOSET." | | | 2 | | | |
| 4 | 14 | `J$` | 5 | 1 | 6 | | | |
| 5 | 15 | `N$` | | | 4 | | | |
| 6 | 16 | "IN A RESTROOM." | 4 | | | | | |
| 7 | 17 | `N$` | 1 | | | | | |
| 8 | 18 | `J$` | 9 | | 10 | 1 | | |
| 9 | 19 | "IN AN ELEVATOR." | | | 8 | | | |
| 10 | 20 | "IN A MAINTENANCE ROOM." | 8 | | | | | |
| 11 | 21 | "IN A CRAWLSPACE ON TOP OF THE ELEVATOR." | | | | | | 9 |
| 12 | 22 | "ON A VERY NARROW LEDGE." | — | — | — | — | — | — |
| 13 | 23 | `J$` | | 14 | 16 | | | |
| 14 | 24 | "IN A VISITOR'S LOUNGE." | | 13 | | 15 | | |
| 15 | 25 | "IN A CLOSET." | | 14 | | | | |
| 16 | 26 | `N$` | 13 | 17 | | | | |
| 17 | 27 | `N$` | | | | 16 | | |
| 18 | 28 | `J$` | 19 | 24 | 21 | 20 | | |
| 19 | 29 | `N$` | | | 18 | | | |
| 20 | 30 | "IN A TOOL CRIB." | | 18 | | | | |
| 21 | 31 | `J$` (partial read) | 18 | 22 | | | | |

## Floor 9 items — PIXEL-VERIFIED (listing lines 2000-2010)

Sign convention CONFIRMED by the magazine's own marginal note on page 4:
*"A negative number indicates an item cannot be [taken]"*. So number = room
location, sign = takeable (positive) / fixed scenery (negative).

    PAPER NOTE, 2              ROOM 2   takeable
    DESK, -2                   ROOM 2   fixed
    CHAIR, 2                   ROOM 2   takeable
    LONG BROOM, 3              ROOM 3   takeable
    TV SET, -5                 ROOM 5   fixed
    CLOCK, -5                  ROOM 5   fixed
    GRAFFITI ON WALL, -6       ROOM 6   fixed
    OPEN WINDOW, -7            ROOM 7   fixed
    TRAP DOOR IN CEILING, -9   ROOM 9   fixed
    DOWN BUTTON, -9            ROOM 9   fixed
    CABINET, -10               ROOM 10  fixed
    ENDS OF 2 'LIVE' WIRES, -11 ROOM 11 fixed
    AQUARIUM, -14              ROOM 14  fixed
    ROPE, 15                   ROOM 15  takeable
    SLEEPING PILL, 16          ROOM 16  takeable
    OPEN WINDOW, -17           ROOM 17  fixed
    DESK, -17                  ROOM 17  fixed
    KEY MAKING MACHINE, -19    ROOM 19  fixed
    SUPER GLUE, 20             ROOM 20  takeable
    WOODEN STAIR STEP, 20      ROOM 20  takeable

Also confirmed from the listing's own handlers (not DATA): room 7's window has a
"SMALL LEDGE" outside with a "SINGLE KEY ON A KEY CHAIN" on it.

## OPEN QUESTIONS (must not be guessed)

1. **Room 12 "ON A VERY NARROW LEDGE." lists NO exits at all.** Either a one-way
   death ledge, or an exit set by a handler rather than the description line. The
   port's invented room-3 `U=4` / room-4 `D=3` may have been an attempt to paper
   over exactly this asymmetry.
2. **Room 18 has E=24 and S=21**, which cross the suspected floor-9 boundary
   (rooms 1-20). Either floor 9 is 1-21, or those two are handled by the
   elevator special-case code near listing line 1000, or one of those digits is
   still misread. Floor-9 membership needs resolving before the map is final.
3. **Item DATA continues past line 2030.** The listing shows 58 item slots
   (`A$(58)`); only 2000-2030 are captured above. FLASHLIGHT and TAPE (both
   claimed for floor 9 by `GAME_ANALYSIS.txt` and by the port) are NOT in the
   captured lines, so they live in 2040+.
4. The literal text behind `J$` and `N$` room descriptions is set elsewhere and
   has not been recovered yet.

## What is known-wrong in the port (`floors/floor_9.py`)

- rooms 11-15 form an invented 4-cycle (11->13->14->15->11); the source says
  13<->14 and 14<->15.
- invented vertical links (room 3 `U=4`, room 4 `D=3`) are not in the source.
- rooms 18-20 dropped entirely from the port.
- room 7 and room 10 have no items, but the source puts a window+ledge key at 7
  and a cabinet at 10.
- room 15 = ROPE vs source ROPE,15 (agrees); room 16 = SMALL KEY but source
  says SLEEPING PILL,16.
- README's "72 rooms vs the original's 65" is 7 INVENTED rooms.
- `tests/test_all_floors_map.py` compares the port against SOURCE_PAIRS pulled
  from the same suspect table -> circular. Floors 1-5 get structural checks only.
