"""Plain-script tests for app.notes.

Run:  python3 tests/test_notes.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.notes import (MAX_NOTE_LEN, add_note, count_notes,  # noqa: E402
                       count_notes_for_day, get_note, has_note,
                       latest_note, notes_for_day)

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


if __name__ == "__main__":
    main()
    test_latest_note()
    test_notes_for_day()
    test_count_notes_for_day()
    print(f"{PASSED} tests passed")
