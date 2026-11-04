# OCR vs PIXELS -- source-correction log (2026-11-04)

Subject: the SoftSide Dec-1980 *KIDNAPPED!* listing (Vol.3 No.03), scanned as
`KIDNAPPED_Original.pdf` in this repo.

## Method
1. Native 300 ppi render of each PDF page (`pdftoppm -r 300 -gray`).
2. Focused crops of the disputed tokens, read at magnification.
3. Cross-read against two independent OCR passes of the same listing:
   - the PDF's embedded text layer (`KIDNAPPED_OCR.txt`)
   - Archive.org `SoftSide_27_Vol_3-03_1980-12_Kidnapped_djvu.txt` (same magazine scan)
   - Archive.org SoftSide issue 34 (Jul-1981 Apple/Atari re-listing of the program)
4. Where the audit re-lists a token in a room whose module is already audited in this
   repo, the module was used as an independent third witness.

## The systematic corruption
The print is degraded and both OCR passes read the digit **4 as 1**.
`FLOOR9_GROUND_TRUTH.md` already proved it on the map lines
(line 23: OCR `W=11` vs pixels `W=14`; line 25: `E=11` vs `E=14`; line 28: `E=21` vs `E=24`).
The same repair is required in the DATA rows, where it changes e.g.
`KNITTING NEEDLES,10` -> `,40`, `LOCKED DOOR,-13` -> `,-43`, `STAIRS,-11` -> `,-44`,
`SMALL BOOK,61` -> `,64`, `AQUARIUM,-11` -> `,-14`, `PUSH BUTTON ON WALL,-16` -> `,-46`.

## Token-by-token

| # | passage | OCR reading | pixel / 2nd-listing reading | verdict |
|---|---|---|---|---|
| 1 | floor 9 room 6 graffiti (listing line 650) | `MATCH WT FOR LIVE INMATES` (BAS), `MATCH WIT FOR LIVE WIRES.` (repo) | `WATCH OUT FOR LIVE ONES` | **FIXED** in `floors/floor_9.py` + `KIDNAPPED.BAS` |
| 2 | second graffiti literal (line 650, A=53) | `DO YOU HAVE A SPLIT PERSONALITY?` | same, plus Jul-1981 re-listing `GRAFFITI; Do you have a split personality` | confirmed, unchanged |
| 3 | DATA 2000, broom | `BROOM`,4 (BAS) | `LONG BROOM`,3 | **confirmed 3**; broom stays on floor 9 room 3 (user verified in play) |
| 4 | DATA 2000, aquarium | `ADMISSION`,-11 (BAS) | `AQUARIUM`,-14 | **FIXED** to -14 (matches audited floor 8 room 14) |
| 5 | DATA 2000, elevator button | `PUSH BUTTON`,-9 (BAS) | `DOWN BUTTON`,-9 | **FIXED** (audited floor 9 room 9) |
| 6 | DATA 2000, live wires | `TWO 'LIVE' WIRES`,-11 (BAS) | `ENDS OF 2 'LIVE' WIRES`,-11 | **FIXED** (audited floor 9 room 11) |
| 7 | DATA 2020 row | `LOCKED ~,-13 ... NEEDLES,10 ... -12 ... STAIRS,-11` | `LOCKED DOOR,-43 ... NEEDLES,40 ... -42 ... STAIRS,-44` | **FIXED** in transcription file |
| 8 | DATA 2030 row | `BOOK,~7 ... -16` | `BOOK,47 ... PUSH BUTTON ON WALL,-46` | **FIXED** in transcription file |
| 9 | DATA 2040 row | `SHALL BQOK,61` | `SMALL BOOK,64` | **FIXED** in transcription file |
| 10 | DATA 2040, BAS row was empty | `10040 DATA"",0` | real 2040 row present in the listing | **FIXED** in transcription file |
| 11 | item name `KEY ON A KEY CHAIN` (BAS) | KEY ON A KEY CHAIN | `KEY MAKING MACHINE` | **FIXED** in transcription file |
| 12 | item name `THICK CURTAIN SHEET` (BAS) | CURTAIN | `COPPER` | **FIXED** in transcription file |
| 13 | `TIN FOIL`,-33 (BAS) | TIN FOIL | `OPEN WINDOW`,-33 | **FIXED** in transcription file |
| 14 | `GOLD'S SLIDE` (BAS) | GOLD'S | `CHILD'S SLIDE` | **FIXED** in transcription file |
| 15 | `EVERY PUPIL'S LAMP`,50 (BAS) | EVERY PUPIL'S LAMP | `MARY POPPIN'S UMBRELLA`,50 | **FIXED** in transcription file |
| 16 | DATA 2010 row, `LOCKED DOOR` room | -21 | Jul-1981 re-listing: `LOCKED DOOR, -24` | **RESOLVED -24** -- second listing agrees with the 4->1 repair |

## Still open (marked UNRESOLVED, not guessed)
- The item lists for source rooms 18-25 (floor 7) and 45-52 (floor 4) are UNRESOLVED here:
  floors 7 and 4 are still on stale room IDs in this repo, so their DATA rows have not
  been reconciled yet.
- The 2010-row "LOCKED DOOR" room is now resolved to -24 (row 16 above); the remaining
  2000/2010 items are confirmed by the audited floor 8/9 modules.

## What was NOT changed
- The broom stays on floor 9 room 3 (source `LONG BROOM`,3; both listings agree; user
  completed floor 9 in play).
- `KIDNAPPED_OCR.txt` is left untouched on purpose: it is the raw evidence layer.
  Corrected readings live in `KIDNAPPED_SOURCE_CORRECTED.txt`.
- `KIDNAPPED.BAS` DATA rows were **not** rewritten wholesale -- that file is a
  hand-transcribed, structurally different artifact; the corrected rows are published
  separately and the BAS now carries a header pointing at them.
- Floors 1-7 code untouched except the floor 9 graffiti string; floors 7, 5, 4, 3, 2, 1
  still carry stale room IDs and are rewritten floor-by-floor (floor 6 is next).

## Artifacts
- `KIDNAPPED_SOURCE_CORRECTED.txt` -- corrected source transcription with confidence tags
- `KIDNAPPED_OCR.txt` -- untouched raw OCR
- `FLOOR9_GROUND_TRUTH.md`, `FLOOR9_AUDIT_2026-11-03.md` -- floor 9 audit
