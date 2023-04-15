"""Event manager class."""
from typing import Set
from src.event import Event
from src.event_listener import EventListener


class EventManager:
    """We coordinate communication between the Model, View, and Controller."""

    def __init__(self) -> None:
        """Constructor for the event manager."""

        self.listeners: Set[EventListener] = set()

    def register_listener(self, listener: EventListener):
        """Add a listener to our listener set.

        Args:
            listener: The listener to add.
        """

        self.listeners.add(listener)

    def unregister_listener(self, listener: EventListener):
        """Remove a listener from our listener set.
        Args:
            listener: The listener to remove.
        """
        self.listeners.remove(listener)

    def post(self, event: Event):
        """Post a new event to the message queue and notifies the listeners.

        Args:
            event: The event to notified to the listeners.
        """

        for listener in self.listeners:
            listener.notify(event)
