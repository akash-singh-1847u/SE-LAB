# Lab 4: VibeCoding - Meteor Dodge

Software Engineering, PES University
Akash Singh, PES2UG24CS042, Section A

Repository (all labs): https://github.com/akash-singh-1847u/SE-project

## About

Meteor Dodge is a space survival game built with Pygame. The assigned repo
(github.com/SETAPESU26/38-meteor-dodge) ships the game with one deliberate bug
and four tasks left to complete. The work here fixes the bug and implements all
four tasks, using an LLM as a pair-programming partner.

Controls: SPACE launches the ship from the title screen and fires lasers during
flight. WASD or the arrow keys steer. SPACE also restarts after a game over.

## What was fixed and added

Task 1, input-state bug and lasers. On the title screen SPACE launched the ship,
but during flight it did nothing because the handler only re-set the started flag.
SPACE now fires an upward laser while flying, and lasers destroy the meteors they
hit. The laser lives in a new module, game/laser.py.

Task 2, meteor splitting. Destroying a large meteor (radius 20 or more) now breaks
it into two or three smaller fragments that spread outwards. Small meteors dissolve
with nothing left behind. The Meteor constructor was extended to build fragments at
a given position, radius and velocity, and a split method returns the children.

Task 3, shield power-up orbs. A drifting energy orb spawns every few seconds and
falls down the screen. Flying into it grants a temporary shield, shown as a ring
around the ship, that absorbs one meteor hit instead of ending the run. The orb
lives in a new module, game/orb.py.

Task 4, survival multiplier. Score used to tick up at a flat rate. It now gains a
multiplier that rises by one for every ten seconds survived without taking a hit,
and drops back to one when a hit lands. Score and multiplier show in the HUD.

## Files changed

- game/game_engine.py, updated to wire in lasers, splitting, orbs and the multiplier
- game/meteor.py, updated for fragment creation and splitting
- game/ship.py, updated to draw the shield ring
- game/laser.py, new
- game/orb.py, new
- main.py and requirements.txt, unchanged

## Running it

```bash
cd meteor-dodge
pip install -r requirements.txt
python main.py
```

Python 3.10 or newer is required.

## Folder contents

- meteor-dodge/, the updated game code
- screenshots/, before and after gameplay screenshots
- Chat_History_PES2UG24CS042.pdf, the prompts used and the change each one produced

## Screenshots

The before screenshot shows the original state, a bare Time counter with no lasers
or power-ups. The after screenshots show the shield ring and shield timer, the
power-up orb, the survival multiplier climbing in the HUD, and the game-over screen
reporting the final score.
