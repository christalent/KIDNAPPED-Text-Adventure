# Floor 6 vault (room 35) - source-verified rules

Audited 2026-11-05 against `KIDNAPPED_Original.pdf` (December 1980 SoftSide
listing), the original December 1980 issue OCR, and the July 1981
Apple/Atari re-listing.  Native pixel crops were the tie-breaker.

## What the source actually does

| Source line | Behaviour |
|---|---|
| 1060 | `IF A=35 AND (E$="PER" OR E$="LAR" OR E$="NEY") THEN IF I(27)=0 THEN PRINT"YOU GET TOO CLOSE TO HIM, HE JUMPS UP AND STRANGLES YOU.":GOTO7300 ELSE IF I(27)=1 THEN PRINT"KIDNAPPER SEES YOUR GUN AND FREEZES. YOU GRAB A DOLLAR":A$(56)="DOLLAR":H$(56)=A$(56):A(56)=35:PM=1:E$="LAR"` |
| 960 | `IF D(B)<>14 THEN 970 ELSE IF E$="GUN" OR E$="PER" IF I(27)=1 IF A=35 THEN PRINT"GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!":GOTO7200 ELSE PRINT"GUN MISFIRES":GOTO5000` |
| 1515 | `PRINT"KIDNAPPER IS COUNTING MONEY, HE DOESN'T SEE YOU YET.":GOTO390` (PM=0) |
| 1516 | `PRINT"KIDNAPPER IS SCARED":GOTO390` (PM=1) |
| 7200 | `PRINT"YOU SEEM TO HAVE GOTTEN YOURSELF KILLED!"` then GOTO7300 |
| 7300 | `PRINT:PRINT"TO TRY AGAIN YOU'LL HAVE TO START OVER FROM THE 9TH FLOOR."` |

Line 1515 is a single `PRINT` with one string, but the magazine typesets it
across two printed lines ("...COUNTING MONEY." on one line, "HE DOESN'T SEE
YOU YET.":GOTO390 on the next).  The punctuation after MONEY reads as a comma
in the PDF text layer and as a period in the December 1980 issue OCR; the
wording is identical either way.

`E$` is the last three letters of the noun: KIDNAPPER -> PER, DOLLAR -> LAR,
MONEY -> NEY.  `I(27)` is the GUN (DATA item 27).  `PM` is the kidnapper's
state flag: 0 while he is counting the money, 1 once he is scared.

## Consequences (all implemented)

1. The DOLLAR is **not** a DATA item.  It is created at run time in room 35
   by line 1060 and only if you are holding the GUN.
2. Asking for the money without the GUN kills you
   (`GOTO7300`).  There is no unarmed way into the vault.
3. With the GUN, the kidnapper freezes and hands over a DOLLAR; `PM=1`
   flips room 35's description to "KIDNAPPER IS SCARED".
4. Firing the gun in the vault is fatal (`GOTO7200` -> `GOTO7300`):
   "GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!"
5. Firing the gun anywhere else just prints "GUN MISFIRES" (`GOTO5000`).

## Corrections to `KIDNAPPED.BAS`

`KIDNAPPED.BAS` is an OCR reconstruction and its vault block was wrong in
several ways.  Line 1060 has been corrected in place; the rest is recorded
here rather than silently patched.

| BAS said | Source says |
|---|---|
| `YOU GET TOO CLOSE TO HIM, HE MUFFLES AND STRAIGHTENS YOU.` | `... HE JUMPS UP AND STRANGLES YOU.` |
| `KIDNAPPER SEES YOU GRAB AND FREEZES` | `KIDNAPPER SEES YOUR GUN AND FREEZES` |
| `IF A=35 AND E$="PER" THEN IF E$="LAR" OR E$="NEY" AND I(27)=0` (operator precedence mangled) | `IF A=35 AND (E$="PER" OR E$="LAR" OR E$="NEY") THEN IF I(27)=0` |
| `1080 IFA=35 AND E$="DOL" THEN PRINT"WHICH DOLLAR?"` | no such branch in the source; `E$` is a 3-letter suffix, so "DOL" can never match "DOLLAR" |
| `7200 PRINT"YOU HAVE DIED A TERRIBLE AND GRUESOME DEATH, YOUR BODY TORN TO SCREDS."` | `7200 PRINT"YOU SEEM TO HAVE GOTTEN YOURSELF KILLED!"` (the "grizzly death" wording belongs to the later Apple/Atari re-listing) |

## Implementation map

* `floors/floor_6.py` -> `Floor6Engine._vault_rules`, `_vault_death`
* `floors/floor_6.py` -> `VAULT_DESC_COUNTING`, `VAULT_DESC_SCARED`,
  `VAULT_DEATH_7200`, `VAULT_DEATH_7300`
* `tests/test_floor6_vault.py` -> regression tests for every branch above

## Running the tests

`python3 -m unittest discover -s tests -p 'test_*.py' -t .` does NOT work
in this repo: `tests/` is not a package and every test file is script-style
with its own `__main__` runner, so unittest collects ZERO tests and prints
"OK".  That is how a broken vault implementation previously passed as green.

Use `python3 tests/run_all.py`, which runs every `tests/test_*.py` as a
subprocess and fails loudly.  Current state: **11/11 test files pass**,
including `tests/test_floor6_vault.py` (9 vault tests) which had never been
executed before this pass.

## Bugs fixed in this pass

* `_vault_death` was defined twice in `floors/floor_6.py`; the second
  definition shadowed the first, so the two-argument call (the shooting
  death) raised TypeError.
* `handle_command` called `_vault_rules(verb, noun="")` with an EMPTY noun,
  so every vault branch returned early and the whole vault rule set was
  dead code.
* `_vault_death` returned a `(text, move)` tuple that the caller wrapped in
  another tuple, so the dispatcher returned `((text, False), False)` and every
  text assertion on the result failed.
* The money is now gone after the payoff (1516), so the DOLLAR cannot be
  taken twice.

## Still open

* `KIDNAPPED.BAS` line 1080 ("WHICH DOLLAR?") has no source counterpart and
  is left untouched pending a native-pixel re-read of the listing line.
* The 7250 death variant ("TERRIBLE AND GRIZZLY DEATH") belongs to the
  July 1981 Apple/Atari version and is not used by this remake.
