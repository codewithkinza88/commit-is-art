# Changelog

All notable changes to Habit Garden are listed here.

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
