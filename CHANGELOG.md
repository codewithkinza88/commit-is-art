# Changelog

All notable changes to Habit Garden are listed here.

## 2026-11-26 — Badges, weekly goals and the last 30 days (version 1.17.0)

- Badges: `has_badge()` checks one badge by label and `badge_emojis()` lists the emojis of the badges earned.
- Weekly goals: `weekly_goal_reached()` is the yes/no form of the weekly goal and `weekly_goal_percent()` is the percent of the target reached, capped at 100.
- Search and categories: `find_habits_by_category()` finds habits in one category, `count_notes_matching()` counts the notes matching a search, `find_notes_by_habit()` lists one habit's notes, `categories_used()` lists the categories in use and `count_categories()` counts them.
- Backup and notifications: `backup_counts()` counts the habits, logs and notes in a backup, and `count_unread_for_habit()` counts the unread notifications naming one habit.
- Habits: `shortest_habit_name()` mirrors the longest name, and `archived_habit_ids()` lists the ids of archived habits.
- Last 30 days: `days_done_last_30_days()`, `minutes_for_habit_last_30_days()`, `notes_for_habit_last_30_days()` and `notes_count_last_30_days()` track one habit and its notes across the last 30 days — Tonight shows how many notes were written in the last month.
- Streaks and garden: `habits_with_best_streak_at_least()` filters by best streak, `names_seeds()` names the plants still seeds — the Garden names the seeds — and `total_flowers()` counts every flower in the garden.
- Due days: `due_tomorrow_names()` names the habits due tomorrow — Tonight shows them — and `count_due_today_done()` counts the due-today habits already done.
- Validation, insights and month: `validate_month()` checks a month 1..12, `done_rate_for_category()` is the done rate for one category, and `average_percent_this_month()` and `perfect_days_this_month()` read the monthly summary.
- Export and celebration: `logs_to_text()` is the text form of the logs, and `milestones_count()` counts the milestones reached.

## 2026-11-25 — Habit ids, last 14 days and sprouting names (version 1.16.0)

- Habit lists: `habit_ids()` lists every habit id, `habits_with_icon()`
  finds the habits using one icon, `archived_habit_names()` names the
  archived habits, and `longest_habit_name()` names the longest habit.
- Yesterday and the last 14 days: `minutes_for_habit_yesterday()` and
  `is_done_yesterday()` look at yesterday for one habit, and
  `days_done_last_14_days()`, `minutes_for_habit_last_14_days()`,
  `notes_for_habit_last_14_days()` and `notes_count_last_14_days()`
  track one habit and its notes across the last 14 days — Tonight
  shows how many notes were written in the last 2 weeks.
- Streaks: `best_streaks_sorted()` ranks every habit by its best
  streak, `count_habits_on_streak()` counts the habits on a streak,
  and `streak_summaries()` gives one summary per habit.
- Garden names: `names_sprouts()` and `names_growing()` name the
  plants at the sprout and growing stages — the Garden names the
  plants that are sprouting.
- Notes: `shortest_note_text()` finds the shortest note, and
  `notes_on_date()` lists every note written on one date.
- Due days: `count_due_every_day()` counts the habits due every day,
  `habits_not_due_today()` lists the habits not due today, and
  `due_today_names()` names the habits due today — Tonight names
  them.
- Validation: `validate_search_query()` cleans a search query.
- Insights: `done_rate_overall()` gives the overall done rate,
  `habit_with_most_minutes()` names the habit with the most minutes
  this week, and `best_category_by_minutes()` names the category
  with the most minutes today — Tonight shows it.
- Monthly: `best_day_date_str()` names the best day's date, and
  `total_minutes_this_month()` gives the month's total minutes.
- Exports: `notes_to_lines()` and `logs_to_lines()` list notes and
  logs as readable lines.
- Milestones: `next_milestone_streak()` names the next milestone
  streak to aim for.

## 2026-11-24 — Counts, last 7 days and badge labels (version 1.15.0)

- Habit counts: `habits_without_target()` lists the habits with no
  daily target, and `count_active_habits()` counts the habits that
  are not archived.
- Last 7 days: `minutes_for_habit_last_7_days()`,
  `days_done_last_7_days()` and `total_minutes_last_7_days()` track
  one habit and the whole garden across the last 7 days, and
  `best_day_last_7_days()` names the biggest day of the week.
- Streak names: `shortest_best_streak()` finds the smallest best
  streak, `habits_with_no_streak()` names the habits with no live
  streak, and `streaks_sorted()` ranks every habit by its streak.
- Garden names: `names_in_full_bloom()` and `names_blooming()` name
  the plants at each stage, and `garden_stage_names()` lists the
  stages present in the garden.
- Notes in the window: `notes_for_habit_last_7_days()`,
  `longest_note_text()` and `notes_count_last_7_days()` find one
  habit's notes in the last 7 days, its longest words, and how
  many were written.
- Due days: `habits_due_on_weekday_name()` finds the habits due on
  a named weekday, and `count_due_tomorrow()` counts the habits
  due tomorrow.
- Validation: `validate_percent()` cleans a percent to 0–100, and
  `validate_habit_id()` cleans a habit id.
- Insights: `least_consistent_habit()` names the habit done least
  often, and `done_rate_for_habit()` gives one habit's done rate
  as a fraction.
- Best day: `best_day_minutes()` reads the minutes of the month's
  best day.
- Readable lines: `habits_to_lines()` and `week_lines()` write the
  habit list and the last 7 days as copyable lines.
- Celebrations: `celebration_message()` gives one line for a streak,
  and `badge_labels()` lists the labels of the badges Tonight shows.
- Goals and search: `weekly_goal_remaining()` counts the minutes
  left on a weekly goal, and `find_habits_by_effort()` finds the
  habits with a daily target of at least N minutes.
- Tonight shows how many habits are active, the minutes of the last
  7 days, and your badge labels.

## 2026-11-23 — Oldest habits, full bloom and monthly notes (version 1.14.0)

- Oldest habit: `oldest_habit()` names the habit planted first, and
  `habits_with_target()` lists the habits with a daily target set.
- Archived habits: Tonight counts the archived habits, and
  `total_target_minutes()` adds up every habit's daily target.
- This month per habit: `minutes_for_habit_this_month()` and
  `days_done_this_month()` track one habit across a calendar month.
- Last 14 days: Tonight shows the minutes logged in the last 14
  days, and `best_day_this_month()` names the month's biggest day.
- Best streaks: `habits_with_best_streak()` names the habits sharing
  the longest best streak, `streaks_by_habit()` maps every habit to
  its live streak, and Tonight shows the total streak days.
- Full bloom: the Garden counts the plants in full bloom and at the
  growing stage, and names the plants in full bloom.
- Notes this month: `notes_for_habit_this_month()`,
  `notes_in_month()` and `latest_note_text()` find a habit's notes
  for one month and its latest words.
- Due weekdays: `count_due_on_weekday()` counts the habits due on
  any weekday, `next_due_weekday_name()` names the next due day, and
  `validate_weekday()` cleans a weekday number to 0–6.
- Above the rate: `habits_above_rate()` lists the habits done at
  least 80% of the time, and `average_consistency()` averages each
  habit's own done-rate.
- Monthly averages: `average_minutes_on_logged_days()` averages only
  the days with minutes, `minutes_for_weekday()` reads one weekday's
  minutes, and `longest_day_minutes()` finds the biggest day.
- Streaks as text: `streaks_to_text()` and `summary_lines()` write
  streaks and one day's summary as copyable lines.
- Streak celebrations: `celebration_for()` pairs a streak with its
  milestone message and garden emoji, and `badges_count()` counts
  the badges Tonight shows.

## 2026-11-22 — Streaks, garden counts and readable exports (version 1.13.0)

- Streaks on cards: a habit card shows "🔥 Streak: N days" when its
  streak is alive, and Tonight names the habit with the longest
  live streak.
- Minutes in the last 30 days: Tonight shows the minutes logged in
  the last 30 days.
- Seeds still waiting: the Garden shows how many plants are still
  seeds, and how many sprouts are growing.
- Notes this week: Tonight counts the notes written in the last 7
  days.
- Due today but not done: Tonight counts the habits due today that
  are still undone.
- Validate habit days: `validate_habit_days()` keeps only weekday
  numbers 0–6.
- Done rate this week: `weekly_done_rate()` is the share of habits
  done over the last 7 days.
- Days logged this month: Tonight counts the days with minutes
  logged this month, and how many days logged nothing.
- A month as readable text: `month_to_text()` writes a calendar
  month as copyable lines, and `notes_to_text()` / `habits_to_text()`
  do the same for notes and the habit list.
- Milestones already reached: `milestones_reached()` lists the
  milestones a streak has passed, and Tonight shows the next
  milestone as a cheery message.
- Habits by effort: Tonight counts habits by effort (Easy / Medium
  / Hard).
- Newest habit: the newest habit is named in Tonight's greeting.
- Days done this week: Tonight counts the days done this week.
- First done date: `first_done_date()` is the earliest day a habit
  was ever ticked.
- Longest live streak: Tonight names the longest live streak.
- Habits at a streak level: Tonight counts the habits at each
  streak level (0, 1–2, 3–6, 7+).
- Average stage progress: the garden's mean growth progress (0.0–1.0).
- Notes for one habit this week: `notes_for_habit_this_week()`.
- Total notes count: `total_notes_count()` counts all non-empty notes.
- Weekday of a date: `weekday_of()` gives 0=Mon..6=Sun, -1 when invalid.
- Habits due every day: `habits_due_every_day()` lists the habits
  with no set days.
- Validate a colour: `validate_colour()` keeps an app colour, else
  falls back to soft sky blue.
- Habits below a rate: `habits_below_rate()` lists the habits done
  less than a threshold percent.
- Perfect day dates: `perfect_day_dates()` lists the month's 100% days.

Tests: 720 checks passing (624 plain-script + 96 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-21 — Medians, milestones and more (version 1.12.0)

- Median current streak: Tonight shows the median of all live
  streaks, so one long streak cannot hide the rest.
- Best day this week by minutes: Tonight names the highest-minutes
  day of the last 7 days.
- Blooming plants count: the Garden shows how many plants are
  blooming right now.
- Longest note: `longest_note()` finds a habit's longest note,
  most recent winning ties.
- Due this week: Tonight counts the habits due this week under the
  Tomorrow (Kal) section.
- Validate a date string: `validate_date_str()` accepts an ISO
  date or a blank, and rejects impossible dates like 2026-02-30.
- Welcome message: a new habit is greeted with "Welcome to the
  garden, <name>! 🌱" instead of a generic message.
- Average minutes per day: the Tonight month line now includes
  "avg N min/day".
- A week as readable text: `week_to_text()` writes the last 7 days
  as copyable lines plus a week total.
- Days to the next milestone: Tonight shows how many days remain
  until the next streak milestone (7, 14, 30, 60 or 100 days).

Tests: 621 checks passing (534 plain-script + 87 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-20 — Leaderboard, ranges and more (version 1.11.0)

- Streak leaderboard: habits ranked by current streak, longest first.
- Minutes in a range: `total_minutes_in_range()` totals minutes
  between any two dates, inclusive.
- Flower count: the Garden can now count every flower it is showing
  (streak days plus blooming bonuses, no display cap).
- Notes in a range: `notes_in_range()` lists notes written between
  two dates, oldest first.
- Next due weekday: `next_due_weekday()` finds the next day a habit
  is due, wrapping Sunday back to Monday.
- Weekly target validation: `validate_weekly_target()` cleans a
  weekly minutes goal to 0..10080 (a whole week).
- Weekly cheer: `weekly_cheer()` cheers progress towards a weekly
  minutes goal — halfway, met, or just getting started.
- Quietest weekday: the Monthly view can now name the quietest
  weekday alongside the busiest one.
- Most consistent habit: `most_consistent_habit()` finds the habit
  done most often over recent days, mirroring needs-attention.

Tests: 582 checks passing (501 plain-script + 81 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-19 — Averages, yesterday and more (version 1.10.0)

- Fixed a stale version check: the 1.9.0 bump changed APP_VERSION but
  tests/test_ui_api.py still expected 1.8.0, so the UI suite failed.
  The check now matches the version (and the 1.10.0 bump updates it
  together, so this cannot drift again unnoticed).
- Average best streak: Tonight now shows "Average best streak ever"
  (mean of every habit's best streak).
- Minutes yesterday: Tonight shows "Yesterday: N min".
- Longest-streak plant: the Garden names the plant with the longest
  current streak — "🏆 Longest streak: ...".
- Notes for one habit: `notes_for_habit()` lists a habit's notes,
  oldest first.
- Due-today count: `count_due_today()` counts habits due on a weekday.
- Note validation: `validate_note_text()` trims and caps notes at 200
  characters.
- Streaks as CSV: `streaks_to_csv()` exports habit_id, best_streak and
  current_streak.
- Comeback message: Tonight welcomes you back ("... days away — come
  back and water your garden!") when the longest absence is 2+ days.

Tests: 541 checks passing (465 plain-script + 76 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-18 — Duplicate, effort, age and more (version 1.9.0)

- Duplicate habit: every habit card has a "📋 Copy" button that plants
  an identical copy (" (copy)").
- Plant of the day: the Garden spotlights one plant — "🌟 Plant of the
  day" — the longest streak not yet watered today.
- Busiest weekday: the Monthly view now names your busiest weekday from
  your minutes.
- Tomorrow preview: Tonight shows "Kal: ..." with tomorrow's due habits.
- Effort level: habits have Easy / Medium / Hard (pickable in the
  add/edit form, default Medium), shown as a 🟢/🟡/🔴 pill on the card.
- Category legend: the Garden shows "Legend: ..." mapping each category
  to its colour/icon.
- Auto-backup nudge: a "💾 Backup your garden" notification appears
  when no backup exists or the last one is 7+ days old.
- Notes search: `find_notes()` searches note text case-insensitively.
- Longest gap: Tonight shows "Longest gap: N days" (longest stretch
  between waterings).
- Habit age: habit cards show "planted N days ago" (or "planted today 🌱").

Tests: 511 checks passing (439 plain-script + 72 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-18 — Backup & restore (version 1.8.0)

- Backup & Restore buttons in the Garden view: "💾 Backup save karo"
  writes a dated habit-garden-backup-YYYY-MM-DD.json with all habits,
  logs and notes (to Downloads when it exists, else the app folder),
  and "📥 Restore karo" picks a backup file and brings everything
  back. A bad file is rejected with "Yeh backup file nahi hai" and
  changes nothing; cancelling the picker stays silent.
- Why now: every GitHub Actions build so far was signed with a fresh
  throwaway key, so the new APK could not update the installed app —
  Kinza has to uninstall once and reinstall, which wipes the app's
  data. The backup logic (app/backup.py) already existed but had no
  button, so the data could never be saved. From this version on,
  save a backup first and restore it after any reinstall.
  (16 checks in tests/test_backup_ui.py.)

Tests: 455 checks passing (391 plain-script + 64 in
tests/test_ui_api.py under .venv for Flet).

## 2026-11-17 — In-app notifications + in-app updates (version 1.7.0)

- Notifications inside the app: a bell 🔔 in the header shows how many
  things need attention — habits to water, streaks about to break,
  weekly-goal warnings, the evening Tonight review, and new badges.
  Tapping the bell opens the list inside the app; tapping a
  notification goes to Today. A soft banner on Today shows the most
  urgent one. "Mark all read" clears the bell for this session.
  (`app/notifications.py`, 31 checks in tests/test_notifications.py.)
- The app updates itself: every minute it refreshes on its own, and at
  midnight it rolls over to the new day and reloads, so there is no
  need to close and reopen it to see fresh notifications.
- In-app updates: when a newer version exists, a pink card appears on
  Today — "🌸 New version {v} is here! — Update now ⬇️". Tapping it
  downloads the new APK inside the app (with a progress bar) and
  shows an Install button; no browser needed. The final step is
  Android's own installer popup (one tap). The build workflow now
  publishes the APK as a public GitHub Release asset ("latest") so the
  app can download it without a GitHub login; the Actions artifact
  stays as a fallback. (`app/updater.py`, 26 checks in
  tests/test_updater.py.)
- Fixed a small badge bug found while testing: `badges_for` counted
  ticks on any logged day, so a badge first earned today also counted
  as earned yesterday and could never be "new".

Tests: 434 checks passing (375 plain-script + 59 in
tests/test_ui_api.py under .venv for Flet).

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
