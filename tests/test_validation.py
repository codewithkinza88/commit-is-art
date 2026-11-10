"""Plain-script tests for app.validation.

Run:  python3 tests/test_validation.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.validation import MAX_NAME_LEN, validate_habit_name, validate_minutes  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    check("good name", validate_habit_name("Study") == (True, "Study", ""))
    check("trims name", validate_habit_name("  Read  ")[1] == "Read")
    check("blank name invalid", validate_habit_name("   ")[0] is False)
    check("long name invalid", validate_habit_name("x" * 61)[0] is False)
    check("long name trimmed", len(validate_habit_name("x" * 61)[1]) == MAX_NAME_LEN)
    check("good minutes", validate_minutes(45) == (True, 45, ""))
    check("string minutes", validate_minutes("30") == (True, 30, ""))
    check("negative minutes", validate_minutes(-5)[0] is False)
    check("text minutes", validate_minutes("lots")[0] is False)
    check("too many minutes capped", validate_minutes(9999)[1] == 1440)


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
