"""Cute theme for Habit Garden (pure data, no Flet).

One place for the pastel palette, soft card shapes and the little
visual rules that make the app feel like a garden, not a form.
The UI in main.py reads these values so every view matches.
"""

# Soft pastel palette 🌸
BG = "#FFF8F0"
CARD_BG = "#FFFFFF"
PINK = "#F9A8D4"
LIGHT_PINK = "#FDE7F3"
LILAC = "#E4C1F9"
SKY = "#BDE0FE"
MINT = "#B5EAD7"
PEACH = "#FFD6A5"
CREAM = "#FFF3D6"
BLUSH = "#FBCFE8"
TEXT = "#5B4B5A"
MUTED = "#9A8A99"
DONE_BG = "#E7F9EE"  # soft mint for a ticked-off habit
DONE_BORDER = "#A8E6C5"

# Soft, rounded shapes
CARD_RADIUS = 22
SMALL_RADIUS = 16
PROGRESS_HEIGHT = 12
GARDEN_CARD_WIDTH = 170

# Garden stage colours — each stage gets its own soft tint
STAGE_COLOURS = {
    "seed": "#E8F5E9",
    "sprout": "#DCEDC8",
    "growing": "#C8E6C9",
    "blooming": "#FCE4EC",
    "full_bloom": "#F8BBD0",
}

# Progress colour by how much of the day is done
PROGRESS_COLOURS = [
    (80, "#F48FB1"),  # almost there — deep pink
    (50, "#F9A8D4"),  # halfway — pink
    (1, "#FBCFE8"),  # started — blush
    (0, "#E4C1F9"),  # not yet — lilac
]


def card_bg(colour, done=False):
    """Soft background for a habit card.

    Done habits get a gentle mint wash so a ticked habit looks
    finished at a glance; otherwise the habit's own pastel colour
    shows through, softened with a light tint.
    """
    if done:
        return DONE_BG
    return (colour or SKY) + "55"


def progress_colour(percent):
    """Pink shade for the Today progress bar from 0-100%."""
    percent = max(0, min(100, int(percent or 0)))
    for minimum, colour in PROGRESS_COLOURS:
        if percent >= minimum:
            return colour
    return LILAC


def stage_colour(stage):
    """Soft tint for a garden plant card by growth stage."""
    return STAGE_COLOURS.get(stage or "seed", "#E8F5E9")


def done_label(done):
    """Little pill text shown on a habit card."""
    return "Done 🌸" if done else "Not yet 🌱"
