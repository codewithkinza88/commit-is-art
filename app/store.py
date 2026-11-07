"""Local JSON storage (pure logic, no Flet, no server, no login).

The whole store is one JSON object:
    {"habits": [...], "logs": {...}}

Default file: habit_garden.json next to the app. It is in .gitignore,
so real user data is never committed.
"""

import json
import os
from datetime import date

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "habit_garden.json")


def empty_store():
    return {"habits": [], "logs": {}}


def seed_store():
    """Starter habits — plain editable sample data, not hard-coded rules.

    The user can edit or delete any of these from inside the app.
    """
    from app.habits import new_habit
    today = date.today().isoformat()
    store = empty_store()
    store["habits"] = [
        new_habit("Study — DSA / course", "Study", 60, "📚", "#A5D8FF", today),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", today),
        new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", today),
    ]
    return store


def load_store(path=DEFAULT_PATH):
    """Load the store; a missing or corrupt file gives an empty store."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return empty_store()
    if not isinstance(data, dict):
        return empty_store()
    habits = data.get("habits")
    logs = data.get("logs")
    return {
        "habits": habits if isinstance(habits, list) else [],
        "logs": logs if isinstance(logs, dict) else {},
    }


def save_store(store, path=DEFAULT_PATH):
    """Save the store, creating parent folders if needed."""
    folder = os.path.dirname(os.path.abspath(path))
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)
    return path
