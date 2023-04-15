"""Handles keyboard input."""
from pygame import event as py_event
from pygame.constants import (K_UP, K_DOWN, K_RETURN, K_ESCAPE, K_RIGHT,
                              K_LEFT, K_SPACE, QUIT, KEYDOWN)

from src.event import (Event, QuitEvent, TickEvent, MovementEvent, Direction,
                       EscapeEvent, SelectEvent, PauseEvent, KeyboardEvent)
from src.event_manager import EventManager
from src.event_listener import EventListener


class Keyboard(EventListener):
    """Handles keyboard input."""

    def __init__(self, event_manager: EventManager):
        """Constructor for the keyboard controller.

        Args:
            event_manager: The event manager.
        """
        self.event_manager = event_manager
        event_manager.register_listener(self)

        self.key_event_map = {
            K_UP: MovementEvent(Direction.UP),
            K_DOWN: MovementEvent(Direction.DOWN),
            K_LEFT: MovementEvent(Direction.LEFT),
            K_RIGHT: MovementEvent(Direction.RIGHT),
            K_RETURN: SelectEvent(),
            K_ESCAPE: EscapeEvent(),
            K_SPACE: PauseEvent()
        }

    def post_keyboard_event(self):
        """Get events from the keyboard."""

        for event in py_event.get():
            if event.type == QUIT:
                self.event_manager.post(QuitEvent())
            if event.type == KEYDOWN:
                if event.key in self.key_event_map:
                    self.event_manager.post(self.key_event_map[event.key])
                else:
                    self.event_manager.post(
                        KeyboardEvent(event.key.__name__, None))

    def notify(self, event: Event):
        """Receive events posted to the message queue."""
        if isinstance(event, TickEvent):
            self.post_keyboard_event()
