"""Habit ordering (pure logic, no Flet).

Ways to sort the habit list for the Today view: by name, by
category, by streak (longest first), or undone habits first so the
user sees what is left to do today.
"""

from app.tracker import current_streak, is_done


def sort_habits(habits, logs=None, date_str=None, by="undone_first"):
    """Return a new sorted list of habits (the input list is unchanged).

    by: "undone_first" (default), "name", "category", or "streak".
    Unknown values fall back to creation order.
    """
    habits = list(habits or [])
    if by == "name":
        return sorted(habits, key=lambda h: h.get("name", "").lower())
    if by == "category":
        return sorted(habits,
                      key=lambda h: (h.get("category", ""), h.get("name", "").lower()))
    if by == "streak":
        from datetime import date as _date
        end = _date.fromisoformat(date_str) if date_str else None
        return sorted(
            habits,
            key=lambda h: current_streak(logs or {}, h, end_date=end),
            reverse=True,
        )
    if by == "undone_first":
        if not date_str:
            return habits
        return sorted(
            habits,
            key=lambda h: (is_done(logs or {}, h, date_str),
                           h.get("name", "").lower()),
        )
    return habits
