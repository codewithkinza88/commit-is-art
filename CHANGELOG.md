# Changelog

All notable changes to Habit Garden are listed here.

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
