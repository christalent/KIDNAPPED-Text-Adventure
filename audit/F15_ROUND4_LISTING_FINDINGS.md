# F15 Round 4 — Full-listing decode: verified source lines, corrected claims

Round 3 established the structural fact; round 4 turns it into source-confirmed
line evidence and corrects two claims this audit had made wrongly.

Method: `KIDNAPPED_OCR.txt` is the **complete** numbered BASIC listing of the
magazine program (744 numbered source lines; the raw file is the OCR text layer
of the scanned magazine pages, not a fragment). `ocrresolve.py` reconstructs the
*printed* line labels by a monotonic walk over the OCR rows, because the OCR
misprints some printed digits (printed `4` frequently reads as `1`; `8`/`5` as
`S`/`B`, `0` as `O`).

Two authorities, as always:
* **pixels (native 300-DPI raster)** = authority,
* **OCR text layer** = witness for structure and for text that is unambiguous.

Every line below is marked with its evidence class. Where OCR text is damaged,
the line is quoted with `[?]` at the damaged glyph rather than silently
normalized.

---

## 1. Corrected claim #1 — `BR`, not `R`, is the book-read flag

**Printed line 696** (READ handler), OCR text:

```
696 | IFE$="OOK"IFI(38)=1OR(I(52)=1)THENR=1:GOT04900
```

Pixel crop of the line tail (`work/crops16/p3r_670_700_BR/`, re-zoomed) reads
`R=1:GOTO4900`. The crop's left edge falls immediately before that token, so
the pixel evidence cannot distinguish `R=1` from `BR=1`.

The logical constraint decides it:

* `BR=1` is **read** in exactly two places in the whole listing —
  *printed 607* (floor-1 tightrope) and *printed 975* (floor-4 SWIM).
* No other line in the complete listing assigns `BR`.
* Line 696 is the only READ handler, and it is the line that sets a flag when
  a book is read (`I(38)` = book, `I(52)` = small book).

If 696 set a different flag, `BR` could never become `1`, and both the
tightrope and SWIM would be permanently unusable — the listing would contain
two dead gates, which the game's own room text contradicts. Therefore the
printed token at 696 is **`BR=1`**, and the `B` was lost to the OCR and
clipped by the crop edge.

**Verdict:** line 696 = `IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN BR=1:GOTO4900`
(evidence: OCR + pixel + logical constraint; certainty: **high**).

This closes the round-3 open question "which line sets the book-read flag".

## 2. Corrected claim #2 — `FR` is a three-state flag, not "naked = FR=1"

The legend groups `PM,FR,DP,PF,SC` as "monster or hazard flags (0 = active,
1 = absent)" — binary — yet `FR` takes the value `2` at printed line 970.
`FR` therefore carries **three** states, and the earlier reading "FR=1 means
naked" (from the floor-4/floor-5 round-2 notes) was wrong.

All three uses of `FR` in the complete listing:

**Printed 710** (PUSH handler, room 42):

```
710 | IFA=42 IFFR=0 PRINT"SPRINKLER TURNS ON. THE FIRE'S OUT. BUT YOUR CLOTHES
     | ARE ALREADY WET AND YOU TAKE THEM OFF. YOU ARE NOW NAKED.":FR=1
     | :A$(57)="WET CLOTHES":H$(57)=A$(57):A(57)=-42:GOTO5000
```
(message wording is OCR-damaged and partially reconstructed; certainty:
**medium** — the flag transitions `FR=0 → FR=1` and the item `WET CLOTHES`
(57) is placed at room 42 are **high**.)

**Printed 970** (KNIT handler):

```
970 | IFD(B)<>15 THEN 980 ELSE IFFR=1 IFI(32)=1 IFI(33)=1 IFE$="[?]ES"
     | PRINT"YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT":FR=2:GOTO5000
```

**Printed 975** (SWIM handler) — see §4.

So the state machine is:

| `FR` | meaning | evidence |
|---|---|---|
| `0` | pre-sprinkler (fire hazard active) | 710 test `IF FR=0` |
| `1` | post-sprinkler: naked, `WET CLOTHES` item exists | 710 assignment, 970 test |
| `2` | wearing the knitted suit | 970 assignment |

**Consequences for the port (must be fixed):**
* KNIT is gated on the *sprinkler* state, **not** on having read a book.
  The previous floor-5 note "`KNIT` requires `R=1` (book read)" is **wrong**
  and must not survive into the code.
* KNIT additionally requires `I(32)=1` (yarn) and `I(33)=1` (needles).
* The `E$` suffix test (`"[?]ES"`) is not yet resolved pixel-wise; the
  candidates are `LES` (NEEDLES), `HES` (CLOTHES) or `IES`. The OCR shows
  `IES`; `L`/`H` are the classic dot-matrix misreads of `I`. **Open.**

## 3. Line 800–810: the JUMP handler (three branches)

OCR structure, printed lines 800 / 805 / 810 (single OCR row wrapping all three):

```
800 | IF A=60 OR A=61 OR A=64 THEN 7100 ELSE IF A=34 OR A=36 IF I(25)=1
     | AND BO=2 THEN PRINT"BALLOON CARRIES YOU DOWN ONE FLOOR":A=43:GOTO8000
     | ELSE 7100 [?]
805 | IF I(39)=1 IF UM=1 THEN PRINT"YOU FLOAT DOWN ONE FLOOR":A=52:GOTO[?]
     | ELSE PRINT"UMBRELLA WASN'T OPEN!":GOTO7100
810 | GOTO730
```

* The umbrella branch requires **both** `I(39)=1` (carrying the umbrella) and
  `UM=1` (umbrella open). Certainty: **high**.
* The refusal text is `UMBRELLA WASN'T OPEN!` and it exits to `7100`.
  Certainty: **high** for the text; the `7100` target line itself is one of
  the open items in §6.
* **The final token of line 800 is unresolved** — `ELSE 7100` (refuse) vs
  `ELSE 805` (fall through to the umbrella branch) vs `ELSE 810` (→ 730,
  "NOTHING HAPPENS"). The pixel zoom of the row tail came back unreadable
  (`0 0 0E1 CETEA-240PA-2/TCI/25\-1A0C0-2TU`), and the earlier high-zoom
  crop of line 800 starts `IF A=60 OR A=61 OR A=64 THEN 7100 ELSE IF A=34 OR
  A=36 IF I(25)=1 AND BO=2 TH…`. **Open, and it matters**: it decides
  whether JUMP from the floor-4 umbrella rooms reaches the float branch at
  all.

## 4. Line 975: SWIM is asymmetric, and failing it is **death**

```
975 | IFSP=0THEN1000ELSEIFA=49THENA=48:GOTO300ELSEIFA=48IFBR=0THENPRINT
     | "YOU DON'T KNOW HOW TO SWIM!":GOTO7200ELSE A=49:GOTO4900
```

with

```
1000 | PRINT"YOU CAN'T DO THAT NOW.":GOTO390
7200 | PRINT"YOU SEEM TO HAVE GOTTEN YOURSELF KILLED!"
```

(The `7200` label is the OCR row `720 | 0 PRINT"Yoo SEEH TO HAVE GOTIEN
YIlRSElF KILlED!"` — the margin reads `720` and the code begins with `0
PRINT`, i.e. the printed label is **7200**.)

Source semantics, exactly:
* `SP=0` → "YOU CAN'T DO THAT NOW." (not a death).
* From room **49** → room **48**, unconditionally, no book required.
* From room **48** → **requires `BR=1`**; if `BR=0` → "YOU DON'T KNOW HOW
  TO SWIM!" → **GOTO 7200 = death**, not a refusal message.

This is asymmetric in a way the port's implementation is not; the port must
send 49→48, gate 48→49 on the book-read flag, and treat the failure as
fatal.

## 5. Other verified lines (OCR witness + context)

| printed | content | certainty |
|---|---|---|
| 390 | parser: `LOOK`→300, `" JUMP"`→800, `SWIM`→975, `WAIT`→1050; then 12 directions `B$(1..12)`, then ordinary verbs | high (pixel-verified earlier) |
| 600 | `IF D(B)<>3 THEN 620 ELSE IF((A=16)X(E$="MAN"))+((A=58)X(E$="TOR")) THEN 7000 ELSE IF((A=41)X(E$="IRE"))+((A=64)X(E="AND")) THEN 7200 ELSE IF A=25 AND E$="IRS" AND SC=0 PRINT"STEP IS MISSING! YOU FELL DOWN THE STAIRS":GOTO7200` | medium (four `E$` tokens still unconfirmed by pixels) |
| 607 | `IF E$="IPE" IF A=65 THEN A=64:GOTO300 ELSE IF RS=2 IF A=64 IF BR=1 THEN A=65:GOTO300 ELSE PRINT"YOU DON'T KNOW HOW TO WALK A TIGHTROPE":GOTO7200` | high (OCR + pixel) |
| 696 | `IF E$="OOK" IF I(38)=1 OR I(52)=1 THEN BR=1:GOTO4900` | high (§1) |
| 710 | sprinkler: `FR=0 → FR=1`, `A$(57)="WET CLOTHES"`, `A(57)=-42` | medium-high |
| 720 | `IF A=46 IF SP=0 PRINT"CLICK":SP=1:GOTO5000` | high |
| 730 | `PRINT"NOTHING HAPPENS":GOTO5000` | medium |
| 840 / 845 | floor-1 TIE/rope chain; TIE is **unconditional**; the tightrope gate lives at 607 | high (pixel-verified earlier) |
| 970 | KNIT: `FR=1` + `I(32)` + `I(33)` + `E$` → `FR=2`, "YOU HAVE KNITTED A FINE SUIT AND ARE WEARING IT" | high except the `E$` token |
| 975 | SWIM (§4) | high |
| 1000 | `PRINT"YOU CAN'T DO THAT NOW.":GOTO390` | high |
| 2100 / 2110 | `DATA` for the 27 ordinary verbs only | high |
| 690–700 | READ handler block; 696 sets the book-read flag | high |

## 6. Open items after round 4 (each needs a pixel read)

1. **Printed 800 final token** — `ELSE 7100` / `ELSE 805` / `ELSE 810`.
   Decides whether JUMP reaches the umbrella float branch.
2. **Printed 970 `E$` token** — `LES` (NEEDLES) / `HES` (CLOTHES) / `IES`.
3. **Printed 710 message wording** — the sprinkler sentence is OCR-damaged;
   only `FR=0 → FR=1`, `WET CLOTHES`, `A(57)=-42` are solid.
4. **Printed 7100** — the refusal target; its own text is unknown and the
   resolver's label walk slipped in the 7000-range (`720` vs `7200`).
5. **Printed 600's four `E$` tokens** (`MAN` / `TOR` / `IRE` / `AND`) — OCR
   witness only, no pixel confirmation yet.
6. **Printed 650** graffiti block — the strings are known from round-2 pixels
   (`GRAFFITI: DO YOU HAVE A SPLIT PERSONALITY?` for room 53,
   `WATCH OUT FOR LIVE ONES` for room 6) but should be re-confirmed as
   printed lines.

## 7. Port changes owed by this round

* `floors/floor_5.py` — KNIT gate: drop the book-read (`R=1`) prerequisite,
  require the sprinkler/`FR=1` state plus yarn plus needles; on success set
  the suit state (`FR=2`). Docstring currently states the wrong `R=1` rule.
* `floors/floor_4.py` — SWIM: 49→48 unconditional; 48→49 gated on the
  book-read flag; failure is **death** (`YOU DON'T KNOW HOW TO SWIM!`), not a
  refusal; `SP=0` → "YOU CAN'T DO THAT NOW."
* `floors/floor_3.py` — the floor-3 graffiti text is invented
  ("THE STEEL DOOR ONLY OPENS FOR THE STRONG MAN…"). The source string for
  room 53 is `GRAFFITI: DO YOU HAVE A SPLIT PERSONALITY?`
* `audit/FLOORS_1_5_SOURCE_HANDLERS.md` — remove the obsolete "`FR=1` = naked"
  reading and the "`KNIT` requires `R=1`" claim.
* `audit/F15_SOURCE_LINES.json` — merge the round-4 lines above.
