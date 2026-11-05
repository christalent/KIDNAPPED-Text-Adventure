"""Floor 6 vault rules, verified against the original listing.

Source lines 467 / 960 / 1515 / 1516 of the December 1980 SoftSide listing
(KIDNAPPED_Original.pdf), cross-checked against the original issue OCR and
the July 1981 Apple/Atari re-listing.  See
audit/FLOOR6_VAULT_2026-11-05.md.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from floors.floor_6 import Floor6Engine  # noqa: E402
from kidnapped import GameState  # noqa: E402


def make_engine(inventory=None, location=35):
    state = GameState(floor=6)
    engine = Floor6Engine(state)
    engine.on_enter()
    state.location = location
    if hasattr(engine, "location"):
        engine.location = location
    state.inventory = list(inventory or [])
    state.pm_scared = False
    return engine, state


def test_vault_description_shows_kidnapper_counting_money():
    engine, _ = make_engine()
    result, _ = engine.handle_command("LOOK", "")
    assert "KIDNAPPER IS COUNTING MONEY" in result
    assert "HE DOESN'T SEE YOU YET" in result


def test_get_dollar_without_gun_kills_you():
    engine, state = make_engine(inventory=[])
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "YOU GET TOO CLOSE TO HIM, HE JUMPS UP AND STRANGLES YOU." in result
    assert state.alive is False
    assert state.game_over is True
    assert "DOLLAR" not in state.inventory


def test_get_money_without_gun_kills_you():
    engine, state = make_engine(inventory=[])
    result, _ = engine.handle_command("GET", "MONEY")
    assert "HE JUMPS UP AND STRANGLES YOU." in result
    assert state.game_over is True


def test_get_dollar_with_gun_freezes_him_and_pays_out():
    engine, state = make_engine(inventory=["GUN"])
    result, _ = engine.handle_command("GET", "DOLLAR")
    assert "KIDNAPPER SEES YOUR GUN AND FREEZES. YOU GRAB A DOLLAR" in result
    assert "DOLLAR" in state.inventory
    assert state.alive is True
    assert state.game_over is False


def test_get_money_with_gun_also_pays_out_the_dollar():
    engine, state = make_engine(inventory=["GUN"])
    result, _ = engine.handle_command("GET", "MONEY")
    assert "KIDNAPPER SEES YOUR GUN AND FREEZES" in result
    assert "DOLLAR" in state.inventory


def test_kidnapper_is_scared_after_the_payoff():
    engine, _ = make_engine(inventory=["GUN"])
    engine.handle_command("GET", "DOLLAR")
    result, _ = engine.handle_command("LOOK", "")
    assert "KIDNAPPER IS SCARED" in result


def test_shooting_the_gun_in_the_vault_kills_you():
    engine, state = make_engine(inventory=["GUN"])
    result, _ = engine.handle_command("SHOOT", "GUN")
    assert "GUN HAD BLANKS! KIDNAPPER SHOOTS YOU!" in result
    assert state.game_over is True


def test_shooting_elsewhere_just_misfires():
    engine, state = make_engine(inventory=["GUN"], location=26)
    result, _ = engine.handle_command("SHOOT", "GUN")
    assert "GUN MISFIRES" in result
    assert state.game_over is False


def test_dollar_is_not_gettable_outside_the_vault():
    engine, state = make_engine(inventory=["GUN"], location=26)
    engine.handle_command("GET", "DOLLAR")
    assert "DOLLAR" not in state.inventory
    assert state.game_over is False


if __name__ == "__main__":
    import traceback

    _fns = [(n, f) for n, f in sorted(globals().items())
            if n.startswith("test_") and callable(f)]
    _failed = 0
    for _n, _f in _fns:
        try:
            _f()
            print(f"PASS {_n}")
        except Exception:
            _failed += 1
            print(f"FAIL {_n}")
            traceback.print_exc()
    print(f"\n{len(_fns) - _failed}/{len(_fns)} vault tests passed")
    sys.exit(1 if _failed else 0)
