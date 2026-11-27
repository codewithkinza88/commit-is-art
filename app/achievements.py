"""Achievements / badges (pure logic, no Flet).

Little badges the garden awards for real milestones — a first tick,
a 3-day streak, a full week, a perfect day, and a 100-minute day.
Each badge is {"key", "label", "emoji"}.
"""

from datetime import date

from app.tracker import current_streak, daily_summary, is_done


def badges_count(logs, habits, date_str):
    """How many badges are earned up to and including date_str.

    The count of badges_for — 0 when nothing is earned yet (or
    there are no habits).
    """
    return len(badges_for(logs, habits, date_str))


def badge_labels(logs, habits, date_str):
    """Labels of the badges earned up to and including date_str.

    The label of each badge in badges_for, in award order;
    [] when nothing is earned yet (or there are no habits).
    """
    return [badge["label"]
            for badge in badges_for(logs, habits, date_str)]


def badges_for(logs, habits, date_str):
    """Badges earned up to and including date_str."""
    habits = list(habits or [])
    badges = []
    end = date.fromisoformat(date_str)

    any_done = any(
        is_done(logs, habit, day)
        for habit in habits
        for day in (logs or {})
        if day <= date_str
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

def has_badge(logs, habits, date_str, label):
    """True when a badge with this label is earned by date_str.

    The label form of badges_for — checks the labels from
    badge_labels; False when nothing is earned yet (or there are
    no habits, or no badge carries the label).
    """
    return (label or "") in badge_labels(logs, habits, date_str)
