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


def weekday_name(weekday):
    """Short name for a weekday number, e.g. 0 -> 'Mon'."""
    if 0 <= weekday <= 6:
        return WEEKDAYS[weekday]
    return "?"
