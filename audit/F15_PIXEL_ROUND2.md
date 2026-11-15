# Floors 1–5 — Pixel Round 2 (source transcription)

Second transcription pass over the **native 300-DPI magazine raster** (`/home/chris/projects/kidnap-decoder/work/crops15/`).
Authority order: **pixel > OCR > inference**. The PDF text layer misprints `4` as `1`, so OCR was used only to
locate lines and flag gross disagreements. Every line below was read from a cropped raster image; where a
character was uncertain the note says so.

This round **changes two audit conclusions** and **closes four open items**.

---

## 1. The command parser (line 390) — `SWIM` and `JUMP` are real source commands

> **390** `ONERRORGOTO3000:C=0:TM=TM+1:PRINT:PRINT"WHAT DO YOU WANT TO DO";:INPUTA$:IFDT=2THEN720ELSEIFA$="LOOK"THEN300ELSEIFA$=" JUMP"THEN800ELSEIFA$="SWIM"THEN975ELSEIFA$="WAIT"THEN1050ELSEPRINT:FORB=1TO12:IFA$=B$(B)THEN392ELSENEXT:GOTO394`
> **392** `IFB(B)<>0THENA=B(B):GOTO300ELSEPRINT"YOU CAN'T MOVE THAT WAY.";:GOTO390`
> **394** `IFA$<>"I"ANDRIGHT$(A$,3)<>"ORY"THEN400ELSEPRINT"YOU ARE CARRYING:";:FORK=1TO7:PRINTTAB(POS(0)+4)C$(K);:IFPOS(0)>45PRINT`
> **396** `NEXT:GOTO390`
> **400** `FORB=13TO39:F=LEN(B$(B)):IFLEFT$(A$,F)=B$(B)THEN450ELSENEXT:PRINT"DON'T KNOW WHAT "CHR$(34)A$CHR$(34)" MEANS.":GOTO390`

*crop:* `work/crops15/p2r_388_400_dispatch/p2R_y0120_00.png` — confidence **high**.

**What this settles.** The previous audit said *"There is no JUMP verb and no SWIM verb."* That is true only of the
`DATA` verb table (`B$(13..39)`, line 400) and the twelve direction words (`B$(1..12)`, line 390). The parser
**special-cases** the rest before it ever consults those tables:

| input | target | source role |
|---|---|---|
| `LOOK` | 300 | look around |
| `" JUMP"` | 800 | the JMP handler (block 800–810) |
| `SWIM` | 975 | the SWIM handler |
| `WAIT` | 1050 | wait a turn |
| `B$(1..12)` | 392 | twelve direction words → `A=B(B)`, else "YOU CAN'T MOVE THAT WAY." |
| `I` / `*ORY` | 394 | inventory ("YOU ARE CARRYING:") |
| `B$(13..39)` | 400 | the 27 ordinary verbs → "DON'T KNOW WHAT … MEANS." |

So **the source does implement a jump and a swim.** The earlier "impossible to reconcile" claim was an artefact of
looking only at the verb table. The port's floor-4 `SWIM` and floor-6 `JUMP` commands are source-faithful.

**Uncertainty:** the `JUMP` literal reads with a **leading space** (`" JUMP"`) in the raster. That may be a printing
artefact of the dot-matrix column rather than a real space in the string. Flagged; does not change behaviour
(`LEFT$`/`=` comparison semantics aside, the command still dispatches to 800).

**The listing labels its own blocks.** The printed comment above 800–810 reads *"Lines 800-810: JMP command."*
Above 830–845: *"Lines 830-845: TIE command."* Above 600–618: *"Lines 600-618: GO command…"*. These are part of
the source and are now recorded in `F15_SOURCE_LINES.json`.

---

## 2. Floor 1 — the rope/tightrope chain (book gate is on the *crossing*, not the *tie*)

> **840** `IF E$<>"OPE" THEN 850 ELSE IF A=64 IF I(54)=1 K3=54:R$="":GOSUB1100:A$(54)="END OF ROPE TIED TO STAKE":H$(54)=A$(54):A(54)=-64:RS=1:GOTO4900`
> **845** `IF A=17 IF I(14)=1 PRINT"ROPE TIED TO DESK":K3=14:R$="":GOSUB1100:A$(54)="MAGNET":H$(54)=A$(54):A(54)=-17:RS=1:GOTO5000` *(last token uncertain)*
> **607** `IF E$="OPE" IF A=65 THEN A=64 ELSE IF RS=2 IF A=64 IF BR=1 THEN A=65:GOTO300 ELSE PRINT"YOU DON'T KNOW HOW TO WALK A TIGHTROPE":GOTO7200`
> **995** `IF D(B)<>21 THEN 1000 ELSE IF E$="OPE" IF A=64 IF RS=0 PRINT"TIE THE OTHER END FIRST":GOTO5000 ELSE IF RS=1 THEN PRINT"HOOK ON ROPE CATCHES HOOK NEAR ENTRANCE AND STRETCHES TIGHT":RS=2:K3=54:H$="":GOSUB1200:GOTO5000`

*crops:* `work/crops15/p3r_830_845/p3R_y0330_00.png`, `work/crops15/p3l_600_618/p3L_y0255_00.png`,
`work/crops15/p4l_970_997/p4L_y0040_00.png`.

**Chain, from source:**

1. `TIE ROPE` at room 64 while carrying the rope (item 54) → item becomes *"END OF ROPE TIED TO STAKE"*, `RS=1`.
   **There is no book check on the tie itself.**
2. `THROW ROPE` at room 64 with `RS=1` → *"HOOK ON ROPE CATCHES HOOK NEAR ENTRANCE AND STRETCHES TIGHT"*, `RS=2`.
3. Cross at 607 (`A=64`): requires **`RS=2` AND `BR=1`**, else *"YOU DON'T KNOW HOW TO WALK A TIGHTROPE"*.
   `BR=1` is the book-read flag.

**Audit correction.** The prior audit's floor-1 claim — *"TIE ROPE needs the book read first; the book-read gate on
TIE is in lines 830-845"* — is **wrong about where the gate lives**. Line 840 shows the tie is unconditional;
the `BR=1` gate is on the **crossing** at 607. The *effect* (you cannot cross without having read the book) is
the same, so the port's outcome need not change, but the stated mechanism was not the source's.

**Still open:** the site where `BR=1` is set. Candidate: the READ handler near 690–696 (the raster band between
`690` and `696` was not fully legible). Flagged, not guessed.

---

## 3. Floor 4 — umbrella, pool, and the swim

> **630** `IF I(39)=1 IF E$="LLA" K3=39:R$="OPEN POPPIN'S UMBRELLA":GOSUB1100:UM=1:GOTO4900`
> **720** `IF A=46 IF SP=0 PRINT"CLICK":SP=1:GOTO5000`
> **975** `IF SP=0 THEN 1000 ELSE IF A=49 THEN A=48:GOTO300 ELSE IF A=48 IF BR=0 THEN PRINT"YOU DON'T KNOW HOW TO SWIM!":GOTO7200 ELSE A=49:GOTO4900`
> **805** `IF I(39)=1 IF UM=1 THEN PRINT"YOU FLOAT DOWN ONE FLOOR":A=52:GOTO8000 ELSE PRINT"UMBRELLA WASN'T OPEN!":GOTO7100`

*crops:* `work/crops15/p3l_620_670/p3L_y0590_00.png`, `work/crops15/p3r_680_730/p3R_y0040_00.png`,
`work/crops15/p4l_970_997/p4L_y0040_00.png`.

- **OPEN UMBRELLA sets `UM=1`** (line 630). This closes the audit's open item on the OPEN UMBRELLA body.
- **`SP` is the pool-filled flag**, set by the button at room 46 (line 720); line 975 refuses the swim while `SP=0`.
- **SWIM itself (975):** from room 49 → 48 is unconditional; from room 48 it needs `BR=1` (you know how to swim),
  else *"YOU DON'T KNOW HOW TO SWIM!"*. The failure routes to `7200`, the same death sink used by
  *"IT'S STUCK! YOU'RE NOT STRONG ENOUGH TO OPEN IT!"* — **a failed swim is fatal in the source.**
- **The JUMP handler is 800–810.** `805` is the umbrella branch: open umbrella (`I(39)=1` and `UM=1`) →
  *"YOU FLOAT DOWN ONE FLOOR"*, `A=52`, `GOTO8000`.

**Still open:** line 800's trailing `ELSE` target reads `7100` in the current crop; if it reads `805` instead, the
umbrella branch is the *general* jump path rather than a special case. Needs a higher-zoom read of that single line.

---

## 4. Floor 3 — steel door and graffiti, verbatim

> **620** `IF D(B)<>4 THEN 650 ELSE IF E$="OOR" IF A=55 THEN IF JK=0 THEN 616 ELSE GOSUB4000:G(1)=1:SD=1:GOTO4900 ELSE IF A=43 OR A=24 OR A=65 IF I(56)=1 OR (A=3)X(I(42)=1) THEN GOSUB4000:G((A/10-INT(A/10))%10)=1:PRINT"DOOR'S OPEN":GOTO5000 ELSE PRINT"YOU NEED A KEY":GOTO5000`
> **616** `IF E$="OOR" IF A=55 IF SD=1 OR JK=1 THEN A=57:GOTO300 ELSE PRINT"IT'S STUCK! YOU'RE NOT STRONG ENOUGH TO OPEN IT!":GOTO5000`
> **650** `IF D(B)<>5 THEN 700 ELSE IF E$="ITI" IF A=6 THEN PRINT"GRAFFITI: WATCH OUT FOR LIVE ONES":GOTO5000 ELSE IF A=53 PRINT"GRAFFITI: DO YOU HAVE A SPLIT PERSONALITY?":GOTO5000`

*crop:* `work/crops15/p3l_620_670/p3L_y0590_00.png` — confidence **high**.

- **Steel door (room 55):** opened via `JK=1` — Mr. Hyde's strength — and doing so sets `SD=1`, which makes the door
  openable thereafter even without Hyde. *"YOU NEED A KEY"* is the fall-through for the other locked doors
  (rooms 43, 24, 65), which open with `I(56)=1` (the piano key) or the small key `I(42)` at room 3.
  **Confirms** the port's "steel door needs Mr. Hyde" claim, and adds the `SD=1` latch the audit never mentioned.
- **Graffiti, verbatim:** room 6 → *"GRAFFITI: WATCH OUT FOR LIVE ONES"*; room 53 →
  *"GRAFFITI: DO YOU HAVE A SPLIT PERSONALITY?"* The audit's "graffiti text is invented — UNPROVEN" is now
  **closed and correct as quoted**.

---

## 5. Floor 2 — plant, cup of water, flute, rope

> **468** `IF I(48)=1 IF E$="TER" IF A=58 I(57)=1:R$="CUP OF WATER":K3=48:GOSUB1100:H$(48)=R$:GOTO4900`
> **985** `IF D(B)<>19 THEN 990 ELSE IF A=59 IF E$="TER" IF I(57)=1 PRINT"PLANT GROWS TO CEILING":A$(49)="HUGE PLANT":PT=1:H$(49)=A$(49):GOTO5000`
> **990** `IF D(B)<>20 THEN 995 ELSE IF E$="UTE" IF A=61 IF I(50)=1 IF R1=0 PRINT"INDIAN ROPE RISES UP TO YOU":R1=1:A$(56)="END OF ROPE":H$(56)=A$(56):A(56)=-61:GOTO5000`
> **606** `IF E$="ANT" IF PT=1 IF A=59 THEN A=60:GOTO300 ELSE IF A=60 A=59:GOTO300`
> **605** `IF E$="OPE" IF R1=1 IF A=17 OR A=61 A=A+1:R1=0:IF A-1=17 THEN 8000 ELSE 300`

*crops:* `work/crops15/p2r_468_480_get/p2R_y0480_00.png`, `work/crops15/p4l_970_997/p4L_y0040_00.png`,
`work/crops15/p3l_600_618/p3L_y0255_00.png`.

- Fill the paper cup (48) at the cooler (58) → runtime item **57 = "CUP OF WATER"**.
- `POUR WATER` at the plant (59) with 57 → *"PLANT GROWS TO CEILING"*, plant becomes *"HUGE PLANT"*, `PT=1`.
- `CLIMB PLANT` (606) requires `PT=1`.
- `PLAY FLUTE` (990) at room 61 with the flute (50) → *"INDIAN ROPE RISES UP TO YOU"*, `R1=1`, and an
  *"END OF ROPE"* (56) appears at room 61; `CLIMB ROPE` (605) then takes you to 62 (`R1=0`).

**Confirms** the port's floor-2 chain end-to-end, including the item identities the audit could only infer.

---

## 6. Floor 5 — book before knit

> **696** `IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN R=1:GOTO4900`
> **970** `IF D(B)<>15 THEN 980 ELSE IF R=1 IF I(32)=1 IF I(33)=1 IF E$="IES" PRINT"YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT":FR=2:GOTO5000`
> **710** `IF A=42 IF FR=0 PRINT"SPRINKLER TURNED ON. FIRE OUT, BUT YOUR CLOTHES ARE VERY WET. YOU TAKE THEM OFF. YOU ARE NOW NAKED. ":FR=1:A$(57)="WET CLOTHES":H$(57)=A$(57):A(57)=-42:GOTO5000`

*crops:* `work/crops15/p3r_680_730/p3R_y0040_00.png`, `work/crops15/p3r_850_970/p3R_y0555_00.png`.

- **`R=1` is set at 696**: reading the BOOK (38) or the SMALL BOOK (52) sets it. This **closes** the audit's open
  item "R — where is it set?".
- **`KNIT` requires `R=1`** plus yarn (32) and needles (33) → *"YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT"*,
  `FR=2`. The book-read prerequisite is real in the source.

---

## 7. Other handlers read this round

| line | what it does |
|---|---|
| 465 | piano hands over runtime item **56 = "KEY"** in room 63 |
| 520 | DROP body — moves a carried item into the room |
| 540 | dropping the pill in the aquarium → sleeping piranha (`PF=1`) |
| 545 | the piranha devours Doberman Pinchen → dead piranha (`DP=1`) |
| 600 | GO handler; `X()` is the listing's AND; hazards at rooms 16/58/41/64/25 |
| 608 | `GO DOWN` at 34/36 → room −1 |
| 610 | `LEDGE` at 7 breaks (death); at 33/35 → +1 |
| 612 | `STAIRS` at 25/44/62 → +1 (44→45, 62→63) |
| 615 | locked doors 24/43/30/65; opening sets `G(digit)=1` |
| 617 | `SLIDE` at 57 → 58 (floor 3 → floor 2) |
| 625 | cabinet at 10 opens if `I(58)=1` |
| 660 | NOTE — *"IMPORTANT TV PROGRAM ON"* |
| 670 | SIGN — *"STRING COSTS $1.00"* |
| 680 | TV bulletin — *"POWER WILL BE SHUT OFF AT MIDNIGHT"* |
| 690 | clock — reports `INT(TM/2)` as the hour |
| 700 | `PUSH BUTTON` at 9 → elevator down |
| 730 | *"NOTHING HAPPENS"* |
| 810 | `GOTO730` |
| 830 | tape the wires (electrocuted / *"TAPED WIRES"*) |
| 835 | tie balloon to string → `BO=2` |
| 850 | light the flashlight (`DK=1`) |
| 900 | MAKE KEY at 19 → *"CRUDE KEY"* |
| 930 | GLUE the stair → `SC=1` |
| 950 | INFLATE the balloon → `BO=1` |
| 960 | SHOOT the gun at 35 → blanks → death |
| 980 | DRINK — turns Hyde back |
| 982 | DRINK the acid — turns you into Mr. Hyde |
| 993 | *"LIBERACE YOU'RE NOT!"* |

---

## Open after round 2

1. **`BR=1` set site** — where the "knows how to swim / walk a tightrope" flag is raised. Likely the READ handler
   between 690 and 696; the raster band was not fully legible.
2. **Line 800's trailing `ELSE` target** — `7100` (refuse) vs `805` (umbrella branch). Single-line high-zoom read.
3. **Line 618** — string clipped at the right margin (*"YOU STEP ON THE HAIR AND MIST…"*).
4. **Line 600's `E$` tokens** — `MAN` / `TOR` / `IRE` / `AND` uncertain at the current zoom.
5. **Line 970's `E$="IES"`** — uncertain; probably a three-letter noun suffix for KNIT.

None of these change a floor 1–5 outcome that the port currently implements; all are recorded as open rather than
guessed.
