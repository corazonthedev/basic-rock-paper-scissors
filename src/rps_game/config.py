from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _read_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


@dataclass(frozen=True)
class AppConfig:
    app_title: str = "Rock Paper Scissors"
    default_best_of: int = 3
    window_width: int = 980
    window_height: int = 680
    log_level: str = "INFO"
    log_path: Path = Path("logs/rps.log")

    @classmethod
    def from_project_root(cls, project_root: Path | None = None) -> "AppConfig":
        root = project_root or Path(__file__).resolve().parents[2]
        env_values = _read_env_file(root / ".env")

        def get_value(key: str, default: str) -> str:
            return os.environ.get(key, env_values.get(key, default))

        return cls(
            app_title=get_value("RPS_APP_TITLE", cls.app_title),
            default_best_of=int(get_value("RPS_DEFAULT_BEST_OF", str(cls.default_best_of))),
            window_width=int(get_value("RPS_WINDOW_WIDTH", str(cls.window_width))),
            window_height=int(get_value("RPS_WINDOW_HEIGHT", str(cls.window_height))),
            log_level=get_value("RPS_LOG_LEVEL", cls.log_level),
            log_path=root / get_value("RPS_LOG_PATH", str(cls.log_path)),
        )
