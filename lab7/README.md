# Lab 7: Fuzz Testing - Elevator Dispatch

Software Engineering, PES University
Akash Singh, PES2UG24CS042, Section A

Assigned repo: github.com/SETAPESU26/L6_L7_38_elevator_dispatch

## About

`elevator_dispatch.py` reads three kinds of text input from the user:

- `parse_request(text)` turns `"5->9"` into `(5, 9)`.
- `total_travel(floors_csv)` turns `"1,5,3,9"` into the total floors moved (12).
- `load_percent(text)` turns `"450 of 630"` into a load percentage (71).

The handout calls the files `processor.py` and `test_processor.py`. In this
repo they are `elevator_dispatch.py` and `test_elevator_dispatch.py`.

Tools used: Python 3.14.3, pytest 9.2.0, Hypothesis 6.170.14.

## Steps

1. Installed the tools with `pip install hypothesis pytest`.
2. Ran the original program. It works for the sample inputs, but typing `5-9`
   crashes it with a `ValueError`.
3. Filled in `test_elevator_dispatch.py`. Each function gets a "no crash" test
   that feeds it random text, `None`, and random strings made from digits,
   `-`, `>`, `,`, spaces and the letters in "of". I added the last strategy
   because plain random text almost never contains `->` or ` of `, so the
   fuzzer would not get past `split()`. Each test runs 500 examples. There is
   also one test per function that checks valid input still gives the right
   answer, so a "fix" that returns `None` for everything would fail.
4. Ran the tests on the original code: 3 failed, 3 passed.
5. Fixed the program (see below) and ran it again.
6. Ran the tests on the fixed code: 6 passed.

## Bugs found

Hypothesis found these inputs and shrank each one to the smallest failing
case. I found the last four by hand while fixing, since the first errors hide
the later ones in each function.

| Function | Input | Error in original code |
|---|---|---|
| `parse_request` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| `parse_request` | `''` | `ValueError: not enough values to unpack` |
| `parse_request` | `'->'` | `ValueError: invalid literal for int()` |
| `total_travel` | `None` | `AttributeError` |
| `total_travel` | `''` | `ValueError: invalid literal for int()` |
| `load_percent` | `None` | `AttributeError` |
| `load_percent` | `''` | `ValueError: not enough values to unpack` |
| `load_percent` | `' of '` | `ValueError: invalid literal for int()` |
| `load_percent` | `'450 of 0'` | `ZeroDivisionError` |
| `load_percent` | `'-50 of 630'` | no crash, but returns `-8` |
| `parse_request` | `'1->2->3'` | `ValueError: too many values to unpack` |
| `total_travel` | `'1,,3'` | `ValueError: invalid literal for int()` |

## Fix

Each function now returns `None` for bad input instead of crashing:

- It checks that the input is a string.
- It checks that `split()` gave exactly two parts (`parse_request`,
  `load_percent`) and that the floor list is not empty (`total_travel`).
- A small helper `to_int()` strips spaces and returns `None` when the text is
  not a whole number, instead of letting `int()` raise.
- `load_percent` rejects a negative load and a capacity of 0 or less.

`main()` prints `invalid input` when a function returns `None`. Valid input
gives the same answers as before.

## Screenshots

| Step | File |
|---|---|
| 2. Original program, a normal run and a crash | `screenshots/1_buggy_program_PES2UG24CS042.png` |
| 4. Tests failing on the original code | `screenshots/2_tests_failing_PES2UG24CS042.png` |
| 4. Failing inputs Hypothesis found for `parse_request` | `screenshots/2b_failing_inputs_PES2UG24CS042.png` |
| 5. Fixed program, valid and invalid input | `screenshots/3_fixed_program_PES2UG24CS042.png` |
| 6. Tests passing on the fixed code | `screenshots/4_tests_passing_PES2UG24CS042.png` |

The full text output of every run is in `reports/`. All of it is collected in
`Lab7_FuzzTesting_PES2UG24CS042.pdf`.

## Running it

```bash
cd lab7
pip install hypothesis pytest
python elevator_dispatch.py
python -m pytest test_elevator_dispatch.py -v
```

## Files

| File | Contents |
|---|---|
| `elevator_dispatch.py` | Fixed program |
| `test_elevator_dispatch.py` | Hypothesis fuzz tests |
| `original/elevator_dispatch.py` | Program as given in the repo, before the fix |
| `Lab7_FuzzTesting_PES2UG24CS042.pdf` | Report with all screenshots |
| `reports/` | Text output of each run |
| `screenshots/` | Terminal screenshots for steps 2, 4, 5 and 6 |
