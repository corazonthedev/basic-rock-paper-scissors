from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Sequence

MOVES = ("rock", "paper", "scissors")
WIN_MAP = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


@dataclass(frozen=True)
class RoundSnapshot:
    round_number: int
    player_choice: str
    ai_choice: str
    outcome: str
    player_score: int
    ai_score: int


@dataclass
class GameEngine:
    best_of: int = 3
    rng: Callable[[Sequence[str]], str] = random.choice
    player_score: int = 0
    ai_score: int = 0
    history: list[RoundSnapshot] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.best_of not in (3, 5):
            raise ValueError("best_of must be 3 or 5")

    @property
    def target_wins(self) -> int:
        return self.best_of // 2 + 1

    @property
    def is_over(self) -> bool:
        return self.player_score >= self.target_wins or self.ai_score >= self.target_wins

    @property
    def match_winner(self) -> str | None:
        if self.player_score >= self.target_wins:
            return "player"
        if self.ai_score >= self.target_wins:
            return "ai"
        return None

    @property
    def rounds_played(self) -> int:
        return len(self.history)

    def play_round(self, player_choice: str) -> RoundSnapshot:
        if self.is_over:
            raise RuntimeError("The match is already over. Reset to play again.")
        if player_choice not in MOVES:
            raise ValueError(f"Invalid move: {player_choice}")

        ai_choice = self.rng(MOVES)
        outcome = self._resolve_round(player_choice, ai_choice)
        snapshot = RoundSnapshot(
            round_number=self.rounds_played + 1,
            player_choice=player_choice,
            ai_choice=ai_choice,
            outcome=outcome,
            player_score=self.player_score,
            ai_score=self.ai_score,
        )
        self.history.append(snapshot)
        return snapshot

    def reset(self, best_of: int | None = None) -> None:
        if best_of is not None:
            if best_of not in (3, 5):
                raise ValueError("best_of must be 3 or 5")
            self.best_of = best_of
        self.player_score = 0
        self.ai_score = 0
        self.history.clear()

    def _resolve_round(self, player_choice: str, ai_choice: str) -> str:
        if player_choice == ai_choice:
            return "tie"
        if WIN_MAP[player_choice] == ai_choice:
            self.player_score += 1
            return "player"
        self.ai_score += 1
        return "ai"
