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


def weekly_goal_remaining(logs, habit, weekly_target_minutes, end_date=None):
    """Minutes left to reach a weekly minutes goal, 0 when met.

    The "remaining" of weekly_goal_progress — 0 when there is no
    goal, or when the goal is already met.
    """
    return weekly_goal_progress(logs, habit, weekly_target_minutes,
                                end_date)["remaining"]


def weekly_goal_warning(progress):
    """Warning line when a weekly goal is not met yet, else ''.

    Takes the dict returned by weekly_goal_progress.
    """
    progress = progress or {}
    if not progress.get("target") or progress.get("met"):
        return ""
    remaining = progress.get("remaining", 0)
    return f"⚠️ {remaining} min left to hit your weekly goal"

def weekly_goal_reached(logs, habit, weekly_target_minutes, end_date=None):
    """True when the weekly minutes goal is met.

    The bool form of weekly_goal_progress's "met" — a target of 0
    or less is always met, matching weekly_goal_progress.
    """
    return weekly_goal_progress(logs, habit, weekly_target_minutes,
                                end_date)["met"]

def weekly_goal_percent(logs, habit, weekly_target_minutes, end_date=None):
    """Percent of the weekly minutes goal reached, capped at 100.

    0 when the target is 0 (there is no goal to measure against).
    """
    target = max(0, int(weekly_target_minutes or 0))
    if target == 0:
        return 0
    minutes = minutes_in_last_7_days(logs, habit, end_date)
    return min(100, round(100 * minutes / target))
