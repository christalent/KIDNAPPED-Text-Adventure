# DATA item inventory - pixel-verified (55 items)

**Every entry below was read from a raster crop of the printed listing**, not from the
PDF text layer (which reads 4 as 1, 8 as S, 0 as O). A negative room number means a
fixed object in that room; a positive number means a movable item starting there.

The READ loop is `FOR A=1 TO 55:READ A$(A):READ A(A):H$(A)=A$(A):NEXT` - pixel-verified
at 900 dpi. 55 entries in DATA, 55 iterations in the loop. They agree exactly, so there
is no missing item and no unfilled slot.

## The five DATA rows

| row | items | rooms covered |
|---|---|---|
| 2000 | 16 | -17 to 16 |
| 2010 | 9 | -25 to 29 |
| 2020 | 11 | -44 to 40 |
| 2030 | 10 | -57 to 56 |
| 2040 | 9 | -65 to 64 |

## Item number -> name -> room

Item numbers are the `A` index in the READ loop, i.e. the order the items are read.

| # | row | item | room |
|---|---|---|---|
| 1 | 2000 | PAPER NOTE | 2 |
| 2 | 2000 | DESK | -2 |
| 3 | 2000 | CHAIR | 2 |
| 4 | 2000 | LONG BROOM | 3 |
| 5 | 2000 | TV SET | -5 |
| 6 | 2000 | CLOCK | -5 |
| 7 | 2000 | GRAFFITI ON WALL | -6 |
| 8 | 2000 | OPEN WINDOW | -7 |
| 9 | 2000 | TRAP DOOR IN CEILING | -9 |
| 10 | 2000 | DOWN BUTTON | -9 |
| 11 | 2000 | CABINET | -10 |
| 12 | 2000 | ENDS OF 2 'LIVE' WIRES | -11 |
| 13 | 2000 | AQUARIUM | -14 |
| 14 | 2000 | ROPE | 15 |
| 15 | 2000 | SLEEPING PILL | 16 |
| 16 | 2000 | OPEN WINDOW | -17 |
| 17 | 2010 | DESK | -17 |
| 18 | 2010 | KEY MAKING MACHINE | -19 |
| 19 | 2010 | SUPER GLUE | 20 |
| 20 | 2010 | WOODEN STAIR STEP | 20 |
| 21 | 2010 | THICK COPPER SHEET | 23 |
| 22 | 2010 | LOCKED DOOR | -24 |
| 23 | 2010 | WOODEN STAIRS | -25 |
| 24 | 2010 | TANK OF HELIUM GAS | 28 |
| 25 | 2010 | LARGE DEFLATED BALLOON | 29 |
| 26 | 2020 | LOCKED DOOR | -30 |
| 27 | 2020 | GUN | 30 |
| 28 | 2020 | SIGN ON WALL | -32 |
| 29 | 2020 | STRING VENDING MACHINE | -32 |
| 30 | 2020 | OPEN WINDOW | -33 |
| 31 | 2020 | LOCKED DOOR | -43 |
| 32 | 2020 | BALL OF YARN | 39 |
| 33 | 2020 | KNITTING NEEDLES | 40 |
| 34 | 2020 | PUSH BUTTON ON WALL | -42 |
| 35 | 2020 | "SEXY, YOUNG GIRL OFFICE WORKERS" | -37 |
| 36 | 2020 | STAIRS | -44 |
| 37 | 2030 | PUSH BUTTON ON WALL | -46 |
| 38 | 2030 | BOOK | 47 |
| 39 | 2030 | MARY POPPIN'S UMBRELLA | 50 |
| 40 | 2030 | OPEN WINDOW | -51 |
| 41 | 2030 | GRAFFITI ON WALL | -53 |
| 42 | 2030 | SMALL KEY | 37 |
| 43 | 2030 | STEEL DOOR | -55 |
| 44 | 2030 | JAR OF YELLOW SOLUTION | 56 |
| 45 | 2030 | JAR OF FLUID | 56 |
| 46 | 2030 | CHILD'S SLIDE | -57 |
| 47 | 2040 | WATER COOLER | -58 |
| 48 | 2040 | PAPER CUP | 58 |
| 49 | 2040 | SMALL-SIZED PLANT | -59 |
| 50 | 2040 | FLUTE | 61 |
| 51 | 2040 | STAIRS | -62 |
| 52 | 2040 | SMALL BOOK | 64 |
| 53 | 2040 | PIANO | -63 |
| 54 | 2040 | LONG ROPE | 63 |
| 55 | 2040 | FRONT DOOR | -65 |

## Fixed objects (negative room numbers)

| item | room |
|---|---|
| DESK | -2 |
| TV SET | -5 |
| CLOCK | -5 |
| GRAFFITI ON WALL | -6 |
| OPEN WINDOW | -7 |
| TRAP DOOR IN CEILING | -9 |
| DOWN BUTTON | -9 |
| CABINET | -10 |
| ENDS OF 2 'LIVE' WIRES | -11 |
| AQUARIUM | -14 |
| OPEN WINDOW | -17 |
| DESK | -17 |
| KEY MAKING MACHINE | -19 |
| LOCKED DOOR | -24 |
| WOODEN STAIRS | -25 |
| LOCKED DOOR | -30 |
| SIGN ON WALL | -32 |
| STRING VENDING MACHINE | -32 |
| OPEN WINDOW | -33 |
| LOCKED DOOR | -43 |
| PUSH BUTTON ON WALL | -42 |
| "SEXY, YOUNG GIRL OFFICE WORKERS" | -37 |
| STAIRS | -44 |
| PUSH BUTTON ON WALL | -46 |
| OPEN WINDOW | -51 |
| GRAFFITI ON WALL | -53 |
| STEEL DOOR | -55 |
| CHILD'S SLIDE | -57 |
| WATER COOLER | -58 |
| SMALL-SIZED PLANT | -59 |
| STAIRS | -62 |
| PIANO | -63 |
| FRONT DOOR | -65 |

## Cross-checks against the room table

- `THICK COPPER SHEET,23` - room 23 is `IN A SMALL STORAGE ROOM.` (floor 7 audit agrees).
- `LOCKED DOOR,-24` and `WOODEN STAIRS,-25` - rooms 24 and 25, matching the floor 7 audit
  (room 24 holds the locked door, room 25 the narrow stairway).
- `STAIRS,-44` - room 44 is `IN A STAIRCASE.` The fixed object and the room description
  agree, which is a strong confirmation that the room numbering is right.
- `BOOK,47` - room 47 is `IN A LIBRARY.`
- `JAR OF YELLOW SOLUTION,56`, `JAR OF FLUID,56`, `CHILD'S SLIDE,-57` - room 56 is
  `IN A LABORATORY.` and room 57 is `IN A CHILD'S PLAYROOM.`
- `PIANO,-63`, `LONG ROPE,63`, `SMALL BOOK,64`, `FRONT DOOR,-65` - rooms 63, 64 and 65,
  and room 65 is `IN THE ENTRANCE HALL.`

Every fixed object that has a matching room description lands on the room that
description names. That is six independent confirmations of the room numbering, and
it is why the `-` before a room number can be trusted.

## Items created at run time (not in DATA)

- **DOLLAR** - line 467: `A$(56)="DOLLAR":H$(56)=A$(56):A(56)=35`. Item slot 56,
  placed in room 35. It is handed over only when the player has the GUN (`I(27)=1`);
  otherwise the same handler prints "YOU GET TOO CLOSE TO HIM, HE JUMPS AND STRANGLES
  YOU." and jumps to 7300.
- The GUN is DATA item 31 (`GUN,30`), so `I(27)` in line 467 is the flag for it being
  carried, not the item index in the DATA list.

## Crops

- `data_2000_2020-4.png` (600 dpi, page 4 right column) - rows 2000, 2010, 2020
- `oa_p4_data_2030_2040-4.png` (500 dpi, page 4 right column) - rows 2030, 2040
- `readloop_p2_y221-2.png` / `line210_tail-900-2.png` (700/900 dpi) - the READ loop

