"""In-app notifications for Habit Garden (pure logic, no Flet).

These are notifications *inside* the app itself: every time the app
draws, it rebuilds them from the current habits, logs and notes, so
they are always fresh — no server, no Play Store, no system push.

A notification is a plain dict:
    {"kind", "icon", "title", "text"} and "habit_id" when it names one
    habit. Kinds: "streak", "due", "goal", "evening", "morning",
    "badge", "backup". Most urgent first, capped at 10.
"""

from datetime import date, datetime, timedelta

from app.achievements import badges_for
from app.backup import should_auto_backup
from app.goals import weekly_goal_progress, weekly_goal_warning
from app.habits import active_habits
from app.schedule import is_due_today
from app.tracker import current_streak, done_count_today, is_done

MAX_NOTIFICATIONS = 10
STREAK_AT_RISK_MIN = 3


def notification_key(notification):
    """Stable session key for a notification (kind + habit or title)."""
    habit_id = notification.get("habit_id") or ""
    return f"{notification.get('kind', '')}:{habit_id or notification.get('title', '')}"


def unread_count(notifications):
    """How many notifications are unread (just the count, for now)."""
    return len(notifications or [])


def should_refresh(last_date_str, current_date_str):
    """True when the day rolled over since the last refresh."""
    return (last_date_str or "") != (current_date_str or "")


def _note(kind, icon, title, text, habit_id=None):
    note = {"kind": kind, "icon": icon, "title": title, "text": text}
    if habit_id:
        note["habit_id"] = habit_id
    return note


def build_notifications(habits, logs, notes, date_str, hour=None,
                        last_backup_date=None):
    """Notifications for one day, most urgent first, capped at 10.

    hour is the hour of day (0-23); when None it is read from the
    clock, so tests pass it in instead of depending on the real time.
    `notes` is accepted for future note-based reminders; the rules
    below only need habits and logs. `last_backup_date` (None, a date
    or an ISO string) adds a gentle backup nudge when the last backup
    was 7+ days ago.
    """
    if hour is None:
        hour = datetime.now().hour
    day = date.fromisoformat(date_str)
    weekday = day.weekday()
    habits = active_habits(habits)
    logs = logs or {}

    streak_notes = []
    due_notes = []
    for habit in habits:
        if is_done(logs, habit, date_str):
            continue
        if not is_due_today(habit, weekday):
            continue
        # The streak that is at risk is the one up to yesterday —
        # today is not done yet, so a streak ending today is 0.
        streak = current_streak(logs, habit,
                                end_date=day - timedelta(days=1))
        if streak >= STREAK_AT_RISK_MIN:
            streak_notes.append(_note(
                "streak", "🔥",
                f"{habit['name']} is on a {streak}-day streak",
                "Don't break it — tick it off today!",
                habit_id=habit["id"]))
        due_notes.append(_note(
            "due", "💧", f"Water {habit['name']}",
            "This habit is waiting for its water today 💧",
            habit_id=habit["id"]))

    goal_notes = []
    for habit in habits:
        target = int(habit.get("target_minutes") or 0)
        if not target:
            continue
        progress = weekly_goal_progress(logs, habit, target * 7,
                                        end_date=day)
        warning = weekly_goal_warning(progress)
        if warning:
            goal_notes.append(_note(
                "goal", "🎯", f"{habit['name']} weekly goal",
                warning, habit_id=habit["id"]))

    time_notes = []
    if habits:
        if hour >= 18:
            time_notes.append(_note(
                "evening", "🌙", "Tonight review ready",
                "See how much you achieved today 🌙"))
        elif hour < 12 and done_count_today(logs, habits, date_str) == 0:
            time_notes.append(_note(
                "morning", "🌞", "Good morning!",
                f"{len(habits)} habits waiting for water 🌞"))

    badge_notes = []
    if habits:
        yesterday = (day - timedelta(days=1)).isoformat()
        today_keys = {b["key"]
                      for b in badges_for(logs, habits, date_str)}
        yesterday_keys = {b["key"]
                          for b in badges_for(logs, habits, yesterday)}
        for badge in badges_for(logs, habits, date_str):
            if badge["key"] in today_keys - yesterday_keys:
                badge_notes.append(_note(
                    "badge", "🏅", f"New badge: {badge['label']}",
                    f"You earned the {badge['label']} badge!"))

    backup_notes = []
    if habits and should_auto_backup(last_backup_date, day):
        backup_notes.append(_note(
            "backup", "💾", "Backup your garden",
            "It's been a while since your last backup — save one "
            "from the Garden so your habits are safe 💾"))

    ordered = (streak_notes + due_notes + goal_notes + time_notes
               + badge_notes + backup_notes)
    return ordered[:MAX_NOTIFICATIONS]

def count_unread_for_habit(notifications, habit_id):
    """Unread notifications naming one habit (0 when none).

    The list holds unread notifications only (see unread_count),
    so this counts the ones carrying this habit's id.
    """
    return sum(1 for n in (notifications or [])
               if n.get("habit_id") == habit_id)
