# Floor-6 (Kidnapped) handler audit — pixel-verified notes

Working scratch copy of the audit; final findings are in the chat report.
Source of truth: KIDNAPPED_Original.pdf, native 300 ppi raster, cropped with
`pdftoppm -r 300 -gray -png` + point upscale (crop300.py).

## Item DATA (pixel-verified, p4)
```
2010 DATA DESK,-17,KEY MAKING MACHINE,-19,SUPER GLUE,20,WOODEN STAIR STEP,20,
     THICK COPPER SHEET,23,LOCKED DOOR,-24,WOODEN STAIRS,-25,TANK OF HELIUM GAS,28,
     LARGE DEFLATED BALLOON,29
2020 DATA LOCKED DOOR,-30,GUN,30,SIGN ON WALL,-32,STRING VENDING MACHINE,-32,
     OPEN WINDOW,-33,LOCKED DOOR,-43,BALL OF YARN,39,KNITTING NEEDLES,40,
     PUSH BUTTON ON WALL,-42,"SEXY, YOUNG GIRL OFFICE WORKERS",-37,STAIRS,-44
```

## Floor-6 rooms (pixel-verified, p1 lines 36-46; room = line - 10)
26 (l36) W31 N27 E29 S30 | 27 (l37) N28 S26 | 28 (l38) "IN A CLOSET." S27
29 (l39) "IN A GAME ROOM." W26 | 30 (l40) N26 | 31 (l41) W33 N32 E26
32 (l42) "IN A STORE ROOM." S31 | 33 (l43) E31
34 (l44) "ON A LARGE LEDGE BY WINDOW." W36 | 35 (l45) "IN THE VAULT." W36
36 (l46) "ON A LARGE LEDGE BY WINDOW." E34

## Handler blocks (pixel-verified)
See /home/chris/.hermes/cache/scratch/kidnap_audit/F6_HANDLER_NOTES.md for the
full verbatim set, and CROP_MANIFEST.md for crop coordinates.
