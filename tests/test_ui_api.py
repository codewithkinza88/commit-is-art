"""Plain-script tests for the Flet UI calls used in main.py.

Run:  python3 tests/test_ui_api.py

Why this exists: Flet 1.0.5 removed some old call names, and the plain
logic tests never build the UI, so a renamed call only crashed the app
on launch. Twice: ft.app (fixed to ft.run) and ft.ElevatedButton
(fixed to ft.Button). On 8 November 2026 the same thing happened a
third time — ft.border.all, used for the cute habit-card borders,
does not exist in Flet 1.0.5; the working call is ft.Border.all.
These checks guard the exact calls main.py uses, without launching
the app (main.py ends with an unguarded ft.run(main)).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def test_ui_api():
    check("flet is 1.0.5", ft.__version__ == "1.0.5")
    border = ft.Border.all(1, "#FDE7F3")
    check("Border.all builds a border",
          isinstance(border, ft.Border))
    check("Border.all sets all four sides to the colour",
          border.top.color == "#FDE7F3"
          and border.right.color == "#FDE7F3"
          and border.bottom.color == "#FDE7F3"
          and border.left.color == "#FDE7F3")
    check("Border.all keeps the width",
          border.top.width == 1)
    check("ft.Button exists (ElevatedButton replacement)",
          hasattr(ft, "Button"))
    check("ft.run exists (ft.app replacement)",
          hasattr(ft, "run"))

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "main.py"), encoding="utf-8") as f:
        source = f.read()
    with open(os.path.join(root, "app", "ui_kit.py"),
              encoding="utf-8") as f:
        kit_source = f.read()
    check("the UI uses ft.Border.all, not ft.border.all",
          "ft.Border.all" in source + kit_source
          and "ft.border.all" not in source + kit_source)
    check("main.py has no removed ft.app call",
          "ft.app(" not in source)
    check("main.py has no removed ft.ElevatedButton call",
          "ft.ElevatedButton" not in source)
    check("main.py launches with ft.run(main)",
          "ft.run(main)" in source)
    check("main.py never assigns the removed page.dialog",
          "page.dialog" not in source)
    check("main.py never assigns the removed page.snack_bar",
          "page.snack_bar" not in source)
    check("dialogs open with page.show_dialog (habit, delete, minutes,"
          " notifications)",
          source.count("page.show_dialog(") == 4)
    check("snack reuses one SnackBar from page.overlay",
          "page.overlay" in source)
    check("a bell button with a count badge sits in the header",
          "ft.Icons.NOTIFICATIONS" in source
          and "ft.Badge(" in source)
    check("tapping the bell opens the notifications panel",
          "open_notifications_dialog()" in source
          and "Notifications 🔔" in source)
    check("notifications can be marked all read",
          "Mark all read" in source)
    check("the most urgent notification banners the Today view",
          "View all 🔔" in source)
    check("the app refreshes itself every minute on a daemon thread",
          "threading.Thread(" in source
          and "daemon=True" in source
          and "time.sleep(60)" in source)
    check("a day rollover reloads the store on refresh",
          "should_refresh(" in source)
    workflow = open(os.path.join(root, ".github", "workflows",
                                 "build-apk.yml"),
                    encoding="utf-8").read()
    check("the workflow still uploads the APK as an artifact",
          "actions/upload-artifact@v4" in workflow
          and "name: habit-garden-apk" in workflow)
    check("the workflow publishes the APK as a public release asset",
          "softprops/action-gh-release@v2" in workflow
          and "tag_name: latest" in workflow
          and "files: build/apk/habit-garden.apk" in workflow)
    check("a release failure can never fail the run",
          "continue-on-error: true" in workflow)
    check("the workflow grants the release step write permission",
          "contents: write" in workflow)
    check("the workflow is still manual-only",
          "workflow_dispatch:" in workflow)
    check("the app checks GitHub releases for a newer version",
          "fetch_latest_release(" in source
          and "is_newer(" in source)
    check("the update check runs in the background, never blocking startup",
          "_check_for_update" in source
          and "threading.Thread(target=_check_for_update" in source)
    check("Today shows an in-app update banner with Update now",
          "New version" in source
          and "Update now ⬇️" in source)
    check("the update banner sits beside the notifications banner",
          "[*banner, *update_cards, header," in source)
    check("the download shows live progress",
          "Downloading version" in source
          and "update_progress[0]" in source)
    check("a failed download shows a friendly retry message",
          "Couldn't download the update" in source)
    check("the downloaded APK opens in Android's own installer, no browser",
          "📲 Install" in source
          and 'page.launch_url("file://" + update_path[0])' in source)
    check("garden view shows each plant's own flower",
          "flower_for(" in source)
    check("garden view shows the flower bed from the plants",
          "flower_bed(garden" in source)
    check("edit path also rejects an empty habit name",
          source.count("Please give your habit a name first") == 2)
    check("delete asks first with a confirm dialog",
          "Delete this habit?" in source)
    check("delete happens only from the confirm button",
          source.count('delete_habit(habits, habit["id"])') == 1)
    check("confirm dialog offers Keep it",
          '"Keep it' in source)
    check("Tonight compares yesterday and today",
          "Yesterday vs today" in source)
    check("yesterday summary comes from daily_summary",
          "daily_summary(logs, habits, yesterday)" in source)
    check("Tonight welcomes you back after days away",
          "comeback_message(longest_absence)" in source
          and "days_since_last_done(logs, h)" in source)
    check("Garden shows the longest-streak plant",
          "🏆 Longest streak:" in source
          and "plant_with_longest_streak(habits, logs, today)" in source)
    check("Tonight shows yesterday's minutes",
          "Yesterday: {yday_minutes} min" in source
          and "total_minutes_yesterday(logs, habits)" in source)
    check("Tonight shows the average best streak ever",
          "Average best streak ever" in source
          and "average_best_streak(logs, habits)" in source)
    check("app version is 1.10.0",
          open(os.path.join(root, "app", "version.py"),
               encoding="utf-8").read().count('APP_VERSION = "1.10.0"') == 1)
    check("garden plants show a flower row, not one big emoji",
          'plant["flowers"]' in source)
    check("garden opens with a full flower bed on top",
          "flower_bed(garden[\"plants\"])" in source
          and "flowers blooming in your garden" in source)
    check("every habit card has a labelled Edit button",
          '"✏️ Edit"' in source)
    check("today view tells you how to edit and add habits",
          "Tap ✏️ Edit on any habit" in source)
    check("saving keeps notes instead of dropping them",
          '"notes": notes' in source)
    check("the Garden view has Backup & Restore buttons",
          "💾 Backup save karo" in source
          and "📥 Restore karo" in source
          and "Backup & Restore 💾" in source)
    check("restore picks a json file with a FilePicker",
          "ft.FilePicker(" in source
          and 'allowed_extensions=["json"]' in source)
    check("a bad backup file is rejected with a friendly message",
          "Yeh backup file nahi hai" in source)
    check("export saves the backup and says so",
          "Backup saved:" in source
          and "backup_to_json(" in source
          and "backup_filename()" in source)
    check("restore replaces the store, saves it and refreshes",
          "restore_from_json(" in source
          and "persist()" in source)

    from app.ui_kit import (  # noqa: E402
        gradient_card, gradient_header, mini_progress, pill, soft_card,
        stat_chip, streak_pill,
    )
    check("pill builds a rounded container",
          isinstance(pill("Study", "#A5D8FF"), ft.Container)
          and pill("Study", "#A5D8FF").border_radius == 10)
    check("streak pill shows the streak",
          "5" in streak_pill(5).content.value)
    check("streak pill turns gold at a week",
          streak_pill(7).content.value.startswith("🔥 7"))
    check("soft card has a soft shadow",
          len(soft_card(ft.Text("hi")).shadow) == 1)
    check("gradient header has a gradient",
          gradient_header("Today", "hi").gradient is not None
          and isinstance(gradient_header("Today", "hi").gradient,
                         ft.LinearGradient))
    check("gradient card has a gradient",
          gradient_card(ft.Text("hi")).gradient is not None)
    check("stat chip shows its value",
          stat_chip("🌱", "plants", 3).content.controls[1].value == "3")
    check("mini progress clamps to full",
          mini_progress(2).value == 1.0)
    check("main.py uses the ui kit",
          "from app.ui_kit import" in source)
    check("main.py shows growth progress in the garden",
          "stage_progress(" in source)
    check("ui kit has no removed ft.app call",
          "ft.app(" not in kit_source)
    check("ui kit has no removed ft.ElevatedButton call",
          "ft.ElevatedButton" not in kit_source)
    check("the UI never uses the removed padding helpers",
          "ft.padding.symmetric" not in source + kit_source
          and "ft.padding.only" not in source + kit_source
          and "ft.padding.all" not in source + kit_source)
    check("tonight previews tomorrow's due habits",
          "habits_due_tomorrow(" in source and "Kal:" in source)
    check("garden shows the plant of the day",
          "plant_of_the_day(" in source and "Plant of the day" in source)
    check("garden shows a category legend",
          "legend_categories(" in source and "Legend:" in source)
    check("tonight shows the longest gap",
          "longest_gap(" in source and "Longest gap:" in source)
    check("tonight shows the busiest weekday",
          "busiest_weekday(" in source and "busiest:" in source)
    check("habit cards show effort and age",
          "effort_text" in source and "planted" in source)
    check("habit cards offer a copy button",
          "clone_habit(" in source and "📋 Copy" in source)
    check("notifications get the last backup date",
          "_last_backup_date(" in source
          and "last_backup_date=_last_backup_date()" in source)


if __name__ == "__main__":
    test_ui_api()
    print(f"{PASSED} tests passed")
