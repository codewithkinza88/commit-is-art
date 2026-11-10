"""Plain-script tests for app.schedule.

Run:  python3 tests/test_schedule.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.schedule import habits_due_on, weekday_name  # noqa: E402

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


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
