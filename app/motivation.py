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


def evening_message(done, total):
    """A short wind-down message for the Tonight view."""
    done = max(0, int(done or 0))
    total = max(0, int(total or 0))
    if total == 0:
        return "No habits yet — tomorrow is a fresh seed. 🌱"
    if done >= total:
        return "Every habit done — rest well, your garden is blooming! 🌸"
    if done == 0:
        return "Nothing ticked today — tomorrow is a fresh start. 🌱"
    return f"{done} of {total} done today — a good day's growing! 🪴"


def comeback_message(days_since):
    """A warm welcome back after days away from a habit (0 = just here)."""
    days = max(0, int(days_since or 0))
    if days == 0:
        return "Welcome back — today is a fresh start. 🌱"
    if days == 1:
        return "One day away — your garden missed you! 🌱"
    if days <= 6:
        return f"{days} days away — come back and water your garden! 🌷"
    return (f"{days} days away — your garden is waiting, "
            "one small step today! 🌸")


def morning_message(done, total):
    """A short greeting for the Today view from how much is done already."""
    done = max(0, int(done or 0))
    total = max(0, int(total or 0))
    if total == 0:
        return "No habits yet — plant one and watch it grow! 🌱"
    if done >= total:
        return "All done already — what a lovely start! 🌸"
    if done == 0:
        return f"Good morning! {total} habits to water today. 🌱"
    return f"Good morning! {done} of {total} done — keep going! 🌸"

