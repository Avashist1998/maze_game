from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from pygame import Surface, Rect, Color
import random
import pygame
import time


class MazeGridCellType(Enum):
	WALL = 1
	PATH = 2
	def __str__(self):
		if self == MazeGridCellType.WALL:
			return "W"
		elif self == MazeGridCellType.PATH:
			return "C"

@dataclass
class Location:
	x: int
	y: int

@dataclass
class MazePlayer:
	location: Location

@dataclass
class GridCell:
	location: Location

@dataclass
class ColoredGridCell(GridCell):
	color: Color

@dataclass
class MazeGridCell(GridCell):
	cell_type: MazeGridCellType

@dataclass
class Grid():
	number_of_rows: int
	number_of_columns: int
	cells: List[GridCell]

	def get_cell_index_at(self, location: Location) -> Optional[int]:
		row = location.y
		column = location.x
		row_is_out_of_bounds = row < 0 or row > self.number_of_rows - 1
		column_is_out_of_bounds = column < 0 or column > self.number_of_columns - 1
		if row_is_out_of_bounds or column_is_out_of_bounds:
			return None

		row_offset = row * self.number_of_rows
		column_offset = column
		index = row_offset + column_offset

		return index

	def get_cell_at_location(self, location: Location) -> Optional[GridCell]:
		row = location.y
		column = location.x
		row_is_out_of_bounds = row < 0 or row > self.number_of_rows - 1
		column_is_out_of_bounds = column < 0 or column > self.number_of_columns - 1
		if row_is_out_of_bounds or column_is_out_of_bounds:
			return None

		index = self.get_cell_index_at(location)

		return self.cells[index]

	def get_cell_neighbors_for_location(self, location: Location) -> [GridCell]:
		north_neighbor_location = Location(location.x, location.y - 1)
		east_neighbor_location = Location(location.x + 1, location.y)
		west_neighbor_location = Location(location.x - 1, location.y)
		south_neighbor_location = Location(location.x, location.y + 1)

		print("get_cell_neighbors_for_location", location, [north_neighbor_location, east_neighbor_location, west_neighbor_location, south_neighbor_location])

		north_neighbor = self.get_cell_at_location(north_neighbor_location)
		east_neighbor = self.get_cell_at_location(east_neighbor_location)
		west_neighbor = self.get_cell_at_location(west_neighbor_location)
		south_neighbor = self.get_cell_at_location(south_neighbor_location)



		return [neighbor for neighbor in [north_neighbor, east_neighbor, west_neighbor, south_neighbor] if neighbor is not None]

@dataclass
class MazeGrid(Grid):
	cells: List[MazeGridCell]

	def __init__(self, number_of_rows: int, number_of_columns: int):
		self.number_of_rows = number_of_rows
		self.number_of_columns = number_of_columns
		self.cells = []

		for row in range(0, number_of_rows):
			for column in range(0, number_of_columns):
				cell = MazeGridCell(Location(column, row), MazeGridCellType.PATH)
				self.cells.append(cell)

	def update_cell_type_at_location(self, location: Location, cell_type: MazeGridCellType):
		row = location.y
		column = location.x
		row_is_out_of_bounds = row < 0 or row > self.number_of_rows - 1
		column_is_out_of_bounds = column < 0 or column > self.number_of_columns - 1
		if row_is_out_of_bounds or column_is_out_of_bounds:
			return None

		index = self.get_cell_index_at(location)
		self.cells[index].cell_type = cell_type


@dataclass
class MazeGameState():
	grid: MazeGrid
	player: MazePlayer
	total_movement_count: int

class MazePlayerMovementEvent(Enum):
	MOVE_UP = 1
	MOVE_LEFT = 2
	MOVE_RIGHT = 3
	MOVE_DOWN = 4


@dataclass
class MazePlayerController():
	def move_player_to_location(self, player: MazePlayer, mazeGrid: MazeGrid, new_location: Location) -> bool:
		neighbors = mazeGrid.get_cell_neighbors_for_location(player.location)
		wall_neighbors = filter(lambda x: x.cell_type == MazeGridCellType.WALL, neighbors)
		new_location_blocked_by_neighbor = any(wall_neighbor.location == new_location for wall_neighbor in wall_neighbors)
		print(player, new_location, neighbors)

		row = new_location.y
		column = new_location.x
		row_is_out_of_bounds = row < 0 or row > mazeGrid.number_of_rows - 1
		column_is_out_of_bounds = column < 0 or column > mazeGrid.number_of_columns - 1
		if row_is_out_of_bounds or column_is_out_of_bounds:
			return False

		if not new_location_blocked_by_neighbor:
			player.location = new_location
			return True
		else:
			return False

	def move_player_up(self, player: MazePlayer, mazeGrid: MazeGrid,) -> bool:
		new_location = Location(player.location.x, player.location.y - 1)
		return self.move_player_to_location(player, mazeGrid, new_location)

	def move_player_left(self, player: MazePlayer, mazeGrid: MazeGrid,) -> bool:
		new_location = Location(player.location.x - 1, player.location.y)
		return self.move_player_to_location(player, mazeGrid, new_location)

	def move_player_right(self, player: MazePlayer, mazeGrid: MazeGrid,) -> bool:
		new_location = Location(player.location.x + 1, player.location.y)
		return self.move_player_to_location(player, mazeGrid, new_location)

	def move_player_down(self, player: MazePlayer, mazeGrid: MazeGrid,) -> bool:
		new_location = Location(player.location.x, player.location.y + 1)
		return self.move_player_to_location(player, mazeGrid, new_location)		

	def handle_maze_player_movement_event(self, player: MazePlayer, mazeGrid: MazeGrid, event: MazePlayerMovementEvent) -> bool:
		if event == MazePlayerMovementEvent.MOVE_UP:
			return self.move_player_up(player, mazeGrid)
		elif event == MazePlayerMovementEvent.MOVE_LEFT:
			return self.move_player_left(player, mazeGrid)
		elif event == MazePlayerMovementEvent.MOVE_RIGHT:
			return self.move_player_right(player, mazeGrid)
		elif event == MazePlayerMovementEvent.MOVE_DOWN:
			return self.move_player_down(player, mazeGrid)



@dataclass
class MazeGame():
	state: MazeGameState
	controller: MazePlayerController








#MAZEGEN
def surroundingCells(maze, rand_wall):
	s_cells = 0
	if (maze[rand_wall[0]-1][rand_wall[1]] == MazeGridCellType.PATH):
		s_cells += 1
	if (maze[rand_wall[0]+1][rand_wall[1]] == MazeGridCellType.PATH):
		s_cells += 1
	if (maze[rand_wall[0]][rand_wall[1]-1] == MazeGridCellType.PATH):
		s_cells +=1
	if (maze[rand_wall[0]][rand_wall[1]+1] == MazeGridCellType.PATH):
		s_cells += 1

	return s_cells


def makeMazeGrid(rows: int, columns: int) -> MazeGrid:
	## Main code
	# Init variables
	wall = MazeGridCellType.WALL
	cell = MazeGridCellType.PATH
	unvisited = None
	height = rows
	width = columns
	maze = []

	# Denote all cells as unvisited
	for i in range(0, height):
		line = []
		for j in range(0, width):
			line.append(unvisited)
		maze.append(line)

	# Randomize starting point and set it a cell
	starting_height = int(random.random()*height)
	starting_width = int(random.random()*width)
	if (starting_height == 0):
		starting_height += 1
	if (starting_height == height-1):
		starting_height -= 1
	if (starting_width == 0):
		starting_width += 1
	if (starting_width == width-1):
		starting_width -= 1

	# Mark it as cell and add surrounding walls to the list
	maze[starting_height][starting_width] = cell
	walls = []
	walls.append([starting_height - 1, starting_width])
	walls.append([starting_height, starting_width - 1])
	walls.append([starting_height, starting_width + 1])
	walls.append([starting_height + 1, starting_width])

	# Denote walls in maze
	maze[starting_height-1][starting_width] = MazeGridCellType.WALL
	maze[starting_height][starting_width - 1] = MazeGridCellType.WALL
	maze[starting_height][starting_width + 1] = MazeGridCellType.WALL
	maze[starting_height + 1][starting_width] = MazeGridCellType.WALL

	while (walls):
		# Pick a random wall
		rand_wall = walls[int(random.random()*len(walls))-1]

		# Check if it is a left wall
		if (rand_wall[1] != 0):
			if (maze[rand_wall[0]][rand_wall[1]-1] == None and maze[rand_wall[0]][rand_wall[1]+1] == MazeGridCellType.PATH):
				# Find the number of surrounding cells
				s_cells = surroundingCells(maze, rand_wall)

				if (s_cells < 2):
					# Denote the new path
					maze[rand_wall[0]][rand_wall[1]] = MazeGridCellType.PATH

					# Mark the new walls
					# Upper cell
					if (rand_wall[0] != 0):
						if (maze[rand_wall[0]-1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]-1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]-1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]-1, rand_wall[1]])


					# Bottom cell
					if (rand_wall[0] != height-1):
						if (maze[rand_wall[0]+1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]+1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]+1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]+1, rand_wall[1]])

					# Leftmost cell
					if (rand_wall[1] != 0):	
						if (maze[rand_wall[0]][rand_wall[1]-1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]-1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]-1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]-1])
				

				# Delete wall
				for wall in walls:
					if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
						walls.remove(wall)

				continue

		# Check if it is an upper wall
		if (rand_wall[0] != 0):
			if (maze[rand_wall[0]-1][rand_wall[1]] == None and maze[rand_wall[0]+1][rand_wall[1]] == MazeGridCellType.PATH):

				s_cells = surroundingCells(maze, rand_wall)
				if (s_cells < 2):
					# Denote the new path
					maze[rand_wall[0]][rand_wall[1]] = MazeGridCellType.PATH

					# Mark the new walls
					# Upper cell
					if (rand_wall[0] != 0):
						if (maze[rand_wall[0]-1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]-1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]-1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]-1, rand_wall[1]])

					# Leftmost cell
					if (rand_wall[1] != 0):
						if (maze[rand_wall[0]][rand_wall[1]-1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]-1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]-1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]-1])

					# Rightmost cell
					if (rand_wall[1] != width-1):
						if (maze[rand_wall[0]][rand_wall[1]+1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]+1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]+1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]+1])

				# Delete wall
				for wall in walls:
					if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
						walls.remove(wall)

				continue

		# Check the bottom wall
		if (rand_wall[0] != height-1):
			if (maze[rand_wall[0]+1][rand_wall[1]] == None and maze[rand_wall[0]-1][rand_wall[1]] == MazeGridCellType.PATH):

				s_cells = surroundingCells(maze, rand_wall)
				if (s_cells < 2):
					# Denote the new path
					maze[rand_wall[0]][rand_wall[1]] = MazeGridCellType.PATH

					# Mark the new walls
					if (rand_wall[0] != height-1):
						if (maze[rand_wall[0]+1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]+1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]+1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]+1, rand_wall[1]])
					if (rand_wall[1] != 0):
						if (maze[rand_wall[0]][rand_wall[1]-1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]-1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]-1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]-1])
					if (rand_wall[1] != width-1):
						if (maze[rand_wall[0]][rand_wall[1]+1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]+1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]+1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]+1])

				# Delete wall
				for wall in walls:
					if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
						walls.remove(wall)


				continue

		# Check the right wall
		if (rand_wall[1] != width-1):
			if (maze[rand_wall[0]][rand_wall[1]+1] == None and maze[rand_wall[0]][rand_wall[1]-1] == MazeGridCellType.PATH):

				s_cells = surroundingCells(maze, rand_wall)
				if (s_cells < 2):
					# Denote the new path
					maze[rand_wall[0]][rand_wall[1]] = MazeGridCellType.PATH

					# Mark the new walls
					if (rand_wall[1] != width-1):
						if (maze[rand_wall[0]][rand_wall[1]+1] != MazeGridCellType.PATH):
							maze[rand_wall[0]][rand_wall[1]+1] = MazeGridCellType.WALL
						if ([rand_wall[0], rand_wall[1]+1] not in walls):
							walls.append([rand_wall[0], rand_wall[1]+1])
					if (rand_wall[0] != height-1):
						if (maze[rand_wall[0]+1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]+1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]+1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]+1, rand_wall[1]])
					if (rand_wall[0] != 0):	
						if (maze[rand_wall[0]-1][rand_wall[1]] != MazeGridCellType.PATH):
							maze[rand_wall[0]-1][rand_wall[1]] = MazeGridCellType.WALL
						if ([rand_wall[0]-1, rand_wall[1]] not in walls):
							walls.append([rand_wall[0]-1, rand_wall[1]])

				# Delete wall
				for wall in walls:
					if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
						walls.remove(wall)

				continue

		# Delete the wall from the list anyway
		for wall in walls:
			if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
				walls.remove(wall)
		


	# Mark the remaining unvisited cells as walls
	for i in range(0, height):
		for j in range(0, width):
			if (maze[i][j] == None):
				maze[i][j] = MazeGridCellType.WALL

	# Set entrance and exit
	for i in range(0, width):
		if (maze[1][i] == MazeGridCellType.PATH):
			maze[0][i] = MazeGridCellType.PATH
			break

	for i in range(width-1, 0, -1):
		if (maze[height-2][i] == MazeGridCellType.PATH):
			maze[height-1][i] = MazeGridCellType.PATH
			break

	grid = MazeGrid(rows, columns)

	for row in range(rows):
		for column in range(columns):
			cell_type = maze[row][column]
			grid.update_cell_type_at_location(Location(column, row), cell_type)

	return grid
#MAZEGEN





#GAME

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
INITIAL_WINDOW_HEIGHT = 400
INITIAL_WINDOW_WIDTH = 400
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0

CURR_X = 0
CURR_Y = 0

def startgame(maze_game: MazeGame):
	global SCREEN, CLOCK, WINDOW_WIDTH, WINDOW_HEIGHT, CURR_Y, CURR_X
	pygame.init()
	SCREEN = pygame.display.set_mode((INITIAL_WINDOW_HEIGHT, INITIAL_WINDOW_WIDTH), pygame.RESIZABLE)
	CLOCK = pygame.time.Clock()
	SCREEN.fill(WHITE)

	while True:
		WINDOW_WIDTH, WINDOW_HEIGHT = SCREEN.get_size()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				# sys.exit()
			elif event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_UP or event.key == pygame.K_w):
					maze_game.controller.handle_maze_player_movement_event(maze_game.state.player, maze_game.state.grid, MazePlayerMovementEvent.MOVE_UP)
				elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
					maze_game.controller.handle_maze_player_movement_event(maze_game.state.player, maze_game.state.grid, MazePlayerMovementEvent.MOVE_DOWN)
				elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
					maze_game.controller.handle_maze_player_movement_event(maze_game.state.player, maze_game.state.grid, MazePlayerMovementEvent.MOVE_RIGHT)
				elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
					maze_game.controller.handle_maze_player_movement_event(maze_game.state.player, maze_game.state.grid, MazePlayerMovementEvent.MOVE_LEFT)

		drawGrid(SCREEN, maze_game.state.grid, SCREEN.get_clip())
		drawPlayer(SCREEN, maze_game.state.player, maze_game.state.grid, SCREEN.get_clip())
		pygame.display.update()

def drawGrid(surface: Surface, grid: MazeGrid, gridRectangle: Rect):
	surface.fill(BLACK)

	blockWidth = (gridRectangle.width // grid.number_of_rows)
	blockHeight = (gridRectangle.height // grid.number_of_columns)

	for row in range(grid.number_of_rows):
		for column in range(grid.number_of_columns):
			cell = grid.get_cell_at_location(Location(column, row))
			x = column * blockWidth
			y = row * blockHeight
			rect = Rect(x, y, blockWidth, blockHeight)

			if (cell.cell_type == MazeGridCellType.WALL):
				pygame.draw.rect(surface, Color(0, 0, 255, 255), rect)
			else:
				pygame.draw.rect(surface, Color(255, 255, 255, 255), rect)

def drawPlayer(surface: Surface, player: MazePlayer, grid: MazeGrid, gridRectangle: Rect):
	blockWidth = (gridRectangle.width // grid.number_of_rows)
	blockHeight = (gridRectangle.height // grid.number_of_columns)
	x = player.location.x * blockWidth
	y = player.location.y * blockHeight
	rect = Rect(x, y, blockWidth, blockHeight)
	pygame.draw.rect(surface, Color(255, 0, 0, 255), rect)






def main():
	maze_grid = makeMazeGrid(25, 25)
	maze_player = MazePlayer(Location(1, 1))
	controller = MazePlayerController()
	maze_state = MazeGameState(maze_grid, maze_player, 0)
	maze_game = MazeGame(maze_state, controller)

	print(maze_grid)
	startgame(maze_game)


if __name__ == '__main__':
	main()