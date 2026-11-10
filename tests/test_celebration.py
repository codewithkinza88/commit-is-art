"""Plain-script tests for app.celebration.

Run:  python3 tests/test_celebration.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.celebration import is_milestone, milestone_message  # noqa: E402

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


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
