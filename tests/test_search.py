"""Plain-script tests for app.search.

Run:  python3 tests/test_search.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.search import (count_matches, find_habits,  # noqa: E402
                        find_habits_by_effort, find_habits_by_icon,
                        find_habits_by_category)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    habits = [
        new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read a book", "Books", 30, "📖", "#FBCFE8", "2026-11-01"),
        new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01"),
    ]
    check("name match", len(find_habits(habits, "dsa")) == 1)
    check("case-insensitive", find_habits(habits, "BOOK")[0]["name"] == "Read a book")
    check("category match", len(find_habits(habits, "health")) == 1)
    check("no match is empty", find_habits(habits, "yoga") == [])
    check("blank query returns all", len(find_habits(habits, "  ")) == 3)
    check("count matches", count_matches(habits, "study") == 1)
    check("empty list", find_habits([], "study") == [])
    check("find by icon returns the matching habit",
          [h["name"] for h in find_habits_by_icon(habits, "📚")] == ["Study - DSA"])
    check("find by icon with no match is empty",
          find_habits_by_icon(habits, "🚀") == [])
    check("find by icon on an empty list is empty",
          find_habits_by_icon([], "📚") == [])
    check("find by effort returns habits at or above the threshold",
          [h["name"] for h in find_habits_by_effort(habits, 30)]
          == ["Study - DSA", "Read a book"])
    check("find by effort with a high threshold is narrow",
          [h["name"] for h in find_habits_by_effort(habits, 60)]
          == ["Study - DSA"])
    check("find by effort with 0 returns all habits",
          len(find_habits_by_effort(habits, 0)) == 3)


def test_find_habits_by_category():
    habits = [
        new_habit("Study - DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read a book", "Books", 30, "📖", "#FBCFE8", "2026-11-01"),
        new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-01"),
    ]
    check("finds the habits in one category",
          [h["name"] for h in find_habits_by_category(habits, "study")]
          == ["Study - DSA"])
    check("the match is case-insensitive",
          [h["name"] for h in find_habits_by_category(habits, "BOOKS")]
          == ["Read a book"])
    check("an empty category finds nothing",
          find_habits_by_category(habits, "Mind") == [])


if __name__ == "__main__":
    main()
    test_find_habits_by_category()
    print(f"{PASSED} tests passed")
