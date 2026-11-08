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
    }
