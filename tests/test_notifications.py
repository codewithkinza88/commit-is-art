"""Plain-script tests for in-app notifications (app/notifications.py).

Kinza asked (17 Nov 2026, WhatsApp) for notifications inside the
app itself, and for the app to update itself automatically — no Play
Store, no system push. The notifications are rebuilt from the live
state every time the app draws, so these tests check the rules that
build them, with the hour passed in (never the real clock).

Run:  python3 tests/test_notifications.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.achievements import badges_for  # noqa: E402
from app.habits import new_habit  # noqa: E402
from app.notifications import (  # noqa: E402
    build_notifications, notification_key, should_refresh, unread_count,
)
from app.tracker import log_minutes, set_done  # noqa: E402

PASSED = 0


def check(name, condition):
    global PASSED
    assert condition, f"FAILED: {name}"
    PASSED += 1
    print(f"PASS {name}")


def _habits():
    return [new_habit("Study — DSA", "Study", 60, "📚", "#A5D8FF",
                      "2026-11-17"),
            new_habit("Read a book", "Books", 30, "📖", "#F9A8D4",
                      "2026-11-17")]


def _plain_habits():
    # No daily targets, so no weekly-goal warnings muddy the counts.
    return [new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                      "2026-11-17"),
            new_habit("Walk outside", "Health", 0, "🏃", "#B5EAD7",
                      "2026-11-17")]


def _kinds(notes):
    return [n["kind"] for n in notes]


def _of_kind(notes, kind):
    return [n for n in notes if n["kind"] == kind]


def test_notifications():
    check("no habits means no notifications",
          build_notifications([], {}, {}, "2026-11-17", hour=14) == [])
    check("unread count is just the count",
          unread_count(build_notifications(_plain_habits(), {}, {},
                                           "2026-11-17", hour=14)) == 2)
    check("unread count of nothing is 0", unread_count([]) == 0)

    habits = _plain_habits()
    notes = build_notifications(habits, {}, {}, "2026-11-17", hour=14)
    check("each undone habit gets a water reminder",
          _kinds(notes) == ["due", "due"])
    check("a due reminder names its habit",
          notes[0]["title"] == "Water Drink water"
          and notes[0]["habit_id"] == habits[0]["id"])
    check("a done habit gets no reminder",
          len(_of_kind(build_notifications(
              habits, {"2026-11-17": {
                  habits[0]["id"]: {"done": True, "minutes": 0}}},
              {}, "2026-11-17", hour=14), "due")) == 1)

    habits = _plain_habits()
    habits[0]["days"] = [0]  # Mondays only; 2026-11-17 is a Tuesday
    due = _of_kind(build_notifications(habits, {}, {}, "2026-11-17",
                                       hour=14), "due")
    check("a habit not due today gets no reminder",
          len(due) == 1 and due[0]["habit_id"] == habits[1]["id"])

    habits = _plain_habits()
    logs = {}
    for day in ("2026-11-14", "2026-11-15", "2026-11-16"):
        set_done(logs, habits[0]["id"], day, True)
    notes = build_notifications(habits, logs, {}, "2026-11-17", hour=14)
    check("a 3-day streak at risk comes first",
          _kinds(notes)[0] == "streak")
    check("the streak reminder names the streak",
          "3-day streak" in notes[0]["title"]
          and notes[0]["habit_id"] == habits[0]["id"])

    logs = {}
    for day in ("2026-11-15", "2026-11-16"):
        set_done(logs, habits[0]["id"], day, True)
    check("a 2-day streak is not at risk yet",
          "streak" not in _kinds(build_notifications(
              habits, logs, {}, "2026-11-17", hour=14)))

    check("evening prompt appears after 6 PM",
          "evening" in _kinds(build_notifications(
              _habits(), {}, {}, "2026-11-17", hour=19)))
    check("no evening prompt before 6 PM",
          "evening" not in _kinds(build_notifications(
              _habits(), {}, {}, "2026-11-17", hour=17)))
    check("morning prompt appears before noon with nothing done",
          "morning" in _kinds(build_notifications(
              _habits(), {}, {}, "2026-11-17", hour=9)))
    check("morning prompt counts the waiting habits",
          "2 habits waiting" in build_notifications(
              _habits(), {}, {}, "2026-11-17", hour=9)[-1]["text"])
    habits = _habits()
    logs = {"2026-11-17": {habits[0]["id"]: {"done": True, "minutes": 0}}}
    check("no morning prompt once something is done",
          "morning" not in _kinds(build_notifications(
              habits, logs, {}, "2026-11-17", hour=9)))
    check("no morning prompt after noon",
          "morning" not in _kinds(build_notifications(
              _habits(), {}, {}, "2026-11-17", hour=13)))

    habits = _habits()
    logs = {}
    log_minutes(logs, habits[0]["id"], "2026-11-16", 60)
    notes = build_notifications(habits, logs, {}, "2026-11-17", hour=14)
    check("a weekly goal behind schedule warns you",
          "goal" in _kinds(notes))
    check("the goal warning names the minutes left",
          any("min left" in n["text"] for n in notes
              if n["kind"] == "goal"))
    logs = {}
    for day in ("2026-11-11", "2026-11-12", "2026-11-13",
                "2026-11-14", "2026-11-15", "2026-11-16",
                "2026-11-17"):
        log_minutes(logs, habits[0]["id"], day, 60)
    check("a met weekly goal warns nobody",
          "goal" not in _kinds(build_notifications(
              [habits[0]], logs, {}, "2026-11-17", hour=14)))
    check("a habit with no target has no weekly goal",
          "goal" not in _kinds(build_notifications(
              [new_habit("Drink water", "Health", 0, "💧", "#BDE0FE",
                         "2026-11-17")], {}, {}, "2026-11-17", hour=14)))

    habits = _habits()
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-17", True)
    check("a badge is not earned before its first tick",
          "first_step" not in {b["key"] for b in badges_for(
              logs, habits, "2026-11-16")})
    notes = build_notifications(habits, logs, {}, "2026-11-17", hour=14)
    check("a badge earned today is announced",
          any(n["kind"] == "badge"
              and n["title"] == "New badge: First Step"
              for n in notes))
    logs = {}
    set_done(logs, habits[0]["id"], "2026-11-16", True)
    check("a badge earned yesterday is not new today",
          "badge" not in _kinds(build_notifications(
              habits, logs, {}, "2026-11-17", hour=14)))
    habits = _habits()
    logs = {"2026-11-17": {habits[0]["id"]: {"done": True, "minutes": 0}}}
    kinds = _kinds(build_notifications(habits, logs, {},
                                       "2026-11-17", hour=14))
    check("due reminders come before badges",
          kinds.index("due") < kinds.index("badge"))

    many = [new_habit(f"Habit {i}", "Study", 0, "🌱", "#BDE0FE",
                      "2026-11-17") for i in range(12)]
    check("the list caps at 10 notifications",
          len(build_notifications(many, {}, {}, "2026-11-17",
                                  hour=14)) == 10)

    note = build_notifications(_plain_habits(), {}, {}, "2026-11-17",
                               hour=14)[0]
    check("a notification key is stable",
          notification_key(note) == notification_key(note))
    plain = build_notifications(_plain_habits(), {}, {}, "2026-11-17",
                                hour=14)
    check("different habits get different keys",
          notification_key(plain[0]) != notification_key(plain[1]))

    check("same day needs no refresh",
          should_refresh("2026-11-17", "2026-11-17") is False)
    check("a new day needs a refresh",
          should_refresh("2026-11-17", "2026-11-18") is True)
    check("no last date needs a refresh",
          should_refresh("", "2026-11-18") is True)
    check("an empty current date needs no refresh",
          should_refresh("", "") is False)


if __name__ == "__main__":
    test_notifications()
    print(f"{PASSED} tests passed")
