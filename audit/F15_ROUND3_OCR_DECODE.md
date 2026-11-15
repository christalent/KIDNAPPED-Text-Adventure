# F15 Round 3 - the OCR text layer IS the complete listing

Status: 2026-11-15.  Supersedes the "six open regions" framing in
`FLOORS_1_5_SOURCE_HANDLERS.md`.

## The finding that changes the method

`KIDNAPPED_OCR.txt` (in the repo root) is **the complete numbered BASIC
listing**, not a fragment.  Earlier notes treated it as a partial fragment that
had to be mined with guesswork.  It is not.  It carries the magazine's own
section headers, and the listing runs from printed line 10 through printed
line 6000 with no gaps.

Its one systematic defect:

    **tesseract reads the printed digit 4 as the digit 1.**

Every printed `4` came back as `1`.  That single rule decodes the whole text
layer, and it is self-verifying: the legend block says "BR = Book read?" and
the decoded line 607 reads `IF RS=2 IF A=64 IF BR=1` - the `4` in `A=64` was
OCR'd as `A=6i`, and the `1` in `BR=1` survived because there was no `4` there.

## How to resolve a printed line number

For printed label N, the OCR label is N with each `4` replaced by `1`.
So the label is ambiguous exactly when N contains a `1`, and unambiguous
otherwise.  `ocrresolve.py` (in `/home/chris/projects/kidnap-decoder`) resolves
the ambiguity by walking the listing in order and requiring printed line
numbers to increase, then dumps decoded ranges.

    python3 ocrresolve.py lines 460 480     # dump a printed line range
    python3 ocrresolve.py grep BR= SD= UM=  # find lines containing tokens

## The listing's own section headers (OCR line numbers in brackets)

| printed lines | section |
|---|---|
| 10-75 | Roof: room descriptions |
| 310-388 | Description of current location |
| 390-100 | Player input (the parser) |
| 150 | String sorting routine |
| 160-180 | GET command, special conditions |
| 180-590 | DROP |
| 600-618 | GO command |
| 700-730 | PUSH |
| 620-630 | (OPEN/door handling) |
| 650-696 | READ command |
| 830-845 | TIE command |
| 975 | SWIM |
| 980-982 | DRINK command |
| 985 | (POUR command) |
| 990-993 | PLAY command |
| 995 | THROW command |
| 1100-1210 | Subroutines: change, add or vanish items |
| 1500-1510 | Descriptions (part of line 388 to further...) |
| 2000-2010 | DATA |
| 2100-2110 | Command data |
| 3000-4100 | Short subroutines |
| 4900-5100 | Timing loop |
| 6000 | You win! |
| 7000-7100 | (death / refusal handlers) |

Two header corrections against earlier notes: the parser block is
**390-400** (not "390-100"), and there is a distinct **"Lines 620-630"** block
sitting *between* the GO block (600-618) and the READ block (650-696), plus a
PUSH block at 700-730.  The earlier "6 regions" list was a guess at which
regions mattered; the listing names its own blocks.

## Decoded corrections to earlier round-2 claims

### 1. Line 970 is FR, not R  (round 2 was WRONG)

Round 2 recorded the KNIT precondition as `R=1` (book read).  The decoded
line is:

    970 IF D(B)<>15 THEN 980 ELSE IF FR=1 IF I(32)=1 IF I(33)=1 IF E$="IES"
        PRINT"YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT":FR=2:GOTO5000

`FR` is the **clothes** flag, not a book-read flag:

    710 IF A=27 IF FR=0 PRINT"SPRINKLER TURNS ON. ... BUT YOUR CLOTHES ARE
        ALREADY OFF. YOU TAKE THEM OFF. YOU ARE NOW NAKED.":FR=1:...
    970 ... FR=2 ... "YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT"

So FR=0 normally clothed, FR=1 naked, FR=2 wearing the finished suit, and
**KNIT requires you to be NAKED** - plus yarn (I(32)=1), needles (I(33)=1) and
`E$="IES"` (the tail of "NEEDLES").  The separate `R` flag is set at line 696
when you READ the book (`IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN R=1`), and
its meaning is still open.

This is a substantive correction: the port must not gate KNIT on having read
a book.

### 2. SWIM is asymmetric

    975 IF SP=0 THEN 1000 ELSE IF A=49 THEN A=48:GOTO300 ELSE IF A=48
        IF BR=0 THEN PRINT"YOU DON'T KNOW HOW TO SWIM!":GOTO7200
        ELSE A=49:GOTO4900

* `SP=0` (pool not filled) -> refusal at 1000.
* From room **49** you go to **48** unconditionally - no know-how needed.
* From room **48** you need `BR=1`; otherwise you **die** at 7200.
* With `BR=1` from 48 you end at room 49.

### 3. The tightrope gate is on the CROSSING, not the tie

    607 IF E$="OPE" IF A=65 THEN A=64:GOTO300 ELSE IF RS=2 IF A=64 IF BR=1
        THEN A=65:GOTO300 ELSE PRINT"YOU DON'T KNOW HOW TO WALK A TIGHTROPE"
        :GOTO7200
    840 IF E$<>"OPE" THEN 850 ELSE IF A=64 IF I(54)=1 ... RS=1:GOTO4900

`840` (TIE) carries no book check.  `607` (the crossing) requires **both**
`RS=2` (rope already stretched) **and** `BR=1` (book read), and kills you at
7200 otherwise.

### 4. Line 800's final token

    800 IF A=60 OR A=61 OR A=64 THEN 7100 ELSE IF A=34 OR A=36 IF I(25)=1
        AND BO=2 THEN PRINT"BALLOON CARRIES YOU DOWN ONE FLOOR":A=43:GOTO8000
        ELSE <FINAL TOKEN>
    805 IF I(39)=1 IF UM=1 THEN PRINT"YOU FLOAT DOWN ONE FLOOR":A=52:GOTO8000
        ELSE PRINT"UMBRELLA WASN'T OPEN!":GOTO7100
    810 GOTO730

The OCR renders the tail of 800 as `ELSE710 o B05` - i.e. `ELSE 7100` followed
by the start of printed line **805** on the same printed row.  `7100` and `805`
are both plausible readings of the same glyph run, so this one still needs a
pixel check; it is the last unresolved token in the JUMP handler.

### 5. BR is set by the READ handler path

The decoded 696 is `IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN R=1:GOTO4900` -
it sets `R`, not `BR`.  `BR` is the "Book read?" flag from the legend, and the
only two places the listing tests it are 607 (tightrope crossing) and 975
(swim).  The line that sets `BR=1` is still not located; the listing's own
legend says only "BR = Book read?".

## Flag legend, decoded (OCR lines 38-87)

    EF,SD,UM,SP,JK,CI,RI = Item flags (0 = natural state, 1 = changed).
    RS = Rope status (0 = loose, 1 = tied to stake, 2 = stretched across quicksand).
    BO = Balloon status (0 = deflated, 1 = inflated, 2 = tied to string).
    PT = Plant status (0 = small, 1 = huge).
    BR = Book read?
    A$ = Player input command.  E$ = Picks last 3 letters of object command.
    J$,N$ = Room descriptions (repeated use).
    M$,R$ = Used to change, add or remove an item in room or if carried.
    H$(X) = Permanent storage of items.  A$(X) = Temporary storage of items.
    B$(X) = Commands.  C$(X) = Items carried by player.
    A(X) = Item location (room #s).  B(X) = Holds room #s accessible from current location.
    D(X) = Command codes.
    I(X) = Main purpose: If item X is carried by player, I(X) = 1.
    G(X) = Door status (0 = locked, 1 = open).

Note `G(X) = Door status (0 = locked, 1 = open)` - a single global door array,
which is what `G(1)=1` in the steel-door handler sets.

## Method note

Pixel reads remain the authority for exact characters; the OCR layer is used
here for **line-number resolution and structure**, which is what it is reliable
for.  Where a decoded reading depends on a single ambiguous glyph run (line
800's final token, the exact `E$` tokens in 600), the pixel check still wins
and is recorded in `F15_SOURCE_LINES.json` with its confidence.
