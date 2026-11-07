# Contributing to Habit Garden 🌸

Welcome! Habit Garden is a small, friendly project. Every contribution
is a small piece of art. 🎨

## Run it

```bash
pip install -r requirements.txt
flet run
```

## Run the tests

No pytest needed — the tests are plain scripts:

```bash
python3 tests/test_habit_garden.py
python3 tests/test_weekly.py
```

Please keep all tests passing before you push.

## How to add a habit category

1. Add the new category name to the `CATEGORIES` list in `app/habits.py`.
2. Add a test in `tests/test_habit_garden.py` that creates a habit
   with the new category.
3. Run the tests and commit the change on its own.

## How daily commits work

- One small, real improvement per commit — a new feature, a fix, a
  test, or a docs page. **No empty commits.**
- Keep each commit focused on one thing, so the history stays readable
  and the contribution graph grows honestly, one real step at a time.

## Code style

- Keep the logic in `app/` free of Flet imports, so it stays testable
  without launching the UI.
- Keep the UI cute and pastel, and keep messages kind and encouraging.
