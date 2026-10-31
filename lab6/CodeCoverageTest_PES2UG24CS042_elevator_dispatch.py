"""Lab 6 - Code (line) coverage tests for elevator_dispatch.py.

Akash Singh, PES2UG24CS042

Goal: execute every line of elevator_dispatch.py at least once.
Each test is chosen to reach a return statement or assignment
that the starter tests never ran.
"""
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- next_direction: moving up ----------

def test_up_with_request_above_keeps_going_up():
    assert next_direction(3, "up", [5, 7]) == "up"


def test_up_with_only_requests_below_turns_down():
    assert next_direction(5, "up", [1, 2]) == "down"


def test_up_with_no_requests_goes_idle():
    assert next_direction(4, "up", []) == "idle"


# ---------- next_direction: moving down ----------

def test_down_with_request_below_keeps_going_down():
    assert next_direction(6, "down", [2]) == "down"


def test_down_with_only_requests_above_turns_up():
    assert next_direction(2, "down", [8]) == "up"


def test_down_with_no_requests_goes_idle():
    assert next_direction(4, "down", []) == "idle"


# ---------- next_direction: idle car ----------

def test_idle_with_request_above_goes_up():
    assert next_direction(1, "idle", [4]) == "up"


def test_idle_with_request_below_goes_down():
    assert next_direction(9, "idle", [3]) == "down"


def test_idle_with_no_requests_stays_idle():
    assert next_direction(3, "idle", []) == "idle"


# ---------- door_action ----------

def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"


def test_overload_blocks_closing():
    assert door_action(700, False, False) == "overload"


def test_blocked_door_reopens():
    assert door_action(200, True, False) == "reopen"


def test_normal_load_closes():
    assert door_action(200, False, False) == "close"


# ---------- pick_elevator ----------

def test_pick_elevator_runs_whole_loop():
    # A busy car followed by a closer idle car: runs the penalty line
    # and the "new best" assignment lines.
    cars = [("A", 10, False), ("B", 4, True)]
    assert pick_elevator(cars, 5) == "B"
