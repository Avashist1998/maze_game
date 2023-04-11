"""Defines the maze game controller"""
from typing import Final
from dataclasses import dataclass
from pygame.constants import (K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_RIGHT,
                              K_LEFT, K_SPACE)

from src.maze_game import MazeGame, MazeGameState
from src.logger import init_logger

LOGGER: Final = init_logger(__name__)


@dataclass
class MazeGameEvent:
    """Data class for maze game event data."""
    key_val: int
    event_type: str


class MazeGameController:
    """Controls the maze game"""

    def __init__(self, maze_game: MazeGame):
        """Constructor for the maze game controller."""
        self.game = maze_game

    def _process_movement_event(self, event: MazeGameEvent):
        """Process the game movement events."""

        if (self.game.state == MazeGameState.PLAYING) or (self.game.state == MazeGameState.PLAYING_WITH_TWITCH):
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
        elif self.game.state == MazeGameState.MENU:
            if event.key_val == K_UP:
                self.game.main_menu_layer.move_up()
            elif event.key_val == K_DOWN:
                self.game.main_menu_layer.move_down()
    

    def process_menu_event(self, event: MazeGameEvent):
        """Process event when game in menu state."""

        if event.key_val == K_UP:
            self.game.main_menu_layer.move_up()
        elif event.key_val == K_DOWN:
            self.game.main_menu_layer.move_down()
        elif event.key_val == K_RETURN:
            if self.game.main_menu_layer.get_current_option() == "Play":
                self.game.set_state(MazeGameState.PLAYING)
            elif self.game.main_menu_layer.get_current_option() == "Twitch Mode":
                self.game.set_state(MazeGameState.PLAYING_WITH_TWITCH)
            elif self.game.main_menu_layer.get_current_option() == "Quit":
                return False
        return True

    def process_pause_event(self, event: MazeGameEvent):
        """Process event when game in pause state."""

        if event.key_val == K_UP:
            self.game.pause_menu_layer.move_up()
        elif event.key_val == K_DOWN:
            self.game.pause_menu_layer.move_down()
        elif event.key_val == K_RETURN:
            if self.game.pause_menu_layer.get_current_option() == "Resume":
                self.game.set_state(MazeGameState.PLAYING)
            elif self.game.pause_menu_layer.get_current_option() == "Quit":
                return False
        return True

    def process_event(self, event: MazeGameEvent) -> bool:
        """Process events user events"""
        LOGGER.info(event)

        # change in settings or pause event
        if self.game.state == MazeGameState.MENU:
            return self.process_menu_event(event)
      
        elif self.game.state == MazeGameState.PAUSED:
            return self.process_pause_event(event)
    
        elif (self.game.state == MazeGameState.PLAYING) or (self.game.state == MazeGameState.PLAYING_WITH_TWITCH):
            if event.key_val == K_SPACE:
                self.game.set_state(MazeGameState.PAUSED)
            elif event.key_val == K_ESCAPE:
                self.game.set_state(MazeGameState.MENU)
            else:
                self._process_movement_event(event)
        return True
