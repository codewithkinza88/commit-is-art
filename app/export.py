"""Export helpers (pure logic, no Flet, no file writes).

Turn habits and logs into plain text the user can copy or share:
CSV for habits and for daily logs, and a short human-readable
summary of one day.
"""

import csv
import io

from app.notes import notes_in_range
from app.streaks import best_streak
from app.tracker import (current_streak, daily_summary, is_done,  # noqa: E402
                         last_7_days, minutes_for)


def habits_to_csv(habits):
    """Habits as CSV text (header + one row per habit)."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "category", "target_minutes",
                     "icon", "colour", "created_date"])
    for habit in habits or []:
        writer.writerow([habit.get("id", ""), habit.get("name", ""),
                         habit.get("category", ""),
                         habit.get("target_minutes", 0),
                         habit.get("icon", ""), habit.get("colour", ""),
                         habit.get("created_date", "")])
    return output.getvalue()


def logs_to_csv(logs):
    """Daily logs as CSV text, oldest date first, habit order as stored."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "habit_id", "done", "minutes"])
    for date_str in sorted(logs or {}):
        for habit_id, entry in (logs[date_str] or {}).items():
            writer.writerow([date_str, habit_id,
                             bool(entry.get("done", False)),
                             int(entry.get("minutes", 0) or 0)])
    return output.getvalue()


def streaks_to_csv(logs, habits, end_date=None):
    """Best + current streak per habit as CSV text (header + one row
    per habit, in habit order)."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["habit_id", "best_streak", "current_streak"])
    for habit in habits or []:
        writer.writerow([habit.get("id", ""),
                         best_streak(logs, habit, end_date=end_date),
                         current_streak(logs, habit, end_date=end_date)])
    return output.getvalue()


def notes_to_csv(notes):
    """Notes as CSV text (header + one row per non-empty note)."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date", "habit_id", "note"])
    for date_str in sorted(notes or {}):
        day_notes = notes[date_str] or {}
        if not isinstance(day_notes, dict):
            continue
        for habit_id, text in day_notes.items():
            if isinstance(text, str) and text.strip():
                writer.writerow([date_str, habit_id, text.strip()])
    return output.getvalue()


def streaks_to_text(logs, habits, end_date=None):
    """Current streak per habit as short readable text lines.

    A header, then one line per habit ("name: N-day streak") in
    habit order — the text mirror of streaks_to_csv, for copying
    into a message. A friendly line when there are no habits.
    """
    lines = ["Habit Garden — streaks"]
    for habit in (habits or []):
        streak = current_streak(logs, habit, end_date=end_date)
        lines.append(f"{habit.get('name', '')}: {streak}-day streak")
    if not habits:
        lines.append("No habits yet 🌱")
    return "\n".join(lines)


def habits_to_lines(habits):
    """Habits as a list of short readable lines, one per habit.

    The list form of habits_to_text: a header, then one line per
    habit (icon, name, category, daily target when set) — handy
    when the caller wants the lines, not one joined block.
    """
    lines = ["Habit Garden — my habits"]
    for habit in (habits or []):
        target = int(habit.get("target_minutes") or 0)
        target_text = f" • 🎯 {target} min/day" if target else ""
        lines.append(f"{habit.get('icon', '🌱')} {habit.get('name', '')} "
                     f"({habit.get('category', 'Daily Life')}){target_text}")
    if not habits:
        lines.append("No habits yet 🌱")
    return lines


def summary_lines(logs, habits, date_str):
    """One day's summary as a list of short readable lines.

    The list form of summary_to_text: a header, one line per habit
    ("name — done / N minutes"), and the day's totals — handy when
    the caller wants the lines, not one joined block.
    """
    summary = daily_summary(logs, habits, date_str)
    lines = [f"Habit Garden — {date_str}",
             f"{summary['done']} / {summary['total']} habits "
             f"({summary['percent']}%)",
             f"Total time: {summary['total_minutes']} minutes"]
    for habit in (habits or []):
        state = "done" if is_done(logs, habit, date_str) else "not done"
        minutes = minutes_for(logs, habit["id"], date_str)
        lines.append(f"- {habit.get('name', '')} — {state} / "
                     f"{minutes} minutes")
    return lines


def summary_to_text(logs, habits, date_str):
    """One day's summary as short readable text lines."""
    summary = daily_summary(logs, habits, date_str)
    lines = [f"Habit Garden — {date_str}",
             f"{summary['done']} / {summary['total']} habits "
             f"({summary['percent']}%)",
             f"Total time: {summary['total_minutes']} minutes"]
    for name, minutes in summary["minutes_per_habit"].items():
        lines.append(f"- {name}: {minutes} min")
    if summary["best_habit"]:
        lines.append(f"Best habit: {summary['best_habit']}")
    longest = max((best_streak(logs, h) for h in (habits or [])),
                  default=0)
    lines.append(f"Longest streak: {longest} day"
                 f"{'s' if longest != 1 else ''}")
    return "\n".join(lines)


def month_to_text(logs, habits, year, month):
    """One calendar month as short readable text lines, oldest first.

    Mirror of week_to_text: a header, one line per day of the month
    (date, done/total, percent, minutes) from monthly_summary, plus
    a total line at the end — copyable into a message.
    """
    from app.monthly import monthly_summary
    import calendar as _calendar

    summary = monthly_summary(logs, habits, year, month)
    lines = [f"Habit Garden — {_calendar.month_name[month]} {year}"]
    for day in summary["days"]:
        lines.append(f"{day['date']}: {day['done']}/{day['total']} "
                     f"({day['percent']}%) • {day['total_minutes']} min")
    lines.append(f"Month total: {summary['total_minutes']} minutes")
    return "\n".join(lines)


def notes_to_text(notes, start_date, end_date):
    """Notes in a date range as short readable text lines.

    A header with the range, then one line per non-empty note
    (date, habit id, text), oldest first; a friendly line when
    nothing was written in the range.
    """
    found = notes_in_range(notes or {}, start_date, end_date)
    lines = [f"Habit Garden notes — {start_date} to {end_date}"]
    for date_str, habit_id, text in found:
        lines.append(f"{date_str} [{habit_id}]: {text}")
    if not found:
        lines.append("No notes in this range 🌱")
    return "\n".join(lines)


def notes_to_lines(notes, start_date, end_date):
    """Notes in a date range as a list of short readable lines.

    The list form of notes_to_text: a header with the range,
    then one line per non-empty note (date, habit id, text),
    oldest first; a friendly line when nothing was written.
    """
    found = notes_in_range(notes or {}, start_date, end_date)
    lines = [f"Habit Garden notes — {start_date} to {end_date}"]
    for date_str, habit_id, text in found:
        lines.append(f"{date_str} [{habit_id}]: {text}")
    if not found:
        lines.append("No notes in this range 🌱")
    return lines


def logs_to_lines(logs):
    """Daily logs as a list of short readable lines, oldest first.

    A header, then one line per log entry ("date — habit — N min
    / done"), in date order and habit order as stored; a friendly
    line when there are no logs.
    """
    lines = ["Habit Garden — logs"]
    for date_str in sorted(logs or {}):
        for habit_id, entry in (logs[date_str] or {}).items():
            state = "done" if entry.get("done") else "not done"
            minutes = int(entry.get("minutes", 0) or 0)
            lines.append(f"{date_str} — {habit_id} — {minutes} min / {state}")
    if not logs:
        lines.append("No logs yet 🌱")
    return lines


def habits_to_text(habits):
    """Habits as short readable text lines, one per habit.

    Icon, name, category, and daily target when one is set —
    the same shape as summary_to_text, but for the habit list
    itself, so it can be copied into a message.
    """
    lines = ["Habit Garden — my habits"]
    for habit in (habits or []):
        target = int(habit.get("target_minutes") or 0)
        target_text = f" • 🎯 {target} min/day" if target else ""
        lines.append(f"{habit.get('icon', '🌱')} {habit.get('name', '')} "
                     f"({habit.get('category', 'Daily Life')}){target_text}")
    if not habits:
        lines.append("No habits yet 🌱")
    return "\n".join(lines)


def week_to_text(logs, habits, end_date=None):
    """The last 7 days as short readable text lines, oldest first.

    One line per day (date, done/total, percent, minutes) plus a
    total line at the end — the same shape as summary_to_text, but
    for a whole week, so it can be copied into a message.
    """
    days = last_7_days(logs, habits, end_date=end_date)
    lines = ["Habit Garden — last 7 days"]
    for day in days:
        lines.append(f"{day['date']}: {day['done']}/{day['total']} "
                     f"({day['percent']}%) • {day['total_minutes']} min")
    total = sum(day["total_minutes"] for day in days)
    lines.append(f"Week total: {total} minutes")
    return "\n".join(lines)


def week_lines(logs, habits, end_date=None):
    """The last 7 days as a list of short readable lines, oldest first.

    The list form of week_to_text: one line per day (date,
    done/total, percent, minutes) plus a total line at the end —
    handy when the caller wants the lines, not one joined block.
    """
    days = last_7_days(logs, habits, end_date=end_date)
    lines = ["Habit Garden — last 7 days"]
    for day in days:
        lines.append(f"{day['date']}: {day['done']}/{day['total']} "
                     f"({day['percent']}%) • {day['total_minutes']} min")
    total = sum(day["total_minutes"] for day in days)
    lines.append(f"Week total: {total} minutes")
    return lines

def logs_to_text(logs):
    """Daily logs as one readable text string.

    A header, then one line per log entry ("date — habit — N min
    / done"), in date order and habit order as stored; a friendly
    line when there are no logs. The text form of logs_to_lines,
    mirror of streaks_to_text.
    """
    return "\n".join(logs_to_lines(logs))
