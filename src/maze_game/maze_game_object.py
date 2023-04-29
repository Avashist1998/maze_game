"""MazeGameObject enum definition"""
from enum import Enum


class MazeGameObject(Enum):
    """Defines the MazeGameObject"""
    PATH = 0
    WALL = 1
    GOAL = 2
    EMPTY = -1
    PLAYER_TILE = 7
    VISITED_TILE = 3
