# Habit Garden UI 🌸

How the app looks — and how to keep it cute when you change it.

## The look

- **Soft pastel palette** — cream background (`#FFF8F0`), pink
  (`#F9A8D4`), lilac, sky, mint, peach and cream. All colours live
  in one place: `app/theme.py`.
- **Soft, rounded cards** — habit cards use a 22px corner radius and
  a thin pastel border, so they feel like petals, not boxes.
- **Done habits glow mint** — a ticked-off habit gets a soft mint
  wash (`#E7F9EE`) and a "Done 🌸" pill, so finished habits are
  easy to spot. Not-yet-done habits show "Not yet 🌱".
- **Progress bar that blushes** — the Today bar starts lilac, turns
  blush, then pink, then deep pink as the day fills up, with a
  "🌸 50% of today done" label underneath.
- **Garden plants** — each plant card is tinted by its growth stage
  (seed → sprout → growing → blooming → full bloom), with a big
  emoji and a "🌷 Blooming • 🔥 3 days" pill.
- **Tonight review** — a soft cream summary card with a peach border,
  and a mini progress bar for each of the last 7 days.
- **Dialogs** — the habit and minutes dialogs use rounded fields
  (16px) with friendly labels and hints, e.g. "e.g. Study — DSA".

## Rules for changing the UI

- Keep all colours in `app/theme.py` — do not hard-code new hex
  colours in `main.py`.
- Flet 1.0.5 only: use `ft.run(main)` to start the app (not the
  removed `ft.app`) and `ft.Button` for buttons (not the removed
  `ft.ElevatedButton`). The removed APIs crash the Android APK.
- No login in the UI — habits are the user's own, added first,
  editable, ticked daily, with study/reading minutes tracked.
