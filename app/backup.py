"""Backup and restore helpers (pure logic, no Flet).

A backup is one dict with habits, logs and notes, plus the app version.
"""

import json
from datetime import date


def backup_filename(day=None):
    """Dated filename for a backup, e.g. habit-garden-backup-2026-11-14.json."""
    day = day or date.today()
    if isinstance(day, str):
        day = date.fromisoformat(day)
    return f"habit-garden-backup-{day.isoformat()}.json"

from app.version import APP_VERSION as VERSION


def make_backup(habits, logs, notes):
    """Build a backup dict that can be saved as JSON."""
    return {"app": "Habit Garden", "version": VERSION,
            "habits": list(habits), "logs": dict(logs), "notes": dict(notes)}


def backup_to_json(habits, logs, notes):
    """Serialise a backup to a JSON string."""
    return json.dumps(make_backup(habits, logs, notes), ensure_ascii=False)


def restore_from_json(text):
    """Parse a backup JSON string. Raises ValueError on bad data."""
    try:
        data = json.loads(text)
    except (TypeError, ValueError) as e:
        raise ValueError("Not a valid backup file") from e
    if not isinstance(data, dict) or "habits" not in data or "logs" not in data:
        raise ValueError("Not a valid backup file")
    return data


BACKUP_REMINDER_DAYS = 7


def should_auto_backup(last_backup_date, today=None):
    """True when a backup is overdue: no backup ever, or the last one
    was 7+ days ago. `last_backup_date` accepts None, a date, or an
    ISO string; `today` is a date or ISO string (defaults to today).
    """
    if last_backup_date is None or last_backup_date == "":
        return True
    if isinstance(last_backup_date, str):
        try:
            last = date.fromisoformat(last_backup_date)
        except ValueError:
            return True
    else:
        last = last_backup_date
    if today is None:
        day = date.today()
    elif isinstance(today, str):
        try:
            day = date.fromisoformat(today)
        except ValueError:
            return True
    else:
        day = today
    return (day - last).days >= BACKUP_REMINDER_DAYS

def backup_counts(habits, logs, notes):
    """Counts of the habits, logs and notes in a backup.

    {"habits": n, "logs": n, "notes": n} — the size of each part
    of make_backup, for the Backup & Restore view.
    """
    return {"habits": len(habits or []),
            "logs": len(logs or {}),
            "notes": len(notes or {})}
