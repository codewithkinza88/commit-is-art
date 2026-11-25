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


def done_rate_overall(logs, habits, date_strs):
    """Share of habit-days done over the dates, as a percent (0-100).

    Total done ticks over habits x dates; 0 when there are no
    dates or no habits. The overall form of consistency_score.
    """
    return consistency_score(logs, habits, date_strs)


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


def done_rate_for_habit(logs, habit, date_strs):
    """Done rate for one habit over the dates, as a fraction 0.0-1.0.

    Done days / window days; 0.0 when there is no habit or no
    dates. The per-habit rate behind least_consistent_habit.
    """
    if not habit or not date_strs:
        return 0.0
    done = sum(1 for d in date_strs if is_done(logs, habit, d))
    return done / len(date_strs)


def most_consistent_habit(logs, habits, date_strs):
    """The habit done most often over the dates, or None when no habits.

    First habit wins a tie (creation order), mirroring needs_attention.
    """
    if not habits or not date_strs:
        return None
    best = None
    best_rate = None
    for h in habits:
        done = sum(1 for d in date_strs if is_done(logs, h, d))
        rate = done / len(date_strs)
        if best_rate is None or rate > best_rate:
            best, best_rate = h, rate
    return best


def least_consistent_habit(logs, habits, date_strs):
    """The habit done least often over the dates, or None when no habits.

    Mirror of most_consistent_habit: first habit wins a tie
    (creation order), mirroring needs_attention.
    """
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


def weekly_done_rate(logs, habits, end_date=None):
    """Share of habit-days done over the last 7 days, as a percent.

    A thin wrapper over consistency_score with the 7 date strings
    ending on end_date (default today). 0-100, and 0 when there are
    no habits.
    """
    from datetime import date as _date
    from datetime import timedelta as _timedelta

    if isinstance(end_date, str):
        end = _date.fromisoformat(end_date)
    else:
        end = end_date or _date.today()
    date_strs = [(end - _timedelta(days=i)).isoformat() for i in range(7)]
    return consistency_score(logs, habits, date_strs)


def habits_below_rate(logs, habits, date_strs, threshold=50):
    """Habits done less than `threshold` percent over the dates.

    Creation order is kept; [] when every habit meets the rate
    (or there are no habits/dates). The strict less-than means a
    habit exactly at the threshold does not count.
    """
    if not habits or not date_strs:
        return []
    below = []
    for h in habits:
        done = sum(1 for d in date_strs if is_done(logs, h, d))
        rate = 100 * done / len(date_strs)
        if rate < threshold:
            below.append(h)
    return below


def habits_above_rate(logs, habits, date_strs, threshold=80):
    """Habits done at least `threshold` percent over the dates.

    Mirror of habits_below_rate, for the garden's stars instead
    of the ones needing attention. Creation order is kept; [] when
    no habit meets the rate (or there are no habits/dates). A habit
    exactly at the threshold counts — the rate is met, not beaten.
    """
    if not habits or not date_strs:
        return []
    above = []
    for h in habits:
        done = sum(1 for d in date_strs if is_done(logs, h, d))
        rate = 100 * done / len(date_strs)
        if rate >= threshold:
            above.append(h)
    return above


def average_consistency(logs, habits, date_strs):
    """Mean per-habit done-rate over the dates, as a percent (0-100).

    Different from consistency_score, which pools every habit-day
    together: this averages each habit's own rate, so a habit done
    every day and one never done average to 50. 0 when there are
    no habits or no dates.
    """
    if not habits or not date_strs:
        return 0
    rates = []
    for h in habits:
        done = sum(1 for d in date_strs if is_done(logs, h, d))
        rates.append(100 * done / len(date_strs))
    return round(sum(rates) / len(rates))


def consistency_message(score):
    """Warm one-liner for a consistency score (0-100)."""
    score = max(0, min(100, int(score or 0)))
    if score >= 90:
        return "Amazingly consistent! 🌸"
    if score >= 70:
        return "Really steady — keep it up! 🌷"
    if score >= 50:
        return "Halfway there — a little push! 🌱"
    if score >= 1:
        return "A slow week — tomorrow is fresh 💧"
    return "No ticks yet this week — plant one today 🌱"
