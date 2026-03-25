from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk

from .config import AppConfig
from .game import GameEngine, RoundSnapshot
from .presenter import format_match_label, format_round_banner, format_score, format_status

PALETTE = {
    "bg": "#0f172a",
    "panel": "#111827",
    "card": "#1f2937",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "accent": "#38bdf8",
    "accent_alt": "#22c55e",
    "danger": "#fb7185",
}

MOVE_META = {
    "rock": {"label": "Rock", "icon": "🪨", "shortcut": "R"},
    "paper": {"label": "Paper", "icon": "📄", "shortcut": "P"},
    "scissors": {"label": "Scissors", "icon": "✂️", "shortcut": "S"},
}


class RPSApp:
    def __init__(self, root: tk.Tk, config: AppConfig) -> None:
        self.root = root
        self.config = config
        self.logger = self._configure_logging()
        self.game = GameEngine(best_of=config.default_best_of)
        self.best_of_var = tk.IntVar(value=self.game.best_of)
        self.banner_var = tk.StringVar(value="First to two wins. Ready when you are.")
        self.score_var = tk.StringVar(value=format_score(self.game))
        self.status_var = tk.StringVar(value=format_status(self.game))
        self.match_var = tk.StringVar(value=format_match_label(self.game))
        self.player_choice_var = tk.StringVar(value="—")
        self.ai_choice_var = tk.StringVar(value="—")
        self.move_buttons: dict[str, ttk.Button] = {}

        self._setup_root()
        self._configure_styles()
        self._build_layout()
        self._bind_shortcuts()
        self.logger.info("Application started with best_of=%s", self.game.best_of)

    def _configure_logging(self) -> logging.Logger:
        logger = logging.getLogger("rps_game")
        if logger.handlers:
            return logger

        self.config.log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.setLevel(self.config.log_level.upper())
        handler = logging.FileHandler(self.config.log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
        return logger

    def _setup_root(self) -> None:
        self.root.title(self.config.app_title)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        self.root.minsize(900, 620)
        self.root.configure(bg=PALETTE["bg"])

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background=PALETTE["bg"])
        style.configure("Panel.TFrame", background=PALETTE["panel"])
        style.configure("Card.TFrame", background=PALETTE["card"])
        style.configure(
            "Title.TLabel",
            background=PALETTE["bg"],
            foreground=PALETTE["text"],
            font=("Segoe UI", 26, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=PALETTE["bg"],
            foreground=PALETTE["muted"],
            font=("Segoe UI", 11),
        )
        style.configure(
            "CardTitle.TLabel",
            background=PALETTE["card"],
            foreground=PALETTE["muted"],
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Value.TLabel",
            background=PALETTE["card"],
            foreground=PALETTE["text"],
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background=PALETTE["panel"],
            foreground=PALETTE["text"],
            font=("Segoe UI", 11),
        )
        style.configure(
            "Small.TLabel",
            background=PALETTE["card"],
            foreground=PALETTE["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 12),
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("!disabled", PALETTE["accent"]), ("pressed", "#0891b2")],
            foreground=[("!disabled", PALETTE["panel"])],
        )
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 10),
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("!disabled", PALETTE["accent_alt"]), ("pressed", "#16a34a")],
            foreground=[("!disabled", PALETTE["panel"])],
        )
        style.configure(
            "Banner.TLabel",
            background=PALETTE["panel"],
            foreground=PALETTE["text"],
            font=("Segoe UI", 12, "bold"),
            padding=(18, 16),
        )
        style.configure(
            "History.Treeview",
            background=PALETTE["card"],
            fieldbackground=PALETTE["card"],
            foreground=PALETTE["text"],
            rowheight=32,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "History.Treeview.Heading",
            background=PALETTE["panel"],
            foreground=PALETTE["muted"],
            font=("Segoe UI", 10, "bold"),
        )

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, style="App.TFrame", padding=24)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(1, weight=1)

        hero = ttk.Frame(container, style="App.TFrame")
        hero.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 18))

        ttk.Label(hero, text="Rock • Paper • Scissors", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            hero,
            text="Same classic rules, rebuilt with a cleaner layout, visible match flow, and quick rematch controls.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(6, 0))

        left_panel = ttk.Frame(container, style="Panel.TFrame", padding=18)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        left_panel.columnconfigure(0, weight=1)

        self.banner = ttk.Label(left_panel, textvariable=self.banner_var, style="Banner.TLabel")
        self.banner.grid(row=0, column=0, sticky="ew")

        stats = ttk.Frame(left_panel, style="Panel.TFrame")
        stats.grid(row=1, column=0, sticky="ew", pady=(18, 14))
        for index in range(3):
            stats.columnconfigure(index, weight=1)

        self._make_stat_card(stats, 0, "Score", self.score_var, "Live match score")
        self._make_stat_card(stats, 1, "Mode", self.match_var, "Adjust at the next match")
        self._make_stat_card(stats, 2, "Status", self.status_var, "Keyboard: R / P / S / N")

        choices = ttk.Frame(left_panel, style="Panel.TFrame")
        choices.grid(row=2, column=0, sticky="ew", pady=(8, 14))
        for index in range(3):
            choices.columnconfigure(index, weight=1)

        for column, move in enumerate(("rock", "paper", "scissors")):
            meta = MOVE_META[move]
            button = ttk.Button(
                choices,
                text=f"{meta['icon']}  {meta['label']}\n[{meta['shortcut']}]",
                style="Primary.TButton",
                command=lambda selected=move: self.play(selected),
            )
            button.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0), ipady=10)
            self.move_buttons[move] = button

        lower = ttk.Frame(left_panel, style="Panel.TFrame")
        lower.grid(row=3, column=0, sticky="nsew")
        lower.columnconfigure(0, weight=1)
        lower.columnconfigure(1, weight=1)
        left_panel.rowconfigure(3, weight=1)

        player_card = ttk.Frame(lower, style="Card.TFrame", padding=18)
        player_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(player_card, text="Your last move", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(player_card, textvariable=self.player_choice_var, style="Value.TLabel").pack(anchor="w", pady=(12, 8))
        ttk.Label(player_card, text="Pick a move to update this panel.", style="Small.TLabel").pack(anchor="w")

        ai_card = ttk.Frame(lower, style="Card.TFrame", padding=18)
        ai_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Label(ai_card, text="AI last move", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(ai_card, textvariable=self.ai_choice_var, style="Value.TLabel").pack(anchor="w", pady=(12, 8))
        ttk.Label(ai_card, text="The AI choice appears after each round.", style="Small.TLabel").pack(anchor="w")

        right_panel = ttk.Frame(container, style="Panel.TFrame", padding=18)
        right_panel.grid(row=1, column=1, sticky="nsew")
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(2, weight=1)

        controls = ttk.Frame(right_panel, style="Panel.TFrame")
        controls.grid(row=0, column=0, sticky="ew")
        ttk.Label(controls, text="New match settings", style="Body.TLabel").pack(anchor="w")
        mode_wrap = ttk.Frame(controls, style="Panel.TFrame")
        mode_wrap.pack(anchor="w", pady=(8, 14), fill="x")
        ttk.Radiobutton(
            mode_wrap,
            text="Best of 3",
            variable=self.best_of_var,
            value=3,
            command=self.preview_mode,
        ).pack(anchor="w")
        ttk.Radiobutton(
            mode_wrap,
            text="Best of 5",
            variable=self.best_of_var,
            value=5,
            command=self.preview_mode,
        ).pack(anchor="w", pady=(4, 0))
        ttk.Button(right_panel, text="New Match [N]", style="Secondary.TButton", command=self.reset_match).grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 18),
        )

        history_wrap = ttk.Frame(right_panel, style="Card.TFrame", padding=16)
        history_wrap.grid(row=2, column=0, sticky="nsew")
        history_wrap.columnconfigure(0, weight=1)
        history_wrap.rowconfigure(1, weight=1)
        ttk.Label(history_wrap, text="Round history", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.history = ttk.Treeview(
            history_wrap,
            columns=("round", "player", "ai", "outcome"),
            show="headings",
            style="History.Treeview",
        )
        for column, title, width in (
            ("round", "Round", 70),
            ("player", "You", 110),
            ("ai", "AI", 110),
            ("outcome", "Outcome", 150),
        ):
            self.history.heading(column, text=title)
            self.history.column(column, width=width, anchor="center")
        self.history.grid(row=1, column=0, sticky="nsew")

    def _make_stat_card(self, parent: ttk.Frame, column: int, title: str, value: tk.StringVar, helper: str) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 8, 0))
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=value, style="Value.TLabel", wraplength=220).pack(anchor="w", pady=(12, 8))
        ttk.Label(card, text=helper, style="Small.TLabel", wraplength=220).pack(anchor="w")

    def _bind_shortcuts(self) -> None:
        self.root.bind("r", lambda _event: self.play("rock"))
        self.root.bind("p", lambda _event: self.play("paper"))
        self.root.bind("s", lambda _event: self.play("scissors"))
        self.root.bind("n", lambda _event: self.reset_match())

    def play(self, move: str) -> None:
        if self.game.is_over:
            self._set_move_buttons_enabled(False)
            self.banner_var.set("Match finished. Start a new match to continue.")
            self.status_var.set(format_status(self.game))
            return

        snapshot = self.game.play_round(move)
        self._apply_snapshot(snapshot)
        self.logger.info(
            "Round %s | player=%s ai=%s outcome=%s score=%s-%s",
            snapshot.round_number,
            snapshot.player_choice,
            snapshot.ai_choice,
            snapshot.outcome,
            snapshot.player_score,
            snapshot.ai_score,
        )

    def _apply_snapshot(self, snapshot: RoundSnapshot) -> None:
        self.banner_var.set(format_round_banner(snapshot, self.game))
        self.score_var.set(format_score(self.game))
        self.status_var.set(format_status(self.game))
        self.match_var.set(format_match_label(self.game))
        self.player_choice_var.set(f"{MOVE_META[snapshot.player_choice]['icon']} {MOVE_META[snapshot.player_choice]['label']}")
        self.ai_choice_var.set(f"{MOVE_META[snapshot.ai_choice]['icon']} {MOVE_META[snapshot.ai_choice]['label']}")
        outcome_label = {
            "player": "You won",
            "ai": "AI won",
            "tie": "Tie",
        }[snapshot.outcome]
        self.history.insert(
            "",
            0,
            values=(
                snapshot.round_number,
                f"{MOVE_META[snapshot.player_choice]['icon']} {MOVE_META[snapshot.player_choice]['label']}",
                f"{MOVE_META[snapshot.ai_choice]['icon']} {MOVE_META[snapshot.ai_choice]['label']}",
                outcome_label,
            ),
        )
        self._set_move_buttons_enabled(not self.game.is_over)

    def _set_move_buttons_enabled(self, enabled: bool) -> None:
        state = "!disabled" if enabled else "disabled"
        for button in self.move_buttons.values():
            button.state([state])

    def preview_mode(self) -> None:
        target = self.best_of_var.get() // 2 + 1
        self.match_var.set(f"Best of {self.best_of_var.get()} • First to {target} wins")
        if self.game.rounds_played:
            self.status_var.set("Mode will apply on the next match.")
        else:
            self.status_var.set("Mode updated for the current match.")
            self.game.best_of = self.best_of_var.get()

    def reset_match(self) -> None:
        self.game.reset(best_of=self.best_of_var.get())
        self.banner_var.set("Fresh match ready. First move decides the pace.")
        self.score_var.set(format_score(self.game))
        self.status_var.set(format_status(self.game))
        self.match_var.set(format_match_label(self.game))
        self.player_choice_var.set("—")
        self.ai_choice_var.set("—")
        for item in self.history.get_children():
            self.history.delete(item)
        self._set_move_buttons_enabled(True)
        self.logger.info("Match reset with best_of=%s", self.game.best_of)


def launch_app(config: AppConfig) -> None:
    root = tk.Tk()
    RPSApp(root, config)
    root.mainloop()
