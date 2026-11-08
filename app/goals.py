"""Weekly minutes goals (pure logic, no Flet).

A habit can have a weekly minutes goal (e.g. study 300 minutes a
week). This module measures progress over the last 7 days ending on
a given date.
"""

from datetime import date, timedelta

from app.tracker import minutes_for


def minutes_in_last_7_days(logs, habit, end_date=None):
    """Total minutes logged for a habit over the last 7 days."""
    end = end_date or date.today()
    if isinstance(end, str):
        end = date.fromisoformat(end)
    total = 0
    for i in range(7):
        day = end - timedelta(days=i)
        total += minutes_for(logs, habit["id"], day.isoformat())
    return total


def weekly_goal_progress(logs, habit, weekly_target_minutes, end_date=None):
    """Progress towards a weekly minutes goal.

    Returns {"minutes", "target", "percent", "remaining", "met"}.
    A target of 0 or less means no goal, so it is always met.
    """
    target = max(0, int(weekly_target_minutes or 0))
    minutes = minutes_in_last_7_days(logs, habit, end_date)
    if target == 0:
        return {"minutes": minutes, "target": 0, "percent": 100,
                "remaining": 0, "met": True}
    percent = min(100, round(100 * minutes / target))
    return {
        "minutes": minutes,
        "target": target,
        "percent": percent,
        "remaining": max(0, target - minutes),
        "met": minutes >= target,
    }
