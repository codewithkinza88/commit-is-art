"""Plain-script tests for app.monthly (pytest is not installed here).

Run:  python3 tests/test_monthly.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.monthly import monthly_summary  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_monthly_november():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    month = monthly_summary(logs, habits, 2026, 11)
    check("november has 30 days", month["days_in_month"] == 30)
    check("monthly total minutes is 45", month["total_minutes"] == 45)
    check("monthly perfect days is 1", month["perfect_days"] == 1)
    check("monthly best day is 2026-11-07",
          month["best_day_date"] == "2026-11-07")
    check("minutes by weekday puts 45 on Saturday",
          month["minutes_by_weekday"]["Sat"] == 45)
    check("minutes by weekday is zero on Monday",
          month["minutes_by_weekday"]["Mon"] == 0)
    check("minutes by weekday adds up to the total",
          sum(month["minutes_by_weekday"].values()) == month["total_minutes"])


def test_monthly_february_leap_year():
    month = monthly_summary({}, [], 2024, 2)
    check("feb 2024 has 29 days", month["days_in_month"] == 29)
    check("empty month total is 0", month["total_minutes"] == 0)
    check("empty month average is 0%", month["average_percent"] == 0)
    check("empty month perfect days is 0", month["perfect_days"] == 0)


def test_monthly_empty_habits():
    month = monthly_summary({}, [], 2026, 11)
    check("empty habits best day is first day",
          month["best_day_date"] == "2026-11-01")


if __name__ == "__main__":
    test_monthly_november()
    test_monthly_february_leap_year()
    test_monthly_empty_habits()
    print(f"{PASSED} tests passed")
