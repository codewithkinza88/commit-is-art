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
                         last_done_label, longest_streak_overall,
                         streak_summary, average_streak,
                         median_best_streak)

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


def test_longest_streak_overall():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-03", True)
    check("longest streak across habits is 3",
          longest_streak_overall(logs, [h1, h2], date(2026, 11, 3)) == 3)
    check("longest streak with no habits is 0",
          longest_streak_overall(logs, [], date(2026, 11, 3)) == 0)
    check("longest streak with no logs is 0",
          longest_streak_overall({}, [h1, h2], date(2026, 11, 3)) == 0)


def test_average_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-03", True)
    check("average best streak of 3 and 1 is 2.0",
          average_streak(logs, [h1, h2], date(2026, 11, 3)) == 2.0)
    check("average streak with no habits is 0.0",
          average_streak(logs, [], date(2026, 11, 3)) == 0.0)
    check("average streak with no logs is 0.0",
          average_streak({}, [h1, h2], date(2026, 11, 3)) == 0.0)


def test_median_best_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-03", True)
    check("median best streak of 3, 1 and 0 is 1.0",
          median_best_streak(logs, [h1, h2, h3], date(2026, 11, 3)) == 1.0)
    check("median best streak with no habits is 0.0",
          median_best_streak(logs, [], date(2026, 11, 3)) == 0.0)
    check("median of two streaks averages them",
          median_best_streak(logs, [h1, h2], date(2026, 11, 3)) == 2.0)


if __name__ == "__main__":
    test_best_streak()
    test_average_streak()
    test_median_best_streak()
    test_days_since_last_done()
    test_streak_summary()
    test_last_done_label()
    test_longest_streak_overall()
    print(f"{PASSED} tests passed")
