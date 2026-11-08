"""Category summaries (pure logic, no Flet).

How each habit category (Study, Books, Health, Mind, Daily Life)
is doing on a given day: how many habits, how many done, the
percent, and the minutes logged.
"""

from app.tracker import daily_summary, is_done, minutes_for


def category_summary(logs, habits, date_str):
    """One entry per category that has at least one habit."""
    summary = {}
    for habit in habits or []:
        category = habit.get("category", "Daily Life")
        entry = summary.setdefault(
            category, {"category": category, "total": 0, "done": 0,
                       "minutes": 0})
        entry["total"] += 1
        if is_done(logs, habit, date_str):
            entry["done"] += 1
        entry["minutes"] += minutes_for(logs, habit["id"], date_str)
    for entry in summary.values():
        total = entry["total"]
        entry["percent"] = round(100 * entry["done"] / total) if total else 0
    return summary


def best_category(logs, habits, date_str):
    """The category with the highest % done today (None if no habits).

    Ties are broken by most minutes, then by category name.
    """
    summary = category_summary(logs, habits, date_str)
    if not summary:
        return None
    return max(summary.values(),
               key=lambda e: (e["percent"], e["minutes"], e["category"]))


def total_minutes_by_category(logs, habits, date_str):
    """Minutes logged per category on a date (uses daily_summary data)."""
    summary = daily_summary(logs, habits, date_str)
    minutes = {}
    for habit in habits or []:
        category = habit.get("category", "Daily Life")
        minutes[category] = minutes.get(category, 0) + summary["minutes_per_habit"].get(habit["name"], 0)
    return minutes
