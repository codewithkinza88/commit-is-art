"""Streak helpers (pure logic, no Flet).

Builds on app.tracker.current_streak: this module answers the
questions the garden view wants — what is the longest streak a habit
ever had, and how long ago was it last done?
"""

from datetime import date, timedelta

from app.tracker import current_streak, is_done


def _done_dates(logs, habit, end_date=None):
    """Sorted list of dates (as date objects) the habit was done, up to end."""
    end = end_date or date.today()
    done = []
    for date_str in logs or {}:
        try:
            day = date.fromisoformat(date_str)
        except ValueError:
            continue
        if day <= end and is_done(logs, habit, date_str):
            done.append(day)
    return sorted(done)


def best_streak(logs, habit, end_date=None):
    """Longest run of consecutive done days ever (up to end_date)."""
    done = _done_dates(logs, habit, end_date)
    best = 0
    run = 0
    previous = None
    for day in done:
        if previous is not None and day == previous + timedelta(days=1):
            run += 1
        else:
            run = 1
        best = max(best, run)
        previous = day
    return best


def days_since_last_done(logs, habit, end_date=None):
    """Days since the habit was last done (0 = done on end_date).

    Returns None when the habit was never done.
    """
    done = _done_dates(logs, habit, end_date)
    if not done:
        return None
    end = end_date or date.today()
    return (end - done[-1]).days


def streak_summary(logs, habit, end_date=None):
    """Current streak, best streak, and days since last done, in one dict."""
    end = end_date or date.today()
    return {
        "habit_id": habit["id"],
        "name": habit["name"],
        "current": current_streak(logs, habit, end_date=end),
        "best": best_streak(logs, habit, end_date=end),
        "days_since_last_done": days_since_last_done(logs, habit, end_date=end),
    }


def last_done_label(logs, habit, end_date=None):
    """Short label for when a habit was last done.

    "Done today 🌸" / "Last done yesterday" / "Last done N days ago"
    / "Not done yet 🌱" when it was never done.
    """
    days = days_since_last_done(logs, habit, end_date=end_date)
    if days is None:
        return "Not done yet 🌱"
    if days == 0:
        return "Done today 🌸"
    if days == 1:
        return "Last done yesterday"
    return f"Last done {days} days ago"
