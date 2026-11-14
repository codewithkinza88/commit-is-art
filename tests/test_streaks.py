"""Plain-script tests for app.streaks (pytest is not installed here).

Run:  python3 tests/test_streaks.py
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done  # noqa: E402
from app.streaks import (best_streak, days_since_last_done,  # noqa: E402
                         last_done_label, streak_summary)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_best_streak():
    habit = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03", "2026-11-05", "2026-11-06"):
        set_done(logs, habit["id"], day, True)
    check("best streak is 3", best_streak(logs, habit, date(2026, 11, 6)) == 3)
    check("best streak with no logs is 0", best_streak({}, habit) == 0)


def test_days_since_last_done():
    habit = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    set_done(logs, habit["id"], "2026-11-05", True)
    check("days since last done is 2",
          days_since_last_done(logs, habit, date(2026, 11, 7)) == 2)
    check("never done returns None",
          days_since_last_done({}, habit) is None)


def test_streak_summary():
    habit = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    for day in ("2026-11-06", "2026-11-07"):
        set_done(logs, habit["id"], day, True)
    summary = streak_summary(logs, habit, date(2026, 11, 7))
    check("summary current streak is 2", summary["current"] == 2)
    check("summary best streak is 2", summary["best"] == 2)
    check("summary days since last is 0",
          summary["days_since_last_done"] == 0)


def test_last_done_label():
    habit = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    set_done(logs, habit["id"], "2026-11-05", True)
    check("label for two days ago",
          last_done_label(logs, habit, date(2026, 11, 7)) == "Last done 2 days ago")
    check("label for done today",
          last_done_label(logs, habit, date(2026, 11, 5)) == "Done today 🌸")
    check("label for never done",
          last_done_label({}, habit, date(2026, 11, 7)) == "Not done yet 🌱")


if __name__ == "__main__":
    test_best_streak()
    test_days_since_last_done()
    test_streak_summary()
    test_last_done_label()
    print(f"{PASSED} tests passed")
