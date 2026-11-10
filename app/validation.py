"""Validation for habit names and minutes (pure logic, no Flet)."""

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
