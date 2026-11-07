"""Plain-script tests for weekly_summary (pytest is not installed here).

Run:  python3 tests/test_weekly.py
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes, weekly_summary  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_weekly_total_minutes():
    habits = [new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-06", 30)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    week = weekly_summary(logs, habits, end_date=date(2026, 11, 7))
    check("weekly has 7 days", len(week["days"]) == 7)
    check("weekly total minutes is 75", week["total_minutes"] == 75)
    check("weekly end date", week["end_date"] == "2026-11-07")


def test_weekly_best_day():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-05"),
    ]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-06", True)
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    set_done(logs, habits[1]["id"], "2026-11-07", True)
    week = weekly_summary(logs, habits, end_date=date(2026, 11, 7))
    check("weekly best day is the full day",
          week["best_day_date"] == "2026-11-07"
          and week["best_day"]["percent"] == 100)
    check("weekly average percent is in range",
          0 <= week["average_percent"] <= 100)


def test_weekly_empty_habits():
    week = weekly_summary({}, [], end_date=date(2026, 11, 7))
    check("weekly empty total is 0", week["total_minutes"] == 0)
    check("weekly empty average is 0%", week["average_percent"] == 0)
    check("weekly empty best day is first day",
          week["best_day_date"] == "2026-11-01")


if __name__ == "__main__":
    test_weekly_total_minutes()
    test_weekly_best_day()
    test_weekly_empty_habits()
    print(f"{PASSED} tests passed")
