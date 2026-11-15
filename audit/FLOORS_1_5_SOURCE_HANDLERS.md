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

**There is no SWIM verb and no JUMP verb** in the `DATA` verb table — but that
does NOT mean the source lacks them.  The parser at **line 390** special-cases
`LOOK`, `" JUMP"` → 800, `SWIM` → 975, and `WAIT` → 1050 *before* it ever
consults `B$(1..12)` (directions) or `B$(13..39)` (the 27 ordinary verbs).
So the source **does** implement a jump and a swim; the earlier "hard finding"
was an artefact of reading only the verb table.  See
`audit/F15_PIXEL_ROUND2.md` section 1.  The codes skip 7, 8, 16 and
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

## Resolved in round 2 (see audit/F15_PIXEL_ROUND2.md)

1. Lines 615-618 (p3L) - the floor 3 STEEL DOOR branch, the room 53 graffiti
   print, and any `FR` refusal on the stairs.
   **RESOLVED (round 2)** for the steel door and graffiti: transcribed verbatim in
   `audit/F15_PIXEL_ROUND2.md` (lines 616, 620, 650) and in `audit/F15_SOURCE_LINES.json`.
   The `FR` refusal on the stairs is still unlocated, but the `FR` flag itself is now
   pixel-confirmed: `710` sets `FR=1` ("YOU ARE NOW NAKED"), `970` sets `FR=2`
   ("YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT"), and line `612` (the stairs
   handler) contains no `FR` test - so the refusal, if it exists, is elsewhere.
2. Lines 460-490 (p2R) - the GET region: plant, flute, piano key body.
   **RESOLVED (round 2)**: line 465 (piano yields runtime item 56 = KEY), 468 (fill the
   paper cup at the cooler -> item 57 = CUP OF WATER), 470-474 (item lookup and the
   book-title print), 480 (the carry put). Transcribed verbatim in
   `audit/F15_PIXEL_ROUND2.md` and `audit/F15_SOURCE_LINES.json`.
3. Lines 985-993 (p4L) - the PLAY region: PLAY FLUTE, and how the SWIM
   command at 975 is reached when SWIM is not a verb.
   **RESOLVED (round 2)**: 985 (POUR WATER -> plant grows, `PT=1`), 990 (PLAY FLUTE at
   room 61 with flute 50 -> `R1=1` and rope item 56 appears), 993 (the "LIBERACE
   YOU'RE NOT!" branch). And the SWIM question is answered outright: the parser at
   line 390 dispatches the literal input `SWIM` to 975, so SWIM *is* a source command -
   it is simply not one of the 27 `DATA` verbs.
4. Line 800-810 header says "JMP command" - a typo'd JUMP?  Worth a
   high-zoom look, because it suggests the magazine does dispatch a JUMP
   somehow.
   **RESOLVED (round 2)**: the listing's own printed comment reads *"Lines 800-810:
   JMP command."* and the parser at line 390 dispatches the literal input
   `" JUMP"` to handler 800. So the magazine's own label "JMP" is a typo for JUMP,
   and the source **does** dispatch a jump command. The umbrella branch at 805
   (`I(39)=1` and `UM=1` -> "YOU FLOAT DOWN ONE FLOOR", `A=52`) is what a jump
   with an open umbrella does; line 810 is `GOTO730`.
5. `BR` - where is it set?  It must be in the READ handler around 650-700.
6. `R` - line 970 requires `R=1` for KNIT; find where R is set.

## Method note

`nativecrop.py bands <page> <L|R> <outdir> [y0] [y1] [height_pt] [scale]`
cuts native-pixel bands from the extracted page rasters; `vision_analyze` on
those crops is the only trustworthy transcription path.  The 3000-DPI render
premise in the old `rowdump2.py` was wrong - the source raster is exactly
300 DPI, so higher-DPI renders only interpolate.

## Round 4 corrections (supersede earlier claims in this file)

* **`FR` is not "naked".** `FR` is a three-state flag: `0` pre-sprinkler,
  `1` post-sprinkler (naked, and the `WET CLOTHES` item 57 exists at room
  42), `2` wearing the knitted suit.  Uses: set at 710 and 970, tested at
  710 and 970.  Any earlier note here reading "`FR=1` means naked" or
  "`FR=1`/`FR=2` are the suit states" is superseded.
* **`KNIT` does not require having read a book.**  Printed 970 requires
  `FR=1` (the sprinkler has run) plus `I(32)=1` (yarn) and `I(33)=1`
  (needles).  The earlier "`KNIT` requires `R=1`" claim is wrong.
* **The book-read flag is `BR`,** set at printed 696
  (`IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN BR=1:GOTO4900`) and read only at
  607 (tightrope) and 975 (SWIM).  Reading a book sets `BR=1`.
* **SWIM is asymmetric and fatal on failure.**  Printed 975: `SP=0` ->
  "YOU CAN'T DO THAT NOW." (1000); from room 49 -> 48 unconditionally; from
  room 48 -> needs `BR=1`, and `BR=0` prints "YOU DON'T KNOW HOW TO SWIM!"
  and jumps to 7200 (death), it does not merely refuse.
* **Floor-3 graffiti text.**  The source string is
  `GRAFFITI: DO YOU HAVE A SPLIT PERSONALITY?`; the earlier
  "steel door / strong man" wording was invented and has been removed.
* Full evidence: `audit/F15_ROUND4_LISTING_FINDINGS.md`,
  `audit/F15_LISTING_VERIFIED.json`.

### Divergence still open (needs a decision, not a blind patch)

* The source has **one** book-read flag, `BR=1`, set at printed 696 by reading
  either book (`I(38)` or `I(52)`) and read at 607 (tightrope) and 975 (SWIM).
  The port keeps two flags, `know_rope` (floor 1) and `can_swim` (floor 4).
  In the printed listing, reading the floor-1 book also sets `BR=1`, and the
  printed book title itself is room-dependent: line 474 prints
  `TITLE OF BOOK: HOW TO ` then `SWIM` for A=47 and `WALK A TIGHTROPE` for
  A=64.  Unifying the two port flags is a gameplay change (a player who has
  read either book can do both), so it is flagged rather than forced.
* `E$` at printed 970 is unresolved between `HES` (CLOTHES), `LES` (NEEDLES)
  and `IES`; the port accepts both `CLOTH...` and a noun ending in `THE`,
  which covers the plausible readings without a risky narrowing.
