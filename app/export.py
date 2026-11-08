"""Export helpers (pure logic, no Flet, no file writes).

Turn habits and logs into plain text the user can copy or share:
CSV for habits and for daily logs, and a short human-readable
summary of one day.
"""

import csv
import io

from app.tracker import daily_summary


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
    return "\n".join(lines)
