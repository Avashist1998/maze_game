"""maze"""
from enum import Enum
from typing import List, Dict

from src.maze_game_layer import MazeGameLayer


class MazeGameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2


class MazeGame:

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

    def get_board(self) -> List[List[int]]:
        return self.curr_level_maze.get_board()

    def set_state(self, state: MazeGameState):
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
        self.curr_level_maze.move_up()
        self.update_stats()

    def move_down(self):
        self.curr_level_maze.move_down()
        self.update_stats()

    def move_left(self):
        self.curr_level_maze.move_left()
        self.update_stats()

    def move_right(self):
        self.curr_level_maze.move_right()
        self.update_stats()
