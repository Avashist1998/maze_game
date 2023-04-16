"""Defining the game engine."""
import asyncio
from typing import Final

from src.event_manager import EventManager
from src.event_listener import EventListener
from src.event import (Direction, Event, QuitEvent, StartGameEvent, TickEvent,
                       MovementEvent, SelectEvent, PauseEvent, EscapeEvent)
from src.maze_game import MazeGame, MazeGameState
from src.logger import init_logger

SCREEN_WIDTH: Final = 1280
SCREEN_HEIGHT: Final = 720
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100

LOGGER: Final = init_logger(__name__)


class GameEngine(EventListener):
    """The game engine class."""

    def __init__(self, event_manager: EventManager, maze: MazeGame):
        """Constructor for the game engine.

        Args:
            event_manager: The event manager.
        """

        self.running = True
        self.maze = maze
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

    def move(self, direction: Direction):
        """Move the player in the given direction.

        Args:
            direction: The direction to move the player.
        """
        if self.maze.state == MazeGameState.PLAYING:
            self.maze.move(direction)
        elif self.maze.state == MazeGameState.MENU:
            if direction == Direction.UP:
                self.maze.main_menu_layer.move_up()
            elif direction == Direction.DOWN:
                self.maze.main_menu_layer.move_down()
        elif self.maze.state == MazeGameState.PAUSED:
            if direction == Direction.UP:
                self.maze.pause_menu_layer.move_up()
            elif direction == Direction.DOWN:
                self.maze.pause_menu_layer.move_down()

    def pause(self):
        """Process pause event."""
        if self.maze.state == MazeGameState.PAUSED:
            self.maze.set_state(MazeGameState.PLAYING)
        else:
            self.maze.set_state(MazeGameState.PAUSED)

    def select(self):
        """Process select event."""
        if self.maze.state == MazeGameState.MENU:
            if self.maze.main_menu_layer.get_current_option() == "Play":
                self.maze.set_state(MazeGameState.PLAYING)
            elif self.maze.main_menu_layer.get_current_option() == "Quit":
                self.event_manager.post(QuitEvent())
        elif self.maze.state == MazeGameState.PAUSED:
            if self.maze.pause_menu_layer.get_current_option() == "Resume":
                self.maze.set_state(MazeGameState.PLAYING)
            elif self.maze.pause_menu_layer.get_current_option() == "Quit":
                self.event_manager.post(QuitEvent())

    def notify(self, event: Event):
        """Receive an event posted to the message queue.

        Args:
            event: The event to receive.
        """
        if not isinstance(event, TickEvent):
            LOGGER.info("Received event: %s", event)
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, MovementEvent):
            self.move(event.direction)
        elif isinstance(event, PauseEvent):
            self.pause()
        elif isinstance(event, SelectEvent):
            self.select()
        elif isinstance(event, EscapeEvent):
            if self.maze.state != MazeGameState.MENU:
                self.maze.set_state(MazeGameState.MENU)

    async def run(self):
        """Run the game engine."""
        LOGGER.info("Starting game engine")
        self.event_manager.post(StartGameEvent())
        while self.running:
            self.event_manager.post(TickEvent())
            await asyncio.sleep(0)
        LOGGER.info("Stopping game engine")
