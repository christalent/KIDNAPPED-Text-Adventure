# Floors 1-5 - handler audit against the printed listing

**Status: floors 1-5 handler audit, first pass.** Room map and item placement
were already verified in `FLOORS_1_5_GROUND_TRUTH.md`.  This file records what
was read *directly from the magazine pixels* for the handler code, and which
port-level claims survive that test.

## Method

The PDF page raster is natively 300 DPI, so every handler line here was read
from an upscaled crop of the native raster (`nativecrop.py bands`), using
`vision_analyze` on the crop.  The PDF's embedded OCR layer was used only to
*locate* lines (its bbox geometry is sound, its characters are not - it prints
`4` as `1`).  Every transcription below was checked against the pixels, not
against the OCR text.

Machine-readable version: `audit/F15_SOURCE_LINES.json` (line number, literal
text, source crop, confidence).

## Dispatch model (confirmed from pixels)

`E$` is the last three characters of the object word (`OPE` matches ROPE,
`OOR` matches DOOR, `OOK` matches BOOK), and handlers test the global room
variable `A=`.  The verb dispatcher keys off `D(B)`, the verb index.

### The verb table (DATA 2100 / 2110, pixel-exact)

```
2100 DATA WEST,N,NORTH,N,EAST,E,SOUTH,S,UP,U,DOWN,D,GET,TAKE,DROP
     ,PUT,GIVE,PAY,CLIMB,GO,ENTER,OPEN,READ,CHECK,WATCH,PRESS,PUSH,TA
     PE,TIE,LIGHT,MAKE,GLUE,INFLATE,SHOOT,KNIT,DRINK,POUR,PLAY,THROW
2110 DATA 1,1,2,2,2,2,3,3,3,4,5,5,5,6,6,9,9,10,11,12,13,14,15,18,
     19,20,21
```

27 verbs, 27 codes.  Mapping the codes onto the verbs in order:

| code | verbs | code | verbs |
|---|---|---|---|
| 1 | GET, TAKE | 9 | TAPE, TIE |
| 2 | DROP, PUT, GIVE, PAY | 10 | LIGHT |
| 3 | CLIMB, GO, ENTER | 11 | MAKE |
| 4 | OPEN | 12 | GLUE |
| 5 | READ, CHECK, WATCH | 13 | INFLATE |
| 6 | PRESS, PUSH | 14 | SHOOT |
| | | 15 | KNIT |
| | | 18 | DRINK |
| | | 19 | POUR |
| | | 20 | PLAY |
| | | 21 | THROW |

**There is no SWIM verb and no JUMP verb.**  That is a hard finding, and it
invalidates one port claim outright (see floor 4).  The codes skip 7, 8, 16 and
17, which is consistent with the magazine omitting those verbs.

## Floor-by-floor

### Floor 1 (rooms 63-65)

| claim | verdict | source |
|---|---|---|
| piano yields the key | **CONFIRMED** | line 465: `IF A=63 IF E$="KEY" PRINT"WE ALL KNOW PIANOS HAVE KEYS"` |
| book is "How to walk a tightrope" | **CONFIRMED** | line 474: `IF E$="OOK" PRINT"TITLE OF BOOK: HOW TO "; IF A=47 THEN PRINT"SWIM" ELSE IF A=64 PRINT"WALK A TIGHTROPE"` |
| TIE ROPE needs the book read first | **PARTIAL** | line 995 shows the rope state machine (`RS=0` -> "TIE THE OTHER END FIRST"; `RS=1` -> "HOOK ON ROPE CATCHES HOOK NEAR ENTRANCE AND STRETCHES TIGHT", sets `RS=2`) but the book-read gate on TIE is in lines 830-845, not yet transcribed |

### Floor 2 (rooms 58-62)

| claim | verdict | source |
|---|---|---|
| cup of water at the water cooler | **CONFIRMED** | line 468 produces "CUP OF WATER" at A=58 |
| plant needs the cup of water; flute makes the rope | **UNPROVEN** | the gating bodies live in the GET region (460-490) and the PLAY region (985-993), not yet transcribed |

### Floor 3 (rooms 52-57)

| claim | verdict | source |
|---|---|---|
| steel door needs Mr. Hyde's strength | **PARTIAL** | line 980 proves `JK` is the transformation flag: `IF D(B)<>18 THEN 985 ELSE IF E$="ION" IF I(44)=1 IF JK=1 THEN PRINT"YOU'VE CHANGED BACK!":JK=0:GOTO5000 ELSE 4900` (DRINK SOLUTION reverts `JK=1` -> `JK=0`).  The door branch itself is at 615-618, not yet transcribed |
| graffiti text is invented | **UNPROVEN** | the room 53 graffiti print is in the unread region 615-618 / 460-490 |

### Floor 4 (rooms 45-51)

| claim | verdict | source |
|---|---|---|
| SWIM needs the filled pool AND the swimming chapter | **CONFIRMED, and the source is stricter than the port** | line 975: `IF SP=0 THEN 1000 ELSE IF A=49 THEN A=48:GOTO300 ELSE IF A=48 IF BR=0 THEN PRINT"YOU DON'T KNOW HOW TO SWIM!":GOTO720 ELSE A=49:GOTO4900`.  Two independent gates: `SP` (pool filled) and `BR` (book read).  `SP` is set by line 720 (`IF A=46 IF SP=0 PRINT"CLICK":SP=1:GOTO5000`) - the button in room 46.  `BR` is the book-read flag; the book in room 47 is the swimming chapter (line 474) |
| JUMP is accepted from room 50 and from room 51 | **REFUTED as stated** | there is no JUMP verb in DATA 2100/2110.  The descent to floor 3 is the UMBRELLA: line 805 `IF I(39)=1 IF UM=1 THEN PRINT"YOU FLOAT DOWN ONE FLOOR":A=52:GOTO800 ELSE PRINT"UMBRELLA WASN'T OPEN":GOTO7100`.  The floor-4 puzzle is open-umbrella-then-float, not jump.  The walkthroughs' "JUMP" is either the magazine's own shorthand for that move or a walkthrough error - either way the port's `JUMP` verb is not in the source |

Also confirmed: line 800 handles the balloon descent (`BALLOON CARRIES YOU DOWN ONE FLOOR` -> A=43) with `I(25)=1` and `B0=2`.

### Floor 5 (rooms 37-44)

| claim | verdict | source |
|---|---|---|
| fire blocks the northward move from room 41 until the button in room 42 is pressed | **CONFIRMED** | line 361 `IF(A=41)X(FR=0)THEN363ELSEIFN>=0PRINT" NORTH";:B(3)=N:B(4)=N` skips the NORTH exit while `FR=0`, and line 1520 prints `THERE IS A PATH NORTH, BUT A RAGING FIRE BLOCKS YOUR WAY.` |
| pressing the button drowns you and costs your clothes | **CONFIRMED, wording differs** | line 710 prints `SPRINKLER TURNED ON, FIRE OUT, BUT YOUR CLOTHES ARE VERY WET, YOU TAKE THEM OFF, YOU ARE NOW NAKED.` and sets `FR=1`.  Not a drowning - a sprinkler |
| KNIT CLOTHES (needles + yarn) replaces them | **CONFIRMED** | line 970 (KNIT) requires `I(32)=1` and `I(33)=1` plus `R=1`, prints `YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT` and sets `FR=2` |
| the stairs refuse a naked player | **UNPROVEN** | the stairs handler is at line 612 (`IF E$="IRS" IF A=25 OR A=44 OR A=62 A=A+1: GOTO 8000`) with no `FR` test visible; the naked-player refusal may live in the 615-618 region, still unread |

## Still to transcribe

1. Lines 615-618 (p3L) - the floor 3 STEEL DOOR branch, the room 53 graffiti
   print, and any `FR` refusal on the stairs.
2. Lines 460-490 (p2R) - the GET region: plant, flute, piano key body.
3. Lines 985-993 (p4L) - the PLAY region: PLAY FLUTE, and how the SWIM
   command at 975 is reached when SWIM is not a verb.
4. Line 800-810 header says "JMP command" - a typo'd JUMP?  Worth a
   high-zoom look, because it suggests the magazine does dispatch a JUMP
   somehow.
5. `BR` - where is it set?  It must be in the READ handler around 650-700.
6. `R` - line 970 requires `R=1` for KNIT; find where R is set.

## Method note

`nativecrop.py bands <page> <L|R> <outdir> [y0] [y1] [height_pt] [scale]`
cuts native-pixel bands from the extracted page rasters; `vision_analyze` on
those crops is the only trustworthy transcription path.  The 3000-DPI render
premise in the old `rowdump2.py` was wrong - the source raster is exactly
300 DPI, so higher-DPI renders only interpolate.
