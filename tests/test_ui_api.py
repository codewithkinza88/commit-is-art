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
    with open(os.path.join(root, "app", "ui_kit.py"),
              encoding="utf-8") as f:
        kit_source = f.read()
    check("the UI uses ft.Border.all, not ft.border.all",
          "ft.Border.all" in source + kit_source
          and "ft.border.all" not in source + kit_source)
    check("main.py has no removed ft.app call",
          "ft.app(" not in source)
    check("main.py has no removed ft.ElevatedButton call",
          "ft.ElevatedButton" not in source)
    check("main.py launches with ft.run(main)",
          "ft.run(main)" in source)
    check("edit path also rejects an empty habit name",
          source.count("Please give your habit a name first") == 2)
    check("delete asks first with a confirm dialog",
          "Delete this habit?" in source)
    check("delete happens only from the confirm button",
          source.count('delete_habit(habits, habit["id"])') == 1)
    check("confirm dialog offers Keep it",
          '"Keep it' in source)
    check("Tonight compares yesterday and today",
          "Yesterday vs today" in source)
    check("yesterday summary comes from daily_summary",
          "daily_summary(logs, habits, yesterday)" in source)
    check("app version is 1.5.0",
          open(os.path.join(root, "app", "version.py"),
               encoding="utf-8").read().count('APP_VERSION = "1.5.0"') == 1)

    from app.ui_kit import (  # noqa: E402
        gradient_card, gradient_header, mini_progress, pill, soft_card,
        stat_chip, streak_pill,
    )
    check("pill builds a rounded container",
          isinstance(pill("Study", "#A5D8FF"), ft.Container)
          and pill("Study", "#A5D8FF").border_radius == 10)
    check("streak pill shows the streak",
          "5" in streak_pill(5).content.value)
    check("streak pill turns gold at a week",
          streak_pill(7).content.value.startswith("🔥 7"))
    check("soft card has a soft shadow",
          len(soft_card(ft.Text("hi")).shadow) == 1)
    check("gradient header has a gradient",
          gradient_header("Today", "hi").gradient is not None
          and isinstance(gradient_header("Today", "hi").gradient,
                         ft.LinearGradient))
    check("gradient card has a gradient",
          gradient_card(ft.Text("hi")).gradient is not None)
    check("stat chip shows its value",
          stat_chip("🌱", "plants", 3).content.controls[1].value == "3")
    check("mini progress clamps to full",
          mini_progress(2).value == 1.0)
    check("main.py uses the ui kit",
          "from app.ui_kit import" in source)
    check("main.py shows growth progress in the garden",
          "stage_progress(" in source)
    check("ui kit has no removed ft.app call",
          "ft.app(" not in kit_source)
    check("ui kit has no removed ft.ElevatedButton call",
          "ft.ElevatedButton" not in kit_source)
    check("the UI never uses the removed padding helpers",
          "ft.padding.symmetric" not in source + kit_source
          and "ft.padding.only" not in source + kit_source
          and "ft.padding.all" not in source + kit_source)


if __name__ == "__main__":
    test_ui_api()
    print(f"{PASSED} tests passed")
