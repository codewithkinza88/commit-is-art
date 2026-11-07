"""Daily tracking logic (pure logic, no Flet).

Logs are stored as:
    logs = {
        "2026-11-07": {           # ISO date YYYY-MM-DD
            "<habit_id>": {"done": True, "minutes": 45},
        },
    }

A habit counts as done for a day when it is ticked, OR when its logged
minutes reach its daily target (target_minutes > 0).
"""

from datetime import date, timedelta


def today_str(on_date=None):
    """ISO date string for today (or for the given date)."""
    return (on_date or date.today()).isoformat()


def _day_log(logs, date_str, habit_id):
    day = logs.setdefault(date_str, {})
    return day.setdefault(habit_id, {"done": False, "minutes": 0})


def set_done(logs, habit_id, date_str, done=True):
    """Tick (or untick) a habit for a date."""
    _day_log(logs, date_str, habit_id)["done"] = bool(done)
    return logs


def toggle_done(logs, habit_id, date_str):
    """Flip the tick for a habit on a date; returns the new done state."""
    entry = _day_log(logs, date_str, habit_id)
    entry["done"] = not entry["done"]
    return entry["done"]


def log_minutes(logs, habit_id, date_str, minutes):
    """Add minutes to a habit for a date. Returns the new total for the day."""
    try:
        minutes = int(minutes or 0)
    except (TypeError, ValueError):
        minutes = 0
    if minutes <= 0:
        return minutes_for(logs, habit_id, date_str)
    entry = _day_log(logs, date_str, habit_id)
    entry["minutes"] = int(entry.get("minutes", 0)) + minutes
    return entry["minutes"]


def minutes_for(logs, habit_id, date_str):
    """Minutes logged for a habit on a date (0 if none)."""
    return int(logs.get(date_str, {}).get(habit_id, {}).get("minutes", 0) or 0)


def is_done(logs, habit, date_str):
    """True if the habit is ticked, or its minutes reached its target."""
    entry = logs.get(date_str, {}).get(habit["id"])
    if not entry:
        return False
    if entry.get("done"):
        return True
    target = int(habit.get("target_minutes") or 0)
    return target > 0 and int(entry.get("minutes", 0) or 0) >= target


def current_streak(logs, habit, end_date=None):
    """Consecutive days (ending on end_date, default today) the habit was done."""
    end = end_date or date.today()
    streak = 0
    day = end
    while is_done(logs, habit, day.isoformat()):
        streak += 1
        day -= timedelta(days=1)
    return streak


def daily_summary(logs, habits, date_str):
    """Summary for one day. Handles an empty habit list (0 total, 0%)."""
    habits = list(habits or [])
    total = len(habits)
    done_count = sum(1 for h in habits if is_done(logs, h, date_str))
    minutes_per_habit = {
        h["name"]: minutes_for(logs, h["id"], date_str) for h in habits
    }
    total_minutes = sum(minutes_per_habit.values())
    percent = round(100 * done_count / total) if total else 0
    # Best habit today: the one with the most minutes (ties -> first done one).
    best_habit = None
    best_minutes = 0
    for h in habits:
        mins = minutes_per_habit[h["name"]]
        if mins > best_minutes or (best_habit is None and is_done(logs, h, date_str)):
            if mins >= best_minutes:
                best_habit = h["name"]
                best_minutes = mins
    return {
        "date": date_str,
        "total": total,
        "done": done_count,
        "percent": percent,
        "total_minutes": total_minutes,
        "minutes_per_habit": minutes_per_habit,
        "best_habit": best_habit,
        "best_minutes": best_minutes,
    }


def last_7_days(logs, habits, end_date=None):
    """One daily summary per day for the last 7 days, oldest first."""
    end = end_date or date.today()
    days = []
    for i in range(6, -1, -1):
        day = end - timedelta(days=i)
        days.append(daily_summary(logs, habits, day.isoformat()))
    return days
