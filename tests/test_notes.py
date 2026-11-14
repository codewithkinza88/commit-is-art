"""Plain-script tests for app.notes.

Run:  python3 tests/test_notes.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.notes import MAX_NOTE_LEN, add_note, count_notes, get_note, has_note  # noqa: E402

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


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
