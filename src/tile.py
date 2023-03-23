from dataclasses import dataclass
from pygame import Color


@dataclass
class Tile:
    row: int
    col: int
    width: int
    height: int
    tile_color: Color
    border_color: Color
