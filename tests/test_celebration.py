"""Plain-script tests for app.celebration.

Run:  python3 tests/test_celebration.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.celebration import (days_to_next_milestone, is_milestone,  # noqa: E402
                             milestone_message)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    check("week milestone", milestone_message(7) == "One whole week! 🌸")
    check("month milestone", "month" in milestone_message(30))
    check("hundred milestone", is_milestone(100) is True)
    check("ordinary day", milestone_message(5) == "")
    check("ordinary not milestone", is_milestone(5) is False)
    check("zero is not milestone", milestone_message(0) == "")


def test_days_to_next_milestone():
    check("5 days in, the 7-day milestone is 2 away",
          days_to_next_milestone(5) == (7, 2))
    check("a milestone day points at the next one",
          days_to_next_milestone(7) == (14, 7))
    check("past the last milestone there is no next one",
          days_to_next_milestone(100) is None)


if __name__ == "__main__":
    main()
    test_days_to_next_milestone()
    print(f"{PASSED} tests passed")
