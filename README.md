# Habit Garden 🌸

**Habit Garden** is a cute habit tracker built in Python with
[Flet](https://flet.dev) — the same Python code runs on desktop and
builds an Android APK. Plant habits, tick them off every day, and watch
your own little garden grow. 🌱 → 🌿 → 🌸 → 🌷

> Every commit is a small piece of art. 🎨

## Cute UI 🌸

Soft pastel colours, rounded cards, a mint glow on ticked-off habits,
a progress bar that blushes pink as the day fills up, and garden
plants tinted by growth stage. All colours live in `app/theme.py` —
see `docs/UI.md` for the full guide.

## Download & install

- **Download the app code (ZIP):**
  <https://github.com/codewithkinza88/commit-is-art/archive/refs/heads/main.zip>
- **Or clone it:**
  ```bash
  git clone https://github.com/codewithkinza88/commit-is-art.git
  cd commit-is-art
  ```
- **Install & run it:**
  ```bash
  pip install -r requirements.txt
  flet run
  ```
  You need Python 3.10+ on your computer. That is all — there is no
  account or sign-in.
- **Android APK (latest built version):**
  [Download Habit Garden APK — 60.4 MB](https://github.com/codewithkinza88/commit-is-art/actions/runs/42611999515/artifacts/13672421654)
  — built 9 November 2026 from commit `9296ef9` (GitHub Actions run #6).
  Sign in to GitHub as `codewithkinza88` first (otherwise the link
  shows a 404), download the ZIP, unzip it, and install the APK inside.
  Do not install older APKs — they crash on launch. This APK has not
  been tested on a phone yet.

## Features

- 🌱 **Add your own habits** — name, category (Study, Books, Health,
  Mind, Daily Life), an optional daily target in minutes, and an
  emoji icon + pastel colour of your choice. Three starter habits are
  included as editable sample data: *Study — DSA / course* (60 min),
  *Read a book* (30 min), and *Drink water*.
- ✏️ **Edit habits** — rename, change the category, target minutes,
  icon or colour, and delete a habit you no longer need.
- ✅ **Daily tick-off** — tick each habit when you do it today, and
  untick to undo. For study and reading habits you can also log
  minutes (+15 min button or a minutes field); reaching the target
  minutes counts as done too.
- 🌷 **Garden** — every habit is a plant. It grows through stages
  (seed 🌱 → sprout 🌿 → growing 🪴 → blooming 🌸 → full bloom 🌷)
  based on your streak of consecutive days. See your whole garden at
  a glance, with each plant's stage and streak.
- 🌙 **Tonight's review** — before sleep, see how much you achieved
  today: habits done out of total, % achieved, total minutes
  studied / read, minutes per habit, minutes by category and best
  category, streaks (including your longest streak ever), badges
  earned today, weekly goal progress per habit, and how November is
  going so far — plus a gentle message and a simple last-7-days view
  (per-day % done).
- 🔒 **No login** — there is no account or sign-in at all (login will
  come later). Everything is stored locally on your device.

## How to run (desktop)

```bash
pip install -r requirements.txt
flet run
```

Or, without the Flet CLI:

```bash
python3 main.py
```

## How to build the Android APK

You need the Flet CLI, Flutter and the Android SDK — Flet's docs walk
through the one-time setup. Then, from this folder:

```bash
flet build apk
```

The APK is produced under `build/apk/`. See
<https://flet.dev/docs/publish/android> for the full setup guide.

## Project structure

```text
commit-is-art/
├── main.py                 # Flet app: Today / Garden / Tonight views
├── requirements.txt        # flet==1.0.5
├── habit_garden.json       # your local data (created on first run, not committed)
├── app/
│   ├── __init__.py
│   ├── achievements.py     # badges for milestones
│   ├── categories.py       # minutes / best category per day
│   ├── export.py           # export habits and logs
│   ├── garden.py           # growth stages from streak + today's tick
│   ├── goals.py            # weekly minutes-goal progress
│   ├── habits.py           # habit add / edit / delete logic
│   ├── monthly.py          # whole-month summary
│   ├── motivation.py       # Tonight messages
│   ├── ordering.py         # habit sorting (undone first)
│   ├── store.py            # load / save the local JSON store
│   ├── streaks.py          # best streak / streak summary
│   ├── theme.py            # cute pastel palette + card helpers
│   ├── tracker.py          # daily ticks, minutes, streaks, summaries
│   └── version.py          # app name + version
└── tests/
    ├── test_achievements.py  test_categories.py  test_export.py
    ├── test_goals.py  test_habit_garden.py  test_monthly.py
    ├── test_motivation.py  test_ordering.py  test_streaks.py
    ├── test_theme.py  test_ui_api.py  test_weekly.py
```

## Data storage

Habits and daily logs live in one local JSON file, `habit_garden.json`
(next to `main.py`). No server, no account, no login yet. The file is
in `.gitignore`, so your real habit data is never committed to GitHub.

## Tests

```bash
# every test file is a plain script — run them all:
for f in tests/test_*.py; do python3 "$f"; done
# 130 checks passing (12 files)
```
