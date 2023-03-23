from random import random
from enum import Enum
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



def remove_wall_from_list(cell: Tuple[int, int], wall_list: List[Tuple[int, int]]):
    for wall in wall_list:
        if wall == cell:
            wall_list.remove(wall)


def fill_walls(maze: List[List[int]]) -> List[List[int]]:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == -1:
                maze[i][j] = 1
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
    start_row, start_col = int(random()*row), int(random()*col)
    
    if start_row == 0:
        start_row += 1
    if start_row == row-1:
        start_row -= 1 
    if start_col == 0:
        start_col += 1
    if start_col == col-1:
        start_col -= 1
    return start_row, start_col


def get_surrounding_cell_count(cell: Tuple[int, int], maze: List[List[int]]):
    s_cell_count = 0
    if (cell[0] > 0 and maze[cell[0]-1][cell[1]] == 0):
        s_cell_count += 1
    if (cell[0] < len(maze)-1 and maze[cell[0]+1][cell[1]] == 0):
        s_cell_count += 1
    if (cell[1] > 0 and maze[cell[0]][cell[1]-1] == 0):
        s_cell_count +=1
    if (cell[1] < len(maze[0])-1 and maze[cell[0]][cell[1]+1] == 0):
        s_cell_count += 1    
    return s_cell_count



def generate_board(n_row: int, n_col: int) -> List[List[int]]:

    wall_list = []
    maze = init_maze(n_row, n_col)
    start_pos = get_star_pos(maze)
    maze[start_pos[0]][start_pos[1]] = 0

    wall_list.append((start_pos[0]-1, start_pos[1]))
    wall_list.append((start_pos[0], start_pos[1]-1))
    wall_list.append((start_pos[0], start_pos[1]+1))
    wall_list.append((start_pos[0]+1, start_pos[1]))
    maze[start_pos[0]-1][start_pos[1]] = 1
    maze[start_pos[0]][start_pos[1]-1] = 1
    maze[start_pos[0]][start_pos[1]+1] = 1
    maze[start_pos[0]+1][start_pos[1]] = 1

    while wall_list:
        rand_wall = wall_list[int(random()*len(wall_list))-1]
        s_cell_count = get_surrounding_cell_count(rand_wall, maze)
        if s_cell_count < 2:
            maze[rand_wall[0]][rand_wall[1]] = 0
            if (rand_wall[0] > 0 and maze[rand_wall[0]-1][rand_wall[1]] == -1):
                maze[rand_wall[0]-1][rand_wall[1]] = 1
                wall_list.append((rand_wall[0]-1, rand_wall[1]))
            if (rand_wall[1] > 0 and maze[rand_wall[0]][rand_wall[1]-1] == -1):
                maze[rand_wall[0]][rand_wall[1]-1] = 1
                wall_list.append((rand_wall[0], rand_wall[1]-1))
            if (rand_wall[0] < n_row-1 and maze[rand_wall[0]+1][rand_wall[1]] == -1):
                maze[rand_wall[0]+1][rand_wall[1]] = 1
                wall_list.append((rand_wall[0]+1, rand_wall[1]))
            if (rand_wall[1] < n_col-1 and maze[rand_wall[0]][rand_wall[1]+1] == -1):
                maze[rand_wall[0]][rand_wall[1]+1] = 1
                wall_list.append((rand_wall[0], rand_wall[1]+1))

        remove_wall_from_list(rand_wall, wall_list)

    maze = fill_walls(maze)
    maze[start_pos[0]][start_pos[1]] = 7
    end_pos = (n_row-1, n_col-1)
    maze[end_pos[0]][end_pos[1]] = 2
    return start_pos, end_pos, maze



class MazeGameLayer:

    def __init__(self, maze_height: int, maze_width: int, level: int = 1):
        
        self.solved = False
        self.step_count = 0
        self.tile_width, self.tile_height = 200//level, 200//level
        self.tile_width_count, self.tile_height_count = maze_width//self.tile_width, maze_height//self.tile_height
        self.start, self.end, self.board = generate_board(self.tile_height_count, self.tile_width_count)
        self.player_loc = (self.start[0], self.start[1])

    def get_board(self) -> List[List[int]]:
        return self.board
    
    def move_left(self):
        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved == False and curr_loc[1] != 0 and self.board[curr_loc[0]][curr_loc[1]-1] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]][curr_loc[1]-1] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0

            if self.board[curr_loc[0]][curr_loc[1]-1] == 2:
                self.solved = True

            self.player_loc = (curr_loc[0], curr_loc[1]-1)
            self.board[self.player_loc[0]][self.player_loc[1]] = 7

    def move_right(self):
        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved == False and curr_loc[1] != self.tile_width_count-1 and self.board[curr_loc[0]][curr_loc[1]+1] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]][curr_loc[1]+1] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0
            
            if self.board[curr_loc[0]][curr_loc[1]+1] == 2:
                self.solved = True
        
            self.player_loc = (curr_loc[0], curr_loc[1]+1)
            self.board[self.player_loc[0]][self.player_loc[1]] = 7


    def move_up(self):
        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved == False and curr_loc[0] != 0 and self.board[curr_loc[0]-1][curr_loc[1]] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]-1][curr_loc[1]] == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0
            if self.board[curr_loc[0]-1][curr_loc[1]] == 2:
                self.solved = True
            self.player_loc = (curr_loc[0]-1, curr_loc[1])
            self.board[self.player_loc[0]][self.player_loc[1]] = 7


    def move_down(self):

        curr_loc = (self.player_loc[0], self.player_loc[1])

        if self.solved == False and curr_loc[0] != self.tile_height_count-1 and self.board[curr_loc[0]+1][curr_loc[1]] != 1:
            self.step_count += 1
            self.board[curr_loc[0]][curr_loc[1]] = 3
            if self.board[curr_loc[0]+1][curr_loc[1]]  == 3:
                self.board[curr_loc[0]][curr_loc[1]] = 0
            if self.board[curr_loc[0]+1][curr_loc[1]]  == 2:
                self.solved = True
            self.player_loc = (curr_loc[0]+1, curr_loc[1])
            self.board[self.player_loc[0]][self.player_loc[1]] = 7


class MazeGame:

    def __init__(self, maze_width: int,  maze_height: int):
        
        self.solved = False
        self.step_count = 0
        self.curr_level: int = 1
        self.state = MazeGameState(0)
        self.level_stats: Dict[int, int] = {1: 0}
        self.maze_width, self.maze_height = maze_width, maze_height 
        self.curr_level_maze: MazeGameLayer = MazeGameLayer(self.maze_height, self.maze_width, self.curr_level)
        self.tile_width, self.tile_height = self.curr_level_maze.tile_width, self.curr_level_maze.tile_height

    def get_board(self) -> List[List[int]]:
        return self.curr_level_maze.get_board()
    
    def set_state(self, state: MazeGameState):
        self.state = state

    def get_next_level(self):
        self.update_stats()
        self.solved = False
        self.curr_level += 1
        self.curr_level_maze = MazeGameLayer(self.maze_height, self.maze_width, self.curr_level)
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