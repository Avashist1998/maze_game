"""Main file to start the maze game."""
from typing import Final
import pygame
from pygame.constants import QUIT, K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_RIGHT, K_LEFT, KEYDOWN, K_SPACE

from src.maze_game import MazeGame, MazeGameState
from src.maze_game_visualization import MazeGameVisualization

SCREEN_WIDTH: Final = 800
SCREEN_HEIGHT: Final = 600
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100


def game_movement_event_handler(key: int, game: MazeGame) -> None:
    """handles game movement events."""

    if key == K_UP:
        game.move_up()
    elif key == K_DOWN:
        if game.solved:
            game.get_next_level()
        else:
            game.move_down()
    elif key == K_RIGHT:
        game.move_right()
    elif key == K_LEFT:
        game.move_left()
    else:
        pass


def main() -> None:
    """Starts the maze games"""

    running = True
    game = MazeGame(MAZE_WIDTH, MAZE_HEIGHT)
    visualizer = MazeGameVisualization(SCREEN_HEIGHT, SCREEN_WIDTH)

    while running:
        if game.state == MazeGameState.MENU:
            visualizer.draw_main_menu()

        elif game.state == MazeGameState.PAUSED:
            print("we have paused the game!")

        else:
            visualizer.draw_maze(game.curr_level_maze)
            visualizer.draw_level_counter(game.curr_level_maze)
            visualizer.draw_step_counter(game.curr_level_maze)
            if game.solved:
                visualizer.draw_game_over()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    game.set_state(MazeGameState.PLAYING)
                elif event.key == K_ESCAPE:
                    game.set_state(MazeGameState.MENU)
                elif event.key == K_SPACE:
                    game.set_state(MazeGameState.PAUSED)
                else:
                    game_movement_event_handler(event.key, game)
            else:
                pass
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
