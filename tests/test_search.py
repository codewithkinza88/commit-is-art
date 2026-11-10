"""Plain-script tests for app.search.

Run:  python3 tests/test_search.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.search import count_matches, find_habits  # noqa: E402

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


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
