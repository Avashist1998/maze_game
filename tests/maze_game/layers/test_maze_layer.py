"""Testing Maze Layer Class."""
from unittest import TestCase, mock
from typing import List, Tuple

from src.maze_game.layers.maze_layer import MazeLayer
from src.maze_game.maze_board import MazeBoard
from src.maze_game.maze_game_object import MazeGameObject


def generate_prim_maze(
        height: int, width: int
) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[int]]]:
    """Fixture for generating a maze."""
    maze: List[List[int]] = [[MazeGameObject.PATH.value for _ in range(width)]
                             for _ in range(height)]
    for i in range(width):
        for j in range(height):
            if i == 0 or j == 0 or i == width - 1 or j == height - 1:
                maze[i][j] = MazeGameObject.WALL.value

    maze[0][1] = MazeGameObject.PLAYER_TILE.value
    maze[height - 1][width - 2] = MazeGameObject.GOAL.value

    return ((0, 1), (height - 1, width - 1), maze)


class TestMazeLayer(TestCase):
    """Test the Maze Layer Class."""

    @mock.patch("src.maze_game.layers.maze_layer.generate_prim_maze")
    def test_maze_layer_board_setup(self,
                                    mock_generate_prim_maze: mock.MagicMock):
        """Test that maze layer is correctly generated."""
        mock_generate_prim_maze.return_value = generate_prim_maze(5, 5)
        maze_layer = MazeLayer(5, 5)
        exp_board = MazeBoard(
            generate_prim_maze(5, 5)[2],
            generate_prim_maze(5, 5)[0],
            generate_prim_maze(5, 5)[1], (0, 1))
        self.assertEqual(maze_layer.step_count, 0)
        self.assertEqual(maze_layer.level_count, 1)
        self.assertEqual(maze_layer.tile_width, 100 // 1)
        self.assertEqual(maze_layer.tile_height, 100 // 1)
        self.assertTrue(isinstance(maze_layer.get_board(), list))
        self.assertEqual(maze_layer.get_board(), exp_board.board)

    @mock.patch("src.maze_game.layers.maze_layer.generate_prim_maze")
    def test_maze_layer_board_movement(
            self, mock_generate_prim_maze: mock.MagicMock):
        """Test that maze layer is correctly generated."""
        mock_generate_prim_maze.return_value = generate_prim_maze(5, 5)
        maze_layer = MazeLayer(5, 5)

        maze_layer.move_up()
        exp_location = (0, 1)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)
        maze_layer.move_up()
        self.assertEqual(maze_layer.board.curr_pos, exp_location)

        maze_layer.move_down()
        exp_location = (1, 1)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)
        maze_layer.move_down()
        exp_location = (2, 1)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)

        maze_layer.move_left()
        exp_location = (2, 1)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)

        maze_layer.move_right()
        exp_location = (2, 2)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)

        maze_layer.move_left()
        exp_location = (2, 1)
        self.assertEqual(maze_layer.board.curr_pos, exp_location)

    @mock.patch("src.maze_game.layers.maze_layer.generate_prim_maze")
    def test_maze_layer_solved(self, mock_generate_prim_maze: mock.MagicMock):
        """Test that maze layer is correctly generated."""
        mock_generate_prim_maze.return_value = generate_prim_maze(5, 5)
        maze_layer = MazeLayer(5, 5)

        maze_layer.move_down()
        maze_layer.move_down()
        maze_layer.move_down()
        maze_layer.move_down()
        maze_layer.move_right()
        maze_layer.move_right()
        maze_layer.move_right()
        maze_layer.move_down()

        self.assertEqual(maze_layer.board.curr_pos, (4, 3))
        self.assertTrue(maze_layer.is_solved())
