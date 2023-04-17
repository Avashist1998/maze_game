"""Main file to start the maze game."""
import asyncio
from typing import Final

from src.event_manager import EventManager
from src.keyboard_controller import Keyboard
from src.view import MazeView
from src.model import GameEngine
from src.maze_game import MazeGame
from src.config import get_config

SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100


async def main() -> None:
    """Starts the maze games"""
    config = get_config()
    event_manger = EventManager()
    game = MazeGame((MAZE_WIDTH, MAZE_HEIGHT), config)
    game_model = GameEngine(event_manger, game)
    _ = MazeView(event_manger, game)
    _ = Keyboard(event_manger)
    await game_model.run()


if __name__ == "__main__":
    asyncio.run(main())
