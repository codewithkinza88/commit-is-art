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


def latest_note(notes, habit_id):
    """(date, text) of the habit's most recent non-empty note.

    Returns ("", "") when the habit has no notes.
    """
    latest_date = ""
    latest_text = ""
    for date_str, day_notes in (notes or {}).items():
        if not isinstance(day_notes, dict):
            continue
        text = day_notes.get(habit_id, "")
        if isinstance(text, str) and text.strip() and date_str > latest_date:
            latest_date, latest_text = date_str, text
    return latest_date, latest_text


def notes_for_habit(notes, habit_id):
    """(date, text) pairs for one habit, oldest date first.

    Non-empty notes only; [] when the habit has no notes.
    """
    found = []
    for date_str in sorted((notes or {}).keys()):
        day_notes = notes.get(date_str) or {}
        if not isinstance(day_notes, dict):
            continue
        text = day_notes.get(habit_id, "")
        if isinstance(text, str) and text.strip():
            found.append((date_str, text))
    return found


def count_notes(notes, habit_id):
    """How many non-empty notes a habit has across all dates."""
    total = 0
    for day_notes in (notes or {}).values():
        if isinstance(day_notes, dict):
            text = day_notes.get(habit_id, "")
            if isinstance(text, str) and text.strip():
                total += 1
    return total


def notes_for_day(notes, date_str):
    """Non-empty notes for one date, as (habit_id, text) pairs.

    In the order they were stored; [] when the date has no notes.
    """
    day_notes = (notes or {}).get(date_str, {})
    if not isinstance(day_notes, dict):
        return []
    return [(habit_id, text) for habit_id, text in day_notes.items()
            if isinstance(text, str) and text.strip()]


def count_notes_for_day(notes, date_str):
    """How many non-empty notes were written on one date (0 when none)."""
    return len(notes_for_day(notes, date_str))


def find_notes(notes, query):
    """(date, habit_id, text) for notes whose text contains the query,
    case-insensitive. [] for a blank query. Ordered by date, then
    habit id.
    """
    query = (query or "").strip().lower()
    if not query:
        return []
    found = []
    for date_str in sorted((notes or {}).keys()):
        day_notes = notes.get(date_str) or {}
        if not isinstance(day_notes, dict):
            continue
        for habit_id in sorted(day_notes.keys()):
            text = day_notes.get(habit_id) or ""
            if isinstance(text, str) and text.strip() and query in text.lower():
                found.append((date_str, habit_id, text))
    return found
