"""Maze Game definition"""
from enum import Enum
from typing import List, Dict

from src.maze_game_layer import MazeGameLayer
from src.game_options_layer import GameOptionsLayer


class MazeGameState(Enum):
    """Enum for managing the state of the MazeGame"""
    MENU = 0
    PLAYING = 1
    PAUSED = 2


class MazeGame:
    """Maze Game class."""

    def __init__(self, maze_width: int, maze_height: int):

        self.solved = False
        self.step_count = 0
        self.curr_level: int = 1
        self.state = MazeGameState(0)
        self.level_stats: Dict[int, int] = {1: 0}
        self.maze_width, self.maze_height = maze_width, maze_height
        self.curr_level_maze: MazeGameLayer = MazeGameLayer(
            self.maze_height, self.maze_width, self.curr_level)
        self.tile_width, self.tile_height = self.curr_level_maze.tile_width, self.curr_level_maze.tile_height

        self.main_menu_layer = GameOptionsLayer({"Play": "PLAY", "Twitch Mode": "TWITCH_MODE", "Quit": "QUIT"}, "Play")
        self.pause_menu_layer = GameOptionsLayer({"Resume": "RESUME", "Quit": "QUIT"}, "Resume")

    def get_board(self) -> List[List[int]]:
        return self.curr_level_maze.get_board()

    def set_state(self, state: MazeGameState):
        """Sets the state of the game."""

        self.state = state

    def get_next_level(self):
        self.update_stats()
        self.solved = False
        self.curr_level += 1
        self.curr_level_maze = MazeGameLayer(self.maze_height, self.maze_width,
                                             self.curr_level)
        self.tile_width, self.tile_height = self.curr_level_maze.tile_width, self.curr_level_maze.tile_height

    def update_stats(self):
        self.level_stats[self.curr_level] = self.curr_level_maze.step_count
        self.solved = self.curr_level_maze.solved

    def move_up(self):
        """Moves the player up."""

        self.curr_level_maze.move_up()
        self.update_stats()

    def move_down(self):
        """Moves the player down."""

        self.curr_level_maze.move_down()
        self.update_stats()

    def move_left(self):
        """Moves the player left."""

        self.curr_level_maze.move_left()
        self.update_stats()

    def move_right(self):
        """Moves the player right."""

        self.curr_level_maze.move_right()
        self.update_stats()
