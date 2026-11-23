"""Plain-script tests for app.celebration.

Run:  python3 tests/test_celebration.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.celebration import (celebration_for, days_to_next_milestone,  # noqa: E402
                             is_milestone,
                             milestone_message, milestones_reached,
                             next_milestone_message)

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


def test_celebration_for():
    check("a 7-day streak celebrates its milestone",
          celebration_for(7) == {"emoji": "🌷",
                                 "message": "One whole week! 🌸"})
    check("a 3-day streak is growing, with a growing emoji",
          celebration_for(3) == {"emoji": "🪴",
                                 "message": "3 days and growing!"})
    check("a fresh streak sprouts",
          celebration_for(0) == {"emoji": "🌱",
                                 "message": "0 days and growing!"})


def test_next_milestone_message():
    check("5 days in, 2 to go to a 7-day streak",
          next_milestone_message(5) == "🎯 2 more day(s) to a 7-day streak!")
    check("a milestone day looks ahead to the next one",
          next_milestone_message(7) == "🎯 7 more day(s) to a 14-day streak!")
    check("past the last milestone there is no next message",
          next_milestone_message(100) == "")


def test_milestones_reached():
    check("a 14-day streak reached 7 and 14",
          milestones_reached(14) == [7, 14])
    check("a 6-day streak reached nothing yet",
          milestones_reached(6) == [])
    check("a 100-day streak reached every milestone",
          milestones_reached(100) == [7, 14, 30, 100])


if __name__ == "__main__":
    main()
    test_days_to_next_milestone()
    test_milestones_reached()
    test_next_milestone_message()
    test_celebration_for()
    print(f"{PASSED} tests passed")
