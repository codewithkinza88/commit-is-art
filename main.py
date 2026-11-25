"""Habit Garden 🌸 — a cute habit tracker in Python (Flet).

No login at all (login comes later). All data lives locally in
habit_garden.json on the device.

Run on desktop:
    pip install -r requirements.txt
    flet run            # or: python3 main.py

Build the Android APK (needs the Flet CLI + Flutter + Android SDK):
    flet build apk
"""

import os
import threading
import time

import flet as ft

from datetime import date, timedelta

from app.habits import (
    CATEGORIES, COLOURS, EFFORTS, EFFORT_EMOJI, ICONS, add_habit,
    clone_habit, count_active_habits, count_archived, delete_habit,
    edit_habit, get_habit,
    habit_age_days, new_habit,
)
from app.garden import (count_blooming, count_full_bloom, count_seeds,
                        count_sprouts, names_sprouts,
                        counts_text,
                        days_to_next_stage,
                        flower_bed, flower_count, flower_for, garden_summary,
                        next_habit_to_water,
                        plant_of_the_day, plant_with_longest_streak,
                        plants_at_stage, plants_by_stage, stage_progress,
                        total_plants)
from app.insights import (consistency_message, consistency_score,
                          most_consistent_habit, weekly_done_rate)
from app.notes import (count_notes, latest_note,
                       notes_count_last_14_days)
from app.ordering import sort_habits
from app.motivation import (comeback_message, evening_message,
                            morning_message, nightly_message, weekly_cheer,
                            welcome_message)
from app.notifications import (build_notifications, notification_key,
                               should_refresh, unread_count)
from app.updater import (default_apk_path, download_apk,
                         fetch_latest_release, is_newer)
from app.streaks import (average_best_streak, average_streak, best_streak,
                         days_since_last_done, habits_on_streak,
                         last_done_label,
                         longest_current_streak, longest_gap,
                         longest_streak_overall,
                         median_best_streak, median_current_streak,
                         streak_leaderboard, total_streak_days)
from app.achievements import badge_labels, badges_count, badges_for
from app.backup import backup_filename, backup_to_json, restore_from_json
from app.categories import (
    best_category, legend_categories, total_minutes_by_category)
from app.monthly import (average_minutes_per_day, busiest_weekday,
                         days_logged_this_month, monthly_summary,
                         quietest_weekday)
from app.schedule import (count_due_this_week, count_due_today_undone,
                          due_today_names, habits_due_tomorrow)
from app.celebration import days_to_next_milestone, milestones_reached
from app.goals import weekly_goal_progress, weekly_goal_warning
from app.store import DEFAULT_PATH, load_store, save_store, seed_store
from app.theme import (
    BG, CARD_BG, DONE_BORDER, GARDEN_CARD_WIDTH,
    GOLD, LIGHT_PINK, MUTED, PINK, PROGRESS_HEIGHT, SKY,
    TEXT, TONIGHT_GRADIENT, card_bg, category_colour, done_label,
    progress_colour, stage_colour, DEEP_ROSE,
)
from app.ui_kit import (
    category_pill, gradient_card, gradient_header, mini_progress, pill,
    section_title, soft_card, stat_chip, streak_pill,
)
from app.validation import (validate_category, validate_icon,
                            validate_target_minutes)
from app.version import APP_NAME, APP_VERSION
from app.tracker import (
    best_day_by_minutes, current_streak, daily_summary, done_count_today,
    is_done, last_7_days, log_minutes, minutes_for, set_done, today_str,
    total_minutes_last_30_days, total_minutes_this_week,
    total_minutes_last_14_days, total_minutes_last_7_days,
    total_minutes_today, total_minutes_yesterday,
)

# Pastel palette — soft, cute, friendly 🌸 (see app/theme.py)


def main(page: ft.Page):
    page.title = f"{APP_NAME} 🌸 v{APP_VERSION}"
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    store = load_store(DEFAULT_PATH)
    if not store["habits"]:
        store = seed_store()
        save_store(store, DEFAULT_PATH)
    habits = store["habits"]
    logs = store["logs"]
    notes = store.get("notes", {})
    today = today_str()
    last_date = [today]  # the day refresh() last built for
    read_keys = set()  # notification keys read this session (not saved)
    current_view = [0]  # 0 Today, 1 Garden, 2 Tonight

    # ---------- in-app updater ⬇️ ----------
    # The app checks GitHub for a newer public release itself and
    # downloads it right here — no browser, no Play Store. Offline
    # just means no banner; the check can never crash the app.
    update_info = [None]  # {"version", "apk_url", "tag"} when newer
    update_state = ["idle"]  # idle | downloading | downloaded | failed
    update_progress = [0]  # download percent, 0-100
    update_path = [None]  # where the downloaded APK was saved

    def _install_update(_e):
        # The final step is Android's own installer popup — one tap,
        # inside the app flow, no browser. The APK file is opened
        # with the system handler, which offers the package installer.
        if update_path[0]:
            page.launch_url("file://" + update_path[0])

    def _start_update_download(_e):
        info = update_info[0]
        if info is None or update_state[0] == "downloading":
            return
        update_state[0] = "downloading"
        update_progress[0] = 0
        refresh()

        def _download():
            try:
                dest = default_apk_path()
                last_pct = [-1]

                def _progress(done, total):
                    if total:
                        pct = min(100, round(100 * done / total))
                    else:
                        pct = update_progress[0]
                    if pct != last_pct[0]:
                        last_pct[0] = pct
                        update_progress[0] = pct
                        try:
                            refresh()
                        except Exception:
                            pass

                download_apk(info["apk_url"], dest, progress_cb=_progress)
                update_path[0] = dest
                update_state[0] = "downloaded"
                update_progress[0] = 100
            except Exception:
                update_state[0] = "failed"
                snack("Couldn't download the update — check your "
                      "internet and try again later 📶")
            try:
                refresh()
            except Exception:
                pass
            if update_state[0] == "downloaded":
                snack("Downloaded — tap Install 🌸")

        threading.Thread(target=_download, daemon=True).start()

    # ---------- in-app notifications 🔔 ----------
    # The bell lives in the header row; the count badge is rebuilt on
    # every refresh from the live state, so it is never stale.

    def _visible_notifications():
        return [n for n in build_notifications(
                    habits, logs, notes, today,
                    last_backup_date=_last_backup_date())
                if notification_key(n) not in read_keys]

    def _rebuild_header():
        visible = _visible_notifications()
        count = unread_count(visible)
        bell = ft.IconButton(icon=ft.Icons.NOTIFICATIONS,
                             tooltip="Notifications 🔔",
                             on_click=lambda e: open_notifications_dialog())
        if count:
            bell.badge = ft.Badge(label=str(count), bgcolor=DEEP_ROSE,
                                  text_color="white")
        header_row.controls = [
            ft.Text(f"🌸 {APP_NAME}", size=20, weight=ft.FontWeight.BOLD,
                    color=TEXT, expand=True),
            bell,
        ]

    def open_notifications_dialog():
        visible = _visible_notifications()
        dlg = [None]

        def _go_today(note):
            def _handler(_e):
                read_keys.add(notification_key(note))
                if dlg[0] is not None:
                    dlg[0].open = False
                current_view[0] = 0
                page.update()
                refresh()
            return _handler

        def _mark_all_read(_e):
            for note in visible:
                read_keys.add(notification_key(note))
            if dlg[0] is not None:
                dlg[0].open = False
            page.update()
            refresh()

        if not visible:
            rows = [ft.Text("All caught up! 🌸 No notifications right now.",
                            size=15, color=MUTED)]
        else:
            rows = []
            for note in visible:
                rows.append(ft.TextButton(
                    f"{note['icon']} {note['title']}\n{note['text']}",
                    on_click=_go_today(note)))
        dlg[0] = ft.AlertDialog(
            title=ft.Text("Notifications 🔔"),
            bgcolor=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=24),
            content=ft.Column(rows, tight=True, spacing=8,
                              scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Mark all read ✅", on_click=_mark_all_read),
                ft.TextButton("Close", on_click=lambda e: _close(dlg[0])),
            ])
        page.show_dialog(dlg[0])

    def persist():
        # Save everything — habits, logs AND notes. (Notes used to be
        # dropped here, so any note vanished on the next tick or save.)
        save_store({"habits": habits, "logs": logs, "notes": notes},
                   DEFAULT_PATH)

    # One reusable SnackBar, kept in page.overlay. Flet 1.0.5 has no
    # snack-bar attribute on the page and no show_snack_bar — the old
    # assignment silently did nothing, so no message ever appeared.
    _snack_bar = [None]

    def snack(message):
        if _snack_bar[0] is None:
            _snack_bar[0] = ft.SnackBar(ft.Text(message))
            page.overlay.append(_snack_bar[0])
        else:
            _snack_bar[0].content = ft.Text(message)
        _snack_bar[0].open = True
        page.update()

    # ---------- backup & restore 💾 ----------
    # The app already knew how to build a backup (app/backup.py) but
    # there was no button for it — so before a reinstall the data
    # could never be saved. Now it can, from the Garden view.
    _restore_picker = [None]

    def _backup_folder():
        # Downloads when it exists (Android), else the working dir.
        downloads = os.path.join(os.path.expanduser("~"), "Download")
        return downloads if os.path.isdir(downloads) else os.getcwd()

    def _last_backup_date():
        # Newest backup file date in the backup folder (None when no
        # backup was ever saved) — drives the gentle backup nudge.
        prefix, suffix = "habit-garden-backup-", ".json"
        latest = None
        try:
            names = os.listdir(_backup_folder())
        except OSError:
            return None
        for name in names:
            if name.startswith(prefix) and name.endswith(suffix):
                day = name[len(prefix):-len(suffix)]
                if len(day) == 10 and (latest is None or day > latest):
                    latest = day
        return latest

    def _export_backup(_e):
        # Synchronous on purpose: the file must exist before the
        # SnackBar promises it.
        try:
            text = backup_to_json(habits, logs, notes)
            filename = backup_filename()
            dest = os.path.join(_backup_folder(), filename)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(text)
            snack(f"Backup saved: {filename} ✅")
        except Exception:
            snack("Backup save nahi hua — dobara try karo")

    def _on_restore_picked(e):
        nonlocal habits, logs, notes
        # The picker staying silent on cancel is on purpose: the
        # user just changed their mind, nothing went wrong.
        if not e.files:
            return
        try:
            with open(e.files[0].path, "r", encoding="utf-8") as f:
                text = f.read()
            data = restore_from_json(text)
            habits = data["habits"]
            logs = data["logs"]
            backup_notes = data.get("notes")
            notes = backup_notes if isinstance(backup_notes, dict) else {}
            persist()
            refresh()
            snack("Backup restore ho gaya ✅")
        except Exception:
            snack("Yeh backup file nahi hai")

    def _import_backup(_e):
        if _restore_picker[0] is not None:
            _restore_picker[0].pick_files(
                allowed_extensions=["json"], allow_multiple=False)

    _restore_picker[0] = ft.FilePicker(on_result=_on_restore_picked)
    page.overlay.append(_restore_picker[0])

    # ---------- habit form (add / edit) ----------
    def open_habit_dialog(habit=None):
        is_edit = habit is not None
        name_field = ft.TextField(
            label="Habit name 🌸", hint_text="e.g. Study — DSA / course",
            value=habit["name"] if is_edit else "",
            autofocus=True, border_radius=16)
        category_field = ft.Dropdown(
            label="Category 🌿",
            value=habit["category"] if is_edit else "Study",
            options=[ft.dropdown.Option(c) for c in CATEGORIES],
            border_radius=16)
        target_field = ft.TextField(
            label="Daily target (minutes, 0 = none)",
            hint_text="How many minutes a day?",
            value=str(habit["target_minutes"]) if is_edit else "0",
            keyboard_type=ft.KeyboardType.NUMBER, border_radius=16)
        icon_field = ft.Dropdown(
            label="Icon ✨",
            value=habit["icon"] if is_edit else "🌱",
            options=[ft.dropdown.Option(i) for i in ICONS],
            border_radius=16)
        colour_field = ft.Dropdown(
            label="Colour 🎨",
            value=habit["colour"] if is_edit else "#BDE0FE",
            options=[ft.dropdown.Option(c) for c in COLOURS],
            border_radius=16)
        effort_field = ft.Dropdown(
            label="Effort 💪",
            value=habit.get("effort", "Medium") if is_edit else "Medium",
            options=[ft.dropdown.Option(e) for e in EFFORTS],
            border_radius=16)

        def save_clicked(_e):
            target = validate_target_minutes(target_field.value)
            if is_edit:
                if not (name_field.value or "").strip():
                    snack("Please give your habit a name first 🌱")
                    return
                edit_habit(habits, habit["id"], name=name_field.value,
                           category=validate_category(category_field.value),
                           target_minutes=target, icon=validate_icon(icon_field.value),
                           colour=colour_field.value,
                           effort=effort_field.value)
                snack("Habit updated! 💕")
            else:
                try:
                    add_habit(habits, new_habit(
                        name_field.value, validate_category(category_field.value), target,
                        validate_icon(icon_field.value), colour_field.value, today,
                        effort_field.value))
                except ValueError:
                    snack("Please give your habit a name first 🌱")
                    return
                snack(welcome_message(name_field.value))
            persist()
            dialog.open = False
            page.update()
            refresh()

        def confirm_delete(_e):
            delete_habit(habits, habit["id"])
            persist()
            confirm_dialog.open = False
            dialog.open = False
            snack("Habit removed 🌿")
            page.update()
            refresh()

        def delete_clicked(_e):
            page.show_dialog(confirm_dialog)

        confirm_dialog = None
        if is_edit:
            confirm_dialog = ft.AlertDialog(
                title=ft.Text("Delete this habit? 🗑️"),
                bgcolor=CARD_BG,
                shape=ft.RoundedRectangleBorder(radius=24),
                content=ft.Text(
                    f"'{habit['name']}' will be gone for good — "
                    "there is no undo yet. Are you sure?"),
                actions=[
                    ft.TextButton("Keep it 💕",
                                  on_click=lambda e: _close(confirm_dialog)),
                    ft.TextButton("Delete 🗑️", on_click=confirm_delete),
                ])

        buttons = [ft.TextButton("Cancel",
                                 on_click=lambda e: _close(dialog))]
        if is_edit:
            buttons.append(ft.TextButton("Delete 🗑️", on_click=delete_clicked))
        buttons.append(ft.Button("Save 💾", on_click=save_clicked))
        dialog = ft.AlertDialog(
            title=ft.Text("Edit habit ✏️" if is_edit else "Plant a new habit 🌱"),
            bgcolor=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=24),
            content=ft.Column(
                [name_field, category_field, target_field,
                 icon_field, colour_field, effort_field],
                tight=True, spacing=12),
            actions=buttons)
        # Flet 1.0.5 has no dialog attribute on the page — the old
        # assignment silently did nothing, so the add/edit form never
        # appeared. show_dialog is the call that actually opens it.
        page.show_dialog(dialog)

    def _close(dialog):
        dialog.open = False
        page.update()

    # ---------- minutes dialog ----------
    def open_minutes_dialog(habit):
        field = ft.TextField(label="Minutes ⏱️", hint_text="e.g. 15, 30 or 60",
                             value="15",
                             keyboard_type=ft.KeyboardType.NUMBER,
                             autofocus=True, border_radius=16)

        def add_clicked(_e):
            try:
                minutes = int(field.value or 0)
            except ValueError:
                minutes = 0
            if minutes > 0:
                log_minutes(logs, habit["id"], today, minutes)
                persist()
                snack(f"+{minutes} min logged for {habit['name']} ⏱️")
            dialog.open = False
            page.update()
            refresh()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Log minutes — {habit['name']} ⏱️"),
            bgcolor=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=24),
            content=field,
            actions=[ft.TextButton("Cancel",
                                   on_click=lambda e: _close(dialog)),
                     ft.Button("Add ✨", on_click=add_clicked)])
        page.show_dialog(dialog)

    # ---------- views ----------
    def today_view():
        summary = daily_summary(logs, habits, today)
        header = gradient_header(
            "Today 🌞", "Water your garden, one tick at a time 🌱", [
                ft.Text(morning_message(done_count_today(logs, habits, today),
                                        summary["total"]),
                        size=14, color=MUTED),
                ft.Text(f"{summary['done']} of {summary['total']} habits done "
                        f"• {summary['percent']}% • "
                        f"⏱ {total_minutes_today(logs, habits, today)} min today",
                        size=14, color=MUTED),
                ft.Text(f"Still to do today: "
                        f"{count_due_today_undone(habits, logs, date.today().weekday(), today)}",
                        size=14, color=PINK),
                ft.ProgressBar(value=summary["percent"] / 100,
                               color=progress_colour(summary["percent"]),
                               bgcolor=LIGHT_PINK, height=PROGRESS_HEIGHT,
                               border_radius=8),
                ft.Text(f"🌸 {summary['percent']}% of today done",
                        size=13, color=PINK),
            ])

        cards = []
        for habit in sort_habits(habits, logs, today):
            done = is_done(logs, habit, today)
            streak = current_streak(logs, habit)
            minutes = minutes_for(logs, habit["id"], today)
            target = habit.get("target_minutes") or 0
            target_text = f"🎯 {target} min" if target else "no target"
            note_count = count_notes(notes, habit["id"])
            note_text = (f"📝 {note_count} note" +
                         ("s" if note_count != 1 else "")
                         if note_count else "")
            _latest_date, latest_text = latest_note(notes, habit["id"])
            latest_preview = (f" • “{latest_text[:40]}”"
                              if latest_text else "")
            best = best_streak(logs, habit)
            effort = habit.get("effort") or "Medium"
            effort_text = (f"{EFFORT_EMOJI.get(effort, '🟡')} {effort}")
            age = habit_age_days(habit, today)
            age_text = ("planted today 🌱" if age == 0
                        else f"planted {age} day"
                        + ("s" if age != 1 else "") + " ago")
            # Actions sit in their own row under the habit text, with
            # labels — on a narrow phone the old single row squeezed
            # the three icon buttons off-screen, so Edit looked missing.
            card = soft_card(
                content=ft.Column([
                    ft.Row([
                        ft.Checkbox(
                            value=done,
                            on_change=lambda e, h=habit: _tick(h, e.control.value)),
                        ft.Column([
                            ft.Row([
                                ft.Text(f"{habit['icon']}  {habit['name']}",
                                        size=16, weight=ft.FontWeight.BOLD, color=TEXT),
                                pill(done_label(done),
                                     GOLD if done else LIGHT_PINK,
                                     color="#8A6D1B" if done else TEXT),
                            ], spacing=8),
                            ft.Row([
                                category_pill(habit["category"]),
                                streak_pill(streak),
                                pill(effort_text, "#FFF3D6"),
                                ft.Text(f"🏆 best {best} days",
                                        size=12, color=GOLD),
                            ], spacing=6),
                            ft.Text(f"{target_text} • ⏱️ {minutes} min",
                                    size=13, color=MUTED),
                            (mini_progress(min(1.0, minutes / target),
                                           progress_colour(
                                               min(100, round(100 * minutes / target))))
                             if target else ft.Container(height=0)),
                            ft.Text(" • ".join(
                                [p for p in [note_text,
                                             last_done_label(logs, habit),
                                             age_text]
                                 if p]) + latest_preview,
                                    size=12, color=MUTED),
                        ], expand=True, spacing=4),
                    ]),
                    ft.Row([
                        ft.TextButton("＋15 min ⏱️",
                                      on_click=lambda e, h=habit: _quick_minutes(h)),
                        ft.TextButton("⏱ Minutes",
                                      on_click=lambda e, h=habit: open_minutes_dialog(h)),
                        ft.TextButton("✏️ Edit",
                                      on_click=lambda e, h=habit: open_habit_dialog(h)),
                        ft.TextButton("📋 Copy",
                                      on_click=lambda e, h=habit: _copy_habit(h)),
                    ], alignment=ft.MainAxisAlignment.END, spacing=4),
                ], spacing=8),
                bgcolor=card_bg(habit.get("colour", SKY), done=done),
                border_color=DONE_BORDER if done else LIGHT_PINK)
            cards.append(card)

        if not habits:
            cards.append(ft.Text("No habits yet — plant your first one! 🌱",
                                 size=15, color=MUTED))
        # The most urgent notification as a soft banner on top, so the
        # app itself tells you what needs attention today.
        banner = []
        visible = _visible_notifications()
        if visible:
            top = visible[0]
            banner.append(soft_card(
                content=ft.Column([
                    ft.Text(f"{top['icon']} {top['title']}", size=15,
                            weight=ft.FontWeight.BOLD, color=TEXT),
                    ft.Text(top["text"], size=13, color=MUTED),
                    ft.TextButton("View all 🔔",
                                  on_click=lambda e: open_notifications_dialog()),
                ], spacing=4),
                bgcolor=LIGHT_PINK, border_color=PINK))
        # The in-app update banner sits right beside it — a new
        # version downloads and installs from inside the app.
        update_cards = []
        info = update_info[0]
        if info is not None:
            state = update_state[0]
            if state == "downloading":
                update_cards.append(soft_card(
                    content=ft.Column([
                        ft.Text(f"🌸 Downloading version "
                                f"{info['version']}… "
                                f"{update_progress[0]}%", size=15,
                                weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.ProgressBar(value=update_progress[0] / 100,
                                       color=PINK, bgcolor=LIGHT_PINK,
                                       height=PROGRESS_HEIGHT,
                                       border_radius=8),
                        ft.Text("Hold on, your new version is on its "
                                "way 💕", size=13, color=MUTED),
                    ], spacing=4),
                    bgcolor=LIGHT_PINK, border_color=PINK))
            elif state == "downloaded":
                update_cards.append(soft_card(
                    content=ft.Column([
                        ft.Text("🌸 New version downloaded!", size=15,
                                weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.Text("Tap Install and Android will do the "
                                "rest 📲", size=13, color=MUTED),
                        ft.Button("📲 Install",
                                  on_click=_install_update),
                    ], spacing=4),
                    bgcolor=LIGHT_PINK, border_color=PINK))
            else:
                update_cards.append(soft_card(
                    content=ft.Column([
                        ft.Text(f"🌸 New version {info['version']} "
                                "is here!", size=15,
                                weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.Text("Fresh flowers, fresh fixes — update "
                                "from right here, no browser needed 💕",
                                size=13, color=MUTED),
                        ft.Button("Update now ⬇️",
                                  on_click=_start_update_download),
                    ], spacing=4),
                    bgcolor=LIGHT_PINK, border_color=PINK))
        return ft.Column(
            [*banner, *update_cards, header,
             ft.Text("Tap ✏️ Edit on any habit to change it — "
                     "or plant a brand-new one below 🌱",
                     size=13, color=MUTED),
             ft.Button("＋ Plant a new habit 🌱",
                       on_click=lambda e: open_habit_dialog()),
             *cards],
            spacing=12)

    def _tick(habit, value):
        set_done(logs, habit["id"], today, value)
        persist()
        snack("Well done! 🌸" if value else "Unticked — no worries, try again 💕")
        refresh()

    def _quick_minutes(habit):
        log_minutes(logs, habit["id"], today, 15)
        persist()
        snack(f"+15 min for {habit['name']} ⏱️")
        refresh()

    def _copy_habit(habit):
        copy = clone_habit(habits, habit["id"])
        if copy is not None:
            persist()
            snack(f"Copied! 📋 {copy['name']}")
            refresh()

    def garden_view():
        garden = garden_summary(habits, logs, today)
        plants = []
        for plant in garden["plants"]:
            days_left = days_to_next_stage(plant["streak"])
            next_text = ("in full bloom! 🌷" if days_left == 0
                         else f"next stage in {days_left} day"
                         + ("s" if days_left != 1 else ""))
            plants.append(soft_card(
                content=ft.Column([
                    ft.Text(flower_for(plant["stage"], plant["habit_id"]),
                            size=56),
                    ft.Text(plant["flowers"], size=22),
                    ft.Text(plant["name"], size=15,
                            weight=ft.FontWeight.BOLD, color=TEXT),
                    pill(f"🌷 {plant['label']}",
                         stage_colour(plant["stage"])),
                    streak_pill(plant["streak"]),
                    mini_progress(stage_progress(plant["streak"])),
                    ft.Text(next_text, size=12, color=PINK),
                    ft.Text(plant["message"], size=12, color=MUTED),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6),
                bgcolor=stage_colour(plant["stage"]),
                border_color=LIGHT_PINK,
                width=GARDEN_CARD_WIDTH))
        if not plants:
            plants.append(ft.Text("Your garden is empty — plant a habit! 🌱",
                                  size=15, color=MUTED))
        header = gradient_header(
            "My Garden 🌷", garden["message"], [
                ft.Text(counts_text(plants_by_stage(habits, logs, today)),
                        size=14, color=MUTED),
            ])
        garden_rows = [header]
        if garden["plants"]:
            # A full flower bed right at the top, so lots of flowers
            # show as soon as the garden opens 🌷🌸🌼
            bed = flower_bed(garden["plants"])
            garden_rows.append(soft_card(
                content=ft.Column([
                    ft.Text(bed, size=26),
                    ft.Text(f"🌸 {len(bed)} flowers blooming in your garden",
                            size=14, color=PINK),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4),
                bgcolor=LIGHT_PINK, border_color=PINK))
            garden_rows.append(ft.Row([
                stat_chip("🌱", "plants", total_plants(habits)),
                stat_chip("🌸", "watered", f"{garden['percent_done']}%"),
                stat_chip("💧", "to water", garden["due_today"]),
            ], spacing=10))
            next_habit = next_habit_to_water(habits, logs, today)
            garden_rows.append(ft.Text(
                f"Next to water: {next_habit['icon']} {next_habit['name']}"
                if next_habit else "All watered! 🌸",
                size=14, color=PINK))
            star = plant_of_the_day(habits, logs, today)
            if star is not None:
                garden_rows.append(soft_card(
                    content=ft.Column([
                        ft.Text(f"🌟 Plant of the day: {star['icon']} "
                                f"{star['name']}",
                                size=15, weight=ft.FontWeight.BOLD,
                                color=TEXT),
                        ft.Text(f"🔥 {star['streak']}-day streak — "
                                + ("water it today! 💧"
                                   if not star["done_today"]
                                   else "already watered today 🌸"),
                                size=13, color=MUTED),
                    ], spacing=4),
                    bgcolor=LIGHT_PINK, border_color=PINK))
            longest = plant_with_longest_streak(habits, logs, today)
            if longest is not None:
                garden_rows.append(ft.Text(
                    f"🏆 Longest streak: {longest['icon']} "
                    f"{longest['name']} — {longest['streak']} days",
                    size=14, color=PINK))
            garden_rows.append(ft.Text(
                f"🌸 {flower_count(habits, logs, today)} flowers blooming "
                "in your garden",
                size=14, color=PINK))
            garden_rows.append(ft.Text(
                f"🌸 {count_blooming(habits, logs, today)} plants blooming "
                "right now",
                size=14, color=PINK))
            garden_rows.append(ft.Text(
                f"🌷 {count_full_bloom(habits, logs, today)} in full bloom",
                size=14, color=PINK))
            full_bloom_names = plants_at_stage(habits, logs, today,
                                               "full_bloom")
            if full_bloom_names:
                garden_rows.append(ft.Text(
                    f"🌷 In full bloom: {', '.join(full_bloom_names)}",
                    size=14, color=PINK))
            garden_rows.append(ft.Text(
                f"🌱 {count_seeds(habits, logs, today)} seeds waiting "
                "for their first day",
                size=14, color=PINK))
            garden_rows.append(ft.Text(
                f"🌿 {count_sprouts(habits, logs, today)} sprouts growing",
                size=14, color=PINK))
            sprout_names = names_sprouts(habits, logs, today)
            if sprout_names:
                garden_rows.append(ft.Text(
                    f"🌿 Sprouting: {', '.join(sprout_names)}",
                    size=14, color=PINK))
            legend = legend_categories(habits)
            if legend:
                first_icon = {}
                for habit in habits:
                    first_icon.setdefault(
                        habit.get("category") or "Daily Life",
                        habit.get("icon") or "🌱")
                garden_rows.append(ft.Row(
                    [ft.Text("Legend:", size=13, color=MUTED)] +
                    [ft.Text(f"{first_icon[c]} {c}", size=13,
                             color=category_colour(c)) for c in legend],
                    spacing=8, wrap=True))
        garden_rows.append(ft.Row(plants, wrap=True, spacing=12))
        garden_rows.append(soft_card(
            content=ft.Column([
                section_title("Backup & Restore 💾"),
                ft.Text("Save your habits before a reinstall, or bring "
                        "an old backup back.",
                        size=13, color=MUTED),
                ft.Row([
                    ft.Button("💾 Backup save karo",
                              on_click=_export_backup),
                    ft.Button("📥 Restore karo",
                              on_click=_import_backup),
                ], spacing=10, wrap=True),
            ], spacing=8),
            bgcolor=CARD_BG, border_color=LIGHT_PINK))
        return ft.Column(garden_rows, spacing=14)

    def tonight_view():
        summary = daily_summary(logs, habits, today)
        week = last_7_days(logs, habits)
        week_dates = [d["date"] for d in week]
        consistency = consistency_score(logs, habits, week_dates)
        consistency_text = (f"💪 Consistency (last 7 days): {consistency}% — "
                            f"{consistency_message(consistency)}")
        message = nightly_message(summary)
        longest_streak = longest_streak_overall(logs, habits)
        worst_gap = max((longest_gap(logs, h) for h in habits), default=0)
        absences = [days_since_last_done(logs, h) for h in habits]
        longest_absence = max((a for a in absences if a is not None),
                              default=0)
        comeback = (comeback_message(longest_absence)
                    if longest_absence >= 2 else "")
        avg_streak = average_streak(logs, habits)
        avg_best = average_best_streak(logs, habits)
        median_streak = median_best_streak(logs, habits)
        median_now = median_current_streak(logs, habits)
        week_minutes = total_minutes_this_week(logs, habits)
        best_week_day = best_day_by_minutes(logs, habits)
        if best_week_day:
            best_week_text = (
                f"Best day this week: "
                f"{date.fromisoformat(best_week_day['date']).strftime('%a')} "
                f"{best_week_day['date']} ({best_week_day['minutes']} min)")
        else:
            best_week_text = "Best day this week: —"
        next_milestone = days_to_next_milestone(longest_streak)
        if next_milestone:
            milestone_text = (f"Next milestone: {next_milestone[0]}-day "
                              f"streak in {next_milestone[1]} day"
                              + ("s" if next_milestone[1] != 1 else ""))
        else:
            milestone_text = "Next milestone: all milestones reached! 🌳"
        reached = milestones_reached(longest_streak)
        reached_text = (f"Milestones reached: "
                        f"{', '.join(str(m) for m in reached)}"
                        if reached else "")
        board = streak_leaderboard(logs, habits)
        board_text = (", ".join(
            f"{entry['name']} ({entry['current']}d)"
            for entry in board[:3]) if board else "—")
        steady = most_consistent_habit(logs, habits, week_dates)
        steady_text = (f"🌟 Most consistent: {steady['name']}"
                       if steady else "🌟 Most consistent: —")
        evening = evening_message(summary["done"], summary["total"])
        badges = badges_for(logs, habits, today)
        labels = badge_labels(logs, habits, today)
        badges_text = (", ".join(
            f"{b['emoji']} {label}" for b, label in zip(badges, labels))
            if badges else "No badges yet today — plant a habit! 🌱")
        goal_rows = []
        for habit in habits:
            target = habit.get("target_minutes") or 0
            if not target:
                continue
            progress = weekly_goal_progress(logs, habit, target * 7)
            warning = weekly_goal_warning(progress)
            cheer = weekly_cheer(progress["minutes"], progress["target"])
            goal_rows.append(ft.Text(
                f"🎯 {habit['name']}: {progress['minutes']}/"
                f"{progress['target']} min this week "
                f"({progress['percent']}%)"
                + (f" — {warning}" if warning else "")
                + f" — {cheer}",
                size=14, color=TEXT))
        if not goal_rows:
            goal_rows.append(ft.Text(
                "No daily targets set — add one to track a weekly goal 🎯",
                size=14, color=MUTED))
        month = monthly_summary(logs, habits, 2026, 11)
        busiest = busiest_weekday(month)
        quietest = quietest_weekday(month)
        month_text = (f"📅 November so far: {month['total_minutes']} min • "
                      f"{month['average_percent']}% average • "
                      f"{month['perfect_days']} perfect days"
                      f" • {days_logged_this_month(month)} days logged"
                      f" • avg {average_minutes_per_day(month)} min/day"
                      + (f" • busiest: {busiest}" if busiest else "")
                      + (f" • quietest: {quietest}" if quietest else ""))
        best_cat = best_category(logs, habits, today)
        best_cat_text = (f"🏆 Best category today: {best_cat['category']} "
                         f"({best_cat['percent']}% • {best_cat['minutes']} min)"
                         if best_cat else "🏆 Best category today: —")
        minutes_by_category = total_minutes_by_category(logs, habits, today)
        category_rows = []
        for category, mins in minutes_by_category.items():
            category_rows.append(ft.Text(f"⏱️ {category}: {mins} min",
                                        size=14, color=TEXT))
        if not category_rows:
            category_rows.append(ft.Text("No minutes logged yet today ⏱️",
                                        size=14, color=MUTED))
        yesterday = today_str(date.today() - timedelta(days=1))
        yday = daily_summary(logs, habits, yesterday)
        yday_minutes = total_minutes_yesterday(logs, habits)
        yday_text = (f"Yesterday vs today: {yday['done']}/{yday['total']} "
                     f"({yday['percent']}%) • {yday['total_minutes']} min → "
                     f"today {summary['done']}/{summary['total']} "
                     f"({summary['percent']}%) • "
                     f"{summary['total_minutes']} min")
        rows = []
        for day in week:
            rows.append(ft.Row([
                ft.Text(day["date"], size=14, color=TEXT, width=110),
                ft.ProgressBar(value=day["percent"] / 100,
                               color=progress_colour(day["percent"]),
                               bgcolor=LIGHT_PINK, height=8,
                               border_radius=6, expand=True),
                ft.Text(f"{day['done']}/{day['total']} • {day['percent']}%",
                        size=13, color=MUTED),
            ], spacing=8))
        minutes_rows = []
        for name, mins in summary["minutes_per_habit"].items():
            minutes_rows.append(ft.Text(f"⏱️ {name}: {mins} min",
                                        size=14, color=TEXT))
        tomorrow_due = habits_due_tomorrow(habits, date.today().weekday())
        tomorrow_text = ("Kal: " + ", ".join(
            f"{h.get('icon', '🌱')} {h['name']}" for h in tomorrow_due)
            if tomorrow_due else "Kal: nothing due — a free morning! 🌸")
        due_week = count_due_this_week(habits, date.today().weekday())
        due_today = due_today_names(habits, date.today().weekday())
        due_today_text = (f"Due today: {', '.join(due_today)}"
                          if due_today else "Due today: nothing — all free! 🌸")
        due_week_text = (f"Due this week: {due_week} habit"
                         + ("s" if due_week != 1 else ""))
        return ft.Column([
            gradient_header("Tonight's review 🌙", message, []),
            gradient_card(ft.Column([
                ft.Text(f"{summary['done']} / {summary['total']} habits",
                        size=22, weight=ft.FontWeight.BOLD, color=TEXT),
                ft.Text(f"{summary['percent']}% achieved today",
                        size=16, color=TEXT),
                ft.Text(evening, size=15, weight=ft.FontWeight.BOLD,
                        color=DEEP_ROSE),
                ft.Text(comeback, size=15, color=PINK) if comeback else ft.Container(),
                ft.Text(f"Total time: {summary['total_minutes']} minutes",
                        size=15, color=MUTED),
                ft.Text(f"Yesterday: {yday_minutes} min",
                        size=15, color=MUTED),
                ft.Text(yday_text, size=15, color=MUTED),
                ft.Text(f"Best habit today: "
                        f"{summary['best_habit'] or '—'} "
                        f"({summary['best_minutes']} min)",
                        size=15, color=MUTED),
                ft.Text(best_week_text, size=15, color=MUTED),
                ft.Text(f"Average best streak: {avg_streak} days",
                        size=15, color=MUTED),
                ft.Text(f"Average best streak ever: {avg_best} days",
                        size=15, color=MUTED),
                ft.Text(f"Median current streak: {median_now} days",
                        size=15, color=MUTED),
                ft.Text(f"🔥 {habits_on_streak(logs, habits)} habits on a streak",
                        size=15, color=MUTED),
                ft.Text(f"🌳 Longest live streak: "
                        f"{longest_current_streak(logs, habits)} days",
                        size=15, color=MUTED),
                ft.Text(f"Total streak days: "
                        f"{total_streak_days(logs, habits)}",
                        size=15, color=MUTED),
                ft.Text(f"🏆 Streak leaderboard: {board_text}",
                        size=15, color=MUTED),
                ft.Text(steady_text, size=15, color=MUTED),
                ft.Row([
                    stat_chip("🌳", "longest streak",
                              f"{longest_streak} days"),
                    stat_chip("🌸", "median best streak",
                              f"{median_streak} days"),
                    stat_chip("⏱️", "minutes this week",
                              f"{week_minutes} min"),
                ], spacing=10),
                ft.Text(f"Last 30 days: "
                        f"{total_minutes_last_30_days(logs, habits)} minutes",
                        size=15, color=MUTED),
                ft.Text(f"Last 14 days: "
                        f"{total_minutes_last_14_days(logs, habits)} minutes",
                        size=15, color=MUTED),
                ft.Text(f"📝 {notes_count_last_14_days(notes)} notes in the last 2 weeks",
                        size=15, color=MUTED),
                ft.Text(f"Last 7 days: "
                        f"{total_minutes_last_7_days(logs, habits)} minutes",
                        size=15, color=MUTED),
                ft.Text(f"📦 {count_archived(habits)} archived habits",
                        size=15, color=MUTED),
                ft.Text(f"🌱 {count_active_habits(habits)} active habits",
                        size=15, color=MUTED),
                ft.Text(f"Longest gap: {worst_gap} days", size=15,
                        color=MUTED),
                ft.Text(f"Done rate this week: "
                        f"{weekly_done_rate(logs, habits)}%",
                        size=15, color=MUTED),
                ft.Text(milestone_text, size=15, color=MUTED),
                ft.Text(reached_text, size=15, color=MUTED) if reached_text else ft.Container(),
                ft.Text(consistency_text, size=15, color=MUTED),
            ], spacing=6), colors=TONIGHT_GRADIENT),
            section_title("Badges earned 🏅"),
            ft.Text(f"Badges earned: {badges_count(logs, habits, today)}",
                    size=14, color=TEXT),
            ft.Text(badges_text, size=14, color=TEXT),
            section_title("Minutes per habit"),
            *minutes_rows,
            section_title("Minutes by category 🌿"),
            ft.Text(best_cat_text, size=14, color=TEXT),
            *category_rows,
            ft.Text(month_text, size=14, color=TEXT),
            section_title("Weekly goals 🎯"),
            *goal_rows,
            section_title("Tomorrow (Kal) 🌅"),
            ft.Text(tomorrow_text, size=14, color=TEXT),
            ft.Text(due_week_text, size=14, color=TEXT),
            ft.Text(due_today_text, size=14, color=TEXT),
            section_title("Last 7 days 📅"),
            *rows,
        ], spacing=12)

    content = ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    header_row = ft.Row(spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def refresh():
        # The app updates itself: recompute today, and if the day
        # rolled over since the last build, reload the store from disk
        # (in case it changed elsewhere) and forget what was read.
        nonlocal today, habits, logs, notes
        now = today_str()
        if should_refresh(last_date[0], now):
            today = now
            last_date[0] = now
            read_keys.clear()
            fresh = load_store(DEFAULT_PATH)
            if not fresh["habits"]:
                fresh = seed_store()
                save_store(fresh, DEFAULT_PATH)
            habits = fresh["habits"]
            logs = fresh["logs"]
            notes = fresh.get("notes", {})
        _rebuild_header()
        views = [today_view(), garden_view(), tonight_view()]
        content.controls = [views[current_view[0]]]
        page.update()

    def _check_for_update():
        # Runs once, in the background, so it can never slow startup
        # or crash the app: offline just means no banner, silently.
        try:
            latest = fetch_latest_release()
        except Exception:
            return
        if latest and is_newer(latest["version"], APP_VERSION):
            update_info[0] = latest
            try:
                refresh()
            except Exception:
                pass

    threading.Thread(target=_check_for_update, daemon=True).start()

    def _auto_refresh_loop():
        # Every minute, rebuild the views so new ticks, a new day or
        # new notifications show up on their own. A refresh failure
        # must never crash the app, so everything is guarded.
        while True:
            time.sleep(60)
            try:
                refresh()
            except Exception:
                pass

    threading.Thread(target=_auto_refresh_loop, daemon=True).start()

    def on_nav(e):
        current_view[0] = e.control.selected_index
        refresh()

    page.navigation_bar = ft.NavigationBar(
        bgcolor=LIGHT_PINK,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.TODAY, label="Today"),
            ft.NavigationBarDestination(icon=ft.Icons.LOCAL_FLORIST, label="Garden"),
            ft.NavigationBarDestination(icon=ft.Icons.NIGHTLIGHT_ROUND, label="Tonight"),
        ],
        on_change=on_nav)
    page.add(header_row, content)
    refresh()


ft.run(main)
