"""Plain-script tests for app.notes.

Run:  python3 tests/test_notes.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.notes import (MAX_NOTE_LEN, add_note, count_notes,  # noqa: E402
                       count_notes_for_day, find_notes, get_note, has_note,
                       latest_note, latest_note_text, longest_note,
                                                             notes_count_this_week,
                       notes_for_day, notes_for_habit,
                                          notes_for_habit_this_month,
                       notes_for_habit_this_week, notes_in_month,
                       notes_in_range, notes_for_habit_last_7_days,
                       total_notes_count)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    notes = {}
    check("add and get", add_note(notes, "h1", "2026-11-10", "Read chapter 3") == "Read chapter 3")
    check("get saved note", get_note(notes, "h1", "2026-11-10") == "Read chapter 3")
    check("missing note is empty", get_note(notes, "h2", "2026-11-10") == "")
    check("has note", has_note(notes, "h1", "2026-11-10") is True)
    check("no note", has_note(notes, "h1", "2026-11-11") is False)
    check("trims whitespace", add_note(notes, "h1", "2026-11-11", "  done  ") == "done")
    check("caps long notes", len(add_note(notes, "h1", "2026-11-12", "x" * 500)) == MAX_NOTE_LEN)
    check("blank note clears", add_note(notes, "h1", "2026-11-10", "   ") == "")
    check("count notes across days", count_notes(notes, "h1") == 2)
    check("count notes for other habit", count_notes(notes, "h2") == 0)
    check("count notes with no store", count_notes(None, "h1") == 0)


def test_latest_note():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-11", "Mid note")
    check("latest note is the newest",
          latest_note(notes, "h1") == ("2026-11-12", "Finished chapter 4"))
    add_note(notes, "h1", "2026-11-13", "   ")
    check("latest note skips blank notes",
          latest_note(notes, "h1") == ("2026-11-12", "Finished chapter 4"))
    check("latest note with no notes is empty",
          latest_note(notes, "h2") == ("", ""))


def test_notes_for_day():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-11", "Finished chapter 4")
    add_note(notes, "h3", "2026-11-10", "   ")
    check("notes for a day lists both habits",
          notes_for_day(notes, "2026-11-10") == [("h1", "Read chapter 3"),
                                                  ("h2", "Watered the plants")])
    check("notes for a day skips blank notes",
          len(notes_for_day(notes, "2026-11-10")) == 2)
    check("notes for an empty day is empty",
          notes_for_day(notes, "2026-11-12") == [])


def test_count_notes_for_day():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h3", "2026-11-10", "   ")
    add_note(notes, "h1", "2026-11-11", "Finished chapter 4")
    check("count notes for a day counts two non-empty notes",
          count_notes_for_day(notes, "2026-11-10") == 2)
    check("count notes for a day with one note is 1",
          count_notes_for_day(notes, "2026-11-11") == 1)
    check("count notes for an empty day is 0",
          count_notes_for_day(notes, "2026-11-12") == 0)


def test_find_notes():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3 of the book")
    add_note(notes, "h2", "2026-11-11", "Chapter 4 was hard")
    add_note(notes, "h1", "2026-11-12", "Watered the plants")
    found = find_notes(notes, "chapter")
    check("find_notes matches case-insensitively", len(found) == 2)
    check("find_notes returns date, habit and text",
          found[0] == ("2026-11-10", "h1", "Read chapter 3 of the book"))
    check("find_notes matches an uppercase query",
          len(find_notes(notes, "CHAPTER")) == 2)
    check("find_notes finds one match",
          find_notes(notes, "plants") ==
          [("2026-11-12", "h1", "Watered the plants")])
    check("find_notes finds nothing for no match",
          find_notes(notes, "banana") == [])
    check("blank query finds nothing",
          find_notes(notes, "   ") == [])


def test_notes_for_habit():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes for one habit are oldest first",
          notes_for_habit(notes, "h1") ==
          [("2026-11-10", "Read chapter 3"),
           ("2026-11-12", "Finished chapter 4")])
    check("notes for a habit with no notes is empty",
          notes_for_habit(notes, "h9") == [])
    check("notes for one habit skips blank notes",
          len(notes_for_habit(notes, "h1")) == 2)


def test_longest_note():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4 and started 5")
    add_note(notes, "h2", "2026-11-11", "A very long note indeed, longer")
    check("longest note is the longest text",
          longest_note(notes, "h1")
          == ("2026-11-12", "Finished chapter 4 and started 5"))
    add_note(notes, "h1", "2026-11-13", "Finished chapter 4 and started 5")
    check("a tie goes to the most recent note",
          longest_note(notes, "h1")[0] == "2026-11-13")
    check("a habit with no notes has no longest note",
          longest_note(notes, "h9") == ("", ""))


def test_notes_in_range():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes in range cover both days in order",
          notes_in_range(notes, "2026-11-10", "2026-11-11") ==
          [("2026-11-10", "h1", "Read chapter 3"),
           ("2026-11-10", "h2", "Watered the plants")])
    check("notes in range skip days outside it",
          notes_in_range(notes, "2026-11-12", "2026-11-12") ==
          [("2026-11-12", "h1", "Finished chapter 4")])
    check("notes in range skip blank notes",
          len(notes_in_range(notes, "2026-11-10", "2026-11-12")) == 3)
    check("an empty range has no notes",
          notes_in_range(notes, "2026-11-13", "2026-11-14") == [])


def test_notes_for_habit_this_month():
    notes = {}
    add_note(notes, "h1", "2026-11-03", "Read chapter 3")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-10-31", "Too old to count")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes this month for h1 are the two in-month notes",
          notes_for_habit_this_month(notes, "h1", 2026, 11) ==
          [("2026-11-03", "Read chapter 3"),
           ("2026-11-12", "Finished chapter 4")])
    check("another habit's notes do not leak in",
          notes_for_habit_this_month(notes, "h2", 2026, 11) ==
          [("2026-11-10", "Watered the plants")])
    check("a habit with no notes this month gives []",
          notes_for_habit_this_month(notes, "h1", 2026, 12) == [])


def test_notes_in_month():
    notes = {}
    add_note(notes, "h1", "2026-11-03", "Read chapter 3")
    add_note(notes, "h2", "2026-11-03", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-10-31", "Too old to count")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes in the month are ordered by date then habit",
          notes_in_month(notes, 2026, 11) ==
          [("2026-11-03", "h1", "Read chapter 3"),
           ("2026-11-03", "h2", "Watered the plants"),
           ("2026-11-12", "h1", "Finished chapter 4")])
    check("notes outside the month do not count",
          notes_in_month(notes, 2026, 10) ==
          [("2026-10-31", "h1", "Too old to count")])
    check("a month with no notes gives []",
          notes_in_month({}, 2026, 11) == [])


def test_latest_note_text():
    notes = {}
    add_note(notes, "h1", "2026-11-03", "Read chapter 3")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    check("the latest note text is the newest one",
          latest_note_text(notes, "h1") == "Finished chapter 4")
    check("another habit has its own latest text",
          latest_note_text(notes, "h2") == "Watered the plants")
    check("a habit with no notes has empty text",
          latest_note_text(notes, "h3") == "")


def test_notes_for_habit_this_week():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-01", "Too old to count")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes this week for h1 are the two in-window notes",
          notes_for_habit_this_week(notes, "h1", "2026-11-12") ==
          [("2026-11-10", "Read chapter 3"),
           ("2026-11-12", "Finished chapter 4")])
    check("another habit's notes do not leak in",
          notes_for_habit_this_week(notes, "h2", "2026-11-12") ==
          [("2026-11-10", "Watered the plants")])
    check("a habit with no notes this week gives []",
          notes_for_habit_this_week(notes, "h9", "2026-11-12") == [])


def test_notes_for_habit_last_7_days():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-01", "Too old to count")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes in the last 7 days for h1 are the two in-window notes",
          notes_for_habit_last_7_days(notes, "h1", "2026-11-12") ==
          [("2026-11-10", "Read chapter 3"),
           ("2026-11-12", "Finished chapter 4")])
    check("another habit's notes do not leak in",
          notes_for_habit_last_7_days(notes, "h2", "2026-11-12") ==
          [("2026-11-10", "Watered the plants")])
    check("a habit with no notes in the window gives []",
          notes_for_habit_last_7_days(notes, "h9", "2026-11-12") == [])


def test_total_notes_count():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-01", "Too old to count")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("total notes counts all four real notes",
          total_notes_count(notes) == 4)
    check("total notes is 0 with no notes",
          total_notes_count({}) == 0)
    check("total notes is 0 when only blanks exist",
          total_notes_count({"2026-11-11": {"h1": "   "}}) == 0)


def test_notes_count_this_week():
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    add_note(notes, "h1", "2026-11-01", "Too old to count")
    add_note(notes, "h1", "2026-11-11", "   ")
    check("notes this week counts the 7-day window",
          notes_count_this_week(notes, "2026-11-12") == 3)
    check("notes this week skips blank notes",
          notes_count_this_week(notes, "2026-11-11") == 2)
    check("notes this week is 0 with no notes",
          notes_count_this_week({}, "2026-11-12") == 0)


if __name__ == "__main__":
    main()
    test_latest_note()
    test_notes_for_day()
    test_count_notes_for_day()
    test_find_notes()
    test_notes_for_habit()
    test_longest_note()
    test_notes_in_range()
    test_notes_count_this_week()
    test_notes_for_habit_this_week()
    test_notes_for_habit_last_7_days()
    test_notes_for_habit_this_month()
    test_notes_in_month()
    test_latest_note_text()
    test_total_notes_count()
    print(f"{PASSED} tests passed")
