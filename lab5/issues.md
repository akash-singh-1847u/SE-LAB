# Issues found and fixed

Tournament scoreboard (`tournament_scoreboard.py`), Lab 5 Static Code Analysis.
Line numbers refer to the original file. Rows are ordered by severity, high and medium first.

Tool versions: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1, Python 3.12.3.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 71 | `os.system("scp table.json " + server + ":/var/www/")` builds a shell command from the `server` argument. A value like `x; rm -rf ~` would run a second command. | Replaced with `subprocess.run([...], check=True)` on an argument list with no shell. `scp` is resolved with `shutil.which`, and `server` must match `[A-Za-z0-9._@-]+` and must not start with `-`, so it cannot be read as an scp option. |
| Insecure temp file (Bandit B306, Medium) | Security | 66 | `tempfile.mktemp()` only returns a name. Another process can create a file with that name before we open it (race condition, CWE-377). The function is deprecated. | Replaced with `tempfile.mkstemp(suffix=".json")`, which creates the file atomically, then closed the descriptor and returned the path. |
| Mutable default argument (Pylint W0102) | Bug | 11 | `players=[]` is created once, so every team that is added without a list shares the same list. Appending a player to Royal Strikers also added it to the other three teams. | Default changed to `None`, and a new list is created inside `add_team` when none is given. |
| Hardcoded password (Bandit B105, Low) | Security | 6 | `REFEREE_PASSWORD = "referee-demo"` puts a credential in source code, where it ends up in Git history. | Read from the environment with `os.environ.get("REFEREE_PASSWORD")`. |
| Non-cryptographic random (Bandit B311, Low) | Security | 61 | `random.choice` is predictable if the seed or state is known. | Replaced with `secrets.choice`. The coin toss works the same way. |
| Index error in top-two check (Pylint R1714) | Bug / Refactor | 58 | `teamName == table[0] or teamName == table[1]` raises `IndexError` when fewer than two teams are registered. | Rewritten as `team_name in league_table()[:2]`, which works for any table size. |
| Unnecessary elif/else after return (Pylint R1705) | Refactor | 17-22 | Each branch returns, so `elif` and `else` add nesting without changing behaviour. | Used plain `if` statements and a final `return "draw"`. |
| Non snake_case names (Pylint C0103) | Convention | 11-69 | Functions and arguments used camelCase (`addTeam`, `teamName`, `homeGoals`). | Renamed to snake_case (`add_team`, `team_name`, `home_goals`) and updated every call. |
| Missing docstrings (Pylint C0114, C0116) | Convention | 1, 11-74 | No module docstring and no function docstrings. | Added a module docstring and a one-line docstring to every function. |
| Whitespace before colon (Flake8 E203) | Style | 5 | `{"win" : 3, ...}` | Removed the space: `{"win": 3, ...}`. |
| Missing blank line (Flake8 E302) | Style | 60 | Only one blank line before `def tossCoin`. | Added a second blank line. |
| Missing whitespace after comma (Flake8 E231) | Style | 79 | `2,1` in a `recordMatch` call. | Changed to `2, 1`. |
| Inline comment spacing (Flake8 E261) | Style | 87 | One space before `# one row per team`. | Changed to two spaces. |
| Module-level `main()` call | Robustness | 92 | `main()` ran on import, so importing the file for testing printed the demo and filled the global tables. Not flagged by the tools. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.75/10, 32 messages | 10.00/10, 0 messages |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 violations | 0 violations |

The program prints the same points table as before. Only the coin toss result varies between runs, as it did originally.

## Commits

1. `lab5: fix Bandit security issues`
2. `lab5: fix Flake8 style issues`
3. `lab5: fix Pylint issues (score 4.75 -> 10.00)`

Reports from before and after the fixes are in `reports/before/` and `reports/after/`.
