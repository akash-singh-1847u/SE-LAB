# Software Engineering Lab Work

**Name:** Akash Singh
**SRN:** PES2UG24CS042, Section A
**Course:** Software Engineering, Dept. of CSE, PES University
**Problem Statement:** #38, Dropshipping Inventory & Order Orchestrator (DIOO)
**Domain:** Retail, E-Commerce & Finance

---

## Overview

Labs 1 to 3 follow one project, the **Dropshipping Inventory & Order Orchestrator (DIOO)**, through the software lifecycle:

```
Lab 1: Requirements & Use Cases  →  Lab 2: Agile Backlog & Sprints  →  Lab 3: Architecture & Components
```

DIOO is an e-commerce backend for a dropshipping store. It receives order webhooks from the storefront (Shopify / WooCommerce), checks supplier stock in real time, splits an order that has items from more than one supplier, sends a purchase order to each supplier, and keeps tracking numbers up to date.

Lab 4 is a separate hands-on coding lab. It fixes and extends a Pygame game with an LLM as a pair-programming partner.

Lab 5 is also separate. It uses Pylint, Bandit and Flake8 to find and fix quality, style and security issues in a small Python program.

Lab 6 is also separate. It uses coverage and pytest to measure line and branch coverage of a small Python module and writes tests until both reach 100%.

| Lab | Topic | Main deliverable |
|---|---|---|
| [Lab 1](lab1/) | Requirements Engineering & UML Use-Case Modelling | Requirements table, use-case diagram, use-case flow |
| [Lab 2](lab2/) | Agile Backlog Creation & Sprint Simulation in Jira | Epics, user stories, two sprints, burndown charts |
| [Lab 3](lab3/) | Component Modelling & Architectural Pattern Selection | UML component diagram, architecture justification |
| [Lab 4](lab4/) | VibeCoding: Meteor Dodge | Fixed and extended Pygame game, LLM chat history |
| [Lab 5](lab5/) | Static Code Analysis: Tournament Scoreboard | Fixed program, issue table, reflection, before/after reports |
| [Lab 6](lab6/) | Code and Branch Coverage: Elevator Dispatch | Code and branch coverage test files, coverage screenshots |

---

## Lab 1: Requirements Engineering and UML Use-Case Modelling

**Objective:** Gather and write down the requirements for DIOO, identify the actors, and model the system's behaviour as a UML use-case diagram with `«include»` and `«extend»` relationships.

**What was done**
- Identified four actors: **E-Store Owner**, **Supplier Partner**, **Storefront Platform**, and **Courier Service**.
- Wrote **5 functional requirements** (FR-001 to FR-005): order webhook intake, multi-supplier order splitting, out-of-stock hold and alert, tracking write-back, and an owner dashboard.
- Wrote **2 non-functional requirements**: NFR-001 (reply HTTP 200 within 200 ms, only after an HMAC check) and NFR-002 (retry a failed supplier call 3 times and never drop an order).
- Defined **8 use cases** (UC-01 to UC-08) and drew the use-case diagram:
  - UC-01 Process Storefront Order `«include»` Check Supplier Stock and Send Supplier Purchase Order
  - Split Multi-Vendor Order `«extend»` UC-01 (only when the order has more than one supplier)
  - Flag Out of Stock Item `«extend»` Check Supplier Stock (only when stock is zero)
- Wrote a one-page flow for UC-01 with preconditions, postconditions, the main success scenario, and one alternate flow.

**Files**
| File | Contents |
|---|---|
| [`lab1/PES2UG24CS042_SE_LAB1 1.pdf`](lab1/PES2UG24CS042_SE_LAB1%201.pdf) | Submission: requirements table, use-case diagram, UC-01 flow |
| [`lab1/README.md`](lab1/README.md) | Detailed notes: actors, FR/NFR table, use-case list, relationships |

---

## Lab 2: Agile Backlog Creation and Sprint Simulation in Jira

**Objective:** Turn the Lab 1 requirements into an Agile product backlog in Jira. Group the work into Epics, write prioritised and estimated User Stories, plan and run sprints, and reflect on the results using burndown charts.

**What was done**
- Grouped the Lab 1 requirements into **4 Epics**:

  | Epic | Requirements covered | Stories | Points |
  |---|---|---|---|
  | Order Intake and Processing | FR-001, NFR-001 | 2 | 8 |
  | Supplier Stock and Purchase Orders | FR-001, FR-002 | 3 | 21 |
  | Exception and Stock Handling | FR-003, NFR-002 | 3 | 11 |
  | Tracking and Owner Dashboard | FR-004, FR-005 | 2 | 13 |

- Wrote **10 User Stories** in *As a / I want / So that* format, each with a priority and a Fibonacci story-point estimate.
- Ran **two one-week sprints**. Sprint 1 held all High-priority stories (34 points, the core order path). Sprint 2 held the Medium-priority stories (19 points: alerts, retries, tracking, dashboard). Total velocity was **53 points**.
- Answered the reflection questions on estimation accuracy, backlog prioritisation, how the sprints matched the plan, and what the burndown charts showed.

**Files**
| File | Contents |
|---|---|
| [`lab2/PES2UG24CS042_SE_LAB_2.pdf`](lab2/PES2UG24CS042_SE_LAB_2.pdf) | Submission: epic breakdown, reflection answers, screenshots |
| [`lab2/pics/`](lab2/pics/) | Jira screenshots: backlog with epics and stories, active sprint board, burndown charts for Sprint 1 and Sprint 2 |

---

## Lab 3: Component Modelling and Architectural Pattern Selection

**Objective:** Choose a suitable architectural pattern for DIOO, justify it against the Lab 1 non-functional requirements, and model the system as a UML component diagram with provided/required interfaces, ports, and external dependencies.

**What was done**
- Chose a **Microservices** architecture. NFR-001 needs a sub-200 ms webhook reply, while NFR-002 retries supplier calls on a 30-second clock. Those timings are very different, so the webhook edge and the supplier retry loop run as separate services.
- Modelled **6 components**: Storefront Gateway, Order Manager, Supplier Integration, Inventory and SKU Map, Payment Service, and Owner Dashboard and Alerts. Each one is traced back to the Lab 1 requirements it covers.
- Defined **10 interfaces** (for example `IWebhookIntake`, `IStockCheck`, `IPurchaseOrder`, `IPaymentOps`), showing who provides and who requires each one and over what transport.
- Placed the external systems (Storefront Platform, Supplier Partner Systems, Courier Service, Payment Gateway) outside the system boundary, linked by `<<use>>` dependencies.
- Used standard UML notation: ball (provided), socket (required), assembly connectors, and ports.

**Files**
| File | Contents |
|---|---|
| [`lab3/SE_Lab3_PES2UG24CS042.pdf`](lab3/SE_Lab3_PES2UG24CS042.pdf) | Submission: component diagram and written architecture justification |
| [`lab3/README.md`](lab3/README.md) | Detailed notes: components, interfaces, external systems, notation |

---

## Lab 4: VibeCoding (Meteor Dodge)

**Objective:** Use an LLM (ChatGPT / Claude) as a debugging and pair-programming partner to analyse an existing codebase, fix a deliberate bug, and add new features. Every AI suggestion was reviewed critically before it went in.

**About the project:** Meteor Dodge is a Pygame space-survival game (assigned repo: `SETAPESU26/38-meteor-dodge`). It shipped with one deliberate bug and several unfinished features.

**What was done**
| Task | Change |
|---|---|
| 1. Input-state bug and lasers | SPACE launched the ship but did nothing during flight. It now fires lasers that destroy meteors (new `game/laser.py`). |
| 2. Meteor splitting | Large meteors (radius ≥ 20) break into 2 or 3 fragments that spread outwards. Small ones dissolve. |
| 3. Shield power-up orbs | A falling energy orb gives a temporary shield that absorbs one hit, drawn as a ring around the ship (new `game/orb.py`). |
| 4. Survival multiplier | The score multiplier goes up by 1 for every 10 s survived without a hit and resets to 1 when the ship is hit. Shown in the HUD. |

**Running the game** (Python 3.10+)
```bash
cd lab4/meteor-dodge
pip install -r requirements.txt
python main.py
```
Controls: **SPACE** to launch, fire, and restart. **WASD / arrow keys** to steer.

**Files**
| File | Contents |
|---|---|
| [`lab4/meteor-dodge/`](lab4/meteor-dodge/) | Updated game source (`main.py`, `game/` package) |
| [`lab4/screenshots/`](lab4/screenshots/) | Before and after gameplay screenshots (shield, power-up orb, multiplier, game over) |
| [`lab4/Chat_History_PES2UG24CS042.pdf`](lab4/Chat_History_PES2UG24CS042.pdf) | Full LLM chat history: each prompt and the change it led to |
| [`lab4/README.md`](lab4/README.md) | Detailed write-up of the fixes and features |

---

## Lab 5: Static Code Analysis (Tournament Scoreboard)

**Objective:** Use Pylint, Bandit and Flake8 to find quality, style and security issues in an assigned Python program, fix them, and verify the fixes by rerunning the tools.

**About the project:** A league scoreboard script (assigned repo: `SETAPESU26/L5_38_tournament_scoreboard`) that records match results and builds a points table.

**What was done**
| Tool | Before | After |
|---|---|---|
| Pylint | 4.75/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 violations | 0 violations |

- Replaced a shell `os.system` call (command injection) with `subprocess.run` on a validated argument list, and the deprecated `tempfile.mktemp` with `mkstemp`.
- Fixed a mutable default argument (`players=[]`) that made every team share one player list.
- Renamed functions to snake_case, added docstrings and fixed the PEP 8 spacing issues.
- One commit per tool: Bandit, Flake8, Pylint.

**Files**
| File | Contents |
|---|---|
| [`lab5/tournament_scoreboard.py`](lab5/tournament_scoreboard.py) | Corrected program |
| [`lab5/issues.md`](lab5/issues.md) | Issue documentation table |
| [`lab5/reflection.md`](lab5/reflection.md) | Reflection answers |
| [`lab5/reports/`](lab5/reports/) | Pylint, Bandit and Flake8 reports, before and after |

---

## Lab 6: Code and Branch Coverage (Elevator Dispatch)

**Objective:** Use Python's coverage library with pytest to measure line and branch coverage, find untested paths, and write tests until both reach at least 90%.

**About the project:** A small elevator module (assigned repo: `SETAPESU26/L6_L7_38_elevator_dispatch`) that picks a car's travel direction, decides the door action and chooses which car answers a call.

**What was done**
| Test file | Tests | Line coverage | Branch coverage |
|---|---|---|---|
| Starter tests | 2 | 31% | 25% |
| Code coverage tests | 14 | 100% | 99% |
| Branch coverage tests | 28 | 100% | 100% |

- The code coverage tests run every line but miss one branch (`40->36` in `pick_elevator`): a later car that is not closer than the current best. Line coverage cannot show this because the False case has no line of its own.
- The branch coverage tests add that case plus edge cases: equal distances, the busy-car penalty, an empty car list, the 630 kg overload boundary, door-rule precedence and a request on the current floor.
- One commit per test file: code coverage, then branch coverage.

**Files**
| File | Contents |
|---|---|
| [`lab6/elevator_dispatch.py`](lab6/elevator_dispatch.py) | Module under test |
| [`lab6/CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py`](lab6/CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py) | Tests for line coverage |
| [`lab6/BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py`](lab6/BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py) | Tests for branch coverage |
| [`lab6/screenshots/`](lab6/screenshots/) | Terminal output of the coverage runs |
| [`lab6/reports/`](lab6/reports/) | Text output of every coverage run, including the starter tests |
| [`lab6/README.md`](lab6/README.md) | Detailed write-up |

---

## Repository Structure

```
SE/
├── README.md
├── lab1/   Requirements & use-case modelling
│   ├── PES2UG24CS042_SE_LAB1 1.pdf
│   └── README.md
├── lab2/   Agile backlog & sprint simulation (Jira)
│   ├── PES2UG24CS042_SE_LAB_2.pdf
│   └── pics/
├── lab3/   Component modelling & architecture
│   ├── SE_Lab3_PES2UG24CS042.pdf
│   └── README.md
├── lab4/   VibeCoding: Meteor Dodge
│   ├── Chat_History_PES2UG24CS042.pdf
│   ├── README.md
│   ├── meteor-dodge/
│   └── screenshots/
├── lab5/   Static code analysis: Tournament Scoreboard
│   ├── tournament_scoreboard.py
│   ├── issues.md
│   ├── reflection.md
│   ├── README.md
│   └── reports/   before/ and after/
└── lab6/   Code and branch coverage: Elevator Dispatch
    ├── elevator_dispatch.py
    ├── test_elevator_dispatch.py
    ├── CodeCoverageTest_PES2UG24CS042_elevator_dispatch.py
    ├── BranchCoverageTest_PES2UG24CS042_elevator_dispatch.py
    ├── README.md
    ├── reports/
    └── screenshots/
```
