from enum import Enum
from random import random, sample
from typing import Tuple, List, Dict


class MazeGameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2


class MazeObject(Enum):
    PATH = 0
    WALL = 1
    GOAL = 2
    PLAYER_TILE = 7
    VISITED_TILE = 3


def fill_walls(maze: List[List[int]]) -> List[List[int]]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == -1:
                maze[i][j] = MazeObject.WALL.value
    return maze


def init_maze(height: int, width: int) -> List[List[int]]:
    maze = []
    for i in range(height):
        line = []
        for j in range(width):
            line.append(-1)
        maze.append(line)
    return maze


def get_star_pos(maze: List[List[int]]) -> Tuple[int, int]:
    row, col = len(maze), len(maze[0])
    start_row, start_col = int(random() * row), int(random() * col)

    if start_row == 0:
        start_row += 1
    if start_row == row - 1:
        start_row -= 1
    if start_col == 0:
        start_col += 1
    if start_col == col - 1:
        start_col -= 1
    return start_row, start_col


def get_surrounding_cell_count(cell: Tuple[int, int], maze: List[List[int]]):
    s_cell_count = 0
    if (cell[0] > 0 and maze[cell[0] - 1][cell[1]] == 0):
        s_cell_count += 1
    if (cell[0] < len(maze) - 1 and maze[cell[0] + 1][cell[1]] == 0):
        s_cell_count += 1
    if (cell[1] > 0 and maze[cell[0]][cell[1] - 1] == 0):
        s_cell_count += 1
    if (cell[1] < len(maze[0]) - 1 and maze[cell[0]][cell[1] + 1] == 0):
        s_cell_count += 1
    return s_cell_count


def create_entry_exit(
    maze: List[List[int]]
) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:
    """create the entry and exit to the maze"""
    row, col = len(maze), len(maze[0])
    start_point, exit_point = (0, 0), (row - 1, col - 1)
    # Set entrance and exit
    for i in range(col):
        if (maze[1][i] == MazeObject.PATH.value):
            maze[0][i] = MazeObject.PLAYER_TILE.value
            start_point = (0, i)
            break

    for i in range(col - 1, 0, -1):
        if (maze[row - 2][i] == MazeObject.PATH.value):
            maze[row - 1][i] = MazeObject.GOAL.value
            exit_point = (row - 1, i)
            break
    return start_point, exit_point, maze


def generate_board(
        n_row: int, n_col: int
) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:

    wall_list = set()
    maze = init_maze(n_row, n_col)
    start_pos = get_star_pos(maze)
    maze[start_pos[0]][start_pos[1]] = 0

    wall_list.add((start_pos[0] - 1, start_pos[1]))
    wall_list.add((start_pos[0], start_pos[1] - 1))
    wall_list.add((start_pos[0], start_pos[1] + 1))
    wall_list.add((start_pos[0] + 1, start_pos[1]))
    maze[start_pos[0] - 1][start_pos[1]] = 1
    maze[start_pos[0]][start_pos[1] - 1] = 1
    maze[start_pos[0]][start_pos[1] + 1] = 1
    maze[start_pos[0] + 1][start_pos[1]] = 1

    while wall_list:
        rand_wall = sample(wall_list, 1)[0]
        s_cell_count = get_surrounding_cell_count(rand_wall, maze)

        if s_cell_count < 2:
            if (rand_wall[0] > 0 and rand_wall[0] + 1 < n_row):

                if (maze[rand_wall[0] - 1][rand_wall[1]] == -1
                        and maze[rand_wall[0] + 1][rand_wall[1]]
                        == MazeObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeObject.PATH.value
                    maze[rand_wall[0] -
                         1][rand_wall[1]] = MazeObject.WALL.value
                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))
                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0], rand_wall[1] - 1))

                if (maze[rand_wall[0] + 1][rand_wall[1]] == -1
                        and maze[rand_wall[0] - 1][rand_wall[1]]
                        == MazeObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeObject.PATH.value
                    maze[rand_wall[0] +
                         1][rand_wall[1]] = MazeObject.WALL.value
                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0], rand_wall[1] - 1))

            if (rand_wall[1] > 0 and rand_wall[1] + 1 < n_col):
                if (maze[rand_wall[0]][rand_wall[1] - 1] == -1
                        and maze[rand_wall[0]][rand_wall[1] + 1]
                        == MazeObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeObject.PATH.value
                    maze[rand_wall[0]][rand_wall[1] -
                                       1] = MazeObject.WALL.value
                    wall_list.add((rand_wall[0], rand_wall[1] - 1))
                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))

                if (maze[rand_wall[0]][rand_wall[1] + 1] == -1
                        and maze[rand_wall[0]][rand_wall[1] - 1]
                        == MazeObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeObject.PATH.value
                    maze[rand_wall[0]][rand_wall[1] +
                                       1] = MazeObject.WALL.value
                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))
                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
        wall_list.remove(rand_wall)
    maze = fill_walls(maze)
    entry_point, exit_point, maze = create_entry_exit(maze)
    return entry_point, exit_point, maze


class MazeGameLayer:

    level_count = 0

    def __init__(self, maze_height: int, maze_width: int, level: int = 1):
        MazeGameLayer.level_count += 1
        self.solved = False
        self.step_count = 0
        self.tile_width, self.tile_height = 100 // level, 100 // level
        self.tile_width_count, self.tile_height_count = maze_width // self.tile_width, maze_height // self.tile_height
        self.start, self.end, self.board = generate_board(
            self.tile_height_count, self.tile_width_count)
        self.player_loc = (self.start[0], self.start[1])

    def get_board(self) -> List[List[int]]:
        return self.board

    def move_left(self):
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
