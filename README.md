# Rock Paper Scissors Deluxe

A cleaner, more structured remake of the original Tkinter rock-paper-scissors project.
It stays loyal to the classic desktop version, but adds a better layout, match flow, history,
config support, logging, and automated tests.

## What's improved

- Same core game loop: Rock vs Paper vs Scissors
- Polished desktop UI with a dark modern layout
- Best-of-3 and best-of-5 match modes
- Round history panel
- Quick rematch button and keyboard shortcuts
- Configurable window settings through `.env`
- Logging to `logs/rps.log`
- Unit tests for game logic, presenter logic, config loading, and optional UI smoke test

## Project structure

```text
.
├── main.py
├── rock-paper-scissors.py
├── src/
│   └── rps_game/
│       ├── config.py
│       ├── game.py
│       ├── presenter.py
│       └── ui.py
├── tests/
├── docs/
└── .github/workflows/
```

## Run locally

```bash
python main.py
```

Or keep using the original file name:

```bash
python rock-paper-scissors.py
```

## Optional config

Copy `.env.example` to `.env` and edit values if needed.

## Test commands

```bash
pytest -q
pytest --cov=src.rps_game.game --cov=src.rps_game.presenter --cov=src.rps_game.config --cov-report=term-missing
RPS_RUN_UI_TESTS=1 xvfb-run -a pytest tests/test_ui_smoke.py -q
```

## Design notes

- The game logic is separated from the UI so behavior can be tested safely.
- The original single-file script is preserved as a compatibility launcher.
- No external runtime dependency is required; Tkinter ships with Python.
