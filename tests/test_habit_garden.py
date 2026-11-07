"""Plain-script tests for Habit Garden (pytest is not installed here).

Run:  python3 tests/test_habit_garden.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import (  # noqa: E402
    new_habit, add_habit, edit_habit, delete_habit, get_habit,
)
from app.tracker import (  # noqa: E402
    set_done, toggle_done, log_minutes, is_done, minutes_for,
    current_streak, daily_summary, last_7_days,
)
from app.garden import growth_stage, garden_summary, empty_garden_message  # noqa: E402
from app.store import empty_store, seed_store, load_store, save_store  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_add_edit_delete_habit():
    habits = []
    habit = new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07")
    add_habit(habits, habit)
    check("add_habit", len(habits) == 1 and habits[0]["name"] == "Study — DSA")
    check("edit_habit rename + target",
          edit_habit(habits, habit["id"], name="Study — DSA / course",
                     target_minutes=90)
          and habits[0]["name"] == "Study — DSA / course"
          and habits[0]["target_minutes"] == 90)
    check("edit_habit unknown id returns False",
          edit_habit(habits, "nope", name="X") is False)
    check("edit_habit blank name is ignored",
          edit_habit(habits, habit["id"], name="   ")
          and habits[0]["name"] == "Study — DSA / course")
    check("delete_habit", delete_habit(habits, habit["id"]) and habits == [])
    check("delete_habit unknown id returns False",
          delete_habit(habits, "nope") is False)
    check("get_habit missing returns None", get_habit(habits, "nope") is None)


def test_tick_and_minutes():
    habits = [new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07")]
    habit = habits[0]
    logs = {}
    check("not done at first", is_done(logs, habit, "2026-11-07") is False)
    set_done(logs, habit["id"], "2026-11-07", True)
    check("tick marks done", is_done(logs, habit, "2026-11-07") is True)
    check("toggle unticks", toggle_done(logs, habit["id"], "2026-11-07") is False)
    check("log_minutes adds up", log_minutes(logs, habit["id"], "2026-11-07", 15) == 15
          and log_minutes(logs, habit["id"], "2026-11-07", 15) == 30)
    check("minutes reach target counts as done",
          minutes_for(logs, habit["id"], "2026-11-07") == 30
          and is_done(logs, habit, "2026-11-07") is True)
    check("log_minutes ignores bad input",
          log_minutes(logs, habit["id"], "2026-11-07", "oops") == 30)


def test_streak_and_summary():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-05"),
        new_habit("Drink water", "Health", 0, "💧", "#BDE0FE", "2026-11-05"),
    ]
    logs = {}
    # Study done 3 days in a row, reading only today.
    for day in ("2026-11-05", "2026-11-06", "2026-11-07"):
        set_done(logs, habits[0]["id"], day, True)
    set_done(logs, habits[1]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[1]["id"], "2026-11-07", 20)
    check("streak 3 days", current_streak(logs, habits[0],
          end_date=__import__("datetime").date(2026, 11, 7)) == 3)
    check("streak 1 day for reading", current_streak(
        logs, habits[1], end_date=__import__("datetime").date(2026, 11, 7)) == 1)
    summary = daily_summary(logs, habits, "2026-11-07")
    check("daily summary 2 of 3 done", summary["done"] == 2 and summary["total"] == 3)
    check("daily summary percent", summary["percent"] == 67)
    check("daily summary total minutes", summary["total_minutes"] == 65)
    check("daily summary best habit", summary["best_habit"] == "Study — DSA")
    week = last_7_days(logs, habits,
                       end_date=__import__("datetime").date(2026, 11, 7))
    check("last 7 days has 7 entries", len(week) == 7)
    check("last 7 days oldest first", week[0]["date"] == "2026-11-01"
          and week[-1]["date"] == "2026-11-07")


def test_garden_stages():
    check("seed at streak 0", growth_stage(0)["stage"] == "seed")
    check("tick today grows a sprout", growth_stage(0, True)["stage"] == "sprout")
    check("sprout at streak 1", growth_stage(1)["stage"] == "sprout")
    check("growing at streak 2", growth_stage(2)["stage"] == "growing")
    check("blooming at streak 4", growth_stage(4)["stage"] == "blooming")
    check("full bloom at streak 7", growth_stage(7)["stage"] == "full_bloom")
    habits = [new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    summary = garden_summary(habits, logs, "2026-11-07")
    check("garden summary has one sprout",
          summary["counts"].get("sprout") == 1
          and summary["plants"][0]["label"] == "Sprout")


def test_empty_store_and_seed():
    check("empty summary is 0%", daily_summary({}, [], "2026-11-07")["percent"] == 0)
    check("empty garden message", "empty" in garden_summary([], {}, "2026-11-07")["message"])
    store = seed_store()
    check("seed store has 3 starter habits", len(store["habits"]) == 3)
    check("seed habits are editable sample data",
          store["habits"][0]["name"] == "Study — DSA / course"
          and store["habits"][1]["target_minutes"] == 30)
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "store.json")
        check("missing file loads empty", load_store(path) == empty_store())
        save_store(store, path)
        loaded = load_store(path)
        check("save/load round-trip", len(loaded["habits"]) == 3)
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not json")
        check("corrupt file loads empty", load_store(path) == empty_store())


def test_empty_garden_message():
    message = empty_garden_message()
    check("empty garden message mentions empty", "empty" in message)
    check("empty garden message matches garden summary",
          message == garden_summary([], {}, "2026-11-07")["message"])


if __name__ == "__main__":
    test_add_edit_delete_habit()
    test_tick_and_minutes()
    test_streak_and_summary()
    test_garden_stages()
    test_empty_store_and_seed()
    test_empty_garden_message()
    print(f"{PASSED} tests passed")
