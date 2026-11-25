"""Plain-script tests for app.streaks (pytest is not installed here).

Run:  python3 tests/test_streaks.py
"""

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done  # noqa: E402
from app.streaks import (average_best_streak, best_streak,
                         days_since_last_done,  # noqa: E402
                         habits_on_streak, habits_with_best_streak,
                                              habits_with_streak_at_least,
                         last_done_label, longest_gap,
                         longest_current_streak, longest_streak_overall,
                         median_current_streak,                      streak_leaderboard,                      streak_summaries, streak_summary, streaks_by_habit,
                         total_streak_days, average_streak,
                         median_best_streak, shortest_best_streak,
                         habits_with_no_streak, streaks_sorted,
                         best_streaks_sorted, count_habits_on_streak)

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


def test_shortest_best_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-03", True)
    check("shortest best streak across habits is 1",
          shortest_best_streak(logs, [h1, h2], date(2026, 11, 3)) == 1)
    check("shortest streak with no habits is 0",
          shortest_best_streak(logs, [], date(2026, 11, 3)) == 0)
    check("shortest streak with no logs is 0",
          shortest_best_streak({}, [h1, h2], date(2026, 11, 3)) == 0)


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


def test_average_best_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    for day in ("2026-11-01", "2026-11-02", "2026-11-03"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-03", True)
    check("average best streak of 3 and 1 is 2.0",
          average_best_streak(logs, [h1, h2], date(2026, 11, 3)) == 2.0)
    check("average best streak with no habits is 0.0",
          average_best_streak(logs, [], date(2026, 11, 3)) == 0.0)
    check("average best streak of a never-done habit is 0.0",
          average_best_streak({}, [h2], date(2026, 11, 3)) == 0.0)


def test_longest_gap():
    habit = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    check("never done has no gap", longest_gap(logs, habit) == 0)
    set_done(logs, habit["id"], "2026-11-01", True)
    check("done once has no gap", longest_gap(logs, habit) == 0)
    set_done(logs, habit["id"], "2026-11-02", True)
    check("back-to-back days have no gap", longest_gap(logs, habit) == 0)
    set_done(logs, habit["id"], "2026-11-05", True)
    check("Mon to Thu is a 2-day gap", longest_gap(logs, habit) == 2)
    set_done(logs, habit["id"], "2026-11-06", True)
    check("longest gap stays 2", longest_gap(logs, habit) == 2)


def test_streak_leaderboard():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    board = streak_leaderboard(logs, [h1, h2, h3], date(2026, 11, 6))
    check("longest streak leads the board", board[0]["name"] == "Study")
    check("leaderboard streak is 3", board[0]["current"] == 3)
    check("never-done habit sits last with 0",
          board[-1]["name"] == "Walk" and board[-1]["current"] == 0)
    check("empty habits give an empty board",
          streak_leaderboard(logs, []) == [])


def test_longest_current_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Live streaks on 2026-11-06 are 3, 1, 0 -> longest live is 3.
    check("longest live streak is 3",
          longest_current_streak(logs, [h1, h2, h3],
                                 date(2026, 11, 6)) == 3)
    # On 2026-11-07 every streak is broken -> longest live is 0.
    check("broken streaks give a 0 longest live streak",
          longest_current_streak(logs, [h1, h2, h3],
                                 date(2026, 11, 7)) == 0)
    check("no habits give a 0 longest live streak",
          longest_current_streak(logs, []) == 0)


def test_habits_with_best_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
        set_done(logs, h2["id"], day, True)
    set_done(logs, h3["id"], "2026-11-06", True)
    # Best streaks are 3, 3, 1.
    check("the two habits sharing the best streak are named",
          habits_with_best_streak(logs, [h1, h2, h3],
                                  date(2026, 11, 6)) == ["Study", "Read"])
    check("no habits means an empty list",
          habits_with_best_streak(logs, [], date(2026, 11, 6)) == [])
    check("no streaks at all means an empty list",
          habits_with_best_streak({}, [h1, h2, h3],
                                  date(2026, 11, 6)) == [])


def test_streaks_by_habit():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0.
    check("streaks are keyed by habit id",
          streaks_by_habit(logs, [h1, h2, h3], date(2026, 11, 6))
          == {h1["id"]: 3, h2["id"]: 1, h3["id"]: 0})
    check("no habits means an empty map",
          streaks_by_habit(logs, [], date(2026, 11, 6)) == {})
    check("no logs means every streak is 0",
          streaks_by_habit({}, [h1, h2], date(2026, 11, 6))
          == {h1["id"]: 0, h2["id"]: 0})


def test_streaks_sorted():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0.
    check("streaks sort longest first",
          streaks_sorted(logs, [h1, h2, h3], date(2026, 11, 6))
          == [("Study", 3), ("Read", 1), ("Walk", 0)])
    logs2 = {}
    set_done(logs2, h1["id"], "2026-11-06", True)
    set_done(logs2, h2["id"], "2026-11-06", True)
    check("ties keep creation order",
          streaks_sorted(logs2, [h2, h1, h3], date(2026, 11, 6))
          == [("Read", 1), ("Study", 1), ("Walk", 0)])
    check("no habits means an empty list",
          streaks_sorted(logs, [], date(2026, 11, 6)) == [])


def test_total_streak_days():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0.
    check("total streak days add the live streaks",
          total_streak_days(logs, [h1, h2, h3], date(2026, 11, 6)) == 4)
    check("no habits means 0 streak days",
          total_streak_days(logs, [], date(2026, 11, 6)) == 0)
    check("no logs means 0 streak days",
          total_streak_days({}, [h1, h2, h3], date(2026, 11, 6)) == 0)


def test_habits_with_streak_at_least():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0.
    check("only the 3-day streak reaches level 3",
          habits_with_streak_at_least(logs, [h1, h2, h3], 3,
                                      date(2026, 11, 6)) == ["Study"])
    check("two habits reach level 1, in creation order",
          habits_with_streak_at_least(logs, [h1, h2, h3], 1,
                                      date(2026, 11, 6)) == ["Study", "Read"])
    check("no habit reaches level 4",
          habits_with_streak_at_least(logs, [h1, h2, h3], 4,
                                      date(2026, 11, 6)) == [])


def test_habits_on_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0 -> 2 on a streak.
    check("two habits are on a streak",
          habits_on_streak(logs, [h1, h2, h3], date(2026, 11, 6)) == 2)
    # On 2026-11-07 both streaks are broken -> 0 on a streak.
    check("a broken streak counts as off the streak",
          habits_on_streak(logs, [h1, h2, h3], date(2026, 11, 7)) == 0)
    check("no habits give 0 on a streak",
          habits_on_streak(logs, []) == 0)


def test_habits_with_no_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0 -> only Walk has none.
    check("only the habit with no streak is named",
          habits_with_no_streak(logs, [h1, h2, h3],
                                date(2026, 11, 6)) == ["Walk"])
    # On 2026-11-07 both streaks are broken -> all three have none.
    check("broken streaks all count as no streak",
          habits_with_no_streak(logs, [h1, h2, h3],
                                date(2026, 11, 7)) == ["Study", "Read", "Walk"])
    check("no habits means an empty list",
          habits_with_no_streak(logs, []) == [])


def test_median_current_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    # Current streaks on 2026-11-06 are 3, 1, 0 -> median 1.
    check("median current streak is 1",
          median_current_streak(logs, [h1, h2, h3], date(2026, 11, 6)) == 1.0)
    # A broken streak counts as 0: Study's streak ends 2026-11-07.
    check("a broken streak counts as 0 in the median",
          median_current_streak(logs, [h1, h2, h3], date(2026, 11, 7)) == 0.0)
    check("no habits give a 0.0 median current streak",
          median_current_streak(logs, []) == 0.0)


def test_best_streaks_sorted():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🏃", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-06", True)
    set_done(logs, h3["id"], "2026-11-06", True)
    check("best streaks longest first",
          best_streaks_sorted(logs, [h1, h2], date(2026, 11, 6))
          == [("Study", 3), ("Read", 1)])
    check("a tie keeps creation order",
          best_streaks_sorted(logs, [h2, h3], date(2026, 11, 6))
          == [("Read", 1), ("Walk", 1)])
    check("no habits give no pairs", best_streaks_sorted(logs, []) == [])


def test_count_habits_on_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#FFC6FF", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-06", True)
    check("one habit on a streak",
          count_habits_on_streak(logs, [h1, h2], date(2026, 11, 6)) == 1)
    check("a broken streak counts as 0",
          count_habits_on_streak(logs, [h1, h2], date(2026, 11, 7)) == 0)
    check("no habits give 0", count_habits_on_streak(logs, []) == 0)


def test_streak_summaries():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#FFC6FF", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-06", True)
    summaries = streak_summaries(logs, [h1, h2], date(2026, 11, 6))
    check("one summary per habit", len(summaries) == 2)
    check("the first summary carries the live streak",
          summaries[0]["current"] == 1)
    check("no habits give no summaries", streak_summaries(logs, []) == [])


if __name__ == "__main__":
    test_best_streak()
    test_average_streak()
    test_median_best_streak()
    test_median_current_streak()
    test_average_best_streak()
    test_days_since_last_done()
    test_streak_summary()
    test_last_done_label()
    test_longest_streak_overall()
    test_shortest_best_streak()
    test_longest_gap()
    test_streak_leaderboard()
    test_habits_on_streak()
    test_habits_with_no_streak()
    test_longest_current_streak()
    test_habits_with_streak_at_least()
    test_habits_with_best_streak()
    test_streaks_by_habit()
    test_streaks_sorted()
    test_total_streak_days()
    test_best_streaks_sorted()
    test_count_habits_on_streak()
    test_streak_summaries()
    print(f"{PASSED} tests passed")
