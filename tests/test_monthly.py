"""Plain-script tests for app.monthly (pytest is not installed here).

Run:  python3 tests/test_monthly.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.monthly import (average_minutes_per_day, busiest_weekday,  # noqa: E402
                         days_logged_this_month, monthly_summary,
                         quietest_weekday)

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


def test_busiest_weekday():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-02", 30)  # Monday
    log_minutes(logs, habits[0]["id"], "2026-11-04", 45)  # Wednesday
    log_minutes(logs, habits[0]["id"], "2026-11-05", 45)  # Thursday
    month = monthly_summary(logs, habits, 2026, 11)
    check("busiest weekday is Wednesday (tie goes earliest)",
          busiest_weekday(month) == "Wed")
    check("empty month has no busiest weekday",
          busiest_weekday(monthly_summary({}, [], 2026, 11)) is None)
    check("no summary has no busiest weekday",
          busiest_weekday({}) is None)


def test_quietest_weekday():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-02", 30)  # Monday
    log_minutes(logs, habits[0]["id"], "2026-11-04", 45)  # Wednesday
    log_minutes(logs, habits[0]["id"], "2026-11-05", 45)  # Thursday
    month = monthly_summary(logs, habits, 2026, 11)
    check("quietest weekday is Tuesday (0 minutes, earliest)",
          quietest_weekday(month) == "Tue")
    check("empty month has no quietest weekday",
          quietest_weekday(monthly_summary({}, [], 2026, 11)) is None)
    check("no summary has no quietest weekday",
          quietest_weekday({}) is None)


def test_average_minutes_per_day():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-02", 30)
    log_minutes(logs, habits[0]["id"], "2026-11-04", 45)
    log_minutes(logs, habits[0]["id"], "2026-11-05", 45)
    month = monthly_summary(logs, habits, 2026, 11)
    # 120 minutes over 30 November days = 4 per day.
    check("average minutes per day is 4 for November",
          average_minutes_per_day(month) == 4)
    check("an empty month averages 0 minutes a day",
          average_minutes_per_day(monthly_summary({}, [], 2026, 11)) == 0)
    check("no summary averages 0 minutes a day",
          average_minutes_per_day({}) == 0)


def test_days_logged_this_month():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-02", 30)
    log_minutes(logs, habits[0]["id"], "2026-11-04", 45)
    log_minutes(logs, habits[0]["id"], "2026-11-05", 45)
    month = monthly_summary(logs, habits, 2026, 11)
    check("three days logged in November",
          days_logged_this_month(month) == 3)
    check("an empty month logs 0 days",
          days_logged_this_month(monthly_summary({}, [], 2026, 11)) == 0)
    check("no summary logs 0 days",
          days_logged_this_month(None) == 0)


if __name__ == "__main__":
    test_monthly_november()
    test_monthly_february_leap_year()
    test_monthly_empty_habits()
    test_busiest_weekday()
    test_quietest_weekday()
    test_average_minutes_per_day()
    test_days_logged_this_month()
    print(f"{PASSED} tests passed")
