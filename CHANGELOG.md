# Changelog

All notable changes to Habit Garden are listed here.

## 2026-11-17 — Flower garden + add/edit fix (version 1.6.0)

- Garden grows proper flowers now: each plant shows a flower row that
  gets bigger as it blooms (sprout 🌿🌸 → full bloom 🌷🌸🌼🌺🌻🌷🌸),
  and the Garden opens with a full flower bed across the top
  (`flowers_for_stage` / `flower_bed` in app/garden.py).
- No more parrot-green garden: every stage tint is a floral pastel
  (cream → blush → lilac → pink) in app/theme.py.
- Add/edit habits is unmissable now: the habit card's actions moved
  into their own row with labelled buttons (＋15 min, ⏱ Minutes,
  ✏️ Edit) — on a narrow phone the old single row squeezed the Edit
  button off-screen — plus a hint line and the "Plant a new habit"
  button on Today. The add/edit dialog itself was already wired.
- Fixed a data-loss bug: saving used to drop notes (`persist` saved
  only habits + logs), so any note vanished on the next save.

Tests: 359 checks passing (318 plain-script + 41 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-17 — Premium UI (version 1.5.0)

- Premium cute look: blush → lilac → cream gradient headers, soft
  gold accents, rounded soft-shadow habit cards, pill badges for
  streaks and categories, slim progress bars toward each daily
  target, and a warm gradient Tonight summary card (new
  `app/ui_kit.py`, richer palette in `app/theme.py`).
- Garden plants now show a growth bar toward their next stage
  (`stage_progress` in app/garden.py).
- Fixed a crash: the old habit card used `ft.padding.symmetric`,
  which does not exist in Flet 1.0.5 — the Today view would have
  crashed when building a habit card.

Tests: 327 checks passing (297 plain-script + 30 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-17

### Today (17 November)
- Tonight shows your median best streak as well as the average, plus
  total minutes for the week ("Minutes this week: N min") and a
  gentle evening message.
- Garden tab counts your plants ("🌱 N plants in your garden").
- New helpers: minutes in the last 7 days (`total_minutes_this_week`
  in app/tracker.py), notes written on one day counted
  (`count_notes_for_day` in app/notes.py), habits counted by category
  (`count_by_category` in app/habits.py), habits due tomorrow
  (`habits_due_tomorrow` in app/schedule.py), notes exported as CSV
  (`notes_to_csv` in app/export.py), and an evening message
  (`evening_message` in app/motivation.py).
- Daily targets are cleaned when saving a habit — a blank, negative
  or over-a-day target becomes a safe 0..1440 minutes
  (`validate_target_minutes` in app/validation.py).

Tests: 305 checks passing (288 plain-script + 17 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-16

### Today (16 November)
- Today greets you with a morning message ("Good morning! N of M done")
  and the header counts how many habits are done.
- Garden tab counts plants by growth stage, and Tonight shows your
  average best streak as well as your longest streak.
- New helpers: which habits are due today (`is_due_today` in
  app/schedule.py), habits in one category (`habits_by_category` in
  app/habits.py), notes written on one day (`notes_for_day` in
  app/notes.py), and finding habits by icon (`find_habits_by_icon` in
  app/search.py).
- Categories are validated when saving a habit — an unknown category
  falls back to Daily Life.
- README now correctly says the APK is run #9, built 15 November 2026
  from commit `1e6c002` (its text still said run #8).

Tests: 274 plain-script checks passing across 19 test files
(`for f in tests/test_*.py; do python3 "$f"; done`, with
tests/test_ui_api.py run under .venv for Flet).

## 2026-11-15

### Today (15 November)
- Tonight shows your longest streak across all habits
  ("Longest streak: N days 🌳").
- Today header shows total minutes for the day ("⏱ N min today").
- Garden tab shows the next habit to water ("Next to water: 📚 Study")
  or "All watered! 🌸" when everything is done, plus how much of the
  garden is watered ("🌸 N% watered today").
- Today cards preview your latest note, and each category has its own
  coloured chip (Study sky, Books pink, Health mint, Mind lilac,
  Daily Life peach).
- Habits can be archived instead of deleted (`archive_habit` /
  `active_habits` in app/habits.py); new habits start unarchived.
- Icons are validated when saving a habit — an unknown icon falls back
  to 🌱.
- New helper: which habits are due before the week ends
  (`due_this_week` in app/schedule.py).

Tests: 246 plain-script checks passing across 19 test files
(`for f in tests/test_*.py; do python3 "$f"; done`, with
tests/test_ui_api.py run under .venv for Flet).

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
