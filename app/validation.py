"""Validation for habit names and minutes (pure logic, no Flet)."""

from app.habits import ICONS

from app.habits import CATEGORIES, ICONS
from app.notes import MAX_NOTE_LEN

MAX_NAME_LEN = 60
MAX_MINUTES = 1440  # a whole day


def validate_habit_name(name):
    """(is_valid, clean_name, error) for a habit name."""
    clean = (name or "").strip()
    if not clean:
        return False, "", "Habit name cannot be empty"
    if len(clean) > MAX_NAME_LEN:
        return False, clean[:MAX_NAME_LEN], "Habit name is too long"
    return True, clean, ""


def validate_icon(icon):
    """The icon itself when it is one of the app icons, else a seedling."""
    return icon if icon in ICONS else "🌱"


def validate_category(category):
    """The category itself when it is one of the app categories,
    else "Daily Life"."""
    return category if category in CATEGORIES else "Daily Life"



def validate_target_minutes(value):
    """A daily target in minutes, cleaned to a whole number 0..1440.

    Blank or non-numeric input becomes 0; negatives become 0 and
    anything over a day is capped at 1440.
    """
    try:
        minutes = int(value or 0)
    except (TypeError, ValueError):
        return 0
    return max(0, min(MAX_MINUTES, minutes))


MAX_WEEKLY_MINUTES = 10080  # a whole week (7 x 1440)


def validate_weekly_target(value):
    """A weekly target in minutes, cleaned to a whole number 0..10080.

    Blank or non-numeric input becomes 0; negatives become 0 and
    anything over a week is capped at 10080.
    """
    try:
        minutes = int(value or 0)
    except (TypeError, ValueError):
        return 0
    return max(0, min(MAX_WEEKLY_MINUTES, minutes))


def validate_note_text(text):
    """A note cleaned for saving: stripped, capped at MAX_NOTE_LEN.

    Blank or non-text input becomes "".
    """
    if not isinstance(text, str):
        return ""
    return text.strip()[:MAX_NOTE_LEN]


def validate_search_query(text):
    """A search query cleaned for use: stripped, "" when blank or None.

    The clean-or-"" shape of validate_note_text, for the notes
    and habits search box.
    """
    if not isinstance(text, str):
        return ""
    return text.strip()


def validate_date_str(text):
    """A date cleaned to ISO YYYY-MM-DD, or "" when it is not a date.

    Whitespace is stripped; impossible dates like 2026-02-30 and
    non-date text are rejected. Handy before a date is saved anywhere.
    """
    from datetime import date as _date

    if not isinstance(text, str):
        return ""
    try:
        return _date.fromisoformat(text.strip()).isoformat()
    except ValueError:
        return ""


def validate_colour(colour):
    """The colour itself when it is one of the app colours,
    else the soft sky blue "#BDE0FE"."""
    from app.habits import COLOURS

    return colour if colour in COLOURS else "#BDE0FE"


def validate_habit_days(days):
    """A habit's weekday list, cleaned to sorted unique ints 0..6.

    Monday=0 .. Sunday=6; invalid entries (out of range, bools,
    floats, non-numeric text) are dropped; a non-list becomes [].
    Keeps the habit's due days safe before they are saved anywhere.
    """
    if not isinstance(days, list):
        return []
    clean = set()
    for day in days:
        if isinstance(day, bool):
            continue
        if isinstance(day, int):
            value = day
        elif isinstance(day, str) and day.strip().isdigit():
            value = int(day.strip())
        else:
            continue
        if 0 <= value <= 6:
            clean.add(value)
    return sorted(clean)


def validate_weekday(value):
    """A weekday number, cleaned to 0 (Mon) .. 6 (Sun).

    Accepts ints and numeric text ("3" -> 3); -1 when the value
    is out of range, a bool, a float, or unparseable — the same
    -1 that weekday_of returns for a bad date.
    """
    if isinstance(value, bool):
        return -1
    if isinstance(value, int):
        weekday = value
    elif isinstance(value, str) and value.strip().lstrip("-").isdigit():
        weekday = int(value.strip())
    else:
        return -1
    return weekday if 0 <= weekday <= 6 else -1


def validate_minutes(value):
    """(is_valid, minutes, error) for a minutes value."""
    try:
        minutes = int(value)
    except (TypeError, ValueError):
        return False, 0, "Minutes must be a number"
    if minutes < 0:
        return False, 0, "Minutes cannot be negative"
    if minutes > MAX_MINUTES:
        return False, MAX_MINUTES, "Minutes cannot be more than a day"
    return True, minutes, ""


MAX_PERCENT = 100


def validate_percent(value):
    """(is_valid, percent, error) for a percent value 0..100.

    Mirror of validate_minutes, but for percents: non-numeric
    input and negatives are invalid, and anything over 100 is
    capped at 100.
    """
    try:
        percent = int(value)
    except (TypeError, ValueError):
        return False, 0, "Percent must be a number"
    if percent < 0:
        return False, 0, "Percent cannot be negative"
    if percent > MAX_PERCENT:
        return False, MAX_PERCENT, "Percent cannot be more than 100"
    return True, percent, ""


def validate_habit_id(value):
    """(is_valid, clean_id, error) for a habit id.

    Mirror of validate_habit_name without the length cap: a
    non-empty string, stripped; blank or non-text ids are invalid.
    """
    if not isinstance(value, str):
        return False, "", "Habit id must be text"
    clean = value.strip()
    if not clean:
        return False, "", "Habit id cannot be empty"
    return True, clean, ""
