"""Defines the maze game controller"""
from typing import Final
from dataclasses import dataclass

from src.maze_game import MazeGame, MazeGameState
from src.logger import init_logger
from pygame.constants import (K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_RIGHT,
                              K_LEFT, K_SPACE)


@dataclass
class MazeGameEvent:
    key_val: int
    event_type: str


logger: Final = init_logger(__name__)


class MazeGameController:
    """Controls the maze game"""

    def __init__(self, maze_game: MazeGame):
        """Constructor for the maze game controller."""
        self.game = maze_game

    def processMovementEvent(self, event: MazeGameEvent):
        """Process the game movement events."""

        if self.game.state == MazeGameState.PLAYING:
            if event.key_val == K_UP:
                self.game.move_up()
            elif event.key_val == K_DOWN:
                if self.game.solved:
                    self.game.get_next_level()
                else:
                    self.game.move_down()
            elif event.key_val == K_RIGHT:
                self.game.move_right()
            elif event.key_val == K_LEFT:
                self.game.move_left()

    def processEvent(self, event: MazeGameEvent):
        """Process events user events"""
        logger.info(event)

        # change in settings or pause event
        if event.key_val == K_SPACE:
            if self.game.state == MazeGameState.PLAYING:
                self.game.set_state(MazeGameState.PAUSED)
            elif self.game.state == MazeGameState.PAUSED:
                self.game.set_state(MazeGameState.PLAYING)

        elif event.key_val == K_ESCAPE:
            self.game.set_state(MazeGameState.MENU)

        elif event.key_val == K_RETURN:
            self.game.set_state(MazeGameState.PLAYING)
        else:
            self.processMovementEvent(event)
