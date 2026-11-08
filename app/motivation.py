"""Motivational messages (pure logic, no Flet).

Short, kind messages for the Tonight view, chosen from how much of
the day the user achieved — and a little cheer for a growing streak.
"""

_MESSAGES = [
    (100, "Perfect day! You did every single habit. 🌸✨"),
    (75, "So close to perfect — amazing work today! 🌷"),
    (50, "Halfway there — your garden is growing! 🪴"),
    (25, "A little progress is still progress. Keep going! 🌱"),
    (1, "You started today — that is the hardest part. 💧"),
    (0, "Tomorrow is a fresh seed — plant it again. 🌱"),
]


def message_for_percent(percent):
    """Message for a day's achievement percent (0-100)."""
    percent = max(0, min(100, int(percent or 0)))
    for minimum, message in _MESSAGES:
        if percent >= minimum:
            return message
    return _MESSAGES[-1][1]


def nightly_message(summary):
    """Tonight message from a daily_summary dict (percent + minutes)."""
    percent = summary.get("percent", 0)
    minutes = summary.get("total_minutes", 0)
    message = message_for_percent(percent)
    if percent >= 100 and minutes >= 60:
        return message + f" {minutes} minutes of focus — wow!"
    if minutes:
        return message + f" ({minutes} minutes today)"
    return message


def streak_message(streak):
    """Cheer for a streak length (0 = no streak yet)."""
    streak = max(0, int(streak or 0))
    if streak >= 7:
        return f"{streak} days in a row — a whole week strong! 🌷"
    if streak >= 3:
        return f"{streak} days in a row — keep the streak alive! 🌸"
    if streak >= 1:
        return "Day 1 of your streak — water it again tomorrow! 🌱"
    return "No streak yet — today is a good day to start. 🌱"
