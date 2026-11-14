"""Plain-script tests for app.backup.

Run:  python3 tests/test_backup.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backup import (backup_filename, backup_to_json, make_backup,  # noqa: E402
                        restore_from_json)
from app.habits import new_habit  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    habits = [new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01")]
    logs = {"2026-11-10": {habits[0]["id"]: {"done": True, "minutes": 45}}}
    notes = {"2026-11-10": {habits[0]["id"]: "chapter 3"}}
    backup = make_backup(habits, logs, notes)
    check("backup has app name", backup["app"] == "Habit Garden")
    check("backup keeps habits", len(backup["habits"]) == 1)
    check("backup keeps logs", backup["logs"]["2026-11-10"][habits[0]["id"]]["minutes"] == 45)
    text = backup_to_json(habits, logs, notes)
    restored = restore_from_json(text)
    check("round trip habits", restored["habits"][0]["name"] == "Study")
    check("round trip notes", restored["notes"]["2026-11-10"][habits[0]["id"]] == "chapter 3")
    try:
        restore_from_json("not json at all")
        check("bad json raises", False)
    except ValueError:
        check("bad json raises", True)
    try:
        restore_from_json('{"hello": 1}')
        check("missing keys raises", False)
    except ValueError:
        check("missing keys raises", True)
    check("dated filename for a given date",
          backup_filename("2026-11-14") == "habit-garden-backup-2026-11-14.json")
    check("dated filename ends in .json",
          backup_filename("2026-11-14").endswith(".json"))
    check("dated filename defaults to today",
          backup_filename().startswith("habit-garden-backup-20"))


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
