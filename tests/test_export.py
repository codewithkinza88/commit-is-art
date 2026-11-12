"""Plain-script tests for app.export (pytest is not installed here).

Run:  python3 tests/test_export.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.habits import new_habit  # noqa: E402
from app.tracker import set_done, log_minutes  # noqa: E402
from app.export import habits_to_csv, logs_to_csv, summary_to_text  # noqa: E402

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


if __name__ == "__main__":
    test_habits_to_csv()
    test_logs_to_csv()
    test_summary_to_text()
    test_summary_best_streak()
    print(f"{PASSED} tests passed")
