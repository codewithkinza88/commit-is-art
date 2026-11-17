"""Plain-script tests for app.motivation (pytest is not installed here).

Run:  python3 tests/test_motivation.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.motivation import (evening_message, message_for_percent,  # noqa: E402
                            morning_message, nightly_message,
                            streak_message)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_message_for_percent():
    check("100% is perfect", "Perfect" in message_for_percent(100))
    check("80% is close to perfect", "close" in message_for_percent(80))
    check("50% is halfway", "Halfway" in message_for_percent(50))
    check("0% is a fresh seed", "fresh seed" in message_for_percent(0))
    check("percent over 100 is clamped", "Perfect" in message_for_percent(150))


def test_nightly_message():
    summary = {"percent": 100, "total_minutes": 90}
    check("nightly perfect day mentions minutes",
          "90 minutes" in nightly_message(summary))
    check("nightly empty day still has a message",
          len(nightly_message({"percent": 0, "total_minutes": 0})) > 0)


def test_streak_message():
    check("7-day streak mentions a week", "week" in streak_message(7))
    check("3-day streak mentions streak", "streak" in streak_message(3))
    check("0 streak encourages starting", "start" in streak_message(0))


def test_morning_message():
    check("morning with no habits suggests planting one",
          "plant" in morning_message(0, 0))
    check("morning all done celebrates",
          "All done" in morning_message(3, 3))
    check("morning none done counts the habits to water",
          "3 habits" in morning_message(0, 3))
    check("morning partly done shows the count",
          "1 of 3" in morning_message(1, 3))


def test_evening_message():
    check("evening all done celebrates the garden",
          "blooming" in evening_message(3, 3))
    check("evening none done looks to tomorrow",
          "fresh start" in evening_message(0, 3))
    check("evening partly done shows the count",
          "1 of 3" in evening_message(1, 3))
    check("evening with no habits mentions a fresh seed",
          "fresh seed" in evening_message(0, 0))


if __name__ == "__main__":
    test_message_for_percent()
    test_nightly_message()
    test_streak_message()
    test_morning_message()
    test_evening_message()
    print(f"{PASSED} tests passed")
