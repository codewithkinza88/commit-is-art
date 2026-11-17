"""Habit Garden 🌸 — a cute habit tracker in Python (Flet).

No login at all (login comes later). All data lives locally in
habit_garden.json on the device.

Run on desktop:
    pip install -r requirements.txt
    flet run            # or: python3 main.py

Build the Android APK (needs the Flet CLI + Flutter + Android SDK):
    flet build apk
"""

import flet as ft

from datetime import date, timedelta

from app.habits import (
    CATEGORIES, COLOURS, ICONS, add_habit, delete_habit, edit_habit,
    get_habit, new_habit,
)
from app.garden import (counts_text, days_to_next_stage, flower_bed,
                        flower_for, garden_summary, next_habit_to_water,
                        plants_by_stage, stage_progress, total_plants)
from app.insights import consistency_message, consistency_score
from app.notes import count_notes, latest_note
from app.ordering import sort_habits
from app.motivation import evening_message, morning_message, nightly_message
from app.streaks import (average_streak, best_streak, last_done_label,
                         longest_streak_overall, median_best_streak)
from app.achievements import badges_for
from app.categories import (
    best_category, total_minutes_by_category)
from app.monthly import monthly_summary
from app.goals import weekly_goal_progress, weekly_goal_warning
from app.store import DEFAULT_PATH, load_store, save_store, seed_store
from app.theme import (
    BG, CARD_BG, DONE_BORDER, GARDEN_CARD_WIDTH,
    GOLD, LIGHT_PINK, MUTED, PINK, PROGRESS_HEIGHT, SKY,
    TEXT, TONIGHT_GRADIENT, card_bg, done_label, progress_colour,
    stage_colour, DEEP_ROSE,
)
from app.ui_kit import (
    category_pill, gradient_card, gradient_header, mini_progress, pill,
    section_title, soft_card, stat_chip, streak_pill,
)
from app.validation import (validate_category, validate_icon,
                            validate_target_minutes)
from app.version import APP_NAME, APP_VERSION
from app.tracker import (
    current_streak, daily_summary, done_count_today, is_done, last_7_days, log_minutes,
    minutes_for, set_done, today_str, total_minutes_this_week,
    total_minutes_today,
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
    current_view = [0]  # 0 Today, 1 Garden, 2 Tonight

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

        def save_clicked(_e):
            target = validate_target_minutes(target_field.value)
            if is_edit:
                if not (name_field.value or "").strip():
                    snack("Please give your habit a name first 🌱")
                    return
                edit_habit(habits, habit["id"], name=name_field.value,
                           category=validate_category(category_field.value),
                           target_minutes=target, icon=validate_icon(icon_field.value),
                           colour=colour_field.value)
                snack("Habit updated! 💕")
            else:
                try:
                    add_habit(habits, new_habit(
                        name_field.value, validate_category(category_field.value), target,
                        validate_icon(icon_field.value), colour_field.value, today))
                except ValueError:
                    snack("Please give your habit a name first 🌱")
                    return
                snack("New habit planted! 🌱")
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
                 icon_field, colour_field],
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
                                             last_done_label(logs, habit)]
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
                    ], alignment=ft.MainAxisAlignment.END, spacing=4),
                ], spacing=8),
                bgcolor=card_bg(habit.get("colour", SKY), done=done),
                border_color=DONE_BORDER if done else LIGHT_PINK)
            cards.append(card)

        if not habits:
            cards.append(ft.Text("No habits yet — plant your first one! 🌱",
                                 size=15, color=MUTED))
        return ft.Column(
            [header,
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
        garden_rows.append(ft.Row(plants, wrap=True, spacing=12))
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
        avg_streak = average_streak(logs, habits)
        median_streak = median_best_streak(logs, habits)
        week_minutes = total_minutes_this_week(logs, habits)
        evening = evening_message(summary["done"], summary["total"])
        badges = badges_for(logs, habits, today)
        badges_text = (", ".join(
            f"{b['emoji']} {b['label']}" for b in badges)
            if badges else "No badges yet today — plant a habit! 🌱")
        goal_rows = []
        for habit in habits:
            target = habit.get("target_minutes") or 0
            if not target:
                continue
            progress = weekly_goal_progress(logs, habit, target * 7)
            warning = weekly_goal_warning(progress)
            goal_rows.append(ft.Text(
                f"🎯 {habit['name']}: {progress['minutes']}/"
                f"{progress['target']} min this week "
                f"({progress['percent']}%)"
                + (f" — {warning}" if warning else ""),
                size=14, color=TEXT))
        if not goal_rows:
            goal_rows.append(ft.Text(
                "No daily targets set — add one to track a weekly goal 🎯",
                size=14, color=MUTED))
        month = monthly_summary(logs, habits, 2026, 11)
        month_text = (f"📅 November so far: {month['total_minutes']} min • "
                      f"{month['average_percent']}% average • "
                      f"{month['perfect_days']} perfect days")
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
        return ft.Column([
            gradient_header("Tonight's review 🌙", message, []),
            gradient_card(ft.Column([
                ft.Text(f"{summary['done']} / {summary['total']} habits",
                        size=22, weight=ft.FontWeight.BOLD, color=TEXT),
                ft.Text(f"{summary['percent']}% achieved today",
                        size=16, color=TEXT),
                ft.Text(evening, size=15, weight=ft.FontWeight.BOLD,
                        color=DEEP_ROSE),
                ft.Text(f"Total time: {summary['total_minutes']} minutes",
                        size=15, color=MUTED),
                ft.Text(yday_text, size=15, color=MUTED),
                ft.Text(f"Best habit today: "
                        f"{summary['best_habit'] or '—'} "
                        f"({summary['best_minutes']} min)",
                        size=15, color=MUTED),
                ft.Text(f"Average best streak: {avg_streak} days",
                        size=15, color=MUTED),
                ft.Row([
                    stat_chip("🌳", "longest streak",
                              f"{longest_streak} days"),
                    stat_chip("🌸", "median best streak",
                              f"{median_streak} days"),
                    stat_chip("⏱️", "minutes this week",
                              f"{week_minutes} min"),
                ], spacing=10),
                ft.Text(consistency_text, size=15, color=MUTED),
            ], spacing=6), colors=TONIGHT_GRADIENT),
            section_title("Badges earned 🏅"),
            ft.Text(badges_text, size=14, color=TEXT),
            section_title("Minutes per habit"),
            *minutes_rows,
            section_title("Minutes by category 🌿"),
            ft.Text(best_cat_text, size=14, color=TEXT),
            *category_rows,
            ft.Text(month_text, size=14, color=TEXT),
            section_title("Weekly goals 🎯"),
            *goal_rows,
            section_title("Last 7 days 📅"),
            *rows,
        ], spacing=12)

    content = ft.Column([], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    def refresh():
        views = [today_view(), garden_view(), tonight_view()]
        content.controls = [views[current_view[0]]]
        page.update()

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
    page.add(
        ft.Text(f"🌸 {APP_NAME}", size=20, weight=ft.FontWeight.BOLD, color=TEXT),
        content)
    refresh()


ft.run(main)
