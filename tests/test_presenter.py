from src.rps_game.game import GameEngine, RoundSnapshot
from src.rps_game.presenter import format_match_label, format_round_banner, format_score, format_status


def test_presenter_formats_idle_state():
    game = GameEngine()

    assert format_score(game) == "Player 0 • 0 AI"
    assert format_match_label(game) == "Best of 3 • First to 2 wins"
    assert format_status(game) == "Choose Rock, Paper, or Scissors to start the first round."


def test_presenter_formats_round_banner_and_win_state():
    game = GameEngine()
    game.player_score = 2
    snapshot = RoundSnapshot(
        round_number=2,
        player_choice="rock",
        ai_choice="scissors",
        outcome="player",
        player_score=2,
        ai_score=0,
    )

    banner = format_round_banner(snapshot, game)

    assert "Round won" in banner
    assert "Match secured" in banner
    assert "You played 🪨 Rock" in banner


def test_presenter_formats_ai_match_win_state():
    game = GameEngine()
    game.ai_score = 2

    assert format_status(game) == "AI won the match. Hit New Match for a rematch."


def test_presenter_formats_tie_banner():
    game = GameEngine()
    snapshot = RoundSnapshot(
        round_number=1,
        player_choice="paper",
        ai_choice="paper",
        outcome="tie",
        player_score=0,
        ai_score=0,
    )

    banner = format_round_banner(snapshot, game)

    assert "Round tied" in banner
    assert "AI played 📄 Paper" in banner


def test_presenter_formats_ai_round_banner_without_match_end():
    game = GameEngine()
    game.ai_score = 1
    snapshot = RoundSnapshot(
        round_number=2,
        player_choice="scissors",
        ai_choice="rock",
        outcome="ai",
        player_score=0,
        ai_score=1,
    )

    banner = format_round_banner(snapshot, game)

    assert "Round lost" in banner
    assert "Match lost" not in banner


def test_presenter_formats_mid_match_status_after_history_exists():
    game = GameEngine(rng=lambda _moves: "scissors")
    game.play_round("rock")

    assert format_status(game) == "Next round is ready. Choose your move."
