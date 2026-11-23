"""Plain-script tests for Habit Garden (pytest is not installed here).

Run:  python3 tests/test_habit_garden.py
"""

import os
import sys
import tempfile
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import (  # noqa: E402
    new_habit, add_habit, edit_habit, delete_habit, get_habit,
    archive_habit, active_habits, habits_by_category, count_by_category,
    count_by_effort, newest_habit, oldest_habit, habits_with_target,
    clone_habit, habit_age_days, validate_effort,
)
from app.tracker import (  # noqa: E402
    set_done, toggle_done, log_minutes, is_done, minutes_for,
    total_minutes_today, total_minutes_this_week, total_minutes_yesterday,
    total_minutes_in_range, total_minutes_last_30_days,
    best_day_by_minutes, days_done_this_week, first_done_date,
    done_count_today,
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


def test_days_done_this_week():
    habit = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    for day in ("2026-11-04", "2026-11-06", "2026-11-07"):
        set_done(logs, habit["id"], day, True)
    check("three non-consecutive days count as 3",
          days_done_this_week(logs, habit, "2026-11-07") == 3)
    check("days done is 0 with no logs",
          days_done_this_week({}, habit, "2026-11-07") == 0)
    check("days done is 0 outside the window",
          days_done_this_week(logs, habit, "2026-11-20") == 0)


def test_first_done_date():
    habit = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    set_done(logs, habit["id"], "2026-11-06", True)
    set_done(logs, habit["id"], "2026-11-04", True)
    set_done(logs, habit["id"], "2026-11-07", True)
    check("first done date is the earliest done day",
          first_done_date(logs, habit) == "2026-11-04")
    check("never done has no first date",
          first_done_date({}, habit) == "")
    check("a ticked day counts even without minutes",
          first_done_date(logs, habit) != "")


def test_total_minutes_last_30_days():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[0]["id"], "2026-10-20", 30)
    log_minutes(logs, habits[0]["id"], "2026-10-08", 99)
    check("last 30 days sums the 30-day window",
          total_minutes_last_30_days(logs, habits, "2026-11-07") == 75)
    check("last 30 days is 0 with no logs",
          total_minutes_last_30_days({}, habits, "2026-11-07") == 0)
    check("last 30 days is 0 with no habits",
          total_minutes_last_30_days(logs, [], "2026-11-07") == 0)


def test_total_minutes_in_range():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-06", 20)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[0]["id"], "2026-11-09", 10)
    check("range total adds both days in the range",
          total_minutes_in_range(logs, habits, "2026-11-06",
                                 "2026-11-07") == 65)
    check("range total skips days outside the range",
          total_minutes_in_range(logs, habits, "2026-11-06",
                                 "2026-11-06") == 20)
    check("a reversed range is 0",
          total_minutes_in_range(logs, habits, "2026-11-09",
                                 "2026-11-06") == 0)
    check("an empty log range is 0",
          total_minutes_in_range({}, habits, "2026-11-06",
                                 "2026-11-07") == 0)


def test_best_day_by_minutes():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-06", 20)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    log_minutes(logs, habits[0]["id"], "2026-11-09", 10)
    best = best_day_by_minutes(logs, habits, date(2026, 11, 9))
    check("best day by minutes is 2026-11-07",
          best == {"date": "2026-11-07", "minutes": 45})
    check("no minutes logged means no best day",
          best_day_by_minutes({}, habits, date(2026, 11, 9)) is None)
    log_minutes(logs, habits[0]["id"], "2026-11-09", 35)
    check("a tie goes to the most recent day",
          best_day_by_minutes(logs, habits, date(2026, 11, 9))["date"]
          == "2026-11-09")


def test_total_minutes_yesterday():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")]
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-06", 20)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    check("total minutes yesterday reads the day before",
          total_minutes_yesterday(logs, habits, "2026-11-07") == 20)
    check("total minutes yesterday is 0 with no logs",
          total_minutes_yesterday({}, habits, "2026-11-07") == 0)
    check("total minutes yesterday is 0 with no habits",
          total_minutes_yesterday(logs, [], "2026-11-07") == 0)


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


def test_count_by_effort():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-07"),
              new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-07"),
              new_habit("Revise", "Study", 30, "✍️", "#FFE5A3", "2026-11-07")]
    habits[0]["effort"] = "Hard"
    habits[1]["effort"] = "Easy"
    habits[2]["effort"] = "Hard"
    check("count by effort groups Hard and Easy",
          count_by_effort(habits) == {"Hard": 2, "Easy": 1})
    check("a missing effort counts as Medium",
          count_by_effort([new_habit("Walk", "Health", 0, "🚶", "#BDE0FE",
                                     "2026-11-07")]) == {"Medium": 1})
    check("count by effort is empty with no habits",
          count_by_effort([]) == {})


def test_newest_habit():
    h1 = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")
    h2 = new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-07")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-06")
    check("the newest habit is the latest created date",
          newest_habit([h1, h2, h3]) is h2)
    check("no habits means no newest habit",
          newest_habit([]) is None)
    check("a habit with no date never wins",
          newest_habit([{"name": "Mystery"}, h1]) is h1)


def test_oldest_habit():
    h1 = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")
    h2 = new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-07")
    h3 = new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-06")
    check("the oldest habit is the earliest created date",
          oldest_habit([h1, h2, h3]) is h1)
    check("no habits means no oldest habit",
          oldest_habit([]) is None)
    check("a habit with no date counts as the oldest",
          oldest_habit([h1, {"name": "Mystery"}])["name"] == "Mystery")


def test_habits_with_target():
    h1 = new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-05")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-07")
    h3 = new_habit("Walk", "Health", 30, "🚶", "#BDE0FE", "2026-11-06")
    check("habits with a target keep creation order",
          habits_with_target([h1, h2, h3]) == [h1, h3])
    check("no targets means an empty list",
          habits_with_target([h2]) == [])
    check("no habits means an empty list",
          habits_with_target([]) == [])


def test_stage_progress():
    check("stage progress is 0 at a fresh seed", stage_progress(0) == 0.0)
    check("stage progress is 0 at the start of sprout",
          stage_progress(1) == 0.0)
    check("stage progress is halfway through growing",
          stage_progress(3) == 0.5)
    check("stage progress is 1 in full bloom", stage_progress(7) == 1.0)
    check("stage progress stays 1 past a week", stage_progress(10) == 1.0)


def test_clone_habit():
    habits = []
    habit = new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF",
                      "2026-11-07")
    add_habit(habits, habit)
    copy = clone_habit(habits, habit["id"])
    check("clone is a different habit",
          copy is not None and copy["id"] != habit["id"])
    check("clone name has (copy)",
          copy["name"] == "Study — DSA (copy)")
    check("clone keeps category", copy["category"] == "Study")
    check("clone keeps target", copy["target_minutes"] == 60)
    check("clone keeps icon and colour",
          copy["icon"] == "📚" and copy["colour"] == "#A5D8FF")
    check("clone is added to the list", len(habits) == 2)
    check("clone is not archived", copy["archived"] is False)
    check("cloning a missing habit is None",
          clone_habit(habits, "nope") is None)


def test_effort_level():
    habit = new_habit("Read", "Books", 30, "📖", "#F9A8D4", "2026-11-07")
    check("new habit defaults to Medium effort",
          habit["effort"] == "Medium")
    hard = new_habit("Run", "Health", 0, "🏃", "#BDE0FE", "2026-11-07",
                     "Hard")
    check("new habit keeps Hard effort", hard["effort"] == "Hard")
    weird = new_habit("Nap", "Health", 0, "😴", "#BDE0FE", "2026-11-07",
                      "Impossible")
    check("unknown effort falls back to Medium",
          weird["effort"] == "Medium")
    check("validate_effort passes Easy", validate_effort("Easy") == "Easy")
    check("validate_effort rejects junk",
          validate_effort("extreme") == "Medium")
    habits = [habit]
    edit_habit(habits, habit["id"], effort="Easy")
    check("edit changes effort", habit["effort"] == "Easy")
    edit_habit(habits, habit["id"], effort="nope")
    check("edit rejects bad effort", habit["effort"] == "Medium")


def test_habit_age_days():
    habit = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-07")
    check("age on the planted day is 0",
          habit_age_days(habit, "2026-11-07") == 0)
    check("age counts days",
          habit_age_days(habit, "2026-11-17") == 10)
    check("age never goes negative",
          habit_age_days(habit, "2026-11-01") == 0)
    check("missing created_date is 0",
          habit_age_days({}, "2026-11-17") == 0)
    check("bad created_date is 0",
          habit_age_days({"created_date": "soon"}, "2026-11-17") == 0)


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
    test_total_minutes_yesterday()
    test_total_minutes_last_30_days()
    test_days_done_this_week()
    test_first_done_date()
    test_total_minutes_in_range()
    test_best_day_by_minutes()
    test_total_plants()
    test_count_by_category()
    test_count_by_effort()
    test_newest_habit()
    test_oldest_habit()
    test_habits_with_target()
    test_stage_progress()
    test_clone_habit()
    test_effort_level()
    test_habit_age_days()
    print(f"{PASSED} tests passed")

