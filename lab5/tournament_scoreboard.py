"""Tournament scoreboard for Lab 5."""
import os
import re
import secrets
import shutil
import subprocess  # nosec B404
import tempfile

POINTS = {"win": 3, "draw": 1, "loss": 0}
REFEREE_PASSWORD = os.environ.get("REFEREE_PASSWORD")
teams = {}
matches = []


def add_team(team_name, players=None):
    """Add a team with empty stats."""
    if players is None:
        players = []
    teams[team_name] = {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                        "gf": 0, "ga": 0, "players": players}


def match_result(home_goals, away_goals):
    """Return who won the match."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Update stats of both teams after a match."""
    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded
    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, home_goals, away_goals))


def points(team_name):
    """Get points of a team."""
    stats = teams[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Get goal difference of a team."""
    return teams[team_name]["gf"] - teams[team_name]["ga"]


def league_table():
    """Sort teams by points and goal difference."""
    return sorted(teams, key=lambda t: (points(t), goal_difference(t)),
                  reverse=True)


def is_top_two(team_name):
    """Check if a team is in the top two."""
    return team_name in league_table()[:2]


def toss_coin():
    """Toss a coin."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Make a temp file for the table."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    return path


def publish_table(server):
    """Send table.json to the server."""
    if not re.fullmatch(r"[A-Za-z0-9._@-]+", server) or server[0] == "-":
        raise ValueError("invalid server name")
    scp = shutil.which("scp")
    if scp is None:
        raise FileNotFoundError("scp not found")
    subprocess.run([scp, "table.json", server + ":/var/www/"],  # nosec B603
                   check=True)


def main():
    """Run the demo."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(league_table(), 1):
        stats = teams[name]
        print(pos, name, stats["played"], stats["won"], stats["drawn"],
              stats["lost"], points(name))
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(matches))


if __name__ == "__main__":
    main()
