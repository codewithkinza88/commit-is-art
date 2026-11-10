"""Simple insights over recent days (pure logic, no Flet).

Different from monthly totals: this looks at consistency and which
habit needs the most attention right now.
"""

from app.tracker import is_done


def consistency_score(logs, habits, date_strs):
    """Share of habit-days done over the given dates, as a percent (0-100)."""
    if not habits or not date_strs:
        return 0
    done = 0
    total = 0
    for d in date_strs:
        for h in habits:
            total += 1
            if is_done(logs, h, d):
                done += 1
    return round(100 * done / total) if total else 0


def needs_attention(logs, habits, date_strs):
    """The habit done least often over the dates, or None when no habits."""
    if not habits or not date_strs:
        return None
    worst = None
    worst_rate = None
    for h in habits:
        done = sum(1 for d in date_strs if is_done(logs, h, d))
        rate = done / len(date_strs)
        if worst_rate is None or rate < worst_rate:
            worst, worst_rate = h, rate
    return worst
