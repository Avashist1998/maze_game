"""Main file to start the maze game."""
from typing import Final
import pygame
from pygame.constants import (QUIT, KEYDOWN)

from src.maze_game import MazeGame
from src.maze_game_controller import MazeGameController, MazeGameEvent
from src.maze_game_visualization import MazeGameVisualization

SCREEN_WIDTH: Final = 800
SCREEN_HEIGHT: Final = 600
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100


def main() -> None:
    """Starts the maze games"""

    running = True
    game = MazeGame(MAZE_WIDTH, MAZE_HEIGHT)
    controller = MazeGameController(game)
    visualizer = MazeGameVisualization(SCREEN_HEIGHT, SCREEN_WIDTH)

    while running:
        visualizer.draw_game(game)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                curr_event = MazeGameEvent(event.key, "Key_down")
                controller.processEvent(curr_event)
            else:
                pass
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
