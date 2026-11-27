"""Plain-script tests for app.search.

Run:  python3 tests/test_search.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.search import (count_matches, find_habits,  # noqa: E402
                        find_habits_by_effort, find_habits_by_icon,
                        find_habits_by_category, count_notes_matching,
                        find_notes_by_habit)

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


def test_count_notes_matching():
    notes = {"2026-11-07": {"h1": "Studied DSA"},
             "2026-11-08": {"h1": "Read a book",
                            "h2": "Studied DSA again"}}
    check("counts the notes matching a word",
          count_notes_matching(notes, "DSA") == 2)
    check("counts a single matching note",
          count_notes_matching(notes, "book") == 1)
    check("a blank query matches nothing",
          count_notes_matching(notes, "") == 0)


def test_find_notes_by_habit():
    notes = {"2026-11-07": {"h1": "Studied DSA"},
             "2026-11-08": {"h1": "Read a book",
                            "h2": "Studied DSA again"}}
    check("lists one habit's notes oldest first",
          find_notes_by_habit(notes, "h1")
          == [("2026-11-07", "Studied DSA"),
              ("2026-11-08", "Read a book")])
    check("another habit's notes are separate",
          find_notes_by_habit(notes, "h2")
          == [("2026-11-08", "Studied DSA again")])
    check("an unknown habit has no notes",
          find_notes_by_habit(notes, "h9") == [])


if __name__ == "__main__":
    main()
    test_find_habits_by_category()
    test_count_notes_matching()
    test_find_notes_by_habit()
    print(f"{PASSED} tests passed")
