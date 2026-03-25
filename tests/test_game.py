import pytest

from src.rps_game.game import GameEngine


@pytest.mark.parametrize(
    ("player", "ai", "expected_outcome", "player_score", "ai_score"),
    [
        ("rock", "scissors", "player", 1, 0),
        ("paper", "rock", "player", 1, 0),
        ("scissors", "paper", "player", 1, 0),
        ("rock", "paper", "ai", 0, 1),
        ("paper", "scissors", "ai", 0, 1),
        ("scissors", "rock", "ai", 0, 1),
        ("rock", "rock", "tie", 0, 0),
    ],
)
def test_round_resolution(player, ai, expected_outcome, player_score, ai_score):
    game = GameEngine(rng=lambda _moves: ai)

    snapshot = game.play_round(player)

    assert snapshot.outcome == expected_outcome
    assert snapshot.player_score == player_score
    assert snapshot.ai_score == ai_score
    assert game.player_score == player_score
    assert game.ai_score == ai_score


def test_best_of_five_requires_three_wins():
    choices = iter(["scissors", "scissors", "rock"])
    game = GameEngine(best_of=5, rng=lambda _moves: next(choices))

    game.play_round("rock")
    game.play_round("rock")
    final_round = game.play_round("paper")

    assert game.is_over is True
    assert game.match_winner == "player"
    assert final_round.player_score == 3
    assert game.target_wins == 3


def test_cannot_play_after_match_is_over():
    choices = iter(["scissors", "scissors"])
    game = GameEngine(rng=lambda _moves: next(choices))

    game.play_round("rock")
    game.play_round("rock")

    with pytest.raises(RuntimeError):
        game.play_round("rock")


def test_reset_clears_scores_and_history_and_can_change_mode():
    game = GameEngine(rng=lambda _moves: "scissors")
    game.play_round("rock")

    game.reset(best_of=5)

    assert game.player_score == 0
    assert game.ai_score == 0
    assert game.history == []
    assert game.best_of == 5
    assert game.target_wins == 3


def test_invalid_move_raises_value_error():
    game = GameEngine(rng=lambda _moves: "rock")

    with pytest.raises(ValueError):
        game.play_round("lizard")


def test_invalid_match_mode_raises_value_error():
    with pytest.raises(ValueError):
        GameEngine(best_of=7)
