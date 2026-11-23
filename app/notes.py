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


def longest_note(notes, habit_id):
    """(date, text) of the habit's longest non-empty note.

    The most recent note wins a tie. Returns ("", "") when the habit
    has no notes.
    """
    best_date, best_text = "", ""
    for date_str, text in notes_for_habit(notes, habit_id):
        if len(text) > len(best_text) or (
                len(text) == len(best_text) and date_str > best_date):
            best_date, best_text = date_str, text
    return best_date, best_text


def notes_in_range(notes, start_date, end_date):
    """(date, habit_id, text) for non-empty notes in a date range, inclusive.

    Ordered by date, then habit id; [] when nothing was written in
    the range.
    """
    found = []
    for date_str in sorted((notes or {}).keys()):
        if date_str < start_date or date_str > end_date:
            continue
        day_notes = notes.get(date_str) or {}
        if not isinstance(day_notes, dict):
            continue
        for habit_id in sorted(day_notes.keys()):
            text = day_notes.get(habit_id) or ""
            if isinstance(text, str) and text.strip():
                found.append((date_str, habit_id, text))
    return found


def notes_for_habit_this_week(notes, habit_id, end_date=None):
    """(date, text) pairs for one habit in the 7 days to end_date.

    Non-empty notes only, oldest date first; [] when the habit
    wrote nothing that week. Mirror of notes_for_habit, but for
    the last 7 days instead of all time.
    """
    from datetime import date as _date
    from datetime import timedelta as _timedelta

    if isinstance(end_date, str):
        end = _date.fromisoformat(end_date)
    else:
        end = end_date or _date.today()
    start = (end - _timedelta(days=6)).isoformat()
    return [(date_str, text)
            for date_str, text in notes_for_habit(notes or {}, habit_id)
            if start <= date_str <= end.isoformat()]


def notes_for_habit_this_month(notes, habit_id, year, month):
    """(date, text) pairs for one habit in a calendar month.

    Non-empty notes only, oldest date first; [] when the habit
    wrote nothing that month. Mirror of notes_for_habit_this_week,
    but for a whole month instead of 7 days.
    """
    import calendar as _calendar

    days_in_month = _calendar.monthrange(year, month)[1]
    start = f"{year:04d}-{month:02d}-01"
    end = f"{year:04d}-{month:02d}-{days_in_month:02d}"
    return [(date_str, text)
            for date_str, text in notes_for_habit(notes or {}, habit_id)
            if start <= date_str <= end]


def notes_in_month(notes, year, month):
    """(date, habit_id, text) for non-empty notes in a calendar month.

    Ordered by date, then habit id; [] when nothing was written
    that month. Mirror of notes_in_range, but for a whole month.
    """
    import calendar as _calendar

    days_in_month = _calendar.monthrange(year, month)[1]
    start = f"{year:04d}-{month:02d}-01"
    end = f"{year:04d}-{month:02d}-{days_in_month:02d}"
    return notes_in_range(notes or {}, start, end)


def total_notes_count(notes):
    """How many non-empty notes exist across all dates and habits.

    Blank notes (spaces only) do not count; 0 when there are no
    notes at all.
    """
    total = 0
    for day_notes in (notes or {}).values():
        if not isinstance(day_notes, dict):
            continue
        for text in day_notes.values():
            if isinstance(text, str) and text.strip():
                total += 1
    return total


def notes_count_this_week(notes, end_date=None):
    """How many non-empty notes were written in the 7 days to end_date.

    Counts notes_in_range over the 7 days ending on end_date
    (default today); 0 when nothing was written that week.
    """
    from datetime import date as _date
    from datetime import timedelta as _timedelta

    if isinstance(end_date, str):
        end = _date.fromisoformat(end_date)
    else:
        end = end_date or _date.today()
    start = (end - _timedelta(days=6)).isoformat()
    return len(notes_in_range(notes or {}, start, end.isoformat()))


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
