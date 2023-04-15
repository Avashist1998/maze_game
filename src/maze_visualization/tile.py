"""Maze Tile Object definition."""

from dataclasses import dataclass
from pygame import Color

from src.maze_visualization.utils import ScreenSize


@dataclass
class Tile:
    """Maze tile data object definition."""
    tile_color: Color
    border_color: Color
    tile_space: ScreenSize
