from src.rps_game.config import AppConfig
from src.rps_game.ui import launch_app


if __name__ == "__main__":
    launch_app(AppConfig.from_project_root())
