"""Regression guard for the 2026-11-04 source corrections.

Checks that the corrected source readings are the ones actually in the game,
the repo docs, and the published transcription -- and that the old OCR text
does not creep back in.
"""
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

SOURCE_CORRECTED = REPO / "KIDNAPPED_SOURCE_CORRECTED.txt"
COMPARISON = REPO / "OCR_CORRECTIONS_2026-11-04.md"
GRAFFITI = "WATCH OUT FOR LIVE ONES"


def test_floor9_graffiti_is_source_text():
    from floors import floor_9
    assert floor_9.ROOMS[6]["items"] == ["GRAFFITI ON WALL"]
    src = (REPO / "floors" / "floor_9.py").read_text()
    assert GRAFFITI in src
    assert "MATCH WIT FOR LIVE WIRES" not in src


def test_broom_stays_on_floor_9_room_3():
    from floors import floor_9
    assert "LONG BROOM" in floor_9.ROOMS[3]["items"]
    assert "LONG BROOM" not in floor_9.ROOMS[2]["items"]


def test_source_transcription_has_corrected_readings():
    txt = SOURCE_CORRECTED.read_text()
    assert GRAFFITI in txt
    assert '"LONG BROOM",3' in txt
    assert '"AQUARIUM",-14' in txt
    assert '"DOWN BUTTON",-9' in txt
    assert '"ENDS OF 2 \'LIVE\' WIRES",-11' in txt
    assert '"KNITTING NEEDLES",40' in txt
    assert '"LOCKED DOOR",-43' in txt
    assert '"SMALL BOOK",64' in txt
    assert "MATCH WT FOR LIVE INMATES" not in txt


def test_raw_ocr_file_kept_as_evidence():
    raw = (REPO / "KIDNAPPED_OCR.txt").read_text(errors="replace")
    assert "DATAPAPER" in raw  # raw layer still present, untouched


def test_comparison_doc_covers_the_disputed_tokens():
    doc = COMPARISON.read_text()
    for token in (GRAFFITI, "LONG BROOM", "AQUARIUM", "UNRESOLVED"):
        assert token in doc


def test_readme_and_spec_do_not_claim_72_rooms():
    readme = (REPO / "README.md").read_text()
    spec = (REPO / "SPEC.md").read_text()
    assert "Total: 72 rooms" not in readme
    assert "65 rooms" in readme
    assert "Room 11: D=9, E=13, W=15" not in spec
    assert "ADMISSION" not in spec


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as exc:
                failures += 1
                print("FAIL", name, exc)
    print("failures:", failures)
    sys.exit(1 if failures else 0)
