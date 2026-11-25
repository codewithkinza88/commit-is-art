"""Streak helpers (pure logic, no Flet).

Builds on app.tracker.current_streak: this module answers the
questions the garden view wants — what is the longest streak a habit
ever had, and how long ago was it last done?
"""

from datetime import date, timedelta

from app.tracker import current_streak, is_done


def _done_dates(logs, habit, end_date=None):
    """Sorted list of dates (as date objects) the habit was done, up to end."""
    end = end_date or date.today()
    done = []
    for date_str in logs or {}:
        try:
            day = date.fromisoformat(date_str)
        except ValueError:
            continue
        if day <= end and is_done(logs, habit, date_str):
            done.append(day)
    return sorted(done)


def best_streak(logs, habit, end_date=None):
    """Longest run of consecutive done days ever (up to end_date)."""
    done = _done_dates(logs, habit, end_date)
    best = 0
    run = 0
    previous = None
    for day in done:
        if previous is not None and day == previous + timedelta(days=1):
            run += 1
        else:
            run = 1
        best = max(best, run)
        previous = day
    return best


def longest_gap(logs, habit, end_date=None):
    """Longest run of missed days between two done days.

    E.g. done Mon and Thu means a 2-day gap (Tue, Wed missed).
    0 when the habit was done fewer than twice.
    """
    done = _done_dates(logs, habit, end_date)
    if len(done) < 2:
        return 0
    return max((done[i + 1] - done[i]).days - 1
               for i in range(len(done) - 1))


def longest_streak_overall(logs, habits, end_date=None):
    """Longest best streak across all habits (0 when there are none)."""
    return max(
        (best_streak(logs, habit, end_date=end_date)
         for habit in (habits or [])),
        default=0)


def shortest_best_streak(logs, habits, end_date=None):
    """Smallest best streak across all habits (0 when there are none).

    Mirror of longest_streak_overall: the shortest ever-run any
    habit managed, so the garden can cheer on its slowest grower.
    """
    return min(
        (best_streak(logs, habit, end_date=end_date)
         for habit in (habits or [])),
        default=0)

def average_streak(logs, habits, end_date=None):
    """Mean best streak across all habits (0.0 when there are none)."""
    habits = list(habits or [])
    if not habits:
        return 0.0
    total = sum(best_streak(logs, habit, end_date=end_date)
                for habit in habits)
    return round(total / len(habits), 1)


def median_best_streak(logs, habits, end_date=None):
    """Median best streak across all habits (0.0 when there are none)."""
    values = sorted(best_streak(logs, habit, end_date=end_date)
                    for habit in (habits or []))
    if not values:
        return 0.0
    n = len(values)
    if n % 2:
        return float(values[n // 2])
    return round((values[n // 2 - 1] + values[n // 2]) / 2, 1)


def median_current_streak(logs, habits, end_date=None):
    """Median current streak across all habits (0.0 when there are none).

    Different from median_best_streak: this is about streaks alive
    right now, so a habit whose streak broke yesterday counts as 0.
    """
    values = sorted(current_streak(logs, habit, end_date=end_date)
                    for habit in (habits or []))
    if not values:
        return 0.0
    n = len(values)
    if n % 2:
        return float(values[n // 2])
    return round((values[n // 2 - 1] + values[n // 2]) / 2, 1)


def average_best_streak(logs, habits, end_date=None):
    """Mean best streak across all habits (0.0 when there are none)."""
    values = [best_streak(logs, habit, end_date=end_date)
              for habit in (habits or [])]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)


def habits_on_streak(logs, habits, end_date=None):
    """How many habits have a live streak right now (current >= 1).

    A habit whose streak broke yesterday counts as 0, so this is
    the number of plants still growing today. 0 when there are
    no habits (or none on a streak).
    """
    return sum(1 for habit in (habits or [])
               if current_streak(logs, habit, end_date=end_date) >= 1)


def habits_with_no_streak(logs, habits, end_date=None):
    """Names of habits with no live streak right now (current == 0).

    Creation order is kept; [] when every habit is on a streak
    (or there are no habits). The mirror of habits_on_streak, for
    the plants that need a fresh start today.
    """
    return [habit["name"] for habit in (habits or [])
            if current_streak(logs, habit, end_date=end_date) == 0]


def longest_current_streak(logs, habits, end_date=None):
    """Longest live streak across all habits (0 when there are none).

    Different from longest_streak_overall, which is about the best
    streak ever: this is the longest streak still alive right now.
    """
    return max(
        (current_streak(logs, habit, end_date=end_date)
         for habit in (habits or [])),
        default=0)


def habits_with_streak_at_least(logs, habits, minimum, end_date=None):
    """Names of habits whose current streak is at least `minimum`.

    Creation order is kept; [] when no habit reaches the level
    (or there are no habits). A minimum of 0 or less lists every
    habit, since every current streak is >= 0.
    """
    minimum = max(0, int(minimum or 0))
    return [habit["name"] for habit in (habits or [])
            if current_streak(logs, habit, end_date=end_date) >= minimum]


def habits_with_best_streak(logs, habits, end_date=None):
    """Names of the habits sharing the longest best streak ever.

    [] when there are no habits, or when no habit has any streak
    yet (a best streak of 0 is not a streak to share). Ties list
    every habit at the top, in creation order.
    """
    habits = list(habits or [])
    if not habits:
        return []
    bests = [best_streak(logs, habit, end_date=end_date)
             for habit in habits]
    top = max(bests)
    if top <= 0:
        return []
    return [habit["name"] for habit, best in zip(habits, bests)
            if best == top]


def streaks_by_habit(logs, habits, end_date=None):
    """Current streak per habit, keyed by habit id.

    {} when there are no habits. A habit whose streak broke
    counts as 0, so every habit is always in the map.
    """
    return {habit["id"]: current_streak(logs, habit, end_date=end_date)
            for habit in (habits or [])}


def streaks_sorted(logs, habits, end_date=None):
    """(name, current streak) pairs, longest streak first.

    Creation order breaks ties (the sort is stable); [] when
    there are no habits.
    """
    pairs = [(habit["name"],
              current_streak(logs, habit, end_date=end_date))
             for habit in (habits or [])]
    return sorted(pairs, key=lambda pair: pair[1], reverse=True)


def best_streaks_sorted(logs, habits, end_date=None):
    """(name, best streak) pairs, longest best streak first.

    Creation order breaks ties (the sort is stable); [] when
    there are no habits. The best-streak form of streaks_sorted.
    """
    pairs = [(habit["name"],
              best_streak(logs, habit, end_date=end_date))
             for habit in (habits or [])]
    return sorted(pairs, key=lambda pair: pair[1], reverse=True)


def count_habits_on_streak(logs, habits, end_date=None):
    """How many habits have a live streak right now (current >= 1).

    The count form of habits_on_streak; 0 when there are no
    habits (or none on a streak).
    """
    return habits_on_streak(logs, habits, end_date=end_date)


def total_streak_days(logs, habits, end_date=None):
    """Total live streak days across all habits.

    The sum of every habit's current streak — how many
    streak-days the whole garden holds right now. 0 when there
    are no habits (or none on a streak).
    """
    return sum(current_streak(logs, habit, end_date=end_date)
               for habit in (habits or []))


def days_since_last_done(logs, habit, end_date=None):
    """Days since the habit was last done (0 = done on end_date).

    Returns None when the habit was never done.
    """
    done = _done_dates(logs, habit, end_date)
    if not done:
        return None
    end = end_date or date.today()
    return (end - done[-1]).days


def streak_summary(logs, habit, end_date=None):
    """Current streak, best streak, and days since last done, in one dict."""
    end = end_date or date.today()
    return {
        "habit_id": habit["id"],
        "name": habit["name"],
        "current": current_streak(logs, habit, end_date=end),
        "best": best_streak(logs, habit, end_date=end),
        "days_since_last_done": days_since_last_done(logs, habit, end_date=end),
    }


def streak_leaderboard(logs, habits, end_date=None):
    """Habits ranked by current streak, longest first.

    Each entry is {"habit_id", "name", "current"}. Ties keep creation
    order (stable sort); [] when there are no habits.
    """
    end = end_date or date.today()
    board = [{
        "habit_id": habit["id"],
        "name": habit["name"],
        "current": current_streak(logs, habit, end_date=end),
    } for habit in (habits or [])]
    board.sort(key=lambda entry: -entry["current"])
    return board


def last_done_label(logs, habit, end_date=None):
    """Short label for when a habit was last done.

    "Done today 🌸" / "Last done yesterday" / "Last done N days ago"
    / "Not done yet 🌱" when it was never done.
    """
    days = days_since_last_done(logs, habit, end_date=end_date)
    if days is None:
        return "Not done yet 🌱"
    if days == 0:
        return "Done today 🌸"
    if days == 1:
        return "Last done yesterday"
    return f"Last done {days} days ago"
