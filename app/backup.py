"""Backup and restore helpers (pure logic, no Flet).

A backup is one dict with habits, logs and notes, plus the app version.
"""

import json

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
