"""Maze board class."""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MazeBoard:
    """Maze board class."""
    board: List[List[int]]
    start: Tuple[int, int]
    end: Tuple[int, int]
    curr_pos: Tuple[int, int]
    solved: bool = False
