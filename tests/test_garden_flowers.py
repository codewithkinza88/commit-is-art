"""Plain-script tests for the flower garden (app/garden.py + theme).

Kinza asked (17 Nov 2026, WhatsApp) for proper flowers that grow in
the garden — lots of them as soon as it opens — instead of every
completed habit turning the same parrot-green colour.

Run:  python3 tests/test_garden_flowers.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.garden import (  # noqa: E402
    average_stage_progress, count_blooming, count_seeds, count_sprouts,
    flower_bed, flower_count, flower_for, flowers_for_stage,
    plant_for, plant_of_the_day, plant_with_longest_streak,
)
from app.habits import new_habit  # noqa: E402
from app.theme import STAGE_COLOURS, stage_colour  # noqa: E402
from app.tracker import set_done  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_garden_flowers():
    check("a seed is still just a seed",
          flowers_for_stage("seed") == "🌱")
    check("a sprout already has a flower",
          "🌸" in flowers_for_stage("sprout"))
    check("flowers grow in number as the plant blooms",
          len(flowers_for_stage("sprout"))
          < len(flowers_for_stage("growing"))
          < len(flowers_for_stage("blooming"))
          < len(flowers_for_stage("full_bloom")))
    check("full bloom is a whole bouquet, not one flower",
          len(flowers_for_stage("full_bloom")) >= 7)
    check("unknown stage falls back to a seed",
          flowers_for_stage("mystery") == "🌱")
    check("no stage colour is green (no parrot garden)",
          all(not c.upper().startswith("#C8E6")
              and c.upper() not in ("#E8F5E9", "#DCEDC8", "#C8E6C9")
              for c in STAGE_COLOURS.values()))
    check("every stage tint is a floral pastel (cream/blush/lilac/pink)",
          all(c.upper() in ("#FFF3D6", "#FDE7F3", "#EDE7FB",
                            "#FCE4EC", "#F8BBD0")
              for c in STAGE_COLOURS.values()))
    check("unknown stage falls back to the cream seed tint",
          stage_colour("mystery") == "#FFF3D6")

    habits = [new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF",
                        "2026-11-17"),
              new_habit("Read a book", "Books", 30, "📖", "#F9A8D4",
                        "2026-11-17")]
    logs = {}
    check("a plant carries its flowers",
          plant_for(habits[0], logs, "2026-11-17")["flowers"] == "🌱")
    set_done(logs, habits[0]["id"], "2026-11-17", True)
    set_done(logs, habits[1]["id"], "2026-11-17", True)
    check("a ticked plant shows flowers, not just a seed",
          "🌸" in plant_for(habits[0], logs, "2026-11-17")["flowers"])
    plants = [plant_for(h, logs, "2026-11-17") for h in habits]
    bed = flower_bed(plants)
    check("the flower bed shows lots of flowers on opening",
          len(bed) >= 2)
    check("the flower bed is empty with no habits",
          flower_bed([]) == "")
    check("each plant gets its own flower, stable per habit",
          flower_for("blooming", habits[0]["id"])
          == flower_for("blooming", habits[0]["id"]))
    check("different habits get different flowers",
          len({flower_for("blooming", f"habit-{i}")
               for i in range(10)}) > 1)
    check("a seed is still just a seed for its own flower",
          flower_for("seed", habits[0]["id"]) == "🌱")
    check("the flower bed grows with streaks",
          len(flower_bed([{"habit_id": "a", "stage": "sprout",
                           "streak": 1}]))
          < len(flower_bed([{"habit_id": "a", "stage": "sprout",
                             "streak": 5}])))
    check("blooming plants add extra flowers to the bed",
          len(flower_bed([{"habit_id": "a", "stage": "blooming",
                           "streak": 1}]))
          > len(flower_bed([{"habit_id": "a", "stage": "sprout",
                             "streak": 1}])))
    check("the flower bed caps at 40 flowers",
          len(flower_bed([{"habit_id": f"h{i}", "stage": "full_bloom",
                           "streak": 30} for i in range(10)])) == 40)


def test_plant_of_the_day():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    check("no habits means no plant of the day",
          plant_of_the_day([], {}, "2026-11-10") is None)
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    set_done(logs, h2["id"], "2026-11-09", True)
    star = plant_of_the_day([h1, h2], logs, "2026-11-10")
    check("longest waiting streak is the star",
          star["habit_id"] == h1["id"])
    set_done(logs, h1["id"], "2026-11-10", True)
    star = plant_of_the_day([h1, h2], logs, "2026-11-10")
    check("a watered plant loses the spotlight",
          star["habit_id"] == h2["id"])
    set_done(logs, h2["id"], "2026-11-10", True)
    star = plant_of_the_day([h1, h2], logs, "2026-11-10")
    check("all watered falls back to longest streak",
          star["habit_id"] == h1["id"])


def test_plant_with_longest_streak():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    check("no habits means no longest-streak plant",
          plant_with_longest_streak([], {}, "2026-11-09") is None)
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    set_done(logs, h2["id"], "2026-11-09", True)
    check("longest current streak wins",
          plant_with_longest_streak([h1, h2], logs, "2026-11-09")["habit_id"]
          == h1["id"])
    logs = {}
    set_done(logs, h1["id"], "2026-11-09", True)
    set_done(logs, h2["id"], "2026-11-09", True)
    check("a tie goes to the first-created plant",
          plant_with_longest_streak([h1, h2], logs, "2026-11-09")["habit_id"]
          == h1["id"])


def test_flower_count():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    logs = {}
    for day in ("2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06",
                "2026-11-07", "2026-11-08", "2026-11-09"):
        set_done(logs, h1["id"], day, True)
    check("a full-bloom plant counts streak plus 5",
          flower_count([h1], logs, "2026-11-09") == 7 + 5)
    check("a fresh plant still counts one flower",
          flower_count([h2], logs, "2026-11-09") == 1)
    check("two plants add up",
          flower_count([h1, h2], logs, "2026-11-09") == 13)
    check("no habits means no flowers",
          flower_count([], logs, "2026-11-09") == 0)


def test_count_blooming():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-09", True)
    # h1 streak 4 -> blooming; h2 streak 1 -> sprout; h3 seed.
    check("one blooming plant counts as 1",
          count_blooming([h1, h2, h3], logs, "2026-11-09") == 1)
    check("a sprout does not count as blooming",
          count_blooming([h2], logs, "2026-11-09") == 0)
    check("no habits means nothing blooming",
          count_blooming([], logs, "2026-11-09") == 0)


def test_count_seeds():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-09", True)
    # h1 streak 4 -> blooming; h2 streak 1 -> sprout; h3 seed.
    check("one seed waits for its first day",
          count_seeds([h1, h2, h3], logs, "2026-11-09") == 1)
    check("a sprout is not a seed",
          count_seeds([h2], logs, "2026-11-09") == 0)
    check("no habits means no seeds",
          count_seeds([], logs, "2026-11-09") == 0)


def test_count_sprouts():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-06", "2026-11-07", "2026-11-08", "2026-11-09"):
        set_done(logs, h1["id"], day, True)
    set_done(logs, h2["id"], "2026-11-09", True)
    # h1 streak 4 -> blooming; h2 streak 1 -> sprout; h3 seed.
    check("one sprout grows",
          count_sprouts([h1, h2, h3], logs, "2026-11-09") == 1)
    check("a seed is not a sprout",
          count_sprouts([h3], logs, "2026-11-09") == 0)
    check("no habits means no sprouts",
          count_sprouts([], logs, "2026-11-09") == 0)


def test_average_stage_progress():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Reading", 0, "📖", "#FFC6FF", "2026-11-01")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-05", "2026-11-06", "2026-11-07",
                "2026-11-08", "2026-11-09"):
        set_done(logs, h1["id"], day, True)
    for day in ("2026-11-07", "2026-11-08", "2026-11-09"):
        set_done(logs, h2["id"], day, True)
    # Streaks 6, 3, 0 -> progress 0.67, 0.5, 0.0 -> mean 0.39.
    check("average stage progress is 0.39",
          average_stage_progress([h1, h2, h3], logs, "2026-11-09") == 0.39)
    check("no habits average 0.0 progress",
          average_stage_progress([], logs, "2026-11-09") == 0.0)


if __name__ == "__main__":
    test_garden_flowers()
    test_plant_of_the_day()
    test_plant_with_longest_streak()
    test_flower_count()
    test_count_blooming()
    test_count_seeds()
    test_count_sprouts()
    test_average_stage_progress()
    print(f"{PASSED} tests passed")
