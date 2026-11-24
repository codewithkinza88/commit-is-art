"""Milestone celebration messages (pure logic, no Flet).

Different from daily motivation messages: these fire when a streak
reaches a milestone number of days.
"""

MILESTONES = {7: "One whole week! 🌸",
              14: "Two weeks strong! 🌷",
              30: "A full month of blooming! 🌻",
              100: "One hundred days — a real garden! 🌳"}


def milestone_message(streak):
    """Celebration text when streak hits a milestone, else ''."""
    return MILESTONES.get(int(streak or 0), "")


def is_milestone(streak):
    """True when the streak is a milestone day."""
    return int(streak or 0) in MILESTONES


def milestones_reached(streak):
    """Milestone streaks already reached, smallest first.

    The MILESTONES keys (7/14/30/100) at or below the streak —
    [] when the streak has not reached any milestone yet.
    """
    streak = max(0, int(streak or 0))
    return sorted(m for m in MILESTONES if m <= streak)


def days_to_next_milestone(streak):
    """(milestone, days_left) until the next milestone streak.

    Returns None when the streak is already past the last milestone
    (100 days). A streak sitting exactly on a milestone points at
    the next one.
    """
    streak = max(0, int(streak or 0))
    for milestone in sorted(MILESTONES):
        if milestone > streak:
            return milestone, milestone - streak
    return None


def celebration_for(streak):
    """{"emoji", "message"} celebrating a streak.

    A milestone streak (7/14/30/100) gets its milestone_message;
    any other streak gets "N days and growing!". The emoji is
    always the garden stage emoji for the streak, so a week-long
    streak blooms 🌷 and a fresh one sprouts 🌱.
    """
    from app.garden import growth_stage

    streak = max(0, int(streak or 0))
    emoji = growth_stage(streak)["emoji"]
    if is_milestone(streak):
        message = milestone_message(streak)
    else:
        message = (f"{streak} day{'s' if streak != 1 else ''} "
                   "and growing!")
    return {"emoji": emoji, "message": message}


def celebration_message(streak):
    """One-line celebration message for a streak.

    The milestone text on a milestone day, else "N days and
    growing!" — the message part of celebration_for, for places
    that only need the words.
    """
    return celebration_for(streak)["message"]


def next_milestone_message(streak):
    """A cheery line naming the next milestone and the days to go.

    "" (empty) when the streak is already at the highest milestone
    — there is nothing bigger to aim for.
    """
    streak = max(0, int(streak or 0))
    for milestone in sorted(MILESTONES):
        if streak < milestone:
            return (f"🎯 {milestone - streak} more day(s) to a "
                    f"{milestone}-day streak!")
    return ""
