"""Defining the maze game layer"""

from typing import List

from src.maze_game.maze_generation import generate_prim_maze


class MazeLayer:
    """Maze Layer Definition."""

    def __init__(self, maze_height: int, maze_width: int, level: int = 1):

        self.solved = False
        self.step_count = 0
        self.level_count = level
        self.tile_width, self.tile_height = 100 // level, 100 // level
        self.tile_width_count, self.tile_height_count = maze_width // self.tile_width, maze_height // self.tile_height
        self.start, self.end, self.board = generate_prim_maze(
            self.tile_height_count, self.tile_width_count)
        self.player_loc = (self.start[0], self.start[1])

    def get_board(self) -> List[List[int]]:
        """Returns the maze board."""
        return self.board

    def move_left(self):
        """Moves the player one place left."""

        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved is False and curr_loc[1] != 0 and self.board[
                curr_loc[0]][curr_loc[1] - 1] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]][curr_loc[1] - 1] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0

            if self.board[curr_loc[0]][curr_loc[1] - 1] == 2:
                self.solved = True

            self.player_loc = (curr_loc[0], curr_loc[1] - 1)
            self.board[self.player_loc[0]][self.player_loc[1]] = 7

    def move_right(self):
        """Moves the player one place right."""

        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved is False and curr_loc[
                1] != self.tile_width_count - 1 and self.board[curr_loc[0]][
                    curr_loc[1] + 1] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]][curr_loc[1] + 1] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0

            if self.board[curr_loc[0]][curr_loc[1] + 1] == 2:
                self.solved = True

            self.player_loc = (curr_loc[0], curr_loc[1] + 1)
            self.board[self.player_loc[0]][self.player_loc[1]] = 7

    def move_up(self):
        """Moves the player one place up."""

        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved is False and curr_loc[0] != 0 and self.board[
                curr_loc[0] - 1][curr_loc[1]] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0] - 1][curr_loc[1]] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0
            if self.board[curr_loc[0] - 1][curr_loc[1]] == 2:
                self.solved = True
            self.player_loc = (curr_loc[0] - 1, curr_loc[1])
            self.board[self.player_loc[0]][self.player_loc[1]] = 7

    def move_down(self):
        """Moves the player one place down."""

        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved is False and curr_loc[
                0] != self.tile_height_count - 1 and self.board[
                    curr_loc[0] + 1][curr_loc[1]] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0] + 1][curr_loc[1]] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0
            if self.board[curr_loc[0] + 1][curr_loc[1]] == 2:
                self.solved = True
            self.player_loc = (curr_loc[0] + 1, curr_loc[1])
            self.board[self.player_loc[0]][self.player_loc[1]] = 7
