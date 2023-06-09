"""Maze generation function definition."""

from typing import List, Tuple
from random import random, choices

from src.maze_game.maze_game_object import MazeGameObject


def init_maze(height: int, width: int) -> List[List[int]]:
    """Initialize the maze matrix for any given dimension.

    Args:
        height: number of rows in the resulting matrix.
        width: number of cols in the resulting matrix.
    Returns:
        a generated maze matrix of height by width dimensions.
    """

    maze = []
    for _ in range(height):
        maze_row = [MazeGameObject.EMPTY.value for _ in range(width)]
        maze.append(maze_row)
    return maze


def fill_walls(maze: List[List[int]]) -> None:
    """Fills the remaining tiles.

    Args:
        maze: the input maze array.
    """

    for i, _ in enumerate(maze):
        for j in range(len(maze[0])):
            if maze[i][j] == MazeGameObject.EMPTY.value:
                maze[i][j] = MazeGameObject.WALL.value


def get_start_pos(maze: List[List[int]]) -> Tuple[int, int]:
    """Returns an appropriate start position
    Args:
        maze: 2d array representing the maze board
    Returns:
        coordinates of the start position as tuple pair
    """

    row, col = len(maze), len(maze[0])
    start_row, start_col = int(random() * (row - 2)) + 1, int(random() * (col - 2)) + 1
    return start_row, start_col


def get_surrounding_cell_count(cell: Tuple[int, int], maze: List[List[int]]):
    """Returns the number of surrounding cells in the maze
    Args:
        cell: any coordinates that are valid for the maze
        maze: 2d array representing the maze board
    Returns:
        number of surrounding cells around the input cell
    """

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


def create_entry_exit(maze: List[List[int]]) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:
    """create the entry and exit to the maze

    Args:
        maze: 2d array representing the maze board
    Returns:
        start position coordinates
        end position coordinates
        modified maze as a 2d list
    """
    row, col = len(maze), len(maze[0])
    start_point, exit_point = (0, 0), (row - 1, col - 1)
    # Set entrance and exit
    for i in range(col):
        if maze[1][i] == MazeGameObject.PATH.value:
            maze[0][i] = MazeGameObject.PLAYER_TILE.value
            start_point = (0, i)
            break

    for i in range(col - 1, 0, -1):
        if maze[row - 2][i] == MazeGameObject.PATH.value:
            maze[row - 1][i] = MazeGameObject.GOAL.value
            exit_point = (row - 1, i)
            break
    return start_point, exit_point, maze


def generate_prim_maze(n_row: int, n_col: int) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:
    """Generates a solvable maze using the prim's algorithm

    Links:
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm
    Args:
        n_row: number of rows in the maze board.
        n_col: number of columns the maze board.
    Returns:
        start position coordinates
        end position coordinates
        maze board as a 2D List
    """
    wall_list = set()
    maze = init_maze(n_row, n_col)
    start_pos = get_start_pos(maze)
    maze[start_pos[0]][start_pos[1]] = MazeGameObject.PATH.value

    for val in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        wall_list.add((start_pos[0] + val[0], start_pos[1] + val[1]))
        maze[start_pos[0] + val[0]][start_pos[1] + val[1]] = MazeGameObject.WALL.value

    while wall_list:
        rand_wall = choices(list(wall_list), k=1)[0]
        s_cell_count = get_surrounding_cell_count(rand_wall, maze)

        if s_cell_count < 2:
            if (rand_wall[0] > 0 and rand_wall[0] + 1 < n_row):

                if (maze[rand_wall[0] - 1][rand_wall[1]] == MazeGameObject.EMPTY.value
                        and maze[rand_wall[0] + 1][rand_wall[1]] == MazeGameObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeGameObject.PATH.value

                    maze[rand_wall[0] - 1][rand_wall[1]] = MazeGameObject.WALL.value
                    maze[rand_wall[0]][rand_wall[1] - 1] = MazeGameObject.WALL.value
                    maze[rand_wall[0]][rand_wall[1] + 1] = MazeGameObject.WALL.value

                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))
                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0], rand_wall[1] - 1))

                if (maze[rand_wall[0] + 1][rand_wall[1]] == MazeGameObject.EMPTY.value
                        and maze[rand_wall[0] - 1][rand_wall[1]] == MazeGameObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeGameObject.PATH.value

                    maze[rand_wall[0] + 1][rand_wall[1]] = MazeGameObject.WALL.value
                    maze[rand_wall[0]][rand_wall[1] - 1] = MazeGameObject.WALL.value
                    maze[rand_wall[0]][rand_wall[1] + 1] = MazeGameObject.WALL.value

                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0], rand_wall[1] - 1))

            if (rand_wall[1] > 0 and rand_wall[1] + 1 < n_col):
                if (maze[rand_wall[0]][rand_wall[1] - 1] == MazeGameObject.EMPTY.value
                        and maze[rand_wall[0]][rand_wall[1] + 1] == MazeGameObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeGameObject.PATH.value

                    maze[rand_wall[0]][rand_wall[1] - 1] = MazeGameObject.WALL.value
                    maze[rand_wall[0] - 1][rand_wall[1]] = MazeGameObject.WALL.value
                    maze[rand_wall[0] + 1][rand_wall[1]] = MazeGameObject.WALL.value

                    wall_list.add((rand_wall[0], rand_wall[1] - 1))
                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))

                if (maze[rand_wall[0]][rand_wall[1] + 1] == MazeGameObject.EMPTY.value
                        and maze[rand_wall[0]][rand_wall[1] - 1] == MazeGameObject.PATH.value):
                    maze[rand_wall[0]][rand_wall[1]] = MazeGameObject.PATH.value

                    maze[rand_wall[0]][rand_wall[1] + 1] = MazeGameObject.WALL.value
                    maze[rand_wall[0] - 1][rand_wall[1]] = MazeGameObject.WALL.value
                    maze[rand_wall[0] + 1][rand_wall[1]] = MazeGameObject.WALL.value

                    wall_list.add((rand_wall[0], rand_wall[1] + 1))
                    wall_list.add((rand_wall[0] - 1, rand_wall[1]))
                    wall_list.add((rand_wall[0] + 1, rand_wall[1]))
        wall_list.remove(rand_wall)
    fill_walls(maze)
    entry_point, exit_point, maze = create_entry_exit(maze)
    return entry_point, exit_point, maze
