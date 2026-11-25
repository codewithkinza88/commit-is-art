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

import calendar
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


def total_minutes_today(logs, habits, date_str):
    """Total minutes logged across all habits on a date (0 when none)."""
    return sum(minutes_for(logs, habit["id"], date_str)
               for habit in (habits or []))

def total_minutes_this_week(logs, habits, end_date=None):
    """Total minutes logged across all habits in the 7 days to end_date."""
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    total = 0
    for i in range(7):
        day = (end - timedelta(days=i)).isoformat()
        total += total_minutes_today(logs, habits, day)
    return total


def total_minutes_in_range(logs, habits, start_date, end_date):
    """Total minutes logged across all habits between two dates, inclusive.

    start_date / end_date may be date objects or ISO strings. 0 when
    the range is empty or reversed.
    """
    if isinstance(start_date, str):
        start = date.fromisoformat(start_date)
    else:
        start = start_date
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date
    if end < start:
        return 0
    total = 0
    day = start
    while day <= end:
        total += total_minutes_today(logs, habits, day.isoformat())
        day += timedelta(days=1)
    return total


def days_done_this_week(logs, habit, end_date=None):
    """How many of the last 7 days (ending on end_date) the habit
    was done — a number from 0 to 7.

    Different from current_streak, which needs the days to be
    consecutive: a habit done Mon, Wed and Fri counts as 3 here.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    return sum(1 for i in range(7)
               if is_done(logs, habit,
                          (end - timedelta(days=i)).isoformat()))


def days_done_last_7_days(logs, habit, end_date=None):
    """How many of the last 7 days (ending on end_date) the habit
    was done — a number from 0 to 7.

    The windowed name for days_done_this_week, for callers that
    think in rolling weeks rather than calendar weeks.
    """
    return days_done_this_week(logs, habit, end_date)


def days_done_last_14_days(logs, habit, end_date=None):
    """How many of the last 14 days (ending on end_date) the habit
    was done — a number from 0 to 14.

    The 14-day form of days_done_last_7_days.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    return sum(1 for i in range(14)
               if is_done(logs, habit,
                          (end - timedelta(days=i)).isoformat()))


def first_done_date(logs, habit):
    """The earliest ISO date the habit was ever done.

    "" when the habit was never done — the day its garden journey
    started. Invalid log dates are skipped.
    """
    done = []
    for date_str in (logs or {}):
        try:
            date.fromisoformat(date_str)
        except ValueError:
            continue
        if is_done(logs, habit, date_str):
            done.append(date_str)
    return min(done) if done else ""


def total_minutes_last_30_days(logs, habits, end_date=None):
    """Total minutes logged across all habits in the 30 days to end_date.

    Mirror of total_minutes_this_week with a 30-day rolling window;
    0 when there are no logs or no habits.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    total = 0
    for i in range(30):
        day = (end - timedelta(days=i)).isoformat()
        total += total_minutes_today(logs, habits, day)
    return total


def total_minutes_last_14_days(logs, habits, end_date=None):
    """Total minutes logged across all habits in the 14 days to end_date.

    Mirror of total_minutes_last_30_days with a 14-day window;
    0 when there are no logs or no habits.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    total = 0
    for i in range(14):
        day = (end - timedelta(days=i)).isoformat()
        total += total_minutes_today(logs, habits, day)
    return total


def total_minutes_last_7_days(logs, habits, end_date=None):
    """Total minutes logged across all habits in the 7 days to end_date.

    Mirror of total_minutes_last_14_days with a 7-day window;
    0 when there are no logs or no habits.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    total = 0
    for i in range(7):
        day = (end - timedelta(days=i)).isoformat()
        total += total_minutes_today(logs, habits, day)
    return total


def minutes_for_habit_this_month(logs, habit, year, month):
    """Minutes logged for one habit across a whole calendar month.

    Sums minutes_for over every day of the month; 0 when the habit
    logged nothing that month.
    """
    days_in_month = calendar.monthrange(year, month)[1]
    return sum(minutes_for(logs, habit.get("id"),
                           date(year, month, day).isoformat())
               for day in range(1, days_in_month + 1))


def minutes_for_habit_last_7_days(logs, habit, end_date=None):
    """Minutes logged for one habit over the last 7 days.

    Sums minutes_for over the 7 days ending on end_date; 0 when
    the habit logged nothing in the window. Mirror of
    minutes_in_last_7_days in goals.py, kept on the tracker so
    callers need only one import.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    return sum(minutes_for(logs, habit.get("id"),
                           (end - timedelta(days=i)).isoformat())
               for i in range(7))


def minutes_for_habit_last_14_days(logs, habit, end_date=None):
    """Minutes logged for one habit over the last 14 days.

    Sums minutes_for over the 14 days ending on end_date; 0 when
    the habit logged nothing in the window. The 14-day form of
    minutes_for_habit_last_7_days.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    return sum(minutes_for(logs, habit.get("id"),
                           (end - timedelta(days=i)).isoformat())
               for i in range(14))


def days_done_this_month(logs, habit, year, month):
    """How many days in a calendar month the habit was done.

    Counts the days is_done is True (ticked, or minutes reached
    the target); 0 when the habit was never done that month.
    """
    days_in_month = calendar.monthrange(year, month)[1]
    return sum(1 for day in range(1, days_in_month + 1)
               if is_done(logs, habit,
                          date(year, month, day).isoformat()))


def best_day_this_month(logs, habits, year, month):
    """(date, minutes) with the most minutes logged in a month.

    ("", 0) when nothing was logged that month. Ties go to the
    most recent day, mirroring best_day_by_minutes.
    """
    days_in_month = calendar.monthrange(year, month)[1]
    best_date, best_minutes = "", 0
    for day in range(1, days_in_month + 1):
        day_str = date(year, month, day).isoformat()
        minutes = total_minutes_today(logs, habits, day_str)
        if minutes > 0 and minutes >= best_minutes:
            best_date, best_minutes = day_str, minutes
    return best_date, best_minutes


def best_day_last_7_days(logs, habits, end_date=None):
    """(date, minutes) with the most minutes logged in the last 7 days.

    ("", 0) when nothing was logged in the window. Ties go to the
    most recent day, mirroring best_day_this_month.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    best_date, best_minutes = "", 0
    for i in range(6, -1, -1):
        day_str = (end - timedelta(days=i)).isoformat()
        minutes = total_minutes_today(logs, habits, day_str)
        if minutes > 0 and minutes >= best_minutes:
            best_date, best_minutes = day_str, minutes
    return best_date, best_minutes


def total_minutes_yesterday(logs, habits, end_date=None):
    """Total minutes logged across all habits on the day before end_date."""
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    yesterday = (end - timedelta(days=1)).isoformat()
    return total_minutes_today(logs, habits, yesterday)


def minutes_for_habit_yesterday(logs, habit, end_date=None):
    """Minutes logged for one habit on the day before end_date.

    0 when the habit logged nothing yesterday — the one-habit
    mirror of total_minutes_yesterday.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    yesterday = (end - timedelta(days=1)).isoformat()
    return minutes_for(logs, habit.get("id"), yesterday)


def is_done_yesterday(logs, habit, end_date=None):
    """True when the habit was done on the day before end_date."""
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    yesterday = (end - timedelta(days=1)).isoformat()
    return is_done(logs, habit, yesterday)


def done_count_today(logs, habits, date_str):
    """How many habits are done on a date (0 when none)."""
    return sum(1 for habit in (habits or [])
               if is_done(logs, habit, date_str))


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


def weekly_summary(logs, habits, end_date=None):
    """Summary of the last 7 days ending on end_date (default today).

    Returns the per-day summaries (oldest first), the total minutes
    across the week, the average daily % achieved, and the best day
    (highest %, then most minutes). Handles an empty habit list:
    0 total minutes, 0% average, and the first day as best day.
    """
    if isinstance(end_date, str):
        end = date.fromisoformat(end_date)
    else:
        end = end_date or date.today()
    days = last_7_days(logs, habits, end_date=end)
    total_minutes = sum(d["total_minutes"] for d in days)
    average_percent = round(sum(d["percent"] for d in days) / len(days)) if days else 0
    best_day = max(days, key=lambda d: (d["percent"], d["total_minutes"])) if days else None
    return {
        "end_date": end.isoformat(),
        "days": days,
        "total_minutes": total_minutes,
        "average_percent": average_percent,
        "best_day": best_day,
        "best_day_date": best_day["date"] if best_day else None,
    }


def best_day_by_minutes(logs, habits, end_date=None):
    """The day in the last 7 days with the most minutes logged.

    Returns {"date", "minutes"} or None when no minutes were logged
    at all. Different from weekly_summary's best day, which ranks by
    achievement percent first — this one is purely about minutes.
    Ties go to the most recent day.
    """
    days = last_7_days(logs, habits, end_date=end_date)
    best = None
    for day in days:
        if day["total_minutes"] <= 0:
            continue
        if best is None or day["total_minutes"] >= best["minutes"]:
            best = {"date": day["date"], "minutes": day["total_minutes"]}
    return best
