"""Testing Maze Board Generation."""
import unittest

from src.maze_generation import generate_prim_maze


class TestMazeGeneration(unittest.TestCase):
    """Test the Maze Board Generation."""

    def maze_size_generation_test(self):
        """Test that maze of appropriated size is generated"""

        expect_shape = (5, 10)
        _, _, generated_maze = generate_prim_maze(expect_shape[0],
                                                  expect_shape[1])

        assert len(generated_maze) == expect_shape[0]
        assert len(generated_maze[0]) == expect_shape[1]
