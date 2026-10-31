"""Lab 6 - Branch coverage tests for elevator_dispatch.py.

Akash Singh, PES2UG24CS042

Goal: make every decision in elevator_dispatch.py evaluate to both
True and False. The line coverage suite reached 100% of lines but
missed branch 40->36 in pick_elevator (a car that is NOT better than
the current best). This file contains the full suite plus the tests
for that branch and other edge cases.
"""
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- next_direction: direction == "up" (True / False) ----------

def test_up_with_request_above_keeps_going_up():
    # direction == "up" True, above True
    assert next_direction(3, "up", [5, 7]) == "up"


def test_up_with_only_requests_below_turns_down():
    # above False, below True
    assert next_direction(5, "up", [1, 2]) == "down"


def test_up_with_no_requests_goes_idle():
    # above False, below False
    assert next_direction(4, "up", []) == "idle"


def test_up_prefers_above_when_requests_both_sides():
    assert next_direction(5, "up", [2, 8]) == "up"


# ---------- next_direction: direction == "down" (True / False) ----------

def test_down_with_request_below_keeps_going_down():
    # direction == "down" True, below True
    assert next_direction(6, "down", [2]) == "down"


def test_down_with_only_requests_above_turns_up():
    # below False, above True
    assert next_direction(2, "down", [8]) == "up"


def test_down_with_no_requests_goes_idle():
    # below False, above False
    assert next_direction(4, "down", []) == "idle"


def test_down_prefers_below_when_requests_both_sides():
    assert next_direction(5, "down", [2, 8]) == "down"


# ---------- next_direction: neither "up" nor "down" ----------

def test_idle_with_request_above_goes_up():
    assert next_direction(1, "idle", [4]) == "up"


def test_idle_with_request_below_goes_down():
    assert next_direction(9, "idle", [3]) == "down"


def test_idle_with_no_requests_stays_idle():
    assert next_direction(3, "idle", []) == "idle"


def test_idle_prefers_up_when_requests_both_sides():
    assert next_direction(5, "idle", [2, 8]) == "up"


def test_request_on_current_floor_is_ignored():
    # f == current is neither above nor below
    assert next_direction(4, "up", [4]) == "idle"
    assert next_direction(4, "down", [4]) == "idle"
    assert next_direction(4, "idle", [4]) == "idle"


def test_unknown_direction_falls_through_to_idle_logic():
    assert next_direction(2, "stopped", [6]) == "up"


# ---------- door_action ----------

def test_emergency_holds_doors():
    # emergency True
    assert door_action(100, False, True) == "hold_open"


def test_emergency_beats_overload_and_block():
    assert door_action(900, True, True) == "hold_open"


def test_overload_blocks_closing():
    # emergency False, load > 630 True
    assert door_action(700, False, False) == "overload"


def test_overload_beats_blocked():
    assert door_action(700, True, False) == "overload"


def test_load_exactly_at_limit_is_not_overload():
    # boundary: 630 is allowed, 631 is not
    assert door_action(630, False, False) == "close"
    assert door_action(631, False, False) == "overload"


def test_blocked_door_reopens():
    # load > 630 False, blocked True
    assert door_action(200, True, False) == "reopen"


def test_normal_load_closes():
    # blocked False
    assert door_action(200, False, False) == "close"


# ---------- pick_elevator ----------

def test_pick_elevator_with_no_cars_returns_none():
    # for loop body never entered
    assert pick_elevator([], 5) is None


def test_pick_elevator_single_idle_car():
    # not is_idle False, best is None True
    assert pick_elevator([("A", 2, True)], 5) == "A"


def test_pick_elevator_single_busy_car():
    # not is_idle True
    assert pick_elevator([("A", 2, False)], 5) == "A"


def test_pick_elevator_later_closer_car_wins():
    # best is None False, gap < best_gap True
    cars = [("A", 10, False), ("B", 4, True)]
    assert pick_elevator(cars, 5) == "B"


def test_pick_elevator_later_farther_car_loses():
    # gap < best_gap False -> branch 40->36 (back to the loop)
    cars = [("A", 5, True), ("B", 9, True)]
    assert pick_elevator(cars, 5) == "A"


def test_pick_elevator_tie_keeps_first_car():
    # equal gap is not strictly smaller, so the first car stays
    cars = [("A", 3, True), ("B", 7, True)]
    assert pick_elevator(cars, 5) == "A"


def test_pick_elevator_busy_penalty_changes_choice():
    # B is closer (gap 1) but busy, so its gap becomes 6 > 3
    cars = [("A", 8, True), ("B", 4, False)]
    assert pick_elevator(cars, 5) == "A"
