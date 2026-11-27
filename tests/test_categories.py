"""Plain-script tests for app.categories (pytest is not installed here).

Run:  python3 tests/test_categories.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.categories import best_category, category_summary, legend_categories, total_minutes_by_category, categories_used, count_categories  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def _habits():
    return [
        new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-01"),
        new_habit("Water", "Health", 0, "💧", "#BDE0FE", "2026-11-01"),
    ]


def test_category_summary():
    habits = _habits()
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    summary = category_summary(logs, habits, "2026-11-07")
    check("study is 100%", summary["Study"]["percent"] == 100)
    check("study minutes is 45", summary["Study"]["minutes"] == 45)
    check("books is 0%", summary["Books"]["percent"] == 0)
    check("empty habits gives empty summary", category_summary({}, [], "2026-11-07") == {})


def test_best_category():
    habits = _habits()
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    check("best category is Study",
          best_category(logs, habits, "2026-11-07")["category"] == "Study")
    check("no habits gives no best category",
          best_category({}, [], "2026-11-07") is None)


def test_total_minutes_by_category():
    habits = _habits()
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[1]["id"], "2026-11-07", 20)
    minutes = total_minutes_by_category(logs, habits, "2026-11-07")
    check("study minutes is 45", minutes["Study"] == 45)
    check("books minutes is 20", minutes["Books"] == 20)
    check("health minutes is 0", minutes["Health"] == 0)


def test_legend_categories():
    habits = [new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01"),
              new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01"),
              new_habit("Revise", "Study", 0, "✍️", "#FFE5A3", "2026-11-01")]
    check("legend lists each present category once",
          legend_categories(habits) == ["Study", "Books"])
    check("legend is empty with no habits",
          legend_categories([]) == [])


def test_categories_used():
    habits = [
        new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-01"),
        new_habit("Water", "Health", 0, "💧", "#BDE0FE", "2026-11-01"),
    ]
    check("lists the used categories sorted",
          categories_used(habits) == ["Books", "Health", "Study"])
    check("a repeated category is listed once",
          categories_used(habits[:1] + habits[:1]) == ["Study"])
    check("no habits means no categories",
          categories_used([]) == [])


def test_count_categories():
    habits = [
        new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-01"),
        new_habit("Water", "Health", 0, "💧", "#BDE0FE", "2026-11-01"),
    ]
    check("counts three distinct categories",
          count_categories(habits) == 3)
    check("two habits in one category count once",
          count_categories(habits[:1] + habits[:1]) == 1)
    check("no habits means no categories",
          count_categories([]) == 0)


if __name__ == "__main__":
    test_category_summary()
    test_best_category()
    test_total_minutes_by_category()
    test_legend_categories()
    test_categories_used()
    test_count_categories()
    print(f"{PASSED} tests passed")
