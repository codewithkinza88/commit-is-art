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
        "archived": False,               # True when parked (hidden, not deleted)
        "effort": "Medium",              # Easy, Medium or Hard
    }
"""

import uuid
from datetime import date

CATEGORIES = ["Study", "Books", "Health", "Mind", "Daily Life"]

EFFORTS = ["Easy", "Medium", "Hard"]

EFFORT_EMOJI = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}


def validate_effort(effort):
    """Effort level, falling back to Medium for anything unknown."""
    return effort if effort in EFFORTS else "Medium"

ICONS = ["📚", "📖", "💧", "🧘", "🏃", "🌱", "✍️", "🎵", "😴", "🍎", "💻", "🌸"]

COLOURS = ["#F9A8D4", "#FBCFE8", "#A5D8FF", "#BDE0FE", "#C8F7C5",
           "#FFE5A3", "#FFD6A5", "#E4C1F9", "#FFC6FF", "#B5EAD7"]


def new_habit(name, category="Daily Life", target_minutes=0, icon="🌱",
              colour="#BDE0FE", created_date=None, effort="Medium"):
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
        "archived": False,
        "effort": validate_effort(effort),
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

    Allowed changes: name, category, target_minutes, icon, colour,
    effort. A blank new name is ignored (the old name is kept).
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
    if "effort" in changes:
        habit["effort"] = validate_effort(changes["effort"])
    return True


def delete_habit(habits, habit_id):
    """Remove a habit from the list. Returns True if something was removed."""
    for i, habit in enumerate(habits):
        if habit.get("id") == habit_id:
            del habits[i]
            return True
    return False


def archive_habit(habits, habit_id):
    """Park a habit (hide it without deleting it). Returns the habit or None."""
    habit = get_habit(habits, habit_id)
    if habit is None:
        return None
    habit["archived"] = True
    return habit


def clone_habit(habits, habit_id):
    """Copy a habit: same category/target/icon/colour/effort, new id,
    " (copy)" name, fresh created_date, not archived.

    Appends the copy to the list and returns it (None when the habit
    is not found).
    """
    habit = get_habit(habits, habit_id)
    if habit is None:
        return None
    copy = dict(habit)
    copy["id"] = uuid.uuid4().hex[:8]
    copy["name"] = habit["name"] + " (copy)"
    copy["created_date"] = date.today().isoformat()
    copy["archived"] = False
    habits.append(copy)
    return copy


def habit_age_days(habit, today=None):
    """Days since the habit was planted (0 when planted today, or
    when its created_date is missing or invalid).

    `today` is a date or an ISO string; when None it is today.
    """
    created = (habit or {}).get("created_date") or ""
    try:
        born = date.fromisoformat(created)
    except ValueError:
        return 0
    if today is None:
        day = date.today()
    elif isinstance(today, str):
        try:
            day = date.fromisoformat(today)
        except ValueError:
            return 0
    else:
        day = today
    return max(0, (day - born).days)


def active_habits(habits):
    """Habits that are not archived, in display order.

    Habits saved before archiving existed have no "archived" key
    and count as active.
    """
    return [h for h in (habits or []) if not h.get("archived", False)]


def list_habits(habits):
    """Return the habits in display order (creation order)."""
    return list(habits or [])


def habits_by_category(habits, category):
    """Habits in one category, in display order ([] when none)."""
    return [h for h in (habits or [])
            if (h.get("category") or "") == category]


def count_by_category(habits):
    """How many habits sit in each category (only categories present)."""
    counts = {}
    for habit in (habits or []):
        category = habit.get("category") or "Daily Life"
        counts[category] = counts.get(category, 0) + 1
    return counts


def count_by_effort(habits):
    """How many habits sit at each effort level (only efforts present).

    Effort comes from validate_effort, so an unknown or missing
    effort counts as "Medium". {} when there are no habits.
    """
    counts = {}
    for habit in (habits or []):
        effort = validate_effort(habit.get("effort"))
        counts[effort] = counts.get(effort, 0) + 1
    return counts


def newest_habit(habits):
    """The habit planted most recently (latest created_date).

    Ties go to the habit first in creation order. None when there
    are no habits. A habit with no created_date counts as the
    oldest, so it never wins while any dated habit exists.
    """
    habits = list(habits or [])
    if not habits:
        return None
    return max(habits, key=lambda h: h.get("created_date") or "")


def oldest_habit(habits):
    """The habit planted first (earliest created_date).

    Mirror of newest_habit: ties go to the habit first in creation
    order. None when there are no habits. A habit with no
    created_date counts as the oldest, so it wins while any dated
    habit exists.
    """
    habits = list(habits or [])
    if not habits:
        return None
    return min(habits, key=lambda h: h.get("created_date") or "")


def habits_with_target(habits):
    """Habits with a daily target set (target_minutes > 0).

    Creation order is kept; [] when no habit has a target (or
    there are no habits).
    """
    return [h for h in (habits or [])
            if int(h.get("target_minutes") or 0) > 0]


def count_archived(habits):
    """How many habits are archived (parked, not deleted).

    0 when none are archived (or there are no habits).
    """
    return sum(1 for h in (habits or []) if h.get("archived", False))

