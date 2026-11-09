"""Plain-script tests for the Flet UI calls used in main.py.

Run:  python3 tests/test_ui_api.py

Why this exists: Flet 1.0.5 removed some old call names, and the plain
logic tests never build the UI, so a renamed call only crashed the app
on launch. Twice: ft.app (fixed to ft.run) and ft.ElevatedButton
(fixed to ft.Button). On 8 November 2026 the same thing happened a
third time — ft.border.all, used for the cute habit-card borders,
does not exist in Flet 1.0.5; the working call is ft.Border.all.
These checks guard the exact calls main.py uses, without launching
the app (main.py ends with an unguarded ft.run(main)).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_ui_api():
    check("flet is 1.0.5", ft.__version__ == "1.0.5")
    border = ft.Border.all(1, "#FDE7F3")
    check("Border.all builds a border",
          isinstance(border, ft.Border))
    check("Border.all sets all four sides to the colour",
          border.top.color == "#FDE7F3"
          and border.right.color == "#FDE7F3"
          and border.bottom.color == "#FDE7F3"
          and border.left.color == "#FDE7F3")
    check("Border.all keeps the width",
          border.top.width == 1)
    check("ft.Button exists (ElevatedButton replacement)",
          hasattr(ft, "Button"))
    check("ft.run exists (ft.app replacement)",
          hasattr(ft, "run"))

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "main.py"), encoding="utf-8") as f:
        source = f.read()
    check("main.py uses ft.Border.all, not ft.border.all",
          "ft.Border.all" in source and "ft.border.all" not in source)
    check("main.py has no removed ft.app call",
          "ft.app(" not in source)
    check("main.py has no removed ft.ElevatedButton call",
          "ft.ElevatedButton" not in source)
    check("main.py launches with ft.run(main)",
          "ft.run(main)" in source)
    check("edit path also rejects an empty habit name",
          source.count("Please give your habit a name first") == 2)


if __name__ == "__main__":
    test_ui_api()
    print(f"{PASSED} tests passed")
