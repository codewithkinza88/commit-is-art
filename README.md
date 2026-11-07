# Habit Garden 🌸

**Habit Garden** is a cute habit tracker built in Python with
[Flet](https://flet.dev) — the same Python code runs on desktop and
builds an Android APK. Plant habits, tick them off every day, and watch
your own little garden grow. 🌱 → 🌿 → 🌸 → 🌷

> Every commit is a small piece of art. 🎨

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
  studied / read, minutes per habit, streaks, your best habit, and a
  gentle message. Plus a simple last-7-days view (per-day % done).
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
│   ├── habits.py           # habit add / edit / delete logic
│   ├── tracker.py          # daily ticks, minutes, streaks, summaries
│   ├── garden.py           # growth stages from streak + today's tick
│   └── store.py            # load / save the local JSON store
└── tests/
    └── test_habit_garden.py
```

## Data storage

Habits and daily logs live in one local JSON file, `habit_garden.json`
(next to `main.py`). No server, no account, no login yet. The file is
in `.gitignore`, so your real habit data is never committed to GitHub.

## Tests

```bash
python3 tests/test_habit_garden.py
```
