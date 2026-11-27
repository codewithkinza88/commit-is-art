"""Plain-script tests for app.achievements (pytest is not installed here).

Run:  python3 tests/test_achievements.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.achievements import badges_count, badges_for, badge_labels, has_badge, badge_emojis  # noqa: E402

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


def test_badges_count():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    # First step + perfect day = 2 badges.
    check("two badges earned counts as 2",
          badges_count(logs, habits, "2026-11-07") == 2)
    check("no badges earned counts as 0",
          badges_count({}, habits, "2026-11-07") == 0)
    check("no habits means 0 badges",
          badges_count(logs, [], "2026-11-07") == 0)


def test_badge_labels():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    # First step + perfect day = 2 badges.
    check("two badges earned give two labels",
          badge_labels(logs, habits, "2026-11-07")
          == ["First Step", "Perfect Day"])
    check("no badges earned gives no labels",
          badge_labels({}, habits, "2026-11-07") == [])
    check("no habits means no labels",
          badge_labels(logs, [], "2026-11-07") == [])


def test_century_minutes_badge():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 120)
    keys = _keys(badges_for(logs, habits, "2026-11-07"))
    check("100 minutes badge earned", "century_minutes" in keys)


def test_has_badge():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 60)
    check("a badge earned is found by label",
          has_badge(logs, habits, "2026-11-07", "First Step") is True)
    check("a badge not earned is not found",
          has_badge(logs, habits, "2026-11-07", "Week Strong") is False)
    check("no habits means no badge",
          has_badge({}, [], "2026-11-07", "First Step") is False)


def test_badge_emojis():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 60)
    check("the earned badge emojis are listed in award order",
          badge_emojis(logs, habits, "2026-11-07") == ["🌱", "🌸"])
    check("no badges means no emojis",
          badge_emojis({}, [], "2026-11-07") == [])
    check("emojis match the badge labels one to one",
          len(badge_emojis(logs, habits, "2026-11-07"))
          == len(badge_labels(logs, habits, "2026-11-07")))


if __name__ == "__main__":
    test_no_badges_when_nothing_done()
    test_first_step_and_perfect_day()
    test_streak_badges()
    test_century_minutes_badge()
    test_badges_count()
    test_badge_labels()
    test_has_badge()
    test_badge_emojis()
    print(f"{PASSED} tests passed")
