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

    def post_keyboard_event(self):
        """Get events from the keyboard."""

        for event in py_event.get():
            if event.type == QUIT:
                self.event_manager.post(QuitEvent())
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.event_manager.post(EscapeEvent())
                elif event.key == K_RETURN:
                    self.event_manager.post(SelectEvent())
                elif event.key == K_SPACE:
                    self.event_manager.post(PauseEvent())
                elif event.key == K_UP:
                    self.event_manager.post(MovementEvent(Direction.UP))
                elif event.key == K_DOWN:
                    self.event_manager.post(MovementEvent(Direction.DOWN))
                elif event.key == K_LEFT:
                    self.event_manager.post(MovementEvent(Direction.LEFT))
                elif event.key == K_RIGHT:
                    self.event_manager.post(MovementEvent(Direction.RIGHT))
                else:
                    self.event_manager.post(
                        KeyboardEvent(event.key.__name__, None))

    def notify(self, event: Event):
        """Receive events posted to the message queue."""
        if isinstance(event, TickEvent):
            self.post_keyboard_event()
