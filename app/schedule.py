"""Which habits are due on a given weekday (pure logic, no Flet).

A habit may carry an optional "days" list of weekday numbers
(Monday=0 .. Sunday=6). A habit without "days" is due every day.
"""

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def habits_due_on(habits, weekday):
    """Habits due on weekday (0=Mon .. 6=Sun)."""
    due = []
    for h in habits:
        days = h.get("days")
        if not days:
            due.append(h)
        elif weekday in days:
            due.append(h)
    return due


def is_due_today(habit, weekday):
    """True when the habit is due on weekday (0=Mon .. 6=Sun).

    A habit without a "days" list is due every day.
    """
    days = (habit or {}).get("days")
    if not days:
        return True
    return weekday in days


def due_this_week(habits, weekday):
    """Habits due on any day from weekday through Sunday.

    The rest of this week (Mon=0 .. Sun=6): a habit counts when it is
    due on weekday itself or any later day of the week. A habit
    without "days" is due every day, so it always counts.
    """
    due = []
    for h in (habits or []):
        days = h.get("days")
        if not days:
            due.append(h)
        elif any(day >= weekday for day in days):
            due.append(h)
    return due



def habits_due_tomorrow(habits, weekday):
    """Habits due on the next weekday (wraps Sunday -> Monday)."""
    return habits_due_on(habits, (weekday + 1) % 7)


def count_due_today(habits, weekday):
    """How many habits are due on weekday (0 when none)."""
    return len(habits_due_on(habits or [], weekday))


def count_due_this_week(habits, weekday):
    """How many habits are due at least once from weekday to Sunday."""
    return len(due_this_week(habits or [], weekday))


def next_due_weekday(habit, weekday):
    """Next weekday number (0=Mon .. 6=Sun) the habit is due, starting
    from the given weekday (inclusive, wraps Sunday -> Monday).

    A habit without a "days" list is due every day, so it is due on
    the given weekday itself.
    """
    days = (habit or {}).get("days")
    if not days:
        return weekday % 7
    for offset in range(7):
        candidate = (weekday + offset) % 7
        if candidate in days:
            return candidate
    return weekday % 7


def weekday_name(weekday):
    """Short name for a weekday number, e.g. 0 -> 'Mon'."""
    if 0 <= weekday <= 6:
        return WEEKDAYS[weekday]
    return "?"
