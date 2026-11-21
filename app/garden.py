"""Garden growth stages (pure logic, no Flet).

Each habit is a plant. Its stage grows with its streak of consecutive
completed days, and ticking it today gives it a little boost.
"""

import hashlib

# (minimum streak, stage key, emoji, label, message)
_STAGES = [
    (7, "full_bloom", "🌷", "Full bloom!", "A beautiful flower — a whole week strong!"),
    (4, "blooming", "🌸", "Blooming", "Your plant is blooming, keep watering it!"),
    (2, "growing", "🪴", "Growing", "Growing nicely — two days and counting!"),
    (1, "sprout", "🌿", "Sprout", "A little sprout appeared!"),
    (0, "seed", "🌱", "Seed", "A tiny seed, waiting for its first day of care."),
]


# Flowers per stage — proper flowers that grow in number as the plant
# blooms, so opening the Garden shows lots of flowers at once instead
# of one emoji on a green card. A seed is still just a seed (honest),
# but from the first sprout there are real flowers.
FLOWERS_BY_STAGE = {
    "seed": "🌱",
    "sprout": "🌿🌸",
    "growing": "🌿🌸🌷",
    "blooming": "🌸🌷🌼🌸🌷",
    "full_bloom": "🌷🌸🌼🌺🌻🌷🌸",
}


def flowers_for_stage(stage):
    """The flower row for a growth stage (more flowers as it blooms)."""
    return FLOWERS_BY_STAGE.get(stage or "seed", "🌱")


# One flower per plant — every plant gets its own flower, picked
# deterministically from its habit id and stage (never random at
# runtime), so the same plant always shows the same flower and
# different plants show different flowers.
_FLOWERS = ("🌷", "🌸", "🌼", "🌻", "🌺", "💐")


def flower_for(stage, habit_id):
    """A plant's own flower.

    A seed is still just a seed (honest); from the first sprout the
    flower is picked by hashing the habit id together with the stage,
    so it is stable for the same plant and varies across plants.
    """
    if (stage or "seed") == "seed":
        return "🌱"
    key = f"{habit_id}:{stage}".encode("utf-8")
    index = int(hashlib.md5(key).hexdigest(), 16) % len(_FLOWERS)
    return _FLOWERS[index]


FLOWER_BED_CAP = 40


def flower_bed(plants):
    """One big flower row for the whole garden — lots of flowers.

    Takes the plant dicts from plant_for / garden_summary: one flower
    per streak day per plant (at least one per plant, so even a new
    garden blooms), plus 3 extra for a blooming plant and 5 extra for
    one in full bloom. Capped at 40 flowers so the row stays a row.
    Empty when there are no plants.
    """
    flowers = []
    for plant in (plants or []):
        stage = plant.get("stage") or "seed"
        count = max(1, int(plant.get("streak") or 0))
        if stage == "blooming":
            count += 3
        elif stage == "full_bloom":
            count += 5
        flowers.append(flower_for(stage, plant.get("habit_id")) * count)
    return "".join(flowers)[:FLOWER_BED_CAP]


def flower_count(habits, logs, date_str):
    """How many flowers the whole garden is showing on a date.

    Same count as flower_bed() but without the 40-flower display cap:
    one flower per streak day per plant (at least one per plant), plus
    3 extra for a blooming plant and 5 extra for one in full bloom.
    0 when there are no habits.
    """
    plants = [plant_for(h, logs, date_str) for h in (habits or [])]
    total = 0
    for plant in plants:
        count = max(1, int(plant.get("streak") or 0))
        if plant.get("stage") == "blooming":
            count += 3
        elif plant.get("stage") == "full_bloom":
            count += 5
        total += count
    return total


def count_blooming(habits, logs, date_str):
    """How many plants are blooming or in full bloom on a date.

    A plant counts once its streak reaches the blooming stage (4 days)
    — a sprout or a growing plant does not count yet. 0 when there
    are no habits.
    """
    plants = [plant_for(h, logs, date_str) for h in (habits or [])]
    return sum(1 for plant in plants
               if plant.get("stage") in ("blooming", "full_bloom"))


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


def days_to_next_stage(streak):
    """Days until the plant reaches its next growth stage.

    0 when the plant is already in full bloom (the last stage).
    """
    streak = max(0, int(streak or 0))
    for minimum, _stage, _emoji, _label, _message in reversed(_STAGES):
        if minimum > streak:
            return minimum - streak
    return 0


# Growth thresholds: seed 0, sprout 1, growing 2, blooming 4, full bloom 7.
_STAGE_THRESHOLDS = [0, 1, 2, 4, 7]


def stage_progress(streak):
    """How far a plant is toward its next growth stage (0.0-1.0).

    0.0 at the start of a stage, 1.0 once it is in full bloom.
    """
    streak = max(0, int(streak or 0))
    if streak >= _STAGE_THRESHOLDS[-1]:
        return 1.0
    for prev, nxt in zip(_STAGE_THRESHOLDS, _STAGE_THRESHOLDS[1:]):
        if prev <= streak < nxt:
            return (streak - prev) / (nxt - prev)
    return 0.0


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
        "flowers": flowers_for_stage(stage["stage"]),
        **stage,
    }


def next_habit_to_water(habits, logs, date_str):
    """First habit (in creation order) not yet done on a date.

    Returns None when every habit is done (or there are no habits).
    """
    from app.tracker import is_done
    for habit in (habits or []):
        if not is_done(logs, habit, date_str):
            return habit
    return None


def plant_of_the_day(habits, logs, date_str):
    """The garden's spotlight plant: the longest streak among plants
    not yet done today — or the longest streak overall when every
    plant is already watered. None when there are no habits.

    Ties go to the plant first in creation order.
    """
    plants = [plant_for(h, logs, date_str) for h in (habits or [])]
    if not plants:
        return None
    waiting = [p for p in plants if not p["done_today"]]
    pool = waiting if waiting else plants
    return max(pool, key=lambda p: p["streak"])


def plant_with_longest_streak(habits, logs, date_str):
    """The plant with the longest current streak (first-created wins
    ties). None when there are no habits.
    """
    plants = [plant_for(h, logs, date_str) for h in (habits or [])]
    if not plants:
        return None
    return max(plants, key=lambda p: p["streak"])


def plants_by_stage(habits, logs, date_str):
    """How many plants sit at each growth stage on a date.

    Only stages with at least one plant are included.
    """
    counts = {}
    for habit in (habits or []):
        stage = plant_for(habit, logs, date_str)["stage"]
        counts[stage] = counts.get(stage, 0) + 1
    return counts


def total_plants(habits):
    """How many plants are in the garden (0 when there are no habits)."""
    return len(habits or [])


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
    done_count = len(plants) - due_today
    percent_done = round(100 * done_count / len(plants)) if plants else 0
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
            "due_today": due_today, "percent_done": percent_done}
