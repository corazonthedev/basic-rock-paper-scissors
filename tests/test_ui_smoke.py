import os

import pytest
import tkinter as tk

from src.rps_game.config import AppConfig
from src.rps_game.ui import RPSApp


@pytest.mark.skipif(os.environ.get("RPS_RUN_UI_TESTS") != "1", reason="UI smoke test disabled by default")
def test_ui_builds_and_can_reset():
    root = tk.Tk()
    root.withdraw()
    app = RPSApp(root, AppConfig())

    app.play("rock")
    app.reset_match()

    assert app.score_var.get() == "Player 0 • 0 AI"
    assert app.player_choice_var.get() == "—"
    assert all(not button.instate(["disabled"]) for button in app.move_buttons.values())
    root.destroy()


@pytest.mark.skipif(os.environ.get("RPS_RUN_UI_TESTS") != "1", reason="UI smoke test disabled by default")
def test_ui_disables_moves_after_match_is_over():
    root = tk.Tk()
    root.withdraw()
    app = RPSApp(root, AppConfig())
    app.game.rng = lambda _moves: "scissors"

    app.play("rock")
    app.play("rock")

    assert app.game.is_over is True
    assert all(button.instate(["disabled"]) for button in app.move_buttons.values())
    root.destroy()
