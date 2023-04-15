"""Maze state definition."""
from enum import Enum


class MazeGameState(Enum):
    """Enum for managing the state of the MazeGame"""
    MENU = 0
    PLAYING = 1
    PAUSED = 2
