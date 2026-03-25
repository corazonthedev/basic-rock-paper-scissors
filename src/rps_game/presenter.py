from __future__ import annotations

from .game import GameEngine, RoundSnapshot

MOVE_LABELS = {
    "rock": "Rock",
    "paper": "Paper",
    "scissors": "Scissors",
}

ICON_LABELS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
}


def format_score(game: GameEngine) -> str:
    return f"Player {game.player_score} • {game.ai_score} AI"


def format_match_label(game: GameEngine) -> str:
    return f"Best of {game.best_of} • First to {game.target_wins} wins"


def format_status(game: GameEngine) -> str:
    if game.match_winner == "player":
        return "You won the match. Hit New Match to go again."
    if game.match_winner == "ai":
        return "AI won the match. Hit New Match for a rematch."
    if not game.history:
        return "Choose Rock, Paper, or Scissors to start the first round."
    return "Next round is ready. Choose your move."


def format_round_banner(snapshot: RoundSnapshot, game: GameEngine) -> str:
    if snapshot.outcome == "tie":
        lead = "Round tied"
    elif snapshot.outcome == "player":
        lead = "Round won"
    else:
        lead = "Round lost"

    player_move = f"{ICON_LABELS[snapshot.player_choice]} {MOVE_LABELS[snapshot.player_choice]}"
    ai_move = f"{ICON_LABELS[snapshot.ai_choice]} {MOVE_LABELS[snapshot.ai_choice]}"
    banner = f"{lead} • You played {player_move} • AI played {ai_move}"

    if game.match_winner == "player":
        return f"{banner} • Match secured"
    if game.match_winner == "ai":
        return f"{banner} • Match lost"
    return banner
