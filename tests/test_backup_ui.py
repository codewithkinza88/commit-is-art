"""Plain-script tests for the Backup & Restore UI wiring.

Run:  python3 tests/test_backup_ui.py

The backup logic itself (app/backup.py) is covered in
tests/test_backup.py. These checks cover what the UI adds on top:
the export round-trips through a real store file, restoring replaces
the store, and main.py actually has the buttons, the FilePicker and
no banned calls.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backup import (backup_filename, backup_to_json,  # noqa: E402
                        restore_from_json)
from app.habits import new_habit  # noqa: E402
from app.store import load_store, save_store  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def main():
    habits = [
        new_habit("Study", "Study", 60, "📚", "#A5D8FF", "2026-11-01"),
        new_habit("Read a book", "Books", 30, "📖", "#F9A8D4", "2026-11-01"),
    ]
    logs = {"2026-11-17": {habits[0]["id"]: {"done": True, "minutes": 45}}}
    notes = {"2026-11-17": {habits[1]["id"]: "chapter 3"}}
    text = backup_to_json(habits, logs, notes)
    restored = restore_from_json(text)
    check("export round-trips habits",
          [h["name"] for h in restored["habits"]]
          == ["Study", "Read a book"])
    check("export round-trips logs minutes",
          restored["logs"]["2026-11-17"][habits[0]["id"]]["minutes"] == 45)
    check("export round-trips notes",
          restored["notes"]["2026-11-17"][habits[1]["id"]] == "chapter 3")
    check("export filename is dated for a given date",
          backup_filename("2026-11-18")
          == "habit-garden-backup-2026-11-18.json")
    check("export filename defaults to today and ends in .json",
          backup_filename().startswith("habit-garden-backup-20")
          and backup_filename().endswith(".json"))
    old_backup = restore_from_json(
        '{"app": "Habit Garden", "version": "1.0.0", "habits": [],'
        ' "logs": {}}')
    check("a backup without notes still parses",
          "notes" not in old_backup)

    # Restoring replaces the whole store, through a real store file.
    with tempfile.TemporaryDirectory() as folder:
        store_path = os.path.join(folder, "habit_garden.json")
        old = {"habits": [new_habit("Old habit", "Study", 10, "📚",
                                     "#A5D8FF", "2026-11-01")],
               "logs": {}, "notes": {}}
        save_store(old, store_path)
        check("old store loads with the old habit",
              load_store(store_path)["habits"][0]["name"] == "Old habit")
        data = restore_from_json(text)
        save_store({"habits": data["habits"], "logs": data["logs"],
                    "notes": data.get("notes", {})}, store_path)
        reloaded = load_store(store_path)
        check("restore replaces the old habits",
              [h["name"] for h in reloaded["habits"]]
              == ["Study", "Read a book"])
        check("restore brings the logs back",
              reloaded["logs"]["2026-11-17"][habits[0]["id"]]["done"]
              is True)
        check("restore brings the notes back",
              reloaded["notes"]["2026-11-17"][habits[1]["id"]]
              == "chapter 3")

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "main.py"), encoding="utf-8") as f:
        source = f.read()
    check("Garden view has a Backup button",
          "💾 Backup save karo" in source)
    check("Garden view has a Restore button",
          "📥 Restore karo" in source)
    check("restore picks a json file with a FilePicker",
          "ft.FilePicker(" in source
          and 'allowed_extensions=["json"]' in source)
    check("the buttons call the backup helpers",
          "backup_to_json(" in source
          and "restore_from_json(" in source)
    check("the Garden view names the Backup & Restore card",
          "Backup & Restore 💾" in source)
    banned = ("page.dialog", "page.snack_bar", "ft.app(", "ft.ElevatedButton",
              "ft.padding.symmetric", "ft.border.all")
    check("the backup code introduces no banned calls",
          all(b not in source for b in banned))


if __name__ == "__main__":
    main()
    print(f"{PASSED} tests passed")
