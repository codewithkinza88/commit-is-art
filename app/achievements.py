"""Achievements / badges (pure logic, no Flet).

Little badges the garden awards for real milestones — a first tick,
a 3-day streak, a full week, a perfect day, and a 100-minute day.
Each badge is {"key", "label", "emoji"}.
"""

from datetime import date

from app.tracker import current_streak, daily_summary, is_done


def badges_for(logs, habits, date_str):
    """Badges earned up to and including date_str."""
    habits = list(habits or [])
    badges = []
    end = date.fromisoformat(date_str)

    any_done = any(
        is_done(logs, habit, day)
        for habit in habits
        for day in (logs or {})
    )
    if any_done:
        badges.append({"key": "first_step", "label": "First Step",
                       "emoji": "🌱"})

    best_current = max(
        (current_streak(logs, habit, end_date=end) for habit in habits),
        default=0,
    )
    if best_current >= 3:
        badges.append({"key": "three_day", "label": "Three-Day Streak",
                       "emoji": "🌿"})
    if best_current >= 7:
        badges.append({"key": "week_strong", "label": "Week Strong",
                       "emoji": "🌷"})

    summary = daily_summary(logs, habits, date_str)
    if habits and summary["percent"] == 100:
        badges.append({"key": "perfect_day", "label": "Perfect Day",
                       "emoji": "🌸"})
    if summary["total_minutes"] >= 100:
        badges.append({"key": "century_minutes", "label": "100 Minutes",
                       "emoji": "⏱️"})
    return badges
