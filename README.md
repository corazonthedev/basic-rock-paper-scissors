# Rock Paper Scissors Deluxe

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/UI-Tkinter-5b6ee1)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)
![Architecture](https://img.shields.io/badge/Architecture-Modular-black)
![Status](https://img.shields.io/badge/Status-Production%20Ready-2ea44f)

A polished, modular, and fully testable desktop remake of the classic **Rock–Paper–Scissors** project.
It stays close to the original spirit, but upgrades the experience with a cleaner interface, better match flow,
more reliable code structure, and a repo presentation that actually feels worth shipping.

</div>

---

## Overview

This project started as a very small Tkinter game and was rebuilt into a cleaner desktop application without losing its original identity.

The goal was simple:

- keep the game familiar
- improve the UI/UX without overdesigning it
- separate logic from interface
- make the codebase maintainable
- make the repository feel like a serious project, not a quick script dump

The result is a lightweight but well-structured game project with a smoother match experience, reusable architecture,
and automated testing.

---

## Features

### Gameplay
- Classic **Rock / Paper / Scissors** core loop
- **Best-of-3** and **Best-of-5** match modes
- Round-by-round result tracking
- Live score updates
- Reset and rematch flow

### UX Improvements
- Cleaner dark-themed desktop UI
- Better visual hierarchy and spacing
- Readable match history panel
- Keyboard shortcut support
- Clear game-end state handling
- Buttons lock correctly when a match is over

### Engineering Improvements
- Game rules separated from UI logic
- Presenter layer for cleaner state handling
- Config support through `.env`
- Logging support
- Automated tests for core behavior
- Backward-compatible launcher for the original filename

---

## Screens at a Glance

The application keeps the original desktop feeling, but improves the interaction model:

- a stronger title and score section
- more deliberate spacing between actions
- a dedicated history area for round results
- clearer end-of-match feedback
- less clutter, more focus

This means the project still feels like the original game — just sharper, cleaner, and more intentional.

---

## Project Structure

```text
.
├── main.py                         # Main application entry point
├── rock-paper-scissors.py          # Compatibility launcher using the original filename
├── src/
│   └── rps_game/
│       ├── __init__.py
│       ├── config.py               # Environment/config loading
│       ├── game.py                 # Core game logic and rules
│       ├── presenter.py            # UI-facing state orchestration
│       └── ui.py                   # Tkinter interface layer
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_game.py
│   ├── test_presenter.py
│   └── test_ui_smoke.py
├── docs/
│   └── ADR.md                      # Architecture notes / design decisions
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

---

## Tech Stack

- **Python**
- **Tkinter** for the desktop UI
- **Pytest** for testing
- **python-dotenv** for environment configuration

No heavy runtime framework, no unnecessary complexity.
Just a small game project built with discipline.

---

## Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/your-username/rock-paper-scissors.git
cd rock-paper-scissors
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
python main.py
```

If you want to preserve the original execution style:

```bash
python rock-paper-scissors.py
```

---

## Configuration

You can customize parts of the app with environment variables.

Create a local config file:

```bash
cp .env.example .env
```

Then edit the values as needed.

---

## Testing

Run the full test suite:

```bash
pytest -q
```

Run coverage:

```bash
pytest --cov=src.rps_game.game \
       --cov=src.rps_game.presenter \
       --cov=src.rps_game.config \
       --cov-report=term-missing
```

Optional UI smoke test on headless Linux:

```bash
RPS_RUN_UI_TESTS=1 xvfb-run -a pytest tests/test_ui_smoke.py -q
```

---

## Quality Goals

This repo was updated with a few practical standards in mind:

- **clarity over cleverness**
- **small scope, high polish**
- **testable logic**
- **clean separation of concerns**
- **UI improvements that respect the original project**

---

## Why This Version Is Better

Compared to the original one-file implementation, this version is:

- easier to read
- easier to test
- easier to extend
- more stable in edge cases
- visually cleaner
- more professional to present on GitHub

It is still a simple game — but now it looks and behaves like a complete project.

---

## Roadmap

Potential next upgrades:

- sound effects and animations
- persistent score storage
- difficulty modes / smarter opponent behavior
- packaging to executable format
- richer accessibility improvements
- leaderboard or profile support

---

## Contributing

Contributions, improvements, and cleanup suggestions are welcome.

If you want to extend the project, start by reading:

- `CONTRIBUTING.md`
- `docs/ADR.md`

---

## License

This project currently does not define a dedicated license file.
Add one before public distribution if needed.

---

## Final Note

This repository is meant to show that even a very small game project can feel solid when the structure,
UX decisions, and documentation are treated seriously.

If the original version was a quick prototype, this version is the cleaned, shipped, portfolio-ready edition.
