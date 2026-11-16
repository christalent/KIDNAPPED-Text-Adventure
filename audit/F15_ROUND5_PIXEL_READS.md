# F15 Round 5 - pixel reads for the six open items

Date: 2026-11-16
Authority: the native 300-dpi raster (`work3000/native/pgN.jpeg`). Every crop
below is cut from that raster by `open/mkcomp2.py` (see `open/CROP_MANIFEST.md`).
No OCR and no PDF text layer is used as authority. The OCR text layer appears
only as a **second witness** in the right-hand column, and every disagreement
is recorded rather than silently reconciled.

Method: each staged crop was transcribed verbatim from the dot matrix. A
transcription is reported as the pixels are read, including glyph-level noise
(the reader confuses `=` with `:`, `OR A` with `RA`, and the digit `8` with
the letter `B` in this face). Where a token is ambiguous to the reader but
resolvable from the listing's own logic, that is called out explicitly and
marked as a second-step inference, not as a pixel read.

## 1. Reads performed this round

| crop | printed line | pixel transcription (verbatim) | second witness (OCR text layer) | note |
|---|---|---|---|---|
| `open/lines/3R_970.png` | 970 | `IF D(B)<>15 THEN 980 ELSE IF FR=1 IF I(32)=1 IF I(33)=1 IF E$="HES" PRINT` | locator: `... IF E$="IES" ...` | **HES** (see section 2) |
| `open/lines/3L_600.png` | 600 | `IF (B)<>3 THEN 620 ELSE IF ((A=16)X(E$="MAN"))+((A=58)X(E$="TOR"` | locator: `... THEN 7000 ELSE IF ((A=1) I(E$="IRE")) + ((A=61) I(E$="AN")) THEN 7200` | MAN, TOR confirmed; IRE, AND still open |
| `open/lines/3L_650.png` | 650 | `IF D(B)>5 THEN 700 ELSE IF S="ITI" IF A=6 THEN PRINT"GRAFFITI! WATCH` | locator: `650 ...` | E$="ITI", A=6, message head confirmed; tail open |
| `open/lines/3L_617.png` | 617 | `IF$="IDE" IF A=57 PRINT"YOU SLIDE THROUGH HOLE IN FLOOR":A=58` | - | new: this line was never read before |
| `open/lines/2R_465.png` | 465 | `IF A=63 IF$="KEY" PRINT"WE ALL KNOW PIANOS HAVE KEYS":J=56:A$(` | - | GET-region piano key body |
| `open/lines/2R_474.png` | 474 | `IF E$="OOK" PRINT"TITLE OF BOOK; HOW TO ";;IF A=47 THEN PRINT"SHI` | - | GET-region book title |
| `open/lines/4L_985.png` | 985 | `IF D(B)<>19 THEN 990 ELSE IF A=59 IF E$="TER" IF I(57)=1 PRINT"PLANT GR` | - | PLAY/POUR plant |
| `open/lines/4L_990.png` | 990 | `IF D(B)<>20 THEN 995 ELSE SET IF S="UTE" IF A=61 IF I(50)=1 IF R1=0 PRINT"IN` | - | PLAY/POUR flute |

Reads attempted but not completed this round: `open/lines/3L_616.png` (tool
read budget exhausted), `open/band/3R_800_810_jmp.png` (transcription returned
but was not captured), `open/comp/c_3R_670_700.png` (transcription returned
but was not captured).

## 2. Resolutions

### R5-2 - printed 970 E$ token: **HES** (closed)

The pixel read of line 970 gives `IF E$="HES"`. The OCR text layer gives
`IES`. The pixel wins, and the listing's own logic corroborates it: `E$` is
the last three characters of the object, and the only object the source
accepts is CLOTHES, whose last three characters are HES. `LES` (NEEDLES) and
`IES` are the classic dot-matrix misreads of the same three glyphs - exactly
the ambiguity recorded in round 4.

Corroborating detail from the same read: line 970's gate is
`IF D(B)<>15 THEN 980 ELSE IF FR=1 IF I(32)=1 IF I(33)=1 IF E$="HES" PRINT`,
i.e. FR=1 (the sprinkler has run) plus needles and yarn. The reader's `8` is
the letter `B` in `D(B)`.

**Port consequence:** the KNIT handler must accept only an object whose last
three characters are `HES`. The port previously accepted any noun containing
`CLOTH`, which also admits `CLOTH` and `CLOTHS`. See section 3.

### R5-5 - printed 600 E$ tokens: MAN, TOR confirmed (partially closed)

The pixel read of the first visual row of line 600 gives
`IF ((A=16)X(E$="MAN"))+((A=58)X(E$="TOR"`. The OCR witness for the wrapped
continuation of the same line gives
`IF ((A=1) I(E$="IRE")) + ((A=61) I(E$="AN")) THEN 7200`. Two of the four
three-character object fragments are now pixel-confirmed (`MAN`, `TOR`);
`IRE` and `AND` still need a pixel read of the continuation row of line 600.

### R5-6 - printed 650 graffiti block: head confirmed (partially closed)

The pixel read of line 650 gives `IF E$="ITI" IF A=6 THEN PRINT"GRAFFITI! WATCH`.
The `E$="ITI"` fragment is GRAFFITI, the room test is A=6, and the message
begins `GRAFFITI! WATCH`. The remainder of the message is outside the staged
crop and is still open.

### R5-1, R5-3, R5-4 - still open

* **R5-1** printed 800 final token (`ELSE 7100` / `ELSE 805` / `ELSE 810`):
  the head of line 800 is pixel-read (`IF A=60 OR A=61 OR A=64 THEN 7100 ELSE
  IF A=34 OR A=36 IF I(25)=1 AND BO=2 TH...`), the tail is not. The OCR
  locator shows a fragment `ELSE 7100` following line 800's fragment, which is
  suggestive but the OCR text layer is not authority and that fragment may
  belong to a neighbouring line. Needs the pixel read of the tail of the 800
  row: `open/band/3R_800_810_jmp.png`.
* **R5-3** printed 710 message wording: not read this round.
* **R5-4** printed 7100 target text: not read this round.

## 3. Port change made from the pixels

`floors/floor_5.py`, `_v_knit`: the source gate at printed 970 is
`IF E$="HES"`. The port accepted any noun containing `CLOTH`, which admits
objects the source rejects. Tightened to the source-exact test (last three
characters `HES`).


### Discrepancy found while checking the port (floor 9 graffiti)

`floors/floor_9.py` returns the graffiti text as `'WATCH OUT FOR LIVE ONES'`
- with a stray apostrophe at each end, and no `GRAFFITI! ` prefix. The pixel
read of printed 650 gives `... IF E$="ITI" IF A=6 THEN PRINT"GRAFFITI! WATCH`,
so the source prints a string that **starts** `GRAFFITI! WATCH`. The port
string therefore does not match the source head, and the round-2 tail
`WATCH OUT FOR LIVE ONES` is not re-confirmed by any pixel read on record.

This is **not** changed in this round: the crop is truncated mid-string, so
the tail cannot be adjudicated from pixels. Left as an open item rather than
guessed. Needs a wider crop of the printed-650 row.

## 3b. Port change: test status

The `_v_knit` gate change was run against `tests/` with `/usr/bin/python3
-m pytest -q tests/` (the `archive/` directory holds stale attempt snapshots
and is not part of the suite).

Result: **101 passed, 1 collection error** - `ERROR
tests/test_navigation.py::test_floor`. That error is **pre-existing**: the
same 101-pass/1-error result appears with this change reverted
(`git checkout -- floors/floor_5.py`) and with it applied. Nothing in this
round introduced or fixed it.

## 4. What is still owed

| item | next artifact to read |
|---|---|
| R5-1 | `open/band/3R_800_810_jmp.png` (tail of the 800 row, lines 805/810) |
| R5-3 | line 710 crop on page 3 right column (sprinkler message) |
| R5-4 | line 7100 crop (refusal target text) |
| R5-5 | continuation row of printed 600 (`IRE`, `AND`) |
| R5-6 | tail of the 650 message row |
| Q1/Q2/Q3 remaining | `open/lines/3L_616.png`, `open/lines/2R_461.png` |
| Q5 | `open/comp/c_3R_670_700.png` re-read (printed 696, BR set by READ BOOK) |
| floor 9 graffiti | wider crop of printed 650 - source head is `GRAFFITI! WATCH`, port prints `'WATCH OUT FOR LIVE ONES'` |
