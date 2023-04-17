"""Maze Game definition"""
from typing import List, Dict, Tuple

from src.config import Config
from src.event import Direction

from src.maze_game.layers.maze_layer import MazeLayer
from src.maze_game.layers.options_layer import OptionsLayer
from src.maze_game.maze_state import MazeGameState


class MazeGame:
    """Maze Game class."""

    def __init__(self, size: Tuple[int, int], config: Config):
        """Constructor for the maze game.

        Args:
            maze_width: The width of the maze.
            maze_height: The height of the maze.
        """

        self.curr_level: int = 1
        self.state = MazeGameState(0)
        self.level_stats: Dict[int, int] = {1: 0}
        self.size = size
        self.curr_maze: MazeLayer = MazeLayer(self.size[1], self.size[0],
                                              self.curr_level)

        menu_options = {
            "Play": "PLAY",
            "Quit": "QUIT"
        } if not config.TWITCH_MODE else {
            "Play": "PLAY",
            "Twitch Mode": "TWITCH_MODE",
            "Quit": "QUIT"
        }
        self.main_menu_layer = OptionsLayer(menu_options, "Play")
        self.pause_menu_layer = OptionsLayer(
            {
                "Resume": "RESUME",
                "Quit": "QUIT"
            }, "Resume")

    def get_board(self) -> List[List[int]]:
        """Returns the board of the current level."""

        return self.curr_maze.get_board()

    def set_state(self, state: MazeGameState):
        """Sets the state of the game.

        Args:
            state: The state to set the game to.
        """

        self.state = state

    def get_maze(self) -> MazeLayer:
        """Returns the current maze."""

        return self.curr_maze

    def get_next_level(self):
        """Gets the next level of the game."""

        self.update_stats()
        self.curr_level += 1
        self.curr_maze = MazeLayer(self.size[1], self.size[0], self.curr_level)

    def update_stats(self):
        """Updates the stats of the game."""

        self.level_stats[self.curr_level] = self.curr_maze.step_count

    def move(self, direction: Direction):
        """Move the player in the given direction.

        Args:
            direction: The direction to move the player.=
        """

        if direction == Direction.UP:
            self.move_up()
        elif direction == Direction.DOWN:
            if self.curr_maze.is_solved():
                self.get_next_level()
            else:
                self.move_down()
        elif direction == Direction.LEFT:
            self.move_left()
        elif direction == Direction.RIGHT:
            self.move_right()

    def move_up(self):
        """Moves the player up."""

        self.curr_maze.move_up()
        self.update_stats()

    def move_down(self):
        """Moves the player down."""

        self.curr_maze.move_down()
        self.update_stats()

    def move_left(self):
        """Moves the player left."""

        self.curr_maze.move_left()
        self.update_stats()

    def move_right(self):
        """Moves the player right."""

        self.curr_maze.move_right()
        self.update_stats()
