"""Plain-script tests for app.ordering (pytest is not installed here).

Run:  python3 tests/test_ordering.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done  # noqa: E402
from app.ordering import sort_habits  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def _names(habits):
    return [h["name"] for h in habits]


def test_sort_by_name():
    habits = [new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01"),
              new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")]
    check("sorted by name", _names(sort_habits(habits, by="name")) == ["Read", "Study"])
    check("input list is unchanged", _names(habits) == ["Read", "Study"])


def test_sort_undone_first():
    habits = [new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01"),
              new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    ordered = sort_habits(habits, logs, "2026-11-07", by="undone_first")
    check("undone habit comes first", _names(ordered) == ["Read", "Study"])


def test_sort_by_streak():
    habits = [new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01"),
              new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    for day in ("2026-11-06", "2026-11-07"):
        set_done(logs, habits[1]["id"], day, True)
    ordered = sort_habits(habits, logs, "2026-11-07", by="streak")
    check("longest streak comes first", _names(ordered) == ["Study", "Read"])
    check("unknown sort keeps creation order",
          _names(sort_habits(habits, by="nope")) == ["Read", "Study"])


if __name__ == "__main__":
    test_sort_by_name()
    test_sort_undone_first()
    test_sort_by_streak()
    print(f"{PASSED} tests passed")
