# Lab 5: Static Code Analysis - Tournament Scoreboard

Software Engineering, PES University
Akash Singh, PES2UG24CS042, Section A

Assigned repo: github.com/SETAPESU26/L5_38_tournament_scoreboard

## About

The program is a league scoreboard. It registers teams, records match results,
keeps played, won, drawn, lost and goal stats, builds a points table sorted by
points and goal difference, and does a coin toss. The assigned version worked
but had quality, style and security problems. This lab finds them with Pylint,
Bandit and Flake8 and fixes them.

Tools used: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1, Python 3.12.3.

## Results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.75/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 violations | 0 violations |

The demo prints the same points table before and after the fixes.

Two of the findings were real bugs. The `players=[]` default was one list shared
by every team, so adding a player to one team added it to all of them. The
`os.system` call in `publishTable` built a shell command from its argument, which
allowed command injection.

## Commits

1. `lab5: add assigned tournament_scoreboard.py and before reports`
2. `lab5: fix Bandit security issues`
3. `lab5: fix Flake8 style issues`
4. `lab5: fix Pylint issues (score 4.75 -> 10.00)`

## Running it

```bash
cd lab5
python tournament_scoreboard.py
python -m pylint tournament_scoreboard.py
python -m bandit -r tournament_scoreboard.py
python -m flake8 tournament_scoreboard.py
```

## Files

| File | Contents |
|---|---|
| `tournament_scoreboard.py` | Corrected program |
| `issues.md` | Issue documentation table |
| `reflection.md` | Answers to the reflection questions |
| `reports/before/` | Pylint, Bandit and Flake8 reports on the assigned code |
| `reports/after/` | The same reports after the fixes |
