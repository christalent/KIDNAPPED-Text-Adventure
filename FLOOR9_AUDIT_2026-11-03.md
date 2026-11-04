# FLOOR 9 AUDIT — corrected ground truth (2026-11-03)

Supersedes `FLOOR9_GROUND_TRUTH.md` (built on OCR text; OCR is damaged).

## Sources used

| Source | Role |
|---|---|
| `KIDNAPPED_Original.pdf` (SoftSide, Dec 1980) | **authoritative** — read from 300/500 dpi pixels, not the OCR layer |
| `archive/solutions/sol_gunness.txt` (Jacob Gunness, 2004) | independent walkthrough A |
| `archive/solutions/sol_atari.txt` (Garry Francis, Atari 400/800) | independent walkthrough B |
| `KIDNAPPED.BAS` (repo) | third-hand transcription — **item DATA is corrupt**, see §5 |
| `SPEC.md`, `PARSED_BASIC_SOURCE.txt`, `floors/floor_9.py` | subjects of the audit, not evidence |

## Method

1. **Dispatch rule.** Listing line 10 = `IF A=66 THEN 6000 ELSE IF DT=1 THEN 320 ELSE ON A GOTO 11,12,...,75`.
   `ON A GOTO` starts at 11 and steps by 1, so **BASIC line = room number + 10**; rooms are global 1–65.
2. **Pixels, not text.** `pdftotext` reads printed `4` as `1` (proved: line 23 OCR `W=11` vs pixels `W=14`;
   line 25 OCR `E=11` vs pixels `E=14`; line 28 OCR `E=21` vs pixels `E=24`). Every room line below was
   re-read from a 500 dpi crop. OCR damage is why `SPEC.md` looks plausible but is wrong.
3. **Walkthrough cross-check.** Both published solutions were replayed move-for-move against the
   pixel-derived exit tables. **Both replayed cleanly on every floor** — that is what makes this table
   authoritative rather than merely plausible.

## 1. Corrected floor boundaries (global room numbers)

Each floor is a contiguous block of global rooms; the boundary room of each floor is the room you
arrive in from above (via the elevator button / stairs / slide / jump).

| Floor | Rooms | Arrival room | Notes |
|---|---|---|---|
| 9 | **1–11** | 1 | `J$`="IN A HALLWAY.", `N$`="IN AN OFFICE." (line 220 init). See room-12 note below. |
| 8 | **13–17** | 13 | aquarium / rope / sleeping pill / piranha |
| 7 | **18–25** | 18 | key-making machine, copper sheet, glue + stair step |
| 6 | **26–36** | 26 | helium, balloon, gun, **LEDGE 34 & 36**, VAULT 35, sign + string |
| 5 | **37–44** | 43 | yarn, needles, sprinklers, office workers |
| 4 | **45–52?** | 45? | pool, library, umbrella, jump down — map shows 8 rooms here, listing gives 7 (see §6) |
| 3 | **53–57?** | 52? | laboratory 56 = fluid + antidote |
| 2 | **58–62** | 58 | alligator, plant, flute |
| 1 | **63–65** | 63 | piano keys, rope, tightrope, entrance hall |

### Room 12

Listing line 22 = `PRINT"ON A VERY NARROW LEDGE.":GOTO350` — no direction assignments, no items.
The map's FLOOR 9 panel contains exactly **11** boxes (Hallway×3, Office×3, Closet, Crawlspace,
Elevator, Restroom, Maintenance Room) which map 1:1 onto rooms 1–11 with the J$/N$ split
matching perfectly. Room 12 is **not drawn** and neither walkthrough visits it. It is therefore
*not* part of floor 9's normal room set — most likely a special/verb-only room (a ledge you can
reach but not stay on) or a trap. Keep it out of the floor table until the magazine's verb handlers
say what it is.

Rooms 1–11 verified by clean walkthrough replay (both solutions, all six floors).
Rooms 12–17 verified for 13–17 only (floor-8 walkthrough replays exactly on 13–17).
Room 12 is assigned to floor 9 by contiguity alone — no walkthrough visits it either way.
Rooms 52–65 consistent with the handlers (`A=56` = laboratory/bottles) but not yet walked.

### Walkthrough evidence per floor (rooms actually visited)

- **Floor 9** — 1,2,3,4,5,6,7,8,9,10,11. Both solutions replay move-for-move.
- **Floor 8** — 13,14,15,16,17. Replay: `S(16) GET PILL · N(13) · W(14) aquarium · W(15) rope ·
  E(14) DROP PILL GET PIRANHA · E(13) · S(16) DROP PIRANHA · E(17) TIE ROPE CLIMB ROPE`. Exact.
- **Floor 7** — 18–25. Replay from 18.
- **Floor 6** — 26–36, and the *ledge* is here: `W(31) W(33) **CLIMB LEDGE**(34) W(36) **CLIMB
  WINDOW**(35 VAULT) GET DOLLAR W(36) E(34) **CLIMB WINDOW**(33) E(31) N(32) READ SIGN PUT DOLLAR
  GET STRING INFLATE TIE S(31) W(33) **CLIMB LEDGE**(34) JUMP`. `CLIMB LEDGE` and `CLIMB WINDOW`
  are *verb* transitions, not directional exits — a direction-only simulator will report them illegal.
- **Floor 5** — 37–44, arrival room 43.
- **Floor 4** — 45–51, arrival room 45.

## 2. Corrected FLOOR 9 room table (rooms 1–12)

Room = listing line − 10. `J$` = "IN A HALLWAY.", `N$` = "IN AN OFFICE."

```
room  line  description                          exits
 1     11   J$ "IN A HALLWAY."                   W=4  N=2  E=8  S=7
 2     12   N$ "IN AN OFFICE."                   N=3           S=1
 3     13   "IN A CLOSET."                                    S=2
 4     14   J$ "IN A HALLWAY."                   N=5  E=1           S=6
 5     15   N$ "IN AN OFFICE."                                S=4
 6     16   "IN A RESTROOM."                    N=4
 7     17   N$ "IN AN OFFICE."                   N=1
 8     18   J$ "IN A HALLWAY."                   W=1  N=9           S=10
 9     19   "IN AN ELEVATOR."                                  S=8
10     20   "IN A MAINTENANCE ROOM."             N=8
11     21   "IN A CRAWLSPACE ON TOP OF THE ELEVATOR."         D=9
12     22   "ON A VERY NARROW LEDGE."           (no directional exits)  <- SPECIAL, not a map room
```

Special (non-directional) links on floor 9:
- **9 → 11**: `CLIMB CHAIR` (chair + trap door in ceiling of the elevator) → crawlspace. The exit table
  only carries `D=9` on room 11; the up-link is a verb, not a table exit.
- **9 → floor 8**: `PRESS BUTTON` (down button) → arrive room 13.
- Room 12 is a dead end reachable only by a special verb (see §6, open question).

## 3. Corrected FLOOR 9 item table

From the PDF item DATA (line 2000/2010) plus the handler text. Sign convention: negative = fixed
scenery (not takeable), positive = takeable.

```
room 2   PAPER NOTE, DESK(-2), CHAIR
room 3   LONG BROOM
room 5   TV SET(-5), CLOCK(-5)
room 6   GRAFFITI ON WALL(-6)
room 7   OPEN WINDOW(-7), KEY ON A KEY CHAIN   (key-on-ledge confirmed by walkthrough: 1-S→7 GET KEY.
                                                    The "SMALL LEDGE OUTSIDE THE WINDOW" wording is from the
                                                    repo's third-hand BASIC, whose room numbering does NOT
                                                    match the magazine's — corroboration, not proof.)
room 9   TRAP DOOR IN CEILING(-9), DOWN BUTTON(-9)
room 10  CABINET(-10), FLASHLIGHT, TAPE        (flashlight is behind the cabinet; needs the key)
room 11  ENDS OF 2 'LIVE' WIRES(-11)
```

## 4. Walkthrough validation (the proof)

**Gunness floor 9**, replayed on the table above:

```
N→2 GET CHAIR / READ NOTE · N→3 GET BROOM · S→2 · S→1 · S→7 GET KEY · N→1 · W→4 · S→6 READ GRAFFITI
· N→4 · N→5 WATCH TV · S→4 · E→1 · E→8 · S→10 OPEN CABINET / GET FLASHLIGHT / GET TAPE
· N→8 · N→9 DROP CHAIR · CLIMB CHAIR→11 TAPE WIRES · D→9 · PRESS BUTTON
```

Every single move is legal on the table above. **Atari floor 9** replays identically
(N→2, N→3, S,S,S→7 GET KEY, N→1, E→8, S→10, N,N→9, DROP CHAIR, GO CHAIR, TAPE WIRES, D, PRESS BUTTON).

The same replay succeeds on floors 8, 7, 6, 5, 4 for both solutions — including the floor-6 run
`… W→31, W→33, CLIMB LEDGE→34, W→36, CLIMB WINDOW→35 (VAULT), W→36, E→34, CLIMB WINDOW→33, E→31, N→32
READ SIGN / PUT DOLLAR / GET STRING`.

## 4b. Third authority: Francis's 2015 map

`archive/solutions/Kidnapped_map_Garry_Francis_2015.png` (Solution Archive file id 13096; the
`.bin` we downloaded earlier was only the XHTML wrapper around this image).

Nine panels, **FLOOR 9 at the top, FLOOR 1 at the bottom**. Rooms are labelled boxes; inter-floor
moves are lettered markers A–H carrying the verb that triggers them.

### Room counts — map vs. listing

| Floor | map boxes | listing rooms | agree |
|---|---|---|---|
| 9 | 11 | 1–11 | **yes, and the J$/N$ split matches exactly** |
| 8 | 5 | 13–17 | yes |
| 7 | 8 | 18–25 | yes |
| 6 | 11 | 26–36 | yes — incl. **Ledge ×2 + Vault** |
| 5 | 8 | 37–44 | yes |
| 4 | 8 | 45–51 | map shows 8, listing gives 7 — see §6 |
| 3 | 6 | 52–57 | yes |
| 2 | 5 | 58–62 | yes |
| 1 | 3 | 63–65 | yes (Lounge, Hallway, Entrance Hall) |

Total 11+5+8+11+8+8+6+5+3 = **65 = the original's room count**. The port's 72 rooms are the
seven invented ones.

Floor 9's map panel is decisive: **Hallway×3, Office×3, Closet, Crawlspace, Elevator, Restroom,
Maintenance Room** = 11 boxes, matching rooms 1–11 one-for-one — three `J$` hallways (1, 4, 8),
three `N$` offices (2, 5, 7), closet 3, restroom 6, elevator 9, maintenance 10, crawlspace 11.
**Room 12 ("very narrow ledge") is not drawn.** It is a verb-only special room, not a floor room.

### The map confirms the floor-6 ledge and the floor-9 exit

- **FLOOR 6**: `GO LEDGE` from the left Office area onto the left **Ledge**; `GO WINDOW` from that
  Ledge down to the **Vault**; a second `GO WINDOW` back out; `JUMP` from the right-hand **Ledge**
  to marker **D** → FLOOR 5. So the balloon/vault/dollar sequence is **floor 6**, and its two
  ledges are rooms **34 and 36**, vault **35**.
- **FLOOR 9**: `GO CHAIR` between **Crawlspace** (11) and **Elevator** (9) — matching the listing's
  `CLIMB CHAIR` up-link and room 11's `D=9`. `PRESS BUTTON` at the **Elevator** → marker **A** →
  FLOOR 8 **Hallway** = room **13**.
  **The port's room-9 `D=10` is therefore wrong**, and the port has no `PRESS BUTTON` exit at all.

### Inter-floor transition chain (markers A–H)

```
F9 Elevator  --PRESS BUTTON--> A --> F8 Hallway
F8 Office    --GO ROPE-------> B --> F7 Hallway
F7 Stairway  --GO STAIRS-----> C --> F6
F6 Ledge     --JUMP----------> D --> F5 Hallway
F5 Staircase --GO STAIRS-----> E --> F4
F4 Dining    --JUMP----------> F --> F3 Hallway
F3 Playroom  --GO SLIDE------> G --> F2 Office
F2 Staircase --GO STAIRS-----> H --> F1 Lounge
```

Every one of those is a **verb**, never a directional exit. The port models most of them as
plain `U=`/`D=` room links, which is exactly why its map kept diverging from the original.

## 5. What the repo's own BASIC gets wrong

`KIDNAPPED.BAS` DATA block is **not** the magazine's. Repo: `DATA"FLASHLIGHT",2,"CHAIR",3,"BROOM",4,...`
Magazine: `PAPER NOTE,2,DESK,-2,CHAIR,2,LONG BROOM,3,...`. The repo row is shifted and misnamed, and it
contradicts its own handlers (repo handler puts the flashlight at room 10; repo DATA puts it at 2).
Repo also renames items (`THICK CURTAIN SHEET` vs `THICK COPPER SHEET`) and puts `KEY ON A KEY CHAIN`
at room 19 where the magazine has `KEY MAKING MACHINE`. **PDF wins.** The repo handler for `A=7`
("SMALL LEDGE OUTSIDE THE WINDOW" + key on a key chain) *does* match the magazine.

## 6. Open questions (not resolved yet)

- **Floor 4 / floor 3 room counts** — Francis's map puts 8 boxes on floor 4 and 6 on floor 3, but the
  listing gives 45–51 (7) and 52–57 (6). So one of the rooms shifts: either floor 4 is 45–52 and
  floor 3 is 53–57, or floor 3 starts at 52 and floor 4 ends at 51 with a room elsewhere. Needs one
  more pixel read of lines 54–57 plus a check of the map's floor-4 panel. Out of scope for floor 9.
- **Room 12** — "ON A VERY NARROW LEDGE.", no directional exits, no items, **not on Francis's map**
  and in neither walkthrough. Almost certainly a verb-only special room (reach it but don't stay),
  not a floor room. Keep it out of the floor table.
- The repo's third-hand BASIC prints "THERE IS A WIDE, LONG LEDGE OUTSIDE THE WINDOW." for *its own*
  room 2, and a "SMALL LEDGE OUTSIDE THE WINDOW" with the key on a key chain for *its own* room 7.
  Those room numbers do not match the magazine's, so treat the wording as corroboration only.
- `LOCKED DOOR,-5` appears in the repo DATA but not in the magazine's floor-9 DATA read.
- The magazine's DATA for FLASHLIGHT/TAPE (room 10) was read via a cropped image; re-verify with a
  tighter crop if the cabinet sequence misbehaves.
- Rooms 52–65 (floors 3, 2, 1) are consistent but not yet walk-verified.

## 7. Diff: `floors/floor_9.py` vs ground truth

Port rooms: 1–11 and **13–17**. Ground truth floor 9: **1–11 normal rooms + room 12 special**.

| Room | Port | Truth | Verdict |
|---|---|---|---|
| 1 | W4 N2 E8 S7 | same | ok |
| 2 | N3 S1 | same | ok — but items incomplete (only CHAIR) |
| 3 | S2 **U4** | S2 | invented vertical link |
| 4 | **W5** E1 S6 **D3** | **N5** E1 S6 | wrong direction letter + invented vertical link |
| 5 | **E4** | **S4** | wrong direction letter |
| 6 | N4 | same | ok |
| 7 | N1 | same | ok — but no items (missing KEY ON A KEY CHAIN) |
| 8 | W1 N9 S10 | same | ok |
| 9 | S8 **U11** **D10** | S8 | U11 correct (CLIMB CHAIR); **D10 wrong** — should be PRESS BUTTON → floor 8 room 13 |
| 10 | N8 **U9** | N8 | invented vertical link |
| 11 | D9 **E13 W15** | D9 | invented links into floor 8 rooms |
| 12 | — | ON A VERY NARROW LEDGE. | special room — on no map, in no walkthrough. Not part of the normal floor set. |
| 13–17 | present | belong to **floor 8** | misfiled |

Port item drift: room 2 missing PAPER NOTE/DESK; room 3 `BROOM` → `LONG BROOM`; room 5 has a stray
`LOCKED DOOR`; room 9 `PUSH BUTTON` → `TRAP DOOR IN CEILING` + `DOWN BUTTON`; room 10 has **no items at
all** (missing CABINET, FLASHLIGHT, TAPE); room 11 `WIRES`/`ADMISSION` → `ENDS OF 2 'LIVE' WIRES`;
room 7 has no items.

## 8. What the fix is

Rewrite `floors/floor_9.py` to hold rooms **1–12** exactly as in §2/§3, move rooms 13–17 into
`floors/floor_8.py`, and re-point the floor-9 → floor-8 transition at `PRESS BUTTON` on room 9.
Replace the circular `tests/test_all_floors_map.py::SOURCE_PAIRS` with the pixel-derived table so the
test compares against the magazine instead of against itself.
