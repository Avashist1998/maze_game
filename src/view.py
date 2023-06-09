"""Maze view class."""

import pygame

from src.event import Event, StartGameEvent, QuitEvent, TickEvent
from src.event_manager import EventManager
from src.event_listener import EventListener
from src.maze_game import MazeGame
from src.maze_visualization import MazeGameVisualization


class MazeView(EventListener):
    """Draws the model state onto the screen."""

    def __init__(self, event_manager: EventManager, maze: MazeGame):
        """Constructor for the maze view.

        Args:
            event_manager: The event manager.
            maze: The maze game.

        """
        self.maze = maze
        self.is_initialized = False
        self.clock = pygame.time.Clock()
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.maze_visualization = MazeGameVisualization(720, 1280)

    def notify(self, event: Event):
        """Receive events posted to the message queue.

        Args:
            event: The event that was posted.
        """

        if isinstance(event, StartGameEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            self.is_initialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            self.draw()
            self.clock.tick(30)

    def draw(self):
        """Draw the current game state on screen."""

        if not self.is_initialized:
            return
        self.maze_visualization.draw_game(self.maze)
        pygame.display.update()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        self.is_initialized = True
        self.clock = pygame.time.Clock()
