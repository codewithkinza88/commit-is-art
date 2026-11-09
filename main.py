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

from app.habits import (
    CATEGORIES, COLOURS, ICONS, add_habit, delete_habit, edit_habit,
    get_habit, new_habit,
)
from app.garden import garden_summary
from app.ordering import sort_habits
from app.motivation import nightly_message
from app.streaks import best_streak
from app.achievements import badges_for
from app.store import DEFAULT_PATH, load_store, save_store, seed_store
from app.theme import (
    BG, CARD_RADIUS, CREAM, DONE_BG, DONE_BORDER, GARDEN_CARD_WIDTH,
    LIGHT_PINK, LILAC, MINT, MUTED, PEACH, PINK, PROGRESS_HEIGHT, SKY, TEXT,
    card_bg, done_label, progress_colour, stage_colour,
)
from app.version import APP_NAME, APP_VERSION
from app.tracker import (
    current_streak, daily_summary, is_done, last_7_days, log_minutes,
    minutes_for, set_done, today_str,
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
    today = today_str()
    current_view = [0]  # 0 Today, 1 Garden, 2 Tonight

    def persist():
        save_store({"habits": habits, "logs": logs}, DEFAULT_PATH)

    def snack(message):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
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
            try:
                target = int(target_field.value or 0)
            except ValueError:
                target = 0
            if is_edit:
                edit_habit(habits, habit["id"], name=name_field.value,
                           category=category_field.value,
                           target_minutes=target, icon=icon_field.value,
                           colour=colour_field.value)
                snack("Habit updated! 💕")
            else:
                try:
                    add_habit(habits, new_habit(
                        name_field.value, category_field.value, target,
                        icon_field.value, colour_field.value, today))
                except ValueError:
                    snack("Please give your habit a name first 🌱")
                    return
                snack("New habit planted! 🌱")
            persist()
            dialog.open = False
            page.update()
            refresh()

        def delete_clicked(_e):
            delete_habit(habits, habit["id"])
            persist()
            dialog.open = False
            snack("Habit removed 🌿")
            page.update()
            refresh()

        buttons = [ft.TextButton("Cancel",
                                 on_click=lambda e: _close(dialog))]
        if is_edit:
            buttons.append(ft.TextButton("Delete 🗑️", on_click=delete_clicked))
        buttons.append(ft.Button("Save 💾", on_click=save_clicked))
        dialog = ft.AlertDialog(
            title=ft.Text("Edit habit ✏️" if is_edit else "Plant a new habit 🌱"),
            content=ft.Column(
                [name_field, category_field, target_field,
                 icon_field, colour_field],
                tight=True, spacing=12),
            actions=buttons)
        page.dialog = dialog
        dialog.open = True
        page.update()

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
            content=field,
            actions=[ft.TextButton("Cancel",
                                   on_click=lambda e: _close(dialog)),
                     ft.Button("Add ✨", on_click=add_clicked)])
        page.dialog = dialog
        dialog.open = True
        page.update()

    # ---------- views ----------
    def today_view():
        summary = daily_summary(logs, habits, today)
        header = ft.Column([
            ft.Text("Today 🌞", size=26, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text("Water your garden, one tick at a time 🌱",
                    size=14, color=PINK),
            ft.Text(f"{summary['done']} of {summary['total']} habits done "
                    f"• {summary['percent']}% • "
                    f"{summary['total_minutes']} min logged",
                    size=14, color=MUTED),
            ft.ProgressBar(value=summary["percent"] / 100,
                           color=progress_colour(summary["percent"]),
                           bgcolor=LIGHT_PINK, height=PROGRESS_HEIGHT,
                           border_radius=8),
            ft.Text(f"🌸 {summary['percent']}% of today done",
                    size=13, color=PINK),
        ], spacing=6)

        cards = []
        for habit in sort_habits(habits, logs, today):
            done = is_done(logs, habit, today)
            streak = current_streak(logs, habit)
            minutes = minutes_for(logs, habit["id"], today)
            target = habit.get("target_minutes") or 0
            target_text = f"🎯 {target} min" if target else "no target"
            card = ft.Container(
                content=ft.Row([
                    ft.Checkbox(
                        value=done,
                        on_change=lambda e, h=habit: _tick(h, e.control.value)),
                    ft.Column([
                        ft.Text(f"{habit['icon']}  {habit['name']}",
                                size=16, weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.Text(f"{habit['category']} • {target_text} • "
                                f"🔥 {streak} day streak • ⏱️ {minutes} min",
                                size=13, color=MUTED),
                        ft.Text(done_label(done), size=12, color=MUTED),
                    ], expand=True, spacing=2),
                    ft.IconButton(icon=ft.Icons.ADD, tooltip="+15 min",
                                  on_click=lambda e, h=habit: _quick_minutes(h)),
                    ft.IconButton(icon=ft.Icons.TIMER, tooltip="Log minutes",
                                  on_click=lambda e, h=habit: open_minutes_dialog(h)),
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Edit habit",
                                  on_click=lambda e, h=habit: open_habit_dialog(h)),
                ]),
                bgcolor=card_bg(habit.get("colour", SKY), done=done),
                border=ft.Border.all(1, DONE_BORDER if done else LIGHT_PINK),
                border_radius=CARD_RADIUS, padding=12)
            cards.append(card)

        if not habits:
            cards.append(ft.Text("No habits yet — plant your first one! 🌱",
                                 size=15, color=MUTED))
        return ft.Column(
            [header,
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
            plants.append(ft.Container(
                content=ft.Column([
                    ft.Text(plant["emoji"], size=56),
                    ft.Text(plant["name"], size=15,
                            weight=ft.FontWeight.BOLD, color=TEXT),
                    ft.Text(f"🌷 {plant['label']} • 🔥 {plant['streak']} days",
                            size=13, color=MUTED),
                    ft.Text(plant["message"], size=12, color=MUTED),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4),
                bgcolor=stage_colour(plant["stage"]),
                border=ft.Border.all(1, LIGHT_PINK),
                border_radius=CARD_RADIUS,
                padding=16, width=GARDEN_CARD_WIDTH))
        if not plants:
            plants.append(ft.Text("Your garden is empty — plant a habit! 🌱",
                                  size=15, color=MUTED))
        return ft.Column([
            ft.Text("My Garden 🌷", size=26, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text(garden["message"], size=15, color=MUTED),
            ft.Row(plants, wrap=True, spacing=12),
        ], spacing=14)

    def tonight_view():
        summary = daily_summary(logs, habits, today)
        week = last_7_days(logs, habits)
        message = nightly_message(summary)
        longest_streak = max(
            (best_streak(logs, habit) for habit in habits), default=0)
        badges = badges_for(logs, habits, today)
        badges_text = (", ".join(
            f"{b['emoji']} {b['label']}" for b in badges)
            if badges else "No badges yet today — plant a habit! 🌱")
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
            ft.Text("Tonight's review 🌙", size=26,
                    weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text(message, size=15, color=MUTED),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"{summary['done']} / {summary['total']} habits",
                            size=22, weight=ft.FontWeight.BOLD, color=TEXT),
                    ft.Text(f"{summary['percent']}% achieved today",
                            size=16, color=TEXT),
                    ft.Text(f"Total time: {summary['total_minutes']} minutes",
                            size=15, color=MUTED),
                    ft.Text(f"Best habit today: "
                            f"{summary['best_habit'] or '—'} "
                            f"({summary['best_minutes']} min)",
                            size=15, color=MUTED),
                    ft.Text(f"🔥 Longest streak ever: {longest_streak} days",
                            size=15, color=MUTED),
                ], spacing=6),
                bgcolor=CREAM, border=ft.Border.all(1, PEACH),
                border_radius=CARD_RADIUS, padding=18),
            ft.Text("Badges earned 🏅", size=17,
                    weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text(badges_text, size=14, color=TEXT),
            ft.Text("Minutes per habit", size=17,
                    weight=ft.FontWeight.BOLD, color=TEXT),
            *minutes_rows,
            ft.Text("Last 7 days 📅", size=17,
                    weight=ft.FontWeight.BOLD, color=TEXT),
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
