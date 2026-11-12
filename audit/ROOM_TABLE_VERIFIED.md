# Room table - pixel-verified transcription

**Source:** `KIDNAPPED_Original.pdf` (SoftSide Vol 3 No 03, Dec 1980), pages 1-2.
**Method:** the PDF text layer (`pdftotext -bbox-layout`) was used only to locate lines;
every digit below was read from a raster crop (`pdftoppm`, 500-900 dpi) and cross-checked
against the exit-graph reciprocity constraint.

The listing dispatches with `ON A GOTO 11,12,...,75`, so **global room = printed line - 10**.
The room table is listing lines 11-75 = **global rooms 1-65**. There are no rooms above 65.

## Listing lines 33-75 = rooms 23-65 (newly verified)

| room | line | description | exits | source |
|---|---|---|---|---|
| 23 | 33 | IN A SMALL STORAGE ROOM. | W=22 | floor7 audit (pixel) |
| 24 | 34 | J$ | W=18 | floor7 audit (pixel) |
| 25 | 35 | IN A NARROW STAIRWAY. | W=24 | floor7 audit (pixel) |
| 26 | 36 | (repeat) | E=29 N=27 S=30 W=31 | pixel+ocr+graph |
| 27 | 37 | (repeat) | N=28 S=26 | pixel+ocr+graph |
| 28 | 38 | IN A CLOSET. | S=27 | pixel+ocr+graph |
| 29 | 39 | IN A GAME ROOM. | W=26 | pixel+ocr+graph |
| 30 | 40 | (repeat) | N=26 | pixel+ocr+graph |
| 31 | 41 | (repeat) | E=26 N=32 W=33 | pixel+ocr+graph |
| 32 | 42 | IN A STORE ROOM. | S=31 | pixel+ocr+graph |
| 33 | 43 | (repeat) | E=31 | pixel+ocr+graph |
| 34 | 44 | ON A LARGE LEDGE BY WINDOW. | W=36 | pixel x2+ocr+graph |
| 35 | 45 | IN THE VAULT. | W=36 | pixel x2+ocr |
| 36 | 46 | ON A LARGE LEDGE BY WINDOW. | E=34 | pixel x3+ocr+graph |
| 37 | 47 | (repeat) | S=41 | pixel x2+graph |
| 38 | 48 | (repeat) | E=43 N=39 S=40 | pixel+ocr+graph |
| 39 | 49 | (repeat) | S=38 | pixel+ocr+graph |
| 40 | 50 | (repeat) | N=38 | pixel+ocr+graph |
| 41 | 51 | (repeat) | N=37 S=42 W=43 | pixel+ocr+graph |
| 42 | 52 | (repeat) | N=41 | pixel+ocr+graph |
| 43 | 53 | (repeat) | E=41 W=38 | pixel+ocr+graph |
| 44 | 54 | IN A STAIRCASE. | - | pixel+ocr |
| 45 | 55 | (repeat) | E=48 N=46 S=47 | pixel+ocr+graph |
| 46 | 56 | (repeat) | S=45 | pixel+ocr+graph |
| 47 | 57 | IN A LIBRARY. | N=45 | pixel+ocr+graph |
| 48 | 58 | IN THE SWIM ROOM. | W=45 | pixel+ocr+graph |
| 49 | 59 | IN THE SWIM ROOM. | E=51 N=50 | pixel+ocr+graph |
| 50 | 60 | IN A LAUNDRY ROOM. | S=49 | pixel+ocr+graph |
| 51 | 61 | IN A DINING ROOM. | W=49 | pixel+ocr+graph |
| 52 | 62 | (repeat) | E=54 N=53 | pixel+ocr+graph |
| 53 | 63 | IN A RESTROOM. | S=52 | pixel+ocr+graph |
| 54 | 64 | (repeat) | E=55 W=52 | pixel+ocr+graph |
| 55 | 65 | (repeat) | N=56 W=54 | pixel+ocr+graph |
| 56 | 66 | IN A LABORATORY. | S=55 | pixel+ocr+graph |
| 57 | 67 | IN A CHILD'S PLAYROOM. | N=55 | pixel+ocr+graph |
| 58 | 68 | (repeat) | W=59 | pixel+ocr+graph |
| 59 | 69 | IN A LOUNGE. | E=58 | pixel+ocr+graph |
| 60 | 70 | IN A CRAWLWAY. | E=61 | pixel+ocr+graph |
| 61 | 71 | IN A CRAWLWAY. | W=60 | pixel+ocr+graph |
| 62 | 72 | - | - | pixel+ocr+graph |
| 63 | 73 | IN A LOUNGE. | E=64 | pixel+ocr+graph |
| 64 | 74 | (repeat) | W=63 | pixel+ocr+graph |
| 65 | 75 | IN THE ENTRANCE HALL. | - | pixel+ocr+graph |

### Rooms 18-25 (from the floor 7 audit, also pixel-derived)

| room | line | description | exits |
|---|---|---|---|
| 18 | 28 | J$ | E=24 N=19 S=21 W=20 |
| 19 | 29 | N$ | S=18 |
| 20 | 30 | IN A TOOL CRIB. | E=18 |
| 21 | 31 | J$ | E=22 N=18 |
| 22 | 32 | N$ | E=23 W=21 |
| 23 | 33 | IN A SMALL STORAGE ROOM. | W=22 |
| 24 | 34 | J$ | W=18 |
| 25 | 35 | IN A NARROW STAIRWAY. | W=24 |

## Individual notes

- **Line 72 (room 62)** is not a room description: it is `GOTO54`, an alias that sends the
  player to line 54 = room 44, `IN A STAIRCASE.` Room 62 has no exits of its own.
- `J$` and `N$` are the listing's two 'repeat a description' variables; such a line still
  carries its own exits.
- The text layer's systematic damage: digit `4` read as `1`, `8` as `S`, `0` as `O`, and
  `W`/`N`/`M` confused. Every digit above came from the raster.

## Exit-graph validation

Reciprocal edges: **64**. Non-reciprocal: **3**.

| room | exit | to | note |
|---|---|---|---|
| 25 | W | 24 | one-way: room 24's locked door is passed with GO DOOR, never walked back |
| 35 | W | 36 | vertical link (the vault), not a horizontal room pair |
| 57 | N | 55 | vertical link, not a horizontal room pair |

The reciprocity constraint is what fixes the lines the PDF text layer loses. The
text layer has no bbox entry for line 47, and the assignment of `47 PRINTN$:S=41` versus
`48 PRINTJ$:E=43:N=39:S=40` is forced: as assigned, room 37<->41, 38<->39, 38<->40,
38<->43 and 41<->42 are all reciprocal. Swapped, four of those break and none are fixed.

## Crops used

- `/home/chris/projects/kidnap-decoder/pix/p1_right_rooms36_46-1.png`
- `/home/chris/projects/kidnap-decoder/pix/f1_5_rooms47_63-1.png`
- `/home/chris/projects/kidnap-decoder/pix/f1_5_rooms64_75-2.png`
- `/home/chris/projects/kidnap-decoder/pix/tie_lines45_52-1.png`
- `/home/chris/projects/kidnap-decoder/pix/room_33_34-1.png`
- `/home/chris/projects/kidnap-decoder/pix/room_74_75-2.png`

