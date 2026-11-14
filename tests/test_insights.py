"""Plain-script tests for app.insights.

Run:  python3 tests/test_insights.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.insights import (consistency_message, consistency_score,  # noqa: E402
                          needs_attention)
from app.tracker import set_done  # noqa: E402

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
    check("perfect consistency message", "Amazingly" in consistency_message(100))
    check("steady consistency message", "steady" in consistency_message(75))
    check("no ticks message", "No ticks" in consistency_message(0))


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
