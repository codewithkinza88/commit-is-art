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
    flower_bed, flower_for, flowers_for_stage, plant_for,
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


if __name__ == "__main__":
    test_garden_flowers()
    print(f"{PASSED} tests passed")
