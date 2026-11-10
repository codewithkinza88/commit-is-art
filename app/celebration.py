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
