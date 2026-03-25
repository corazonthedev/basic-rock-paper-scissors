from pathlib import Path

from src.rps_game.config import AppConfig


def test_app_config_reads_env_file(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "RPS_APP_TITLE=Custom Title",
                "RPS_DEFAULT_BEST_OF=5",
                "RPS_WINDOW_WIDTH=1200",
                "RPS_WINDOW_HEIGHT=720",
                "RPS_LOG_LEVEL=DEBUG",
                "RPS_LOG_PATH=logs/custom.log",
            ]
        ),
        encoding="utf-8",
    )

    config = AppConfig.from_project_root(tmp_path)

    assert config.app_title == "Custom Title"
    assert config.default_best_of == 5
    assert config.window_width == 1200
    assert config.window_height == 720
    assert config.log_level == "DEBUG"
    assert config.log_path == tmp_path / "logs/custom.log"


def test_app_config_uses_defaults_without_env(tmp_path: Path):
    config = AppConfig.from_project_root(tmp_path)

    assert config.app_title == "Rock Paper Scissors"
    assert config.default_best_of == 3
    assert config.log_path == tmp_path / "logs/rps.log"
