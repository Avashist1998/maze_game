"""Maze Game definition"""
from typing import List, Dict

from src.maze_game.layers.maze_layer import MazeLayer
from src.maze_game.layers.options_layer import OptionsLayer
from src.maze_game.maze_state import MazeGameState


class MazeGame:
    """Maze Game class."""

    def __init__(self, maze_width: int, maze_height: int):
        """Constructor for the maze game.

        Args:
            maze_width: The width of the maze.
            maze_height: The height of the maze.
        """

        self.solved = False
        self.step_count = 0
        self.curr_level: int = 1
        self.state = MazeGameState(0)
        self.level_stats: Dict[int, int] = {1: 0}
        self.maze_width, self.maze_height = maze_width, maze_height
        self.curr_level_maze: MazeLayer = MazeLayer(self.maze_height,
                                                    self.maze_width,
                                                    self.curr_level)
        self.tile_width, self.tile_height = self.curr_level_maze.tile_width, self.curr_level_maze.tile_height

        self.main_menu_layer = OptionsLayer(
            {
                "Play": "PLAY",
                "Twitch Mode": "TWITCH_MODE",
                "Quit": "QUIT"
            }, "Play")
        self.pause_menu_layer = OptionsLayer(
            {
                "Resume": "RESUME",
                "Quit": "QUIT"
            }, "Resume")

    def get_board(self) -> List[List[int]]:
        """Returns the board of the current level."""

        return self.curr_level_maze.get_board()

    def set_state(self, state: MazeGameState):
        """Sets the state of the game.

        Args:
            state: The state to set the game to.
        """

        self.state = state

    def get_next_level(self):
        """Gets the next level of the game."""

        self.update_stats()
        self.solved = False
        self.curr_level += 1
        self.curr_level_maze = MazeLayer(self.maze_height, self.maze_width,
                                         self.curr_level)
        self.tile_width, self.tile_height = self.curr_level_maze.tile_width, self.curr_level_maze.tile_height

    def update_stats(self):
        """Updates the stats of the game."""

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
