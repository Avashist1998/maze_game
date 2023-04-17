"""Defining the maze game layer"""

from typing import List

from src.maze_game.maze_board import MazeBoard
from src.maze_game.maze_generation import generate_prim_maze


class MazeLayer:
    """Maze Layer Definition."""

    def __init__(self, maze_height: int, maze_width: int, level: int = 1):
        """Constructor for the maze layer."""

        self.step_count = 0
        self.level_count = level
        self.tile_width, self.tile_height = 100 // level, 100 // level
        self.tile_width_count, self.tile_height_count = maze_width // self.tile_width, maze_height // self.tile_height

        start, end, board = generate_prim_maze(self.tile_height_count,
                                               self.tile_width_count)
        self.board = MazeBoard(board, start, end, (start[0], start[1]))

    def get_board(self) -> List[List[int]]:
        """Returns the maze board."""
        return self.board.board

    def is_solved(self) -> bool:
        """Returns if the maze is solved."""
        return self.board.solved

    def move_left(self):
        """Moves the player one place left."""

        board = self.board.board
        solved = self.board.solved
        curr_pos = self.board.curr_pos

        if solved is False and curr_pos[1] != 0 and board[curr_pos[0]][
                curr_pos[1] - 1] != 1:
            self.step_count += 1
            board[curr_pos[0]][curr_pos[1]] = 3
            if board[curr_pos[0]][curr_pos[1] - 1] == 3:
                board[curr_pos[0]][curr_pos[1]] = 0

            if board[curr_pos[0]][curr_pos[1] - 1] == 2:
                self.board.solved = True

            self.board.curr_pos = (curr_pos[0], curr_pos[1] - 1)
            self.board.board[curr_pos[0]][curr_pos[1] - 1] = 7

    def move_right(self):
        """Moves the player one place right."""

        board = self.board.board
        solved = self.board.solved
        curr_pos = self.board.curr_pos

        if solved is False and curr_pos[
                1] != self.tile_width_count - 1 and board[curr_pos[0]][
                    curr_pos[1] + 1] != 1:
            self.step_count += 1
            board[curr_pos[0]][curr_pos[1]] = 3
            if board[curr_pos[0]][curr_pos[1] + 1] == 3:
                board[curr_pos[0]][curr_pos[1]] = 0

            if board[curr_pos[0]][curr_pos[1] + 1] == 2:
                self.board.solved = True

            self.board.curr_pos = (curr_pos[0], curr_pos[1] + 1)
            self.board.board[curr_pos[0]][curr_pos[1] + 1] = 7

    def move_up(self):
        """Moves the player one place up."""

        board = self.board.board
        solved = self.board.solved
        curr_pos = self.board.curr_pos

        if solved is False and curr_pos[0] != 0 and board[curr_pos[0] -
                                                          1][curr_pos[1]] != 1:
            self.step_count += 1
            board[curr_pos[0]][curr_pos[1]] = 3
            if board[curr_pos[0] - 1][curr_pos[1]] == 3:
                board[curr_pos[0]][curr_pos[1]] = 0

            if board[curr_pos[0] - 1][curr_pos[1]] == 2:
                self.board.solved = True
            self.board.curr_pos = (curr_pos[0] - 1, curr_pos[1])
            self.board.board[curr_pos[0] - 1][curr_pos[1]] = 7

    def move_down(self):
        """Moves the player one place down."""

        board = self.board.board
        solved = self.board.solved
        curr_pos = self.board.curr_pos

        if solved is False and curr_pos[
                0] != self.tile_height_count - 1 and board[curr_pos[0] + 1][
                    curr_pos[1]] != 1:
            self.step_count += 1
            board[curr_pos[0]][curr_pos[1]] = 3
            if board[curr_pos[0] + 1][curr_pos[1]] == 3:
                board[curr_pos[0]][curr_pos[1]] = 0

            if board[curr_pos[0] + 1][curr_pos[1]] == 2:
                self.board.solved = True
            self.board.curr_pos = (curr_pos[0] + 1, curr_pos[1])
            self.board.board[curr_pos[0] + 1][curr_pos[1]] = 7
