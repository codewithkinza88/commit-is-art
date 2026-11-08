"""Plain-script tests for app.motivation (pytest is not installed here).

Run:  python3 tests/test_motivation.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.motivation import message_for_percent, nightly_message, streak_message  # noqa: E402

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


if __name__ == "__main__":
    test_message_for_percent()
    test_nightly_message()
    test_streak_message()
    print(f"{PASSED} tests passed")
