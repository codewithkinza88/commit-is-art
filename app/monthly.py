"""Monthly summary (pure logic, no Flet).

One summary for a whole calendar month: total minutes, average daily
% achieved, how many days were perfect (100%), and the best day.
"""

import calendar
from datetime import date

from app.tracker import daily_summary


def monthly_summary(logs, habits, year, month):
    """Summary for the given calendar month.

    Handles an empty habit list (0 minutes, 0% average) and months of
    any length, including February in a leap year.
    """
    days_in_month = calendar.monthrange(year, month)[1]
    days = []
    for day in range(1, days_in_month + 1):
        day_str = date(year, month, day).isoformat()
        days.append(daily_summary(logs, habits, day_str))
    total_minutes = sum(d["total_minutes"] for d in days)
    average_percent = round(sum(d["percent"] for d in days) / len(days)) if days else 0
    perfect_days = sum(1 for d in days if d["total"] and d["percent"] == 100)
    best_day = max(days, key=lambda d: (d["percent"], d["total_minutes"])) if days else None
    weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    minutes_by_weekday = {name: 0 for name in weekday_names}
    for day in range(1, days_in_month + 1):
        weekday = date(year, month, day).weekday()
        minutes_by_weekday[weekday_names[weekday]] += days[day - 1]["total_minutes"]
    return {
        "year": year,
        "month": month,
        "days_in_month": days_in_month,
        "days": days,
        "total_minutes": total_minutes,
        "average_percent": average_percent,
        "perfect_days": perfect_days,
        "best_day": best_day,
        "best_day_date": best_day["date"] if best_day else None,
        "minutes_by_weekday": minutes_by_weekday,
    }


def quietest_weekday(summary):
    """Weekday name (Mon..Sun) with the fewest minutes in a monthly
    summary, or None when no minutes were logged at all.

    Ties go to the earliest weekday (Mon first). A weekday with no
    minutes at all still counts as the quietest when some other day
    has minutes.
    """
    minutes = (summary or {}).get("minutes_by_weekday") or {}
    if not minutes or max(minutes.values()) <= 0:
        return None
    return min(minutes, key=lambda name: minutes[name])


def busiest_weekday(summary):
    """Weekday name (Mon..Sun) with the most minutes in a monthly
    summary, or None when no minutes were logged at all.

    Ties go to the earliest weekday (Mon first).
    """
    minutes = (summary or {}).get("minutes_by_weekday") or {}
    if not minutes or max(minutes.values()) <= 0:
        return None
    return max(minutes, key=lambda name: minutes[name])


def days_logged_this_month(summary):
    """How many days in a monthly summary had minutes logged (> 0).

    Different from perfect_days, which needs 100%: any day with
    even a few minutes counts as logged. 0 when the summary is
    empty or nothing was logged.
    """
    days = (summary or {}).get("days") or []
    return sum(1 for day in days
               if int(day.get("total_minutes") or 0) > 0)


def days_with_no_minutes(summary):
    """How many days in a monthly summary logged 0 minutes.

    The other side of days_logged_this_month: days_in_month
    minus days logged. 0 for a fully logged month (or an empty
    summary, which has no days at all).
    """
    summary = summary or {}
    total = summary.get("days_in_month") or 0
    return total - days_logged_this_month(summary)


def perfect_day_dates(summary):
    """ISO dates in a monthly summary that were perfect (100%).

    Oldest first; [] when no day was perfect. A day only counts
    when at least one habit exists (an empty habit list can never
    be 100%).
    """
    days = (summary or {}).get("days") or []
    return [day["date"] for day in days
            if day.get("total") and day.get("percent") == 100]


def average_minutes_on_logged_days(summary):
    """Average minutes per day that actually had minutes logged.

    Different from average_minutes_per_day, which divides by the
    whole month: this divides only by the days with minutes, so a
    month with a few big days reads honestly. 0 when no day was
    logged (or the summary is empty).
    """
    summary = summary or {}
    logged = days_logged_this_month(summary)
    if not logged:
        return 0
    return round((summary.get("total_minutes") or 0) / logged)


def minutes_for_weekday(summary, weekday_name):
    """Minutes logged on one weekday in a monthly summary.

    Looks up minutes_by_weekday by name ("Mon".."Sun"); 0 for an
    unknown name or a summary with no minutes that day.
    """
    minutes = (summary or {}).get("minutes_by_weekday") or {}
    return int(minutes.get(weekday_name) or 0)


def longest_day_minutes(summary):
    """Most minutes logged on any single day in a monthly summary.

    0 when the summary has no days (or nothing was logged).
    """
    days = (summary or {}).get("days") or []
    return max((int(day.get("total_minutes") or 0) for day in days),
               default=0)


def average_minutes_per_day(summary):
    """Average minutes per day across a monthly summary (0 when empty).

    Uses the month's real length, so February counts fewer days than
    January.
    """
    summary = summary or {}
    days = summary.get("days_in_month") or 0
    if not days:
        return 0
    return round((summary.get("total_minutes") or 0) / days)
