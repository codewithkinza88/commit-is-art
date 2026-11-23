"""Plain-script tests for app.export (pytest is not installed here).

Run:  python3 tests/test_export.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.export import (habits_to_csv, habits_to_text, logs_to_csv,  # noqa: E402
                        month_to_text, notes_to_csv, notes_to_text,
                        streaks_to_csv, streaks_to_text, summary_lines,
                        summary_to_text, week_to_text)

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_habits_to_csv():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    csv_text = habits_to_csv(habits)
    check("csv has header", csv_text.startswith("id,name,category"))
    check("csv has the habit name", "Study" in csv_text)
    check("csv has one data row", len(csv_text.strip().splitlines()) == 2)
    check("empty habits csv is header only",
          len(habits_to_csv([]).strip().splitlines()) == 1)


def test_logs_to_csv():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    csv_text = logs_to_csv(logs)
    check("logs csv has the date", "2026-11-07" in csv_text)
    check("logs csv has 45 minutes", "45" in csv_text)
    check("logs csv has True for done", "True" in csv_text)


def test_summary_to_text():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    text = summary_to_text(logs, habits, "2026-11-07")
    check("summary text has the date", "2026-11-07" in text)
    check("summary text has 1 / 1 habits", "1 / 1 habits" in text)
    check("summary text has 45 minutes", "45 minutes" in text)


def test_summary_best_streak():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
              new_habit("Read", "Books", 30, "📖", "#FFD6A5", "2026-11-01")]
    logs = {}
    for day in ("2026-11-05", "2026-11-06", "2026-11-07"):
        set_done(logs, habits[0]["id"], day, True)
    set_done(logs, habits[1]["id"], "2026-11-07", True)
    text = summary_to_text(logs, habits, "2026-11-07")
    check("summary text has longest streak of 3 days",
          "Longest streak: 3 days" in text)
    check("summary text has no streak without logs",
          "Longest streak: 0 days"
          in summary_to_text(logs, [], "2026-11-07"))


def test_notes_to_csv():
    from app.notes import add_note
    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h3", "2026-11-10", "   ")
    csv_text = notes_to_csv(notes)
    check("notes csv has header", csv_text.startswith("date,habit_id,note"))
    check("notes csv has the note text", "Read chapter 3" in csv_text)
    check("notes csv skips blank notes",
          len(csv_text.strip().splitlines()) == 3)
    check("empty notes csv is header only",
          len(notes_to_csv({}).strip().splitlines()) == 1)


def test_streaks_to_text():
    from datetime import date
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    set_done(logs, h2["id"], "2026-11-09", True)
    text = streaks_to_text(logs, [h1, h2], date(2026, 11, 9))
    check("streaks text has a header",
          text.startswith("Habit Garden — streaks"))
    check("streaks text lists each habit's streak",
          "Study: 2-day streak" in text
          and "Read: 1-day streak" in text)
    check("streaks text with no habits is friendly",
          "No habits yet 🌱" in streaks_to_text(logs, [],
                                                date(2026, 11, 9)))


def test_summary_lines():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
              new_habit("Read", "Books", 30, "📖", "#FFD6A5", "2026-11-01")]
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-07", True)
    log_minutes(logs, habits[0]["id"], "2026-11-07", 45)
    lines = summary_lines(logs, habits, "2026-11-07")
    check("summary lines start with the date header",
          lines[0] == "Habit Garden — 2026-11-07")
    check("summary lines name each habit with its state and minutes",
          "- Study — done / 45 minutes" in lines
          and "- Read — not done / 0 minutes" in lines)
    check("summary lines end with the day totals",
          "Total time: 45 minutes" in lines)


def test_streaks_to_csv():
    from datetime import date
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    h2 = new_habit("Read", "Books", 0, "📖", "#F9A8D4", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    set_done(logs, h2["id"], "2026-11-09", True)
    csv_text = streaks_to_csv(logs, [h1, h2], date(2026, 11, 9))
    lines = csv_text.strip().splitlines()
    check("streaks csv has header",
          lines[0] == "habit_id,best_streak,current_streak")
    check("streaks csv lists best and current streaks",
          lines[1] == f"{h1['id']},2,2" and lines[2] == f"{h2['id']},1,1")
    check("streaks csv with no habits is header only",
          len(streaks_to_csv(logs, [], date(2026, 11, 9)).strip().splitlines()) == 1)


def test_week_to_text():
    from datetime import date
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    log_minutes(logs, h1["id"], "2026-11-09", 45)
    text = week_to_text(logs, [h1], date(2026, 11, 9))
    lines = text.splitlines()
    check("week text starts with a header",
          lines[0] == "Habit Garden — last 7 days")
    check("week text has one line per day plus a total",
          len(lines) == 9)
    check("week text shows the minutes on the right days",
          "2026-11-09: 1/1 (100%) • 45 min" in lines)
    check("week text ends with the week total",
          lines[-1] == "Week total: 45 minutes")


def test_habits_to_text():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
              new_habit("Walk", "Health", 0, "🚶", "#BDE0FE", "2026-11-01")]
    text = habits_to_text(habits)
    lines = text.splitlines()
    check("habits text starts with a header",
          lines[0] == "Habit Garden — my habits")
    check("habits text shows the target when set",
          lines[1] == "📚 Study (Study) • 🎯 60 min/day")
    check("habits text skips the target when unset",
          lines[2] == "🌱 Walk (Health)")
    check("an empty habit list says so kindly",
          habits_to_text([]).splitlines()[-1] == "No habits yet 🌱")


def test_notes_to_text():
    from app.notes import add_note

    notes = {}
    add_note(notes, "h1", "2026-11-10", "Read chapter 3")
    add_note(notes, "h2", "2026-11-10", "Watered the plants")
    add_note(notes, "h1", "2026-11-12", "Finished chapter 4")
    text = notes_to_text(notes, "2026-11-10", "2026-11-11")
    lines = text.splitlines()
    check("notes text starts with the range header",
          lines[0] == "Habit Garden notes — 2026-11-10 to 2026-11-11")
    check("notes text lists both notes in range",
          lines[1] == "2026-11-10 [h1]: Read chapter 3"
          and lines[2] == "2026-11-10 [h2]: Watered the plants")
    check("an empty range says so kindly",
          notes_to_text(notes, "2026-11-13", "2026-11-14").splitlines()[-1]
          == "No notes in this range 🌱")


def test_month_to_text():
    h1 = new_habit("Study", "Study", 0, "📚", "#A5D8FF", "2026-11-01")
    logs = {}
    set_done(logs, h1["id"], "2026-11-08", True)
    set_done(logs, h1["id"], "2026-11-09", True)
    log_minutes(logs, h1["id"], "2026-11-09", 45)
    text = month_to_text(logs, [h1], 2026, 11)
    lines = text.splitlines()
    check("month text starts with the month header",
          lines[0] == "Habit Garden — November 2026")
    check("month text has one line per day plus a total",
          len(lines) == 32)
    check("month text shows the minutes on the right days",
          "2026-11-09: 1/1 (100%) • 45 min" in lines)
    check("month text ends with the month total",
          lines[-1] == "Month total: 45 minutes")


if __name__ == "__main__":
    test_habits_to_csv()
    test_logs_to_csv()
    test_summary_to_text()
    test_summary_best_streak()
    test_notes_to_csv()
    test_streaks_to_csv()
    test_streaks_to_text()
    test_summary_lines()
    test_week_to_text()
    test_month_to_text()
    test_notes_to_text()
    test_habits_to_text()
    print(f"{PASSED} tests passed")
