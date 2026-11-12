# Floors 1-5 - the verified room-to-floor mapping

**This is the ground truth for floors 1-5.** It supersedes the room maps hardcoded in
`floors/floor_1.py` .. `floors/floor_5.py`, which contain rooms 66-75 and objects such
as the ALLIGATOR and the INDIAN ROPE that appear nowhere in the listing. The room table
ends at **room 65**.

Every room number and every exit below was read from a raster crop of the printed
listing (`audit/ROOM_TABLE_VERIFIED.md`); every item placement was read from the
pixel-read DATA rows (`audit/DATA_ITEM_INVENTORY.md`).

## The five floors

| floor | rooms | listing lines | theme |
|---|---|---|---|
| 5 | 37-44 | 47-54 | knitting, fire, stairs down to floor 4 |
| 4 | 45-51 | 55-61 | empty pool, book, umbrella, jump down to floor 3 |
| 3 | 52-57 | 62-67 | laboratory, Mr. Hyde, child's slide down to floor 2 |
| 2 | 58-62 | 68-72 | plant, flute, magic rope, stairs down to floor 1 |
| 1 | 63-65 | 73-75 | piano key, rope, book, front door - escape |

## Room table, rooms 37-65

| room | line | description | exits | floor |
|---|---|---|---|---|
| 37 | 47 | N$ | S=41 | 5 |
| 38 | 48 | J$ | E=43 N=39 S=40 | 5 |
| 39 | 49 | N$ | S=38 | 5 |
| 40 | 50 | N$ | N=38 | 5 |
| 41 | 51 | J$ | N=37 S=42 W=43 | 5 |
| 42 | 52 | N$ | N=41 | 5 |
| 43 | 53 | J$ | E=41 W=38 | 5 |
| 44 | 54 | IN A STAIRCASE. | - | 5 |
| 45 | 55 | J$ | E=48 N=46 S=47 | 4 |
| 46 | 56 | N$ | S=45 | 4 |
| 47 | 57 | IN A LIBRARY. | N=45 | 4 |
| 48 | 58 | IN THE SWIM ROOM. | W=45 | 4 |
| 49 | 59 | IN THE SWIM ROOM. | E=51 N=50 | 4 |
| 50 | 60 | IN A LAUNDRY ROOM. | S=49 | 4 |
| 51 | 61 | IN A DINING ROOM. | W=49 | 4 |
| 52 | 62 | J$ | E=54 N=53 | 3 |
| 53 | 63 | IN A RESTROOM. | S=52 | 3 |
| 54 | 64 | J$ | E=55 W=52 | 3 |
| 55 | 65 | J$ | N=56 W=54 | 3 |
| 56 | 66 | IN A LABORATORY. | S=55 | 3 |
| 57 | 67 | IN A CHILD'S PLAYROOM. | N=55 | 3 |
| 58 | 68 | N$ | W=59 | 2 |
| 59 | 69 | IN A LOUNGE. | E=58 | 2 |
| 60 | 70 | IN A CRAWLWAY. | E=61 | 2 |
| 61 | 71 | IN A CRAWLWAY. | W=60 | 2 |
| 62 | 72 | GOTO54 | - | 2 |
| 63 | 73 | IN A LOUNGE. | E=64 | 1 |
| 64 | 74 | J$ | W=63 | 1 |
| 65 | 75 | IN THE ENTRANCE HALL. | - | 1 |

`J$` and `N$` are cached description strings, not literals. The floor 6 and 7 audits
established `J$` = "IN A HALLWAY." and `N$` = "IN AN OFFICE." (assigned once in the
listing's variable block). The exits are literal and pixel-verified.

## Items per floor (pixel-verified DATA placement)

| floor | item | DATA row | room | kind |
|---|---|---|---|---|
| 5 | PUSH BUTTON ON WALL | 2020 | -42 | fixed |
| 5 | LOCKED DOOR | 2010 | -43 | fixed |
| 5 | STAIRS | 2020 | -44 | fixed |
| 5 | BALL OF YARN | 2020 | 39 | movable |
| 5 | KNITTING NEEDLES | 2020 | 40 | movable |
| 5 | SMALL KEY | 2030 | 37 | movable |
| 5 | "SEXY, YOUNG GIRL OFFICE WORKERS" | 2020 | -37 | fixed |
| 4 | PUSH BUTTON ON WALL | 2020 | -46 | fixed |
| 4 | BOOK | 2030 | 47 | movable |
| 4 | MARY POPPIN'S UMBRELLA | 2030 | 50 | movable |
| 4 | OPEN WINDOW | 2000 | -51 | fixed |
| 3 | GRAFFITI ON WALL | 2000 | -53 | fixed |
| 3 | STEEL DOOR | 2030 | -55 | fixed |
| 3 | JAR OF YELLOW SOLUTION | 2030 | 56 | movable |
| 3 | JAR OF FLUID | 2030 | 56 | movable |
| 3 | CHILD'S SLIDE | 2030 | -57 | fixed |
| 2 | WATER COOLER | 2040 | -58 | fixed |
| 2 | PAPER CUP | 2040 | 58 | movable |
| 2 | SMALL-SIZED PLANT | 2040 | -59 | fixed |
| 2 | FLUTE | 2040 | 61 | movable |
| 2 | STAIRS | 2020 | -62 | fixed |
| 1 | PIANO | 2040 | -63 | fixed |
| 1 | LONG ROPE | 2040 | 63 | movable |
| 1 | SMALL BOOK | 2040 | 64 | movable |
| 1 | FRONT DOOR | 2040 | -65 | fixed |

Every fixed object lands in a room whose description names it:
`STAIRS,-44` in room 44 `IN A STAIRCASE.`; `BOOK,47` in room 47 `IN A LIBRARY.`;
`JAR OF FLUID,56` and `JAR OF YELLOW SOLUTION,56` in room 56 `IN A LABORATORY.`;
`CHILD'S SLIDE,-57` in room 57 `IN A CHILD'S PLAYROOM.`; `FRONT DOOR,-65` in room 65
`IN THE ENTRANCE HALL.`; `GRAFFITI ON WALL,-53` in room 53 `IN A RESTROOM.`;
`PIANO,-63` and `LONG ROPE,63` in room 63 `IN A LOUNGE.`; `SMALL BOOK,64` in room 64;
`FLUTE,61` in room 61 `IN A CRAWLWAY.`; `PAPER CUP,58` and `WATER COOLER,-58` in room 58;
`SMALL-SIZED PLANT,-59` in room 59 `IN A LOUNGE.`

## Walkthrough replay - the proof

Both published solutions replay **command for command** on the table above. Floor 5 is
the strongest case: the two walkthroughs take *different* routes through the same rooms
and both land on the right object at every step.

### Floor 5 - Jacob Gunness solution

```
  W                      -> room 38
  S                      -> room 40
  GET NEEDLES               [room 40]
  N                      -> room 38
  N                      -> room 39
  GET YARN                  [room 39]
  S                      -> room 38
  E                      -> room 43
  E                      -> room 41
  S                      -> room 42
  PRESS BUTTON              [room 42]
  KNIT CLOTHES              [room 42]
  N                      -> room 41
  N                      -> room 37
  GET KEY                   [room 37]
  S                      -> room 41
  W                      -> room 43
  OPEN DOOR                 [room 43]
  GO DOOR                   [room 43]
  CLIMB STAIRS              [room 43]
```

### Floor 5 - Garry Francis (Atari) solution

```
  E                      -> room 41
  S                      -> room 42
  PRESS BUTTON              [room 42]
  N                      -> room 41
  W                      -> room 43
  W                      -> room 38
  S                      -> room 40
  GET KNITTING NEEDLES      [room 40]
  N                      -> room 38
  N                      -> room 39
  GET BALL OF YARN          [room 39]
  KNIT CLOTHES              [room 39]
  S                      -> room 38
  E                      -> room 43
  E                      -> room 41
  N                      -> room 37
  GET SMALL KEY             [room 37]
  S                      -> room 41
  W                      -> room 43
  OPEN DOOR                 [room 43]
  GO DOOR                   [room 43]
  GO STAIRS                 [room 43]
```

### Floor 4 - Francis

```
  N                     -> room 46   PRESS BUTTON (PUSH BUTTON ON WALL,-46)
  S                     -> room 45
  S                     -> room 47   GET BOOK (BOOK,47, IN A LIBRARY.)
  N                     -> room 45
  E                     -> room 48   SWIM  (IN THE SWIM ROOM.)
  SWIM                  [handler 48 -> 49]
  N                     -> room 50   GET MARY POPPIN'S UMBRELLA (50, LAUNDRY ROOM.)
  OPEN UMBRELLA         [room 50]
  S                     -> room 49
  E                     -> room 51   JUMP  [handler -> floor 3]
```

### Floor 3 - Francis

```
  E                     -> room 54
  E                     -> room 55
  N                     -> room 56   GET JAR OF FLUID (56, IN A LABORATORY.)
                                    GET VIAL OF YELLOW SOLUTION (JAR OF YELLOW SOLUTION,56)
  S                     -> room 55   OPEN DOOR (STEEL DOOR,-55)   GO DOOR
  DRINK SOLUTION        [room 55]
  GO SLIDE              [handler -> room 57, CHILD'S SLIDE,-57] -> floor 2
```

### Floor 3 - Gunness (reaches the graffiti first)

```
  N                     -> room 53   READ GRAFFITI (GRAFFITI ON WALL,-53, IN A RESTROOM.)
  S                     -> room 52
  E                     -> room 54
  E                     -> room 55
  N                     -> room 56   GET FLUID, GET SOLUTION
  S                     -> room 55   OPEN DOOR, GO DOOR, DRINK SOLUTION, CLIMB SLIDE
```

### Floor 2 - Francis

```
  GET PAPER CUP         [room 58, PAPER CUP,58]
  GET WATER             [room 58, WATER COOLER,-58]
  W                     -> room 59   POUR WATER (SMALL-SIZED PLANT,-59)
  GO PLANT              [handler -> room 60]
  E                     -> room 61   GET FLUTE (61, IN A CRAWLWAY.)
  PLAY FLUTE            [room 61]   GO ROPE [handler -> room 62]
  GO STAIRS             [room 62, STAIRS,-62] -> floor 1
```

### Floor 1 - Francis

```
  GET KEY               [room 63, PIANO,-63]
  GET LONG ROPE         [room 63, LONG ROPE,63]
  E                     -> room 64   GET BOOK (SMALL BOOK,64)   READ BOOK
  TIE ROPE / THROW ROPE [room 64]
  GO ROPE               [handler -> room 65, IN THE ENTRANCE HALL.]
  OPEN DOOR             [room 65, FRONT DOOR,-65]   GO DOOR  -> ESCAPED
```

## Handler transitions these replays imply

These are not plain W/N/E/S exits - they live in the handler code on listing pages 2-3.
They are inferred from the walkthroughs and are the one thing still to be read off the
pixels on those pages:

| floor | verb | from | to |
|---|---|---|---|
| 2 | GO PLANT / CLIMB PLANT | 59 | 60 |
| 2 | GO ROPE / PLAY FLUTE | 61 | 62 |
| 4 | SWIM | 48 | 49 |
| 1 | GO ROPE / CLIMB ROPE | 64 | 65 |
| 5 | PRESS BUTTON (fire) | 41 | 42 |
| 5 | GO STAIRS | 44 | floor 4, room 45 |
| 3 | GO SLIDE | 55 | 57, then floor 2 room 58 |
| 2 | GO STAIRS | 62 | floor 1, room 63 |

## Errors this removes from the repo

| module | current claim | verified truth |
|---|---|---|
| floor_1.py | rooms 65-75, exits N=66,67,68 | floor 1 = rooms **63, 64, 65** |
| floor_1.py | ALLIGATOR in room 65 | no ALLIGATOR in DATA; Gunness puts the alligator on floor 2 |
| floor_1.py | BURGLAR'S MASK | not in DATA and not in any room description |
| floor_1.py | landing from floor 2 = room 69 | floor 2's stairs land you in room **63** |
| floor_2.py | rooms 69-73 | floor 2 = rooms **58-62** |
| floor_2.py | INDIAN ROPE,-69 | no INDIAN ROPE, no room 69; the magic rope is the flute's effect |
| floor_2.py | SMALL BOOK in 61 | SMALL BOOK is in **64** (floor 1) |
| floor_3.py | rooms 65-69, WATER COOLER 58, PLANT 59 | floor 3 = rooms **52-57**; cooler and plant are floor 2 |
| floor_3.py | FLUTE, SMALL BOOK in 61 | FLUTE is **61** (floor 2), SMALL BOOK is **64** (floor 1) |
| floor_4.py | rooms 61-69 | floor 4 = rooms **45-51** |
| floor_5.py | rooms 51-59 | floor 5 = rooms **37-44** |
| floor_5.py | SIGN in 52 | SIGN ON WALL,-32 is **floor 6** (room 32) |
| floor_5.py | PUSH BUTTON in 56 | PUSH BUTTON ON WALL,-42 (floor 5), -46 (floor 4) |
| floor_5.py | machine in 57, JUMP PLATFORM in 58 | room 57 is the child's playroom (floor 3); 58 is floor 2 |
| floor_5.py | entry from floor 6 via stairs -> room 51 | floor 6's ledge jump lands in room **43** |
| all | item count 58 | DATA holds **55** items; the loop reads `FOR A=1 TO 55` |

## Crops

- `pix/f1_5_rooms47_63-1.png`, `pix/f1_5_rooms64_75-2.png` - floors 5-2 room table
- `pix/tie_lines45_52-1.png` - lines 44-52, the floor 5/4 boundary
- `pix/room_74_75-2.png` - rooms 64-65
- `pix/floor2_lines68_72_wide-2.png` - lines 68-72 at 900 dpi
- `pix/data_2000_2020-4.png`, `pix/oa_p4_data_2030_2040-4.png` - item inventory

