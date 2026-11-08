"""Plain-script tests for app.achievements (pytest is not installed here).

Run:  python3 tests/test_achievements.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.achievements import badges_for  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def _keys(badges):
    return [b["key"] for b in badges]


def test_no_badges_when_nothing_done():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    check("no badges when nothing done",
          badges_for({}, habits, "2026-11-07") == [])


def test_first_step_and_perfect_day():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    keys = _keys(badges_for(logs, habits, "2026-11-07"))
    check("first step badge earned", "first_step" in keys)
    check("perfect day badge earned", "perfect_day" in keys)


def test_streak_badges():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    for day in ("2026-11-05", "2026-11-06", "2026-11-07"):
        set_done(logs, habits[0]["id"], day, True)
    keys = _keys(badges_for(logs, habits, "2026-11-07"))
    check("three-day badge earned", "three_day" in keys)
    check("week badge not earned yet", "week_strong" not in keys)


def test_century_minutes_badge():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 120)
    keys = _keys(badges_for(logs, habits, "2026-11-07"))
    check("100 minutes badge earned", "century_minutes" in keys)


if __name__ == "__main__":
    test_no_badges_when_nothing_done()
    test_first_step_and_perfect_day()
    test_streak_badges()
    test_century_minutes_badge()
    print(f"{PASSED} tests passed")
