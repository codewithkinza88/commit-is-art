"""Garden growth stages (pure logic, no Flet).

Each habit is a plant. Its stage grows with its streak of consecutive
completed days, and ticking it today gives it a little boost.
"""

# (minimum streak, stage key, emoji, label, message)
_STAGES = [
    (7, "full_bloom", "🌷", "Full bloom!", "A beautiful flower — a whole week strong!"),
    (4, "blooming", "🌸", "Blooming", "Your plant is blooming, keep watering it!"),
    (2, "growing", "🪴", "Growing", "Growing nicely — two days and counting!"),
    (1, "sprout", "🌿", "Sprout", "A little sprout appeared!"),
    (0, "seed", "🌱", "Seed", "A tiny seed, waiting for its first day of care."),
]


def growth_stage(streak, done_today=False):
    """Stage for a habit from its streak (and today's tick).

    A tick today counts as one day of growth even before a streak exists,
    so a brand-new habit ticked today shows as a sprout, not a seed.
    Returns {"stage", "emoji", "label", "message"}.
    """
    effective = max(int(streak or 0), 1 if done_today else 0)
    for minimum, stage, emoji, label, message in _STAGES:
        if effective >= minimum:
            return {"stage": stage, "emoji": emoji, "label": label,
                    "message": message}
    return {"stage": "seed", "emoji": "🌱", "label": "Seed",
            "message": "A tiny seed, waiting for its first day of care."}


def plant_for(habit, logs, date_str):
    """Full garden entry for one habit on a date."""
    from app.tracker import current_streak, is_done
    from datetime import date as _date
    end = _date.fromisoformat(date_str)
    streak = current_streak(logs, habit, end_date=end)
    done_today = is_done(logs, habit, date_str)
    stage = growth_stage(streak, done_today)
    return {
        "habit_id": habit["id"],
        "name": habit["name"],
        "icon": habit.get("icon", "🌱"),
        "colour": habit.get("colour", "#BDE0FE"),
        "streak": streak,
        "done_today": done_today,
        **stage,
    }


def counts_text(counts):
    """One short line of how many plants sit at each stage.

    Example: "🌱 2 seeds • 🌿 1 sprout • 🌸 1 blooming".
    With no plants at all: "No plants yet 🌱".
    """
    words = {
        "seed": ("seed", "seeds"),
        "sprout": ("sprout", "sprouts"),
        "growing": ("growing", "growing"),
        "blooming": ("blooming", "blooming"),
        "full_bloom": ("in full bloom", "in full bloom"),
    }
    parts = []
    for _minimum, stage, emoji, _label, _message in reversed(_STAGES):
        n = (counts or {}).get(stage, 0)
        if n:
            singular, plural = words[stage]
            parts.append(f"{emoji} {n} {singular if n == 1 else plural}")
    return " • ".join(parts) if parts else "No plants yet 🌱"


def empty_garden_message():
    """Friendly message shown when there are no habits (no plants) yet."""
    return "Your garden is empty — plant your first habit and watch it grow! 🌱"


def garden_summary(habits, logs, date_str):
    """All plants for a date, plus a count of plants at each stage.

    Also counts how many plants are still due today (not ticked yet).
    """
    plants = [plant_for(h, logs, date_str) for h in (habits or [])]
    counts = {}
    for plant in plants:
        counts[plant["stage"]] = counts.get(plant["stage"], 0) + 1
    due_today = sum(1 for plant in plants if not plant["done_today"])
    blooming = counts.get("blooming", 0) + counts.get("full_bloom", 0)
    if not plants:
        message = empty_garden_message()
    elif blooming == len(plants):
        message = "Your whole garden is blooming! 🌸✨ So proud of you!"
    elif blooming:
        message = f"{blooming} of your plants are blooming! 🌸"
    else:
        message = "Your garden is growing — tick a habit to water it! 💧🌱"
    return {"plants": plants, "counts": counts, "message": message,
            "due_today": due_today}
