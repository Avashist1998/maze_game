"""Main file to start the maze game."""
from typing import Final

from src.event_manager import EventManager
from src.keyboard_controller import Keyboard
from src.maze_view import MazeView
from src.model import GameEngine

from src.maze_game import MazeGame

SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100


def main() -> None:
    """Starts the maze games"""

    event_manger = EventManager()
    game = MazeGame(MAZE_WIDTH, MAZE_HEIGHT)
    game_model = GameEngine(event_manger, game)
    _ = MazeView(event_manger, game)
    _ = Keyboard(event_manger)
    game_model.run()


if __name__ == "__main__":
    main()
