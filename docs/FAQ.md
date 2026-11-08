# Habit Garden — Frequently Asked Questions 🌸

## Do I need an account or login?
No. Habit Garden has no login at all right now. Your habits live
on your own device in a file called `habit_garden.json`. A login
may be added later, but it is not needed to use the app.

## Where is my data stored?
Locally, in `habit_garden.json` next to the app. Nothing is sent
to a server. That file is not committed to the GitHub repo.

## How do I add a habit?
Tap "＋ Plant a new habit 🌱" on the Today view. Give it a name,
pick a category (Study, Books, Health, Mind, Daily Life), an
optional daily target in minutes, an emoji icon and a pastel colour.

## Can I edit a habit after adding it?
Yes — tap the ✏️ (edit) button on a habit card. You can change its
name, category, target minutes, icon and colour. You can also
delete a habit from the same dialog.

## How do I tick a habit as done?
Tap the checkbox on its card. Tap again to untick it. You can also
log minutes: the ＋15 min button adds 15 minutes, or use the timer
button to log any amount. If the minutes reach the daily target,
the habit counts as done even without a tick.

## What does the garden mean?
Each habit is a plant. Its stage grows with its streak: seed 🌱,
sprout 🌿, growing 🪴, blooming 🌸, full bloom 🌷. See
`docs/GARDEN_STAGES.md` for the full table.

## What is Tonight's review?
Before you sleep, open the Tonight view. It shows how many habits
you finished today, your %, total minutes, minutes per habit, your
best habit, and the last 7 days — so you can see what you achieved.

## I missed a day — is my garden ruined?
No. A missed day resets that habit's streak to zero, but the plant
is still there. Tick it again tomorrow and it starts growing again.

## Can I export my habits?
Yes — the app logic can export habits and logs as CSV text
(`app/export.py`), so you can keep a copy outside the app.

## How do I install the app on my phone?
Download the latest APK from the GitHub Actions artifacts of the
`commit-is-art` repo, unzip it, and install the APK on your phone.
See the "Download & install" section in `README.md`.
