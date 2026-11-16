"""Validation for habit names and minutes (pure logic, no Flet)."""

from app.habits import ICONS

from app.habits import CATEGORIES, ICONS

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
