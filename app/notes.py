"""Short daily notes for a habit (pure logic, no Flet).

Notes are stored as:
    notes = {"2026-11-10": {"<habit_id>": "Read chapter 3"}}
"""

MAX_NOTE_LEN = 200


def add_note(notes, habit_id, date_str, text):
    """Save a note (trimmed, capped at 200 chars). Returns the saved text."""
    text = (text or "").strip()[:MAX_NOTE_LEN]
    notes.setdefault(date_str, {})[habit_id] = text
    return text


def get_note(notes, habit_id, date_str):
    """The note for a habit on a date, or '' when there is none."""
    return notes.get(date_str, {}).get(habit_id, "")


def has_note(notes, habit_id, date_str):
    """True when a non-empty note exists for the habit on that date."""
    return bool(get_note(notes, habit_id, date_str).strip())
