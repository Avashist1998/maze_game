"""Testing Maze Board Generation."""
import unittest

from src.maze_game.maze_game_object import MazeGameObject
from src.maze_game.maze_generation import generate_prim_maze


class TestMazeGeneration(unittest.TestCase):
    """Test the Maze Board Generation."""

    def test_maze_dimensions_generation(self):
        """Test that maze of appropriated size is generated"""

        expect_shape = (5, 10)
        _, _, generated_maze = generate_prim_maze(expect_shape[0],
                                                  expect_shape[1])

        self.assertEqual(len(generated_maze), expect_shape[0])
        self.assertEqual(len(generated_maze[0]), expect_shape[1])

        expect_shape = (100, 100)
        _, _, generated_maze = generate_prim_maze(expect_shape[0],
                                                  expect_shape[1])

        self.assertEqual(len(generated_maze), expect_shape[0])
        self.assertEqual(len(generated_maze[0]), expect_shape[1])

        expect_shape = (10, 5)
        _, _, generated_maze = generate_prim_maze(expect_shape[0],
                                                  expect_shape[1])

        self.assertEqual(len(generated_maze), expect_shape[0])
        self.assertEqual(len(generated_maze[0]), expect_shape[1])

    def test_maze_initialized_position(self):
        """Test that start and end position are correctly indicated"""

        maze_shape = (5, 10)
        start_pos, end_pos, generated_maze = generate_prim_maze(
            maze_shape[0], maze_shape[1])

        self.assertEqual(start_pos[0], 0)
        self.assertEqual(end_pos[0], maze_shape[0] - 1)
        self.assertEqual(generated_maze[end_pos[0]][end_pos[1]],
                         MazeGameObject.GOAL.value)
        self.assertEqual(generated_maze[start_pos[0]][start_pos[1]],
                         MazeGameObject.PLAYER_TILE.value)

    def test_entry_and_exit(self):
        """Test that maze has an entry and exit"""

        maze_shape = (5, 10)
        start_pos, end_pos, generated_maze = generate_prim_maze(
            maze_shape[0], maze_shape[1])

        self.assertEqual(generated_maze[start_pos[0]][start_pos[1]],
                         MazeGameObject.PLAYER_TILE.value)
        self.assertEqual(generated_maze[end_pos[0]][end_pos[1]],
                         MazeGameObject.GOAL.value)

        for i in range(5):
            self.assertEqual(generated_maze[i][0], MazeGameObject.WALL.value)
            self.assertEqual(generated_maze[i][9], MazeGameObject.WALL.value)

        for i in range(10):

            if i != start_pos[1]:
                self.assertEqual(generated_maze[0][i],
                                 MazeGameObject.WALL.value)
            if i != end_pos[1]:
                self.assertEqual(generated_maze[4][i],
                                 MazeGameObject.WALL.value)
