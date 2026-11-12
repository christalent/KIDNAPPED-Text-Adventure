# DATA rows 2000-2040 - item table

**Pixel-verified** for rows 2030 and 2040 (500 dpi crop of page 4 right column).
Rows 2000-2020 are from the PDF text layer and still need a raster confirm.

| line | items | contents |
|---|---|---|
| 2000 | 16 | `PAPER TABLE,-2,DESK,-2,CHAIR,2,LONG BROOM,3,TV SET,-` |
| 2010 | 9 | `DESK,-17,KEY MAKING MACHINE,-19,STRING GLASS,20,...` |
| 2020 | 11 | `LOCKED DOOR,-30,GUN,30,SIGN ON WALL,-32,STRING VENDOR,...` |
| 2030 | 10 | `PUSH BUTTON ON WALL,-46,BOOK,47,MARY POPPIN'S UMBRELLA,50,OPEN WINDOW,-51,GRAFFITI ON WALL,-53,SMALL KEY,37,STEEL DOOR,-55,JAR OF YELLOW SOLUTION,56,JAR OF FLUID,56,CHILD'S SLIDE,-57` |
| 2040 | 9 | `WATER COOLER,-58,PAPER CUP,58,SMALL-SIZED PLANT,-59,FLUTE,61,STAIRS,-62,SMALL BOOK,64,PIANO,-63,LONG ROPE,63,FRONT DOOR,-65` |

## Findings

- The DATA table **ends at line 2040**. There are no lines 2050 or 2060; the region
  between the 2030 and 2040 rows on page 4 right column is a full-page illustration,
  not code. The last item is `FRONT DOOR,-65`, i.e. room 65 exists.
- The PDF text layer reports the 2040 row as `2010` (the 4->1 error again), so the text
  layer appears to contain **six** DATA rows for **five** logical rows. Anyone counting
  items from the text layer double-counts row 2040.
- Item count from the rows: 16 + 9 + 11 + 10 + 9 = **55 items**, and the READ loop
  reads exactly 55. The two agree.
- The item loop is `FOR A=1 TO 55: READ A$(A): READ A(A): H$(A)=A$(A):NEXT` - pixel-verified at
  900 dpi. The bound is **55**, not 58, and it matches the 55 DATA items exactly. There is
  therefore no unfilled slot and no missing item. The DOLLAR is a 56th, run-time-created
  item (see below), which is why `K3=56` refers to it.

## Line 467 - where the DOLLAR comes from

Pixel read (500 dpi crop, page 2 right column):

```
467 IFA=35IFE$="PER"OR(E$="LAR"ORE$="NEY")X(I(27)=0)THENPRINT"YOU GET TOO CLOSE TO HIM,
HE JUMPS AND STRANGLES YOU.":GOTO7300ELSEIFI(27)=1PRINT"KIDNAPPER SEES YOUR GUN AND FREEZES
YOU GRAB A DOLLAR":A$(56)="DOLLAR":H$(56)=A$(56):A(56)=35:PM=1:E$="LAR"
```

So the DOLLAR is **not** a DATA item. Line 467 creates it at runtime: `A$(56)="DOLLAR"`
with `A(56)=35` places it in room 35 (THE VAULT). `E$` holds the last 3 letters of the
command, so `"LAR"` matches GET DOLLAR, `"NEY"` matches GET MONEY, `"PER"` matches GET PERSON.
`I(27)` is the GUN (item 27).

This resolves the OPEN_QUESTIONS candidate in favour of the runtime-created reading, but
one tight crop is still wanted: the `IFA=7` / `IFA=58` pair on line 468 cannot both hold, so
one of those digits is damaged.

## Lines 1100-1210 - subroutines

Pixel read (500 dpi crop, page 4 left column):

```
1100 FORK2=1TO7:IFC$(K2)=H$(K3)THENC$(K2)=R$:GOSUB1150:RETURNELSENEXT:RETURN
1150 IFR$="":I(K3)=0
1160 RETURN
1200 FORK2=1TO58:IFA$(K2)=H$(K3)THENA$(K2)=M$:H$(K3)=M$:IFM$<>""THENRETURN...:A(K2)=0:I(K3)=0
```

This confirms the roles inferred in OPEN_QUESTIONS.md:

- **1100/1150/1160** = 'set item text'. It scans the `C$` command array for an entry equal
  to `H$(K3)`, overwrites that entry with `R$`, and calls 1150, which clears `I(K3)` when
  `R$` is empty. That is the mechanism behind the GOSUB1100 at line 835 consuming the string.
- **1200** = 'vanish item'. It scans the `A$` item array for `H$(K3)`, overwrites it with
  `M$`, copies `M$` into `H$(K3)`, and zeroes the item. That is the mechanism behind the
  GOSUB1200 at line 550 making the DOLLAR disappear.

Unresolved in this read, both needing one tight crop each:

1. the loop bound on 1100 reads `1TO7` in both the text layer and the raster, but a 7-slot
   scan cannot reach item 48/57 - either it is `1TO78` or the array is bigger than assumed.
2. the tail of 1200 (`IFM$<>""THENRETURN...:A(K2)=0:I(K3)=0`) is damaged in the raster.

## Open items still requiring a raster crop

1. ~~the READ-loop bound~~ - RESOLVED: `FOR A=1 TO 55`
2. line 1100's loop bound - the raster reads `1TO7`; the text layer agrees. Still open:
   7 command slots looks small, so 1100 may scan a short command list rather than the
   full 39-entry command array. Needs the handler pages to interpret.
3. the tail of line 1200 - the raster reads `IFM$<>""THENRETURNEI SE0(K2)=0:T(K3)=0`,
   i.e. `IF M$<>"" THEN RETURN: ... A(K2)=0:I(K3)=0` with the middle damaged
4. ~~listing line 74~~ - RESOLVED: `74 PRINTJ$:W=63:GOTO350`
5. ~~listing lines 33 and 34~~ - RESOLVED: `33 PRINT"IN A SMALL STORAGE ROOM.":W=22:GOTO350`
   and `34 PRINTJ$:W=18:GOTO350`
6. line 468's `IFA=7` / `IFA=58` pair

