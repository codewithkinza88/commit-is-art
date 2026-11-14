# Changelog

All notable changes to Habit Garden are listed here.

## 2026-11-14

### Today (14 November)
- Today cards show how many notes each habit has, and when it was last
  done ("Done today 🌸" / "Last done N days ago" / "Not done yet 🌱").
- Garden tab counts habits still due today, and each plant shows how
  many days until its next stage.
- Backups get a dated filename: `habit-garden-backup-YYYY-MM-DD.json`.
- Completed habit cards now have a soft pink shade instead of mint.
- Tonight shows your 7-day consistency score, and warns when a weekly
  goal still has minutes left ("⚠️ N min left to hit your weekly goal").
- Monthly summary breaks minutes down by weekday (Mon–Sun).

Tests: 217 plain-script checks passing across 19 test files
(`for f in tests/test_*.py; do python3 "$f"; done`, with
tests/test_ui_api.py run under .venv for Flet).

## 2026-11-12

### Today (12 November)
- Delete asks first: deleting a habit now shows a confirm dialog
  ("Delete this habit?") — the habit is removed only from the
  confirm button, so a stray tap cannot wipe it.
- Garden tab shows how many plants sit at each stage
  (`app/garden.py` counts_text, wired into main.py).
- Export summary includes your longest streak
  (`app/export.py` summary_to_text).
- Tonight compares yesterday with today, side by side.
- Version 1.1.0.
- README APK link corrected to the newest built run (#6).

Tests: 192 plain-script checks passing across 19 test files
(`for f in tests/test_*.py; do python3 "$f"; done`, with
tests/test_ui_api.py run under .venv for Flet).

## 2026-11-10

### New helpers (10 November)
- Search habits by name or category (`app/search.py`).
- Weekday schedules: habits due on a given day (`app/schedule.py`).
- Short daily notes per habit (`app/notes.py`).
- Backup and restore your data as JSON (`app/backup.py`).
- Validation for habit names and minutes (`app/validation.py`).
- Insights: consistency score and the habit needing attention (`app/insights.py`).
- Milestone celebrations for 7, 14, 30 and 100 day streaks (`app/celebration.py`).
- New guides: `docs/TIPS.md` (study and reading tips) and
  `docs/PRIVACY.md` (your data stays on your device).

## 2026-11-08 – 2026-11-09

### Cute UI (8 November)
- New pastel theme in `app/theme.py`: shared palette, rounded cards,
  mint glow on ticked-off habits, progress bar that blushes pink.
- Rounder habit cards, cuter Today progress bar, bigger garden plants,
  softer Tonight review, friendlier add/edit and minutes dialogs.
- New `docs/UI.md` guide and a "Cute UI" section in the README.

### Fixed (8 November)
- Today's cute-UI code crashed on launch: `main.py` used
  `ft.border.all`, which does not exist in Flet 1.0.5 (correct call is
  `ft.Border.all`). Fixed at all 3 sites (Today card, Garden card,
  Tonight card) and guarded by new checks in `tests/test_ui_api.py`.
- Android APK rebuilt from the fix (GitHub Actions run #5, commit
  `ab1838c`): artifact `habit-garden-apk`, 60.4 MB. It has not been
  tested on a phone yet — do not install older APKs.

### Tonight's review now uses the backend (9 November)
- Today view sorts undone habits first (`app/ordering.py`).
- Tonight's message comes from `app/motivation.py`; it also shows the
  longest streak ever (`app/streaks.py`), badges earned today
  (`app/achievements.py`), minutes by category and best category
  (`app/categories.py`), how November is going
  (`app/monthly.py`), and weekly goal progress per habit
  (`app/goals.py`, weekly target = daily target × 7).
- Editing a habit with an empty name now shows the same
  "Please give your habit a name first 🌱" message as adding one,
  instead of silently keeping the old name.

### Tests
- 130 plain-script checks passing across 12 test files
  (`for f in tests/test_*.py; do python3 "$f"; done`).

## v1.0.0 — 2026-11-07

First launch of Habit Garden 🌸 — a cute habit tracker in Python (Flet).

### Features
- Add your own habits: name, category (Study, Books, Health, Mind,
  Daily Life), optional daily target in minutes, emoji icon and pastel
  colour. Three editable starter habits are included.
- Edit and delete habits.
- Daily tick-off: tick a habit when it is done, untick to undo.
- Minutes logging for study and reading habits (+15 min button or a
  minutes field); reaching the daily target counts as done.
- Garden: every habit is a plant that grows through stages — seed 🌱,
  sprout 🌿, growing 🪴, blooming 🌸, full bloom 🌷 — based on its
  streak of consecutive days.
- Tonight's review: before sleep, see today's habits done, % achieved,
  total minutes studied / read, minutes per habit, streaks, best habit,
  and a last-7-days view.
- No login at all (login will come later). All data is stored locally
  in `habit_garden.json` on the device.

### Tests
- 35/35 plain-script tests pass
  (`python3 tests/test_habit_garden.py`).

### Known limitation
- The Android APK build is blocked in this VM by a Gradle/Java
  localhost TCP limit (the Gradle daemon client reads garbage from
  the socket: "Unexpected type tag 109"). The APK will be built on a
  machine where the Gradle daemon can run normally.
