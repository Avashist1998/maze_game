"""Maze Tile Object definition."""

from dataclasses import dataclass
from pygame import Color


@dataclass
class Tile:
    """Maze tile data object definition."""
    row: int
    col: int
    width: int
    height: int
    tile_color: Color
    border_color: Color
