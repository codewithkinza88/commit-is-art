"""Search habits by name or category (pure logic, no Flet)."""

from app.notes import find_notes, notes_for_habit

def find_habits(habits, query):
    """Habits whose name or category contains query (case-insensitive).

    A blank query returns all habits, in their original order.
    """
    q = (query or "").strip().lower()
    if not q:
        return list(habits)
    return [h for h in habits
            if q in (h.get("name") or "").lower()
            or q in (h.get("category") or "").lower()]


def count_matches(habits, query):
    """How many habits match the query."""
    return len(find_habits(habits, query))


def find_habits_by_icon(habits, icon):
    """Habits using a given icon, in their original order."""
    return [h for h in (habits or []) if h.get("icon") == icon]


def find_habits_by_effort(habits, min_minutes):
    """Habits whose daily target is at least min_minutes.

    A habit's effort is its daily target in minutes; a 0-target
    habit only matches when min_minutes is 0. Original order kept.
    """
    minimum = max(0, int(min_minutes or 0))
    return [h for h in (habits or [])
            if int(h.get("target_minutes") or 0) >= minimum]


def find_habits_by_category(habits, category):
    """Habits in one category, case-insensitive, creation order.

    The search-module form of habits_by_category; [] when no habit
    is in the category (or there are no habits).
    """
    wanted = (category or "").strip().lower()
    if not wanted:
        return []
    return [h for h in (habits or [])
            if (h.get("category") or "").lower() == wanted]

def count_notes_matching(notes, query):
    """How many notes match the query (0 when none match).

    The count form of find_notes; a blank query matches nothing.
    """
    return len(find_notes(notes, query))

def find_notes_by_habit(notes, habit_id):
    """(date, text) pairs for one habit, oldest date first.

    The search-module form of notes_for_habit; [] when the habit
    has no notes.
    """
    return notes_for_habit(notes or {}, habit_id)
