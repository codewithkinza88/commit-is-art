"""Plain-script tests for the cute theme (app/theme.py).

Run:  python3 tests/test_theme.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.theme import (  # noqa: E402
    BG, CARD_RADIUS, DONE_BG, card_bg, done_label, progress_colour,
    stage_colour,
)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_theme():
    check("background is a soft cream", BG == "#FFF8F0")
    check("cards are nicely rounded", CARD_RADIUS >= 20)
    check("done card is pink", card_bg("#F9A8D4", done=True) == DONE_BG)
    check("undone card keeps habit colour",
          card_bg("#F9A8D4", done=False).startswith("#F9A8D4"))
    check("undone card falls back to sky", card_bg(None).startswith("#BDE0FE"))
    check("progress is lilac at 0%", progress_colour(0) == "#E4C1F9")
    check("progress is pink at 50%", progress_colour(50) == "#F9A8D4")
    check("progress is deep pink at 80%", progress_colour(80) == "#F48FB1")
    check("full bloom has a pink tint",
          stage_colour("full_bloom") == "#F8BBD0")
    check("unknown stage falls back to seed tint",
          stage_colour("mystery") == "#E8F5E9")
    check("done label is cute", done_label(True) == "Done 🌸")
    check("not-yet label is gentle", done_label(False) == "Not yet 🌱")


if __name__ == "__main__":
    test_theme()
    print(f"{PASSED} tests passed")
