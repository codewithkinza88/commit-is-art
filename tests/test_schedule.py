"""Plain-script tests for app.schedule.

Run:  python3 tests/test_schedule.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.schedule import (count_due_every_day, count_due_on_weekday,
                          count_due_this_week,
                          count_due_today, count_due_tomorrow,  # noqa: E402
                          count_due_today_undone, due_this_week,
                          habits_due_every_day, habits_due_on,
                          habits_not_due_today,
                          habits_due_tomorrow, habits_due_on_weekday_name,
                          is_due_today, next_due_weekday,
                          next_due_weekday_name, weekday_name,
                          weekday_of)
from app.tracker import set_done  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    check("monday has daily+weekday", len(habits_due_on(habits, 0)) == 2)
    check("saturday has daily+weekend", len(habits_due_on(habits, 5)) == 2)
    check("sunday excludes weekday habit",
          weekday_only not in habits_due_on(habits, 6))
    check("weekday names", weekday_name(0) == "Mon" and weekday_name(6) == "Sun")
    check("bad weekday name", weekday_name(9) == "?")
    check("empty list", habits_due_on([], 0) == [])


def test_due_this_week():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    monday_only = new_habit("Monday run", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    monday_only["days"] = [0]
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, monday_only, weekend]
    check("friday this week skips the monday-only habit",
          due_this_week(habits, 4) == [daily, weekday_only, weekend])
    check("monday this week has every habit",
          len(due_this_week(habits, 0)) == 4)
    check("sunday this week has daily and weekend only",
          due_this_week(habits, 6) == [daily, weekend])


def test_is_due_today():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    check("a habit with no days is due every day",
          is_due_today(daily, 5) is True)
    check("a Mon-Fri habit is due on Monday",
          is_due_today(weekday_only, 0) is True)
    check("a Mon-Fri habit is not due on Saturday",
          is_due_today(weekday_only, 5) is False)


def test_habits_due_tomorrow():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    check("due tomorrow from Friday is daily and weekend",
          habits_due_tomorrow(habits, 4) == [daily, weekend])
    check("due tomorrow from Sunday wraps to Monday",
          habits_due_tomorrow(habits, 6) == [daily, weekday_only])
    check("due tomorrow with no habits is empty",
          habits_due_tomorrow([], 0) == [])


def test_count_due_today():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    check("two habits due on Monday",
          count_due_today(habits, 0) == 2)
    check("two habits due on Saturday",
          count_due_today(habits, 5) == 2)
    check("no habits due means 0",
          count_due_today([], 0) == 0)


def test_count_due_tomorrow():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    check("two habits due tomorrow from Monday",
          count_due_tomorrow(habits, 0) == 2)
    check("two habits due tomorrow from Friday",
          count_due_tomorrow(habits, 4) == 2)
    check("no habits due means 0",
          count_due_tomorrow([], 0) == 0)


def test_count_due_today_undone():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    logs = {}
    # 2026-11-09 is a Monday: daily + weekday_only due, weekend not.
    check("both due habits are undone at first",
          count_due_today_undone(habits, logs, 0, "2026-11-09") == 2)
    set_done(logs, daily["id"], "2026-11-09", True)
    check("a ticked habit no longer counts as undone",
          count_due_today_undone(habits, logs, 0, "2026-11-09") == 1)
    set_done(logs, weekday_only["id"], "2026-11-09", True)
    check("all due habits done means 0 undone",
          count_due_today_undone(habits, logs, 0, "2026-11-09") == 0)


def test_count_due_this_week():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [daily, weekday_only, weekend]
    check("all three are due at some point from Monday",
          count_due_this_week(habits, 0) == 3)
    check("only the daily and weekend habits are due from Saturday",
          count_due_this_week(habits, 5) == 2)
    check("no habits due this week means 0",
          count_due_this_week([], 0) == 0)


def test_habits_due_every_day():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    check("only the habit without days is due every day",
          habits_due_every_day([daily, weekday_only, weekend]) == [daily])
    check("a habit with an empty days list is due every day",
          habits_due_every_day([daily]) == [daily])
    check("no daily habits gives []",
          habits_due_every_day([weekday_only, weekend]) == [])


def test_weekday_of():
    check("2026-11-09 is a Monday",
          weekday_of("2026-11-09") == 0)
    check("2026-11-14 is a Saturday",
          weekday_of("2026-11-14") == 5)
    check("an impossible date gives -1",
          weekday_of("2026-02-30") == -1)
    check("non-date text gives -1",
          weekday_of("soon") == -1)


def test_count_due_on_weekday():
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF",
                             "2026-11-01")
    weekday_only["days"] = [0, 2, 4]  # Mon, Wed, Fri
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                      "2026-11-01")
    check("two habits are due on Monday",
          count_due_on_weekday([weekday_only, daily], 0) == 2)
    check("only the daily habit is due on Tuesday",
          count_due_on_weekday([weekday_only, daily], 1) == 1)
    check("no habits means nothing due",
          count_due_on_weekday([], 0) == 0)


def test_next_due_weekday_name():
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF",
                             "2026-11-01")
    weekday_only["days"] = [0, 2, 4]  # Mon, Wed, Fri
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                      "2026-11-01")
    check("Tuesday waits until Wednesday",
          next_due_weekday_name(weekday_only, 1) == "Wed")
    check("Saturday wraps around to Monday",
          next_due_weekday_name(weekday_only, 5) == "Mon")
    check("a daily habit names the given weekday",
          next_due_weekday_name(daily, 3) == "Thu")


def test_next_due_weekday():
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF",
                             "2026-11-01")
    weekday_only["days"] = [0, 2, 4]  # Mon, Wed, Fri
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                      "2026-11-01")
    check("due today stays on today",
          next_due_weekday(weekday_only, 2) == 2)
    check("Tuesday waits until Wednesday",
          next_due_weekday(weekday_only, 1) == 2)
    check("Saturday wraps around to Monday",
          next_due_weekday(weekday_only, 5) == 0)
    check("a daily habit is due on the given weekday",
          next_due_weekday(daily, 3) == 3)


def test_habits_due_on_weekday_name():
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF",
                             "2026-11-01")
    weekday_only["days"] = [0, 2, 4]  # Mon, Wed, Fri
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                      "2026-11-01")
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5",
                        "2026-11-01")
    weekend["days"] = [5, 6]
    habits = [weekday_only, daily, weekend]
    check("Tuesday names the daily habit only",
          habits_due_on_weekday_name(habits, "Tue") == [daily])
    check("Saturday names daily and weekend habits",
          habits_due_on_weekday_name(habits, "Sat") == [daily, weekend])
    check("an unknown name names nobody",
          habits_due_on_weekday_name(habits, "Funday") == [])


def test_count_due_every_day():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    check("one habit is due every day",
          count_due_every_day([daily, weekday_only, weekend]) == 1)
    check("no daily habits give 0",
          count_due_every_day([weekday_only, weekend]) == 0)
    check("no habits give 0", count_due_every_day([]) == 0)


def test_habits_not_due_today():
    daily = new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    weekday_only = new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    weekday_only["days"] = [0, 1, 2, 3, 4]  # Mon-Fri
    weekend = new_habit("Long walk", "Health", 0, "🏃", "#C8F7C5", "2026-11-01")
    weekend["days"] = [5, 6]
    check("on Monday the weekend habit is not due",
          habits_not_due_today([daily, weekday_only, weekend], 0) == [weekend])
    check("on Saturday the weekday habit is not due",
          habits_not_due_today([daily, weekday_only, weekend], 5)
          == [weekday_only])
    check("no habits give none", habits_not_due_today([], 0) == [])


if __name__ == "__main__":
    main()
    test_due_this_week()
    test_is_due_today()
    test_habits_due_tomorrow()
    test_count_due_today()
    test_count_due_tomorrow()
    test_count_due_today_undone()
    test_count_due_this_week()
    test_weekday_of()
    test_habits_due_every_day()
    test_next_due_weekday()
    test_habits_due_on_weekday_name()
    test_count_due_on_weekday()
    test_next_due_weekday_name()
    test_count_due_every_day()
    test_habits_not_due_today()
    print(f"{PASSED} tests passed")
