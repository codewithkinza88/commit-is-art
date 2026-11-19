"""Plain-script tests for app.validation.

Run:  python3 tests/test_validation.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.validation import (MAX_NAME_LEN, validate_category,  # noqa: E402
                            validate_habit_name, validate_icon,
                            validate_minutes, validate_note_text,
                            validate_target_minutes)

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
    check("good icon passes", validate_icon("📚") == "📚")
    check("unknown icon falls back to seedling", validate_icon("🚀") == "🌱")
    check("blank icon falls back to seedling", validate_icon("") == "🌱")
    check("good category passes", validate_category("Study") == "Study")
    check("unknown category falls back to Daily Life",
          validate_category("Cooking") == "Daily Life")
    check("blank category falls back to Daily Life",
          validate_category("") == "Daily Life")
    check("good target minutes passes", validate_target_minutes(60) == 60)
    check("blank target minutes is 0", validate_target_minutes("") == 0)
    check("negative target minutes is 0", validate_target_minutes(-10) == 0)
    check("text target minutes is 0", validate_target_minutes("lots") == 0)
    check("huge target minutes caps at a day",
          validate_target_minutes(9999) == 1440)


def test_validate_note_text():
    check("note text is trimmed",
          validate_note_text("  Read chapter 3  ") == "Read chapter 3")
    check("blank note text becomes empty",
          validate_note_text("   ") == "")
    check("long note text is capped at 200 chars",
          len(validate_note_text("x" * 250)) == 200)
    check("non-text note becomes empty",
          validate_note_text(None) == "")


if __name__ == "__main__":
    main()
    test_validate_note_text()
    print(f"{PASSED} tests passed")
