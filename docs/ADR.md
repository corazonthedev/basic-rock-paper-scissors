# Architecture Decision Record

| # | Decision | Alternatives | Reason |
|---|----------|--------------|--------|
| 1 | Keep Tkinter for the desktop UI | Rewrite with PySide or web stack | Staying close to the original repo keeps the spirit intact and avoids runtime dependencies. |
| 2 | Move rules into a standalone `GameEngine` | Keep everything inside the UI file | Testability and maintainability improve immediately. |
| 3 | Keep `rock-paper-scissors.py` as a compatibility launcher | Remove the original entry file | Existing users can still run the project the old way. |
