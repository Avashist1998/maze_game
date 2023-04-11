"""Main file to start the maze game."""
from typing import Final
import pygame
from pygame.constants import (QUIT, KEYDOWN)

from src.twitch_feed import TwitchFeed
from src.maze_game import MazeGame, MazeGameState
from src.maze_game_controller import MazeGameController, MazeGameEvent
from src.maze_game_visualization import MazeGameVisualization
import asyncio

SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100

twitch_feed = TwitchFeed()

def main() -> None:
    """Starts the maze games"""

    running = True
    game = MazeGame(MAZE_WIDTH, MAZE_HEIGHT)
    controller = MazeGameController(game)
    visualizer = MazeGameVisualization(SCREEN_HEIGHT, SCREEN_WIDTH)

    while running:
        if game.state == MazeGameState.PLAYING_WITH_TWITCH:
            if len(twitch_feed.event_queue) != 0:
                latest_event = twitch_feed.event_queue.pop()
                pygame.event.post(latest_event)
                pygame.time.delay(5000)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                curr_event = MazeGameEvent(event.key, "Key_down")
                running = controller.process_event(curr_event)
            else:
                pass
            visualizer.draw_game(game)
            pygame.display.update()

    pygame.quit()




if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.create_task(main())
    # loop.create_task(twitch_feed.run())
    # loop.run_forever()

    # # loop = asyncio.get_event_loop()
    # # loop.create_task(twitch_feed.run())
    # # # loop.create_task(main())
    # # loop.run_forever()
    # asyncio.create_task(twitch_feed.run())
    main()
