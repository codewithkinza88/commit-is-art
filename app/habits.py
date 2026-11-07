"""Habit definitions and list operations (pure logic, no Flet).

A habit is a plain dict:
    {
        "id": "h1",                      # unique string
        "name": "Study - DSA / course",  # user-chosen name
        "category": "Study",             # Study, Books, Health, Mind, Daily Life
        "target_minutes": 60,            # optional daily target, 0 = no target
        "icon": "📚",                     # emoji chosen by the user
        "colour": "#F9A8D4",             # pastel colour chosen by the user
        "created_date": "2026-11-07",    # ISO date YYYY-MM-DD
    }
"""

import uuid
from datetime import date

CATEGORIES = ["Study", "Books", "Health", "Mind", "Daily Life"]

ICONS = ["📚", "📖", "💧", "🧘", "🏃", "🌱", "✍️", "🎵", "😴", "🍎", "💻", "🌸"]

COLOURS = ["#F9A8D4", "#FBCFE8", "#A5D8FF", "#BDE0FE", "#C8F7C5",
           "#FFE5A3", "#FFD6A5", "#E4C1F9", "#FFC6FF", "#B5EAD7"]


def new_habit(name, category="Daily Life", target_minutes=0, icon="🌱",
              colour="#BDE0FE", created_date=None):
    """Build a new habit dict. Raises ValueError on a blank name."""
    name = (name or "").strip()
    if not name:
        raise ValueError("Habit name cannot be empty")
    if category not in CATEGORIES:
        category = "Daily Life"
    try:
        target_minutes = int(target_minutes or 0)
    except (TypeError, ValueError):
        target_minutes = 0
    if target_minutes < 0:
        target_minutes = 0
    return {
        "id": uuid.uuid4().hex[:8],
        "name": name,
        "category": category,
        "target_minutes": target_minutes,
        "icon": icon if icon in ICONS else "🌱",
        "colour": colour if colour in COLOURS else "#BDE0FE",
        "created_date": created_date or date.today().isoformat(),
    }


def add_habit(habits, habit):
    """Append a habit dict to the list and return it."""
    habits.append(habit)
    return habit


def get_habit(habits, habit_id):
    """Return the habit with this id, or None."""
    for habit in habits:
        if habit.get("id") == habit_id:
            return habit
    return None


def edit_habit(habits, habit_id, **changes):
    """Update a habit's fields. Returns True if found, else False.

    Allowed changes: name, category, target_minutes, icon, colour.
    A blank new name is ignored (the old name is kept).
    """
    habit = get_habit(habits, habit_id)
    if habit is None:
        return False
    if "name" in changes:
        name = (changes["name"] or "").strip()
        if name:
            habit["name"] = name
    if "category" in changes and changes["category"] in CATEGORIES:
        habit["category"] = changes["category"]
    if "target_minutes" in changes:
        try:
            target = int(changes["target_minutes"] or 0)
        except (TypeError, ValueError):
            target = habit["target_minutes"]
        habit["target_minutes"] = max(0, target)
    if "icon" in changes and changes["icon"] in ICONS:
        habit["icon"] = changes["icon"]
    if "colour" in changes and changes["colour"] in COLOURS:
        habit["colour"] = changes["colour"]
    return True


def delete_habit(habits, habit_id):
    """Remove a habit from the list. Returns True if something was removed."""
    for i, habit in enumerate(habits):
        if habit.get("id") == habit_id:
            del habits[i]
            return True
    return False


def list_habits(habits):
    """Return the habits in display order (creation order)."""
    return list(habits or [])
