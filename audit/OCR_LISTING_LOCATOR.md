# OCR listing locator - KIDNAPPED_OCR.txt is the FULL listing, not a fragment

Status: 2026-11-15.  Written during the end-of-week development push on the
KIDNAPPED remake.  Purpose: replace guesswork with a deterministic procedure
for the six source regions that were still untranscribed.

## The finding that changes the method

`KIDNAPPED_OCR.txt` (the OCR text layer in this repo) is **the complete
numbered BASIC listing**, with the magazine's own section headers
("GET command", "DROP", "GO cmd", "OPEN cmd", "READ cmd", "TIE cmd",
"LIGHT, MAKE, GLUE, INFLATE, SKILL, KNIT, BOOT COM", "DATA", ...).
Earlier notes treated it as a partial fragment that had to be mined with
guesswork.  It is not.  Its one systematic defect is:

    **tesseract reads the printed digit 4 as the digit 1.**

Every printed `4` in the listing came back as `1`.  That single rule decodes
the whole text layer:

| OCR text          | true source                                             |
|-------------------|---------------------------------------------------------|
| label `160`       | source line 460                                         |
| label `174`       | source line 474                                         |
| `IF A=17`         | `IF A=47`                                               |
| `IF A=61`         | `IF A=64`                                               |
| `GOTO 1900`       | `GOTO 4900`                                             |
| `A$(58)=[$`       | `A$(58)="KEY"`                                          |

Cross-checks against data that was already pixel-verified before this
session (see `audit/FLOORS_1_5_SOURCE_HANDLERS.md`):

* OCR `174 IF E$="OOK" PRINT "TITLE OF BOOK: HOW TO ": IF A=17 THEN PRINT
  "SWIM" ELSE IF A=61 PRINT "WALK A TIGHTROPE"` decodes to source line 474
  with A=47 / A=64 - exactly the line 474 already verified from pixels.
* OCR `612 IF E$="IRS" IF A=25 OR A=44 OR A=62 A=A+1: GOTO 8000` contains no
  4, so it decodes unchanged, and it is the stairs handler already
  verified at line 612.
* The pixel number maps (tesseract over the native rasters, digits only)
  place true lines 460..480 in the same physical column as the OCR block
  labelled 160..180.

Reverse rule: substitute 4 -> 1 to *encode*, so to *decode*, replace a 1 with
4 where the geometry agrees.  Labels containing a `1` are ambiguous in
isolation (a printed `161` is either 161 or 461); disambiguate with the
pixel number map for that page/column.

## E$ semantics (needed to read every conditional)

Source line 450 (OCR label `150`) is the string-splitting routine:

    450 OS=RIGHT$(A$,(LEN(A$)-F)-1):E$=RIGHT$(OS,3)

`A$` is the whole typed command, so `E$` is the last three characters of the
object word:

    GET KEY   -> E$="KEY"      GET FLUTE  -> E$="UTE"
    GET BOOK  -> E$="OOK"      GET STAIRS -> E$="IRS"
    GET DOOR  -> E$="OOR"      GET CHAIR  -> E$="AIR"
    GET WATER -> E$="TER"      GET CLOCK  -> E$="OCK"
    GET SIGN  -> E$="IGN"      GET NOTE   -> E$="OTE"

This is why the OCR fragments like `If Ef="IlR"` are really
`IF E$="AIR"` (CHAIR) and `IF Ef="IlR" ... A=25` is `IF E$="IRS"` (STAIRS).

## Geometry for the six open regions

Number maps live in `/home/chris/projects/kidnap-decoder/work3000/open/all/`
(`ALL.json`, plus `map_<page><col>.json` per column).  Row indices are the
indices into `nativecrop.rowboxes(page, col)`; a few detections are body-text
false positives (e.g. a "640" inside prose), so validate monotonicity before
cropping.

| region | source lines | page/col | rows | composite (read this) |
|---|---|---|---|---|
| steel door / graffiti / stairs | 600-618 | 3L | 16..36 | `open/comp/c_3L_600_618.png` |
| READ handler | 650-696 | 3L 50..55, 3R 0..8 | | `open/comp/c_3L_648_670.png`, `open/comp/c_3R_670_700.png` |
| GET / DROP | 450-490 | 2R | 18..57 | `open/comp/c_2R_450_475.png`, `open/comp/c_2R_476_490.png` |
| PLAY / KNIT / SWIM | 973-1000 | 4L | 0..20 | `open/comp/c_4L_973_993.png` |
| descent (balloon/umbrella) | 800-850 | 3R | 15..36 | `open/comp/c_3R_800_845.png` |
| KNIT | 970 | 3R (end of column) | ~50..54 | not yet composited |

Absolute paths: `/home/chris/projects/kidnap-decoder/open/comp/`.
Regenerate with `/home/chris/projects/kidnap-decoder/mkcomp.py`; the extra
ranges still missing are in `open/mkcomp2.py`.

Read the `comp/` images with `vision_analyze` at ~1616 px wide - they are
scaled so the dot-matrix glyphs survive the model's downscale.  The
single-line `open/lines/` and `work3000/handler/`, `work3000/f15*` crops from
the 2026-11-13 session are still useful for re-checks.

## What the OCR layer says about the open regions

These are LOCATORS, not transcriptions.  Every one of them still needs a
pixel read before it can be written into the floor files, but they are
specific enough to aim the pixel reads.

### Q1 - lines 615-618, floor 3 (steel door, graffiti, stairs/FR)

Decoded OCR for the GO handler (labels are OCR labels):

    600 IF D(B)<>3 THEN 620 ELSE IF ((A=16) I(E$="MAN")) + ((A=58) I(E$="TIE"))
        THEN 7000 ELSE IF ((A=1) I(E$="IRE")) + ((A=61) I(E$="AN")) THEN 7200
        ELSE IF A=25 AND E$="IRS" AND (SC=0) PRINT "STEP IS MISS! YOU FELL
        DOWN THE STAIRS": GOTO 7200
    605 IF E$="OPE" IF R1=1 IF A=17 IF A=61 A=A+1: R1=0: IF A=17 THEN 8000
        ELSE 300
    606 IF E$="AHT" IF PT=1 IF A=59 THEN A=60: GOTO 300 ELSE IF A=60 A=59:
        GOTO 300
    607 IF E$="OPE" IF A=63 THEN A=64: GOTO 300 ELSE IF RS=2 IF A=64 IF BR=1
        THEN A=65: GOTO 300 ELSE PRINT "YOU DON'T KNOW HOW TO TIE A
        TIGHTROPE": GOTO 7200
    608 IF E$="AXI" IF A=36 A=A-1: GOTO 300
    610 IF E$="DGE" IF A=7 THEN PRINT "LEDGE BREAKS!": GOTO 7200 ELSE IF A=33 ...
    612 IF E$="IRS" IF A=25 OR A=44 OR A=62 A=A+1: GOTO 8000
    615 IF E$="OOR" IF A=24 OR A=43 OR A=30 OR A=65 IF G((A/10-INT(A/10))*10)=0
        THEN PRINT "THE DOOR'S LOCKED": GOTO 5000 ELSE A=A+1: GOTO 300
    616 IF E$="OOR" IF A=55 IF SD=1 OR K=1 THEN A=57: GOTO 300 ELSE PRINT
        "IT'S STUCK! YOU'RE NOT STRONG ENOUGH TO OPEN IT": GOTO 5000
    617 IF E$="IDE" IF A=57 PRINT "YOU SLIDE DOWN THE HOLE IN THE FLOOR":
        A=58: GOTO 8000
    618 IF A=49 IF E$="OOR" OR E$="AIR" IF I(3)=4 THEN PRINT "YOU STEP ON THE
        CHAIR ...": A=41: GOTO 5000 ELSE PRINT "YOU CAN'T REACH IT": GOTO 5000

Reading: **line 616 is the STEEL DOOR** - E$="OOR" (DOOR), A=55 (room 55 =
STEEL DOOR), gated on `SD=1 OR K=1`, moving to A=57, else "IT'S STUCK! YOU'RE
NOT STRONG ENOUGH TO OPEN IT".  That matches floor 3's steel door needing
Mr Hyde's strength (the `K` flag).  **The graffiti print is not in this
region** - it is in the READ handler at line 650:

    650 IF D(B)<>5 THEN 700 ELSE IF E$="ITI" IF A=6? THEN PRINT "GRAFFITI! ...":
        GOTO 5000 ELSE IF A=53 PRINT "GRAFFITI! ... YOU WERE A SPLIT PERSON?":
        GOTO 5000
    660 IF E$="OTE" IF I(1)=A00 I(1)=1 OR (A=2) I(I<1)<>0 THEN PRINT "NOTE SAYS: ..."
    670 IF E$="IGN" IF A=32 PRINT "SIGN: STRING COSTS $1.00": GOTO 5000

(E$="ITI" = GRAFFITI, "OTE" = NOTE, "IGN" = SIGN.)  So the floor-3 room-53
graffiti is a READ of the wall graffiti, and the port's current scrawl text
("THE STEEL DOOR ONLY OPENS FOR THE...") is **not source-backed** - it has to
be replaced by whatever line 650 prints.  Q1's graffiti half therefore moves
to the READ handler, and the exact wording of line 650 needs a pixel read.

### Q2 - lines 460-490, GET region (plant, flute, piano key)

    460 IF D(B)<>1 THEN 490
    461 IF E$="GHT" OR E$="APE" IF A=10 IF C1=0 THEN PRINT "CABINET IS
        LOCKED": GOTO 5000 ELSE IF E$="GHT" AND CF=0 THEN J=56:
        A$(J)="FLASHLIGHT": H$(J)=A$(J): A(J)=10: CF=1 ELSE IF E$="APE" AND
        CT=0 THEN J=57: A$(J)="ELECTRIC TAPE": H$(J)=A$(J): A(J)=10: CT=1
    462 IF A=7 IF J<>0 IF E$="KEY" IF I(1)<>0 THEN PRINT "YOUR ARM IS TOO
        SHORT TO REACH IT": GOTO 5000 ELSE J=58: A$(J)="KEY": H$(J)=A$(J):
        A(J)=7: I(58)=1: KY=1
    465 IF A=63 IF E$="KEY" PRINT "WE ALL KNOW PIANOS HAVE KEYS": J=56:
        A$(J)=E$: H$(J)=A$(J): A(J)=63: I(56)=1
    470 FOR J=1 TO 58: IF E$=RIGHT$(A$(J),3) AND A=ABS(A(J)) THEN 473
    471 NEXT
    472 PRINT "THERE'S STILL ONE HERE.": GOTO 390
    473 IF SGN(A(J))=-1 PRINT "BE REASONABLE. THAT'S ENOUGH.": GOTO 390
    474 IF E$="OOK" PRINT "TITLE OF BOOK: HOW TO ": IF A=47 THEN PRINT "SWIM"
        ELSE IF A=64 PRINT "WALK A TIGHTROPE"
    480 PRINT "(J)": FOR I=1 TO 7: IF C$(K)=" " THEN C$(K)=A$(J): GOSUB 9500:
        H(K)=J: A$(J)="": A(J)=0: GOTO 5000 ELSE J=J+1: NEXT

Reading: **line 465 is the piano key body** (A=63 is the piano room; the item
name is copied from `E$`, which is why it reads "KEY" for GET KEY).  Line
474 is the book title (room 47 = swimming chapter, room 64 = tightrope
chapter).  The plant and flute bodies are NOT in 460-490: they are the verb
handlers at 985/990 (see Q3).  So the audit's "plant, flute, piano key body"
was three different places; only the piano key is in the GET region.

### Q3 - lines 985-993, PLAY / POUR (plant, flute)

    985 IF D(B)<>19 THEN 990 ELSE IF A=59 IF E$="TER" IF I(57)=1 THEN PRINT
        "PLANT GROWS ..."
    990 IF D(B)<>20 THEN 995 ELSE IF E$="UTE" IF A=61 IF I(50)=1 IF R1=0 THEN
        PRINT "IN..."
    993 IF E$="AIU" IF A=63 PRINT "LIE ... YOU'RE TOO ...": GOTO 5000

Reading: **verb 19 is POUR** (water on the plant at room 59, needs the cup
of water item I(57)=1), **verb 20 is PLAY** (the flute at room 61, needs
I(50)=1 and R1=0).  The text layer clips the long PRINT strings at the
column edge - the pixel read must capture the full strings.

### Q4 - line 800-810, the descent

    800 IF A=60 OR A=61 OR A=64 THEN 7100 ELSE IF A=34 OR A=36 IF I(25)=1 AND
        BO=2 THEN PRINT "BALLOON CARRIES YOU DOWN ONE FLOOR": A=43: GOTO 11000
        ELSE 7100
    810 GOTO 730

This is the **balloon/umbrella descent**, already confirmed by the audit
(line 805 is the umbrella float to A=52).  It is not a JUMP verb: DATA
2100/2110 hold 27 verbs and no verb maps to JUMP.  The section header that
reads "JMP command" is most likely the magazine's own name for this descent
handler - the magazine can label a block "JMP" without giving the player a
JUMP verb - but the header's exact wording still needs a pixel read.  What
is settled either way: there is no JUMP verb in the verb table, so the
port's `JUMP` verb is a walkthrough convenience, not a source feature, and
the floor-4 descent is open-umbrella-then-float.

### Q5 - where is BR set?

    696 IF E$="OOK" IF I(38)=1 ... GOTO 4900

(the OCR renders E$="OOK" as `Ef="(o("`).  So **BR is set in the READ
handler at line 696: you must be holding the book (I(38)=1) and READ it.**
That is the missing link for the floor 4 SWIM gate (`IF BR=0 THEN PRINT "YOU
DON'T KNOW HOW TO SWIM!"` at line 975).  Pixel read still required.

### Q6 - where is R set?  It is not R.  It is FR.

    970 IF D(B)<>15 THEN 980 ELSE IF FR=1 IF I(32)=1 IF I(33)=1 IF E$="HES"
        PRINT "YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT": FR=2:
        GOTO 5000

`FR` is the clothing flag, and the OCR label `974`/`970` confusion plus the
digit-4 rule made `FR=1` look like `R=1`.  The lifecycle already verified
from pixels is: FR=0 clothed, line 710 (sprinkler) sets FR=1 and prints
"YOUR CLOTHES ARE VERY WET, YOU TAKE THEM OFF, YOU ARE NOW NAKED", line 970
sets FR=2 (wearing the knitted suit).  So **KNIT requires FR=1, i.e. the
player must be NAKED** - that is the gate the audit recorded as a mystery
"R=1", and the floor 5 KNIT handler should test FR=1, not some other R.
(E$="HES" = CLOTHES, last three letters.)

## Consequences for the port

* floor_5 KNIT: gate on `FR == 1` (naked), needles I(32)=1, yarn I(33)=1.
  The docstring in `floors/floor_5.py` currently says "and R=1"; that is an
  OCR artifact and must be corrected.
* floor_2: the plant is `POUR WATER` (verb 19) at room 59 with the cup
  (I(57)=1); the flute is `PLAY FLUTE` (verb 20) at room 61 with I(50)=1
  and R1=0.  The port's floor_2 docstring claims the plant/flute gating
  bodies live in the GET region - they do not.
* floor_4: the swimming gate is `SP` (pool filled) AND `BR` (book read at
  line 696); there is no JUMP verb.
* floor_3: the steel door is line 616, gated on `SD=1 OR K=1`, and the
  graffiti is a READ at line 650, not a print in the GO handler.

## Rule that survives this

OCR is the locator; the raster is the truth.  Nothing above may be written
into a floor file or into `audit/F15_SOURCE_LINES.json` until the matching
composite has been read with `vision_analyze` and the characters confirmed.
