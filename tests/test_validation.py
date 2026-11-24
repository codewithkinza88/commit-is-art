"""Plain-script tests for app.validation.

Run:  python3 tests/test_validation.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.validation import (MAX_NAME_LEN, validate_category,  # noqa: E402
                            validate_colour, validate_date_str,
                            validate_habit_days,                         validate_habit_name,
                            validate_icon, validate_minutes, validate_percent,
                            validate_note_text,                         validate_target_minutes,
                            validate_weekday, validate_weekly_target)

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


def test_validate_date_str():
    check("a good date passes through",
          validate_date_str("2026-11-21") == "2026-11-21")
    check("a date with spaces is trimmed",
          validate_date_str("  2026-11-21  ") == "2026-11-21")
    check("an impossible date becomes empty",
          validate_date_str("2026-02-30") == "")
    check("non-date text becomes empty",
          validate_date_str("tomorrow") == "")
    check("a non-text date becomes empty",
          validate_date_str(None) == "")


def test_validate_weekly_target():
    check("a normal weekly target passes through",
          validate_weekly_target(300) == 300)
    check("a blank weekly target becomes 0",
          validate_weekly_target("") == 0)
    check("a negative weekly target becomes 0",
          validate_weekly_target(-50) == 0)
    check("a weekly target over a week is capped at 10080",
          validate_weekly_target(20000) == 10080)
    check("a non-numeric weekly target becomes 0",
          validate_weekly_target("soon") == 0)


def test_validate_colour():
    check("a real app colour passes through",
          validate_colour("#F9A8D4") == "#F9A8D4")
    check("an unknown colour falls back to soft sky blue",
          validate_colour("#123456") == "#BDE0FE")
    check("a blank colour falls back to soft sky blue",
          validate_colour("") == "#BDE0FE")


def test_validate_weekday():
    check("Monday is 0 and Sunday is 6",
          validate_weekday(0) == 0 and validate_weekday(6) == 6)
    check("numeric text parses to a weekday",
          validate_weekday("3") == 3)
    check("out-of-range, junk and floats are -1",
          validate_weekday(7) == -1
          and validate_weekday("soon") == -1
          and validate_weekday(2.5) == -1
          and validate_weekday(True) == -1
          and validate_weekday(None) == -1)


def test_validate_habit_days():
    check("a normal weekday list passes through sorted",
          validate_habit_days([4, 0, 2]) == [0, 2, 4])
    check("duplicate weekdays are kept once",
          validate_habit_days([1, 1, 3]) == [1, 3])
    check("out-of-range weekdays are dropped",
          validate_habit_days([0, 7, -1, 6]) == [0, 6])
    check("junk entries are dropped, a non-list becomes []",
          validate_habit_days(["soon", None, True, 2.5, "3", 2]) == [2, 3]
          and validate_habit_days("Mon") == [])


def test_validate_percent():
    check("good percent", validate_percent(75) == (True, 75, ""))
    check("string percent", validate_percent("40") == (True, 40, ""))
    check("negative percent", validate_percent(-5)[0] is False)
    check("text percent", validate_percent("lots")[0] is False)
    check("too much percent capped",
          validate_percent(250) == (False, 100, "Percent cannot be more than 100"))


if __name__ == "__main__":
    main()
    test_validate_note_text()
    test_validate_date_str()
    test_validate_weekly_target()
    test_validate_habit_days()
    test_validate_weekday()
    test_validate_colour()
    test_validate_percent()
    print(f"{PASSED} tests passed")
