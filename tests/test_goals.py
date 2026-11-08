"""Plain-script tests for app.goals (pytest is not installed here).

Run:  python3 tests/test_goals.py
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import log_minutes  # noqa: E402
from app.goals import minutes_in_last_7_days, weekly_goal_progress  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_minutes_in_last_7_days():
    habit = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    log_minutes(logs, habit["id"], "2026-11-06", 30)
    log_minutes(logs, habit["id"], "2026-11-07", 45)
    log_minutes(logs, habit["id"], "2026-10-30", 99)  # older than 7 days
    check("last 7 days minutes is 75",
          minutes_in_last_7_days(logs, habit, date(2026, 11, 7)) == 75)


def test_weekly_goal_progress():
    habit = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    log_minutes(logs, habit["id"], "2026-11-07", 45)
    progress = weekly_goal_progress(logs, habit, 90, date(2026, 11, 7))
    check("goal percent is 50", progress["percent"] == 50)
    check("goal remaining is 45", progress["remaining"] == 45)
    check("goal is not met yet", progress["met"] is False)


def test_weekly_goal_met_and_no_goal():
    habit = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    log_minutes(logs, habit["id"], "2026-11-07", 120)
    check("goal met at 120 of 90",
          weekly_goal_progress(logs, habit, 90, date(2026, 11, 7))["met"] is True)
    check("no goal is always met",
          weekly_goal_progress(logs, habit, 0, date(2026, 11, 7))["met"] is True)


if __name__ == "__main__":
    test_minutes_in_last_7_days()
    test_weekly_goal_progress()
    test_weekly_goal_met_and_no_goal()
    print(f"{PASSED} tests passed")
