"""Search habits by name or category (pure logic, no Flet)."""

def find_habits(habits, query):
    """Habits whose name or category contains query (case-insensitive).

    A blank query returns all habits, in their original order.
    """
    q = (query or "").strip().lower()
    if not q:
        return list(habits)
    return [h for h in habits
            if q in (h.get("name") or "").lower()
            or q in (h.get("category") or "").lower()]


def count_matches(habits, query):
    """How many habits match the query."""
    return len(find_habits(habits, query))
