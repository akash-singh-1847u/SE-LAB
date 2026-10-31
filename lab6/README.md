# Lab 6: Code and Branch Coverage - Elevator Dispatch

Software Engineering, PES University
Akash Singh, PES2UG24CS042, Section A

Assigned repo: github.com/SETAPESU26/L6_L7_38_elevator_dispatch

## About

`elevator_dispatch.py` has three functions:

- `next_direction(current, direction, requests)` picks `up`, `down` or `idle`
  from the car's floor, its current direction and the pending requests.
- `door_action(load_kg, blocked, emergency)` returns `hold_open`, `overload`,
  `reopen` or `close`. Emergency wins over overload (> 630 kg), which wins over
  a blocked door.
- `pick_elevator(cars, floor)` sends the car with the smallest distance to the
  call. Busy cars get a +5 penalty, and on a tie the first car stays.

Tools used: Python 3.14.3, pytest 9.2.0, coverage 7.17.0.

## Results

Numbers are for `elevator_dispatch.py`.

| Test file | Tests | Line coverage | Branch coverage | Missing |
|---|---|---|---|---|
| `test_elevator_dispatch.py` (starter) | 2 | 31% | 25% | lines 5-9, 11-15, 17, 19, 26-30, 34-43 |
| `CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py` | 14 | 100% | 99% | branch `40->36` |
| `BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py` | 28 | 100% | 100% | none |

### Code coverage

The starter tests only ran the emergency door case and an idle car with no
requests. The code coverage suite adds one test for each `return` in
`next_direction` (up, down and idle direction, each with requests above, only
below, or none), one for each `door_action` result, and one `pick_elevator`
call with a busy car followed by a closer idle car. That runs every line, so
line coverage is 100%.

### Branch coverage

Running the same 14 tests with `--branch` reports 99% and one partial branch,
`40->36`. Line 40 is `if best is None or gap < best_gap:` in `pick_elevator`.
Every car in the code coverage test became the new best, so the condition was
never False and the loop never skipped the assignment. Line coverage could not
show this because the False case has no line of its own.

The branch coverage suite keeps the earlier tests and adds:

- a car farther away than the current best (covers `40->36`)
- two cars at the same distance, where the first stays
- a closer busy car losing to an idle car because of the +5 penalty
- an empty car list, which returns `None`
- single idle and single busy cars
- the 630 kg boundary (630 closes, 631 is overload)
- precedence: emergency over overload and block, overload over block
- requests on both sides for each direction
- a request on the current floor, which counts as neither above nor below
- an unknown direction string, which uses the idle logic

With these tests every decision is True at least once and False at least
once, so branch coverage is 100%.

## Screenshots

| File | Shows |
|---|---|
| `screenshots/code_coverage_PES2UG24CS042.png` | Line coverage run of the code coverage suite (100%) |
| `screenshots/code_suite_branch_check_PES2UG24CS042.png` | The same suite with `--branch`, showing the missed `40->36` branch |
| `screenshots/branch_coverage_PES2UG24CS042.png` | Branch coverage run of the branch coverage suite (100%) |

The same output is saved as text in `reports/`, along with the starter test
results (`initial_line_coverage.txt`, `initial_branch_coverage.txt`).

## Running it

```bash
cd lab6
pip install coverage pytest
coverage run -m pytest -v CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py
coverage report -m
coverage run --branch -m pytest -v BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py
coverage report -m
```

## Files

| File | Contents |
|---|---|
| `elevator_dispatch.py` | Module under test (unchanged from the assigned repo) |
| `test_elevator_dispatch.py` | Starter tests from the assigned repo |
| `CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py` | Tests for line coverage |
| `BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py` | Tests for branch coverage |
| `reports/` | Text output of every coverage run |
| `screenshots/` | Terminal output for the 90%+ runs |
