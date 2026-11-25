"""Plain-script tests for app.insights.

Run:  python3 tests/test_insights.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.insights import (average_consistency, consistency_message,  # noqa: E402
                          consistency_score,                       habits_above_rate, habits_below_rate,
                                                least_consistent_habit, most_consistent_habit,
                          needs_attention, weekly_done_rate, done_rate_for_habit,
                          done_rate_overall, habit_with_most_minutes,
                          best_category_by_minutes)
from app.tracker import set_done, log_minutes  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    logs = {}
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    check("consistency 4 of 6", consistency_score(logs, habits, days) == 67)
    check("perfect score", consistency_score(logs, [a], days) == 100)
    check("empty habits", consistency_score(logs, [], days) == 0)
    check("empty days", consistency_score(logs, habits, []) == 0)
    check("needs attention is water", needs_attention(logs, habits, days) is b)
    check("no habits is None", needs_attention(logs, [], days) is None)
    check("most consistent habit is study",
          most_consistent_habit(logs, habits, days) is a)
    check("most consistent with no habits is None",
          most_consistent_habit(logs, [], days) is None)
    check("most consistent with no days is None",
          most_consistent_habit(logs, habits, []) is None)
    check("perfect consistency message", "Amazingly" in consistency_message(100))
    check("steady consistency message", "steady" in consistency_message(75))
    check("no ticks message", "No ticks" in consistency_message(0))


def test_weekly_done_rate():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    logs = {}
    # 7 days ending 2026-11-10: a done all 7, b done 3 -> 10/14 = 71%.
    for day in ("2026-11-04", "2026-11-05", "2026-11-06", "2026-11-07",
                "2026-11-08", "2026-11-09", "2026-11-10"):
        set_done(logs, a["id"], day, True)
    for day in ("2026-11-08", "2026-11-09", "2026-11-10"):
        set_done(logs, b["id"], day, True)
    check("done rate this week is 71%",
          weekly_done_rate(logs, habits, "2026-11-10") == 71)
    check("done rate with no habits is 0",
          weekly_done_rate(logs, [], "2026-11-10") == 0)
    check("done rate with no logs is 0",
          weekly_done_rate({}, habits, "2026-11-10") == 0)


def test_habits_above_rate():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    logs = {}
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    # a done 3/3 (100%), b done 1/3 (33%).
    check("only the 100% habit is above 80%",
          habits_above_rate(logs, habits, days) == [a])
    check("a habit exactly at the threshold counts",
          habits_above_rate(logs, habits, days, 100) == [a])
    check("no habits means nobody above the rate",
          habits_above_rate(logs, [], days) == [])


def test_average_consistency():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    logs = {}
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    # a 100%, b 33% -> mean 67 (rounded).
    check("average consistency means the per-habit rates",
          average_consistency(logs, habits, days) == 67)
    check("no habits means 0 consistency",
          average_consistency(logs, [], days) == 0)
    check("no dates means 0 consistency",
          average_consistency(logs, habits, []) == 0)


def test_habits_below_rate():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    logs = {}
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    # a done 3/3 (100%), b done 1/3 (33%).
    check("only the 33% habit is below 50%",
          habits_below_rate(logs, habits, days) == [b])
    check("nobody is below 30%",
          habits_below_rate(logs, habits, days, 30) == [])
    check("no habits means nobody below the rate",
          habits_below_rate(logs, [], days) == [])


def test_least_consistent_habit():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    logs = {}
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    # a done 3/3, b done 1/3 — b is the least consistent.
    check("least consistent habit is walk",
          least_consistent_habit(logs, habits, days) is b)
    check("least consistent with no habits is None",
          least_consistent_habit(logs, [], days) is None)
    check("least consistent with no days is None",
          least_consistent_habit(logs, habits, []) is None)


def test_done_rate_for_habit():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    # a done 3/3, b done 1/3.
    check("a habit done every day has rate 1.0",
          done_rate_for_habit(logs, a, days) == 1.0)
    check("a habit done one day in three has rate 1/3",
          done_rate_for_habit(logs, b, days) == 1 / 3)
    check("no dates means rate 0.0",
          done_rate_for_habit(logs, a, []) == 0.0)


def test_done_rate_overall():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Water", "Health", 0, "💧", "#BDE0FE", "2026-11-01")
    habits = [a, b]
    days = ["2026-11-08", "2026-11-09", "2026-11-10"]
    logs = {}
    for d in days:
        set_done(logs, a["id"], d, True)
    set_done(logs, b["id"], "2026-11-08", True)
    check("overall done rate is 67",
          done_rate_overall(logs, habits, days) == 67)
    check("empty habits give 0", done_rate_overall(logs, [], days) == 0)
    check("empty days give 0", done_rate_overall(logs, habits, []) == 0)


def test_habit_with_most_minutes():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Read", "Books", 0, "📖", "#FFC6FF", "2026-11-01")
    logs = {}
    log_minutes(logs, a["id"], "2026-11-09", 30)
    log_minutes(logs, b["id"], "2026-11-09", 45)
    check("most minutes wins",
          habit_with_most_minutes(logs, [a, b], "2026-11-10")["name"] == "Read")
    tied = {}
    log_minutes(tied, a["id"], "2026-11-09", 30)
    log_minutes(tied, b["id"], "2026-11-09", 30)
    check("a tie keeps the first habit",
          habit_with_most_minutes(tied, [b, a], "2026-11-10")["name"] == "Read")
    check("no habits give None",
          habit_with_most_minutes(logs, [], "2026-11-10") is None)


def test_best_category_by_minutes():
    a = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    b = new_habit("Read", "Books", 0, "📖", "#FFC6FF", "2026-11-01")
    logs = {}
    log_minutes(logs, a["id"], "2026-11-09", 30)
    log_minutes(logs, b["id"], "2026-11-09", 45)
    check("most minutes win",
          best_category_by_minutes(logs, [a, b], "2026-11-09") == "Books")
    tied = {}
    log_minutes(tied, a["id"], "2026-11-09", 30)
    log_minutes(tied, b["id"], "2026-11-09", 30)
    check("a tie keeps the first category",
          best_category_by_minutes(tied, [a, b], "2026-11-09") == "Study")
    check("nothing logged gives None",
          best_category_by_minutes(logs, [a, b], "2026-11-10") is None)


if __name__ == "__main__":
    main()
    test_weekly_done_rate()
    test_habits_below_rate()
    test_least_consistent_habit()
    test_done_rate_for_habit()
    test_habits_above_rate()
    test_average_consistency()
    test_done_rate_overall()
    test_habit_with_most_minutes()
    test_best_category_by_minutes()
    print(f"{PASSED} tests passed")
