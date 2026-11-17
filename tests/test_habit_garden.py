"""Plain-script tests for Habit Garden (pytest is not installed here).

Run:  python3 tests/test_habit_garden.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import (  # noqa: E402
    new_habit, add_habit, edit_habit, delete_habit, get_habit,
    archive_habit, active_habits, habits_by_category, count_by_category,
)
from app.tracker import (  # noqa: E402
    set_done, toggle_done, log_minutes, is_done, minutes_for,
    total_minutes_today, total_minutes_this_week, done_count_today,
    current_streak, daily_summary, last_7_days,
)
from app.garden import (  # noqa: E402
    counts_text, days_to_next_stage, growth_stage, garden_summary,
    empty_garden_message, next_habit_to_water, plants_by_stage,
    stage_progress, total_plants)
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
    check("one day to sprout from seed", days_to_next_stage(0) == 1)
    check("one day to growing at streak 1", days_to_next_stage(1) == 1)
    check("two days to blooming at streak 2", days_to_next_stage(2) == 2)
    check("no days left in full bloom", days_to_next_stage(7) == 0)
    habits = [new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    summary = garden_summary(habits, logs, "2026-11-07")
    check("garden summary has one sprout",
          summary["counts"].get("sprout") == 1
          and summary["plants"][0]["label"] == "Sprout")
    check("due today is zero when the only habit is done",
          summary["due_today"] == 0)
    second = new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07")
    summary2 = garden_summary(habits + [second], logs, "2026-11-07")
    check("due today counts undone habits", summary2["due_today"] == 1)
    check("due today is all when nothing is done",
          garden_summary(habits + [second], {}, "2026-11-07")["due_today"] == 2)


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


def test_garden_counts_text():
    check("counts text lists seeds and sprouts",
          counts_text({"seed": 2, "sprout": 1})
          == "🌱 2 seeds • 🌿 1 sprout")
    check("counts text handles full bloom",
          counts_text({"full_bloom": 2}) == "🌷 2 in full bloom")
    check("counts text is empty without plants",
          counts_text({}) == "No plants yet 🌱")
    check("counts text skips zero stages",
          "🌿" not in counts_text({"seed": 1}))


def test_empty_garden_message():
    message = empty_garden_message()
    check("empty garden message mentions empty", "empty" in message)
    check("empty garden message matches garden summary",
          message == garden_summary([], {}, "2026-11-07")["message"])


def test_total_minutes_today():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-05"),
    ]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[1]["id"], "2026-11-07", 20)
    check("total minutes today sums habits",
          total_minutes_today(logs, habits, "2026-11-07") == 65)
    check("total minutes today is 0 on an empty day",
          total_minutes_today(logs, habits, "2026-11-08") == 0)
    check("total minutes today is 0 with no habits",
          total_minutes_today(logs, [], "2026-11-07") == 0)


def test_next_habit_to_water():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-05"),
    ]
    logs = {}
    check("next to water is the first habit",
          next_habit_to_water(habits, logs, "2026-11-07") is habits[0])
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    check("next to water skips done habits",
          next_habit_to_water(habits, logs, "2026-11-07") is habits[1])
    set_done(logs, habits[1]["id"], "2026-11-07", True)
    check("next to water is None when all done",
          next_habit_to_water(habits, logs, "2026-11-07") is None)


def test_archive_habit():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
    ]
    check("new habits are not archived", habits[0].get("archived") is False)
    check("archive_habit archives and returns the habit",
          archive_habit(habits, habits[0]["id"]) is habits[0]
          and habits[0]["archived"] is True)
    check("active_habits hides archived ones",
          active_habits(habits) == [habits[1]])
    check("archive_habit unknown id returns None",
          archive_habit(habits, "nope") is None)
    check("habits saved before archiving count as active",
          active_habits([{"id": "old", "name": "Old habit"}])[0]["id"] == "old")


def test_done_count_today():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
    ]
    logs = {}
    check("done count is 0 with nothing done",
          done_count_today(logs, habits, "2026-11-07") == 0)
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    check("done count is 1 with one habit done",
          done_count_today(logs, habits, "2026-11-07") == 1)
    check("done count is 0 on an empty day",
          done_count_today(logs, habits, "2026-11-08") == 0)


def test_plants_by_stage():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-05"),
    ]
    logs = {}
    check("plants by stage are seeds with nothing done",
          plants_by_stage(habits, logs, "2026-11-07") == {"seed": 2})
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    check("plants by stage splits done and undone",
          plants_by_stage(habits, logs, "2026-11-07") == {"sprout": 1, "seed": 1})
    check("plants by stage is empty with no habits",
          plants_by_stage([], {}, "2026-11-07") == {})


def test_habits_by_category():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
        new_habit("Revise notes", "Study", 30, "✍️", "#FFE5A3", "2026-11-07"),
    ]
    check("habits by category returns both Study habits",
          [h["name"] for h in habits_by_category(habits, "Study")]
          == ["Study — DSA", "Revise notes"])
    check("habits by category with no match is empty",
          habits_by_category(habits, "Health") == [])
    check("habits by category on an empty list is empty",
          habits_by_category([], "Study") == [])


def test_garden_percent_done():
    habits = [
        new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
    ]
    logs = {}
    check("percent done is 0 with nothing done",
          garden_summary(habits, logs, "2026-11-07")["percent_done"] == 0)
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    check("percent done is 50 with one of two done",
          garden_summary(habits, logs, "2026-11-07")["percent_done"] == 50)
    check("percent done is 0 with no plants",
          garden_summary([], {}, "2026-11-07")["percent_done"] == 0)



def test_total_minutes_this_week():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[0]["id"], "2026-11-06", 20)
    log_minutes(logs, habits[0]["id"], "2026-10-30", 99)
    check("total minutes this week sums the last 7 days",
          total_minutes_this_week(logs, habits, "2026-11-07") == 65)
    check("total minutes this week is 0 with no logs",
          total_minutes_this_week({}, habits, "2026-11-07") == 0)
    check("total minutes this week is 0 with no habits",
          total_minutes_this_week(logs, [], "2026-11-07") == 0)


def test_total_plants():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05"),
              new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-05")]
    check("total plants counts the habits", total_plants(habits) == 2)
    check("total plants is 0 with no habits", total_plants([]) == 0)
    check("total plants is 0 with None", total_plants(None) == 0)


def test_count_by_category():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
              new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
              new_habit("Revise", "Study", 30, "✍️", "#FFE5A3", "2026-11-07")]
    check("count by category groups Study and Books",
          count_by_category(habits) == {"Study": 2, "Books": 1})
    check("count by category is empty with no habits",
          count_by_category([]) == {})
    check("count by category is empty with None",
          count_by_category(None) == {})


def test_stage_progress():
    check("stage progress is 0 at a fresh seed", stage_progress(0) == 0.0)
    check("stage progress is 0 at the start of sprout",
          stage_progress(1) == 0.0)
    check("stage progress is halfway through growing",
          stage_progress(3) == 0.5)
    check("stage progress is 1 in full bloom", stage_progress(7) == 1.0)
    check("stage progress stays 1 past a week", stage_progress(10) == 1.0)

if __name__ == "__main__":
    test_add_edit_delete_habit()
    test_tick_and_minutes()
    test_streak_and_summary()
    test_garden_stages()
    test_garden_counts_text()
    test_empty_store_and_seed()
    test_empty_garden_message()
    test_total_minutes_today()
    test_next_habit_to_water()
    test_archive_habit()
    test_garden_percent_done()
    test_done_count_today()
    test_plants_by_stage()
    test_habits_by_category()
    test_total_minutes_this_week()
    test_total_plants()
    test_count_by_category()
    test_stage_progress()
    print(f"{PASSED} tests passed")

