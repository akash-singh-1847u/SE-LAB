# Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The Flake8 issues were the easiest. Each one pointed to an exact line and column and needed a one-character change, such as removing the space in `"win" : 3` or adding a space in `2,1`. The Pylint naming and docstring messages were also simple, though renaming every camelCase function meant updating each call site, and missing one would have broken the program at runtime instead of at analysis time.

The hardest was Bandit B605, the `os.system` call in `publishTable`. Swapping it for `subprocess.run` removed the High finding, but Bandit then reported B404 (importing subprocess) and B603 (running a subprocess). I also realised that an argument list stops shell injection but not option injection: a server value starting with `-`, such as `-oProxyCommand=...`, would still be read by scp as an option. So I added validation of the server name and resolved `scp` to a full path with `shutil.which`, and only then marked the two remaining Low findings with `# nosec B404` and `# nosec B603`, with a comment explaining why each is safe.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. Bandit B311 flagged `random.choice(["Heads", "Tails"])` in `tossCoin`. A coin toss in a scoreboard demo is not a security decision, so a predictable generator does no harm there. I still switched to `secrets.choice` because it costs nothing and keeps the report clean.

B404 and B603 on the fixed `subprocess.run` call are also false positives once the input is validated and no shell is used. Bandit cannot see that the validation exists, which is why I suppressed them by ID instead of with a bare `# nosec`.

In the other direction, the tools missed something. Nothing flagged the top-level `main()` call that ran the demo on import. I found that one while writing a quick test for the mutable default bug.

## 3. How would you integrate static analysis tools into your actual software development workflow?

Locally, I would add a pre-commit hook that runs Flake8 and Bandit on staged files, since both finish in under a second on a file this size, and run Pylint from the editor so warnings show while typing. In CI, a GitHub Actions job would run all three tools on every push and pull request and fail the build on any Bandit finding of medium severity or above, any Flake8 violation, or a Pylint score below a set threshold such as 9.5. Keeping the settings in a shared config file (`.pylintrc`, `setup.cfg`) means every developer and the CI job check the same rules.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The Pylint score went from 4.75/10 to 10.00/10, Bandit went from 4 issues (1 High, 1 Medium, 2 Low) to 0, and Flake8 went from 4 violations to 0. Two fixes changed behaviour for the better. With the old `players=[]` default, appending a player to one team added it to all four, and after the fix each team has its own list. The old `isTopTwo` raised `IndexError` with fewer than two teams, and the new version returns the right answer for any table size. The `publishTable` helper can no longer be used to run arbitrary shell commands, and `table_file_path` no longer has a race between choosing a name and creating the file. Through all of this the demo prints the same points table as the original.
