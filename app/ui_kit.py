"""Premium cute UI kit for Habit Garden (Flet 1.0.5).

Reusable building blocks so every view looks like one garden:
soft-shadow cards, gradient header bands, pill badges and pretty
progress bars. Pure Flet controls — no logic, no network, no fonts.
"""

import flet as ft

from app.theme import (
    CARD_BG, CARD_RADIUS, GOLD, GOLD_SOFT, HEADER_GRADIENT, LIGHT_PINK,
    MUTED, PINK, SHADOW, TEXT, TONIGHT_GRADIENT, category_colour,
)


def pill(text, bgcolor, color=TEXT):
    """A tiny rounded chip, e.g. a category or a done label."""
    return ft.Container(
        content=ft.Text(text, size=11, color=color),
        bgcolor=bgcolor,
        border_radius=10,
        padding=ft.Padding(left=8, right=8, top=2, bottom=2))


def streak_pill(streak):
    """A flame pill for a streak — gold once it hits a week."""
    streak = max(0, int(streak or 0))
    if streak >= 7:
        return pill(f"🔥 {streak} day streak", GOLD_SOFT, color="#8A6D1B")
    return pill(f"🔥 {streak} day streak", "#FDE7F3")


def soft_card(content, bgcolor=CARD_BG, border_color=LIGHT_PINK, width=None):
    """A rounded card with a soft shadow, the app's signature look."""
    return ft.Container(
        content=content,
        bgcolor=bgcolor,
        border=ft.Border.all(1, border_color),
        border_radius=CARD_RADIUS,
        padding=12,
        width=width,
        shadow=[ft.BoxShadow(blur_radius=12, color=SHADOW,
                              offset=ft.Offset(0, 4))])


def gradient_header(title, subtitle, lines=None):
    """A blush -> lilac -> cream header band for a view."""
    children = [
        ft.Text(title, size=26, weight=ft.FontWeight.BOLD, color=TEXT),
        ft.Text(subtitle, size=14, color=PINK),
    ]
    children.extend(lines or [])
    return ft.Container(
        content=ft.Column(children, spacing=6),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=HEADER_GRADIENT),
        border_radius=CARD_RADIUS,
        padding=18)


def gradient_card(content, colors=TONIGHT_GRADIENT):
    """A warm gradient card, used for the Tonight summary."""
    return ft.Container(
        content=content,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=colors),
        border_radius=CARD_RADIUS,
        padding=18,
        shadow=[ft.BoxShadow(blur_radius=12, color=SHADOW,
                              offset=ft.Offset(0, 4))])


def section_title(text):
    """A cute section heading inside a view."""
    return ft.Text(text, size=17, weight=ft.FontWeight.BOLD, color=TEXT)


def mini_progress(value, color=PINK):
    """A slim rounded progress bar for minutes and growth."""
    value = max(0.0, min(1.0, float(value or 0)))
    return ft.ProgressBar(value=value, color=color, bgcolor=LIGHT_PINK,
                          height=8, border_radius=6)


def stat_chip(emoji, label, value):
    """A little stat tile: one emoji, one value, one label."""
    return ft.Container(
        content=ft.Column([
            ft.Text(emoji, size=20),
            ft.Text(str(value), size=16, weight=ft.FontWeight.BOLD,
                    color=TEXT),
            ft.Text(label, size=11, color=MUTED),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        bgcolor=CARD_BG,
        border=ft.Border.all(1, LIGHT_PINK),
        border_radius=16,
        padding=10,
        expand=True)


def category_pill(category):
    """A pill in the category's own pastel colour."""
    return pill(category, category_colour(category))


def gold_text(text, size=14):
    """Warm gold text for premium accents (streaks, bests)."""
    return ft.Text(text, size=size, color=GOLD)
