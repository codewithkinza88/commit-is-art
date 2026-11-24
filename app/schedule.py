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


def count_due_today_undone(habits, logs, weekday, date_str):
    """How many habits due on weekday are still not done on date_str.

    Due habits come from habits_due_on; a habit counts as done when
    tracker.is_done says so (ticked, or minutes reached its target).
    0 when nothing is due or everything due is already done.
    """
    from app.tracker import is_done

    return sum(1 for habit in habits_due_on(habits or [], weekday)
               if not is_done(logs or {}, habit, date_str))


def count_due_today(habits, weekday):
    """How many habits are due on weekday (0 when none)."""
    return len(habits_due_on(habits or [], weekday))


def count_due_tomorrow(habits, weekday):
    """How many habits are due on the next weekday (0 when none).

    Count form of habits_due_tomorrow; wraps Sunday -> Monday.
    """
    return len(habits_due_tomorrow(habits or [], weekday))


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


def count_due_on_weekday(habits, weekday):
    """How many habits are due on weekday (0=Mon .. 6=Sun).

    Mirror of count_due_today, but for any weekday instead of
    just today; 0 when nothing is due that day.
    """
    return len(habits_due_on(habits or [], weekday))


def next_due_weekday_name(habit, weekday):
    """Short name of the next weekday the habit is due.

    The weekday_name of next_due_weekday(habit, weekday), e.g.
    "Wed" for a Mon/Wed/Fri habit asked on a Tuesday.
    """
    return weekday_name(next_due_weekday(habit, weekday))


def weekday_of(date_str):
    """Weekday number (0=Mon .. 6=Sun) for an ISO date string.

    -1 when the text is not a valid date — handy before a date is
    used to look up due habits.
    """
    from datetime import date as _date

    if not isinstance(date_str, str):
        return -1
    try:
        return _date.fromisoformat(date_str.strip()).weekday()
    except ValueError:
        return -1


def habits_due_every_day(habits):
    """Habits with no "days" list, i.e. due every single day.

    Creation order is kept; [] when every habit has set days (or
    there are no habits).
    """
    return [h for h in (habits or []) if not h.get("days")]


def weekday_name(weekday):
    """Short name for a weekday number, e.g. 0 -> 'Mon'."""
    if 0 <= weekday <= 6:
        return WEEKDAYS[weekday]
    return "?"


def habits_due_on_weekday_name(habits, name):
    """Habits due on the weekday named by its short name.

    "Tue" means weekday 1; creation order is kept. [] when the
    name is unknown (or there are no habits).
    """
    if not isinstance(name, str):
        return []
    short = name.strip().title()[:3]
    if short not in WEEKDAYS:
        return []
    return habits_due_on(habits or [], WEEKDAYS.index(short))
