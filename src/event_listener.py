"""This module contains the EventListener class."""
from abc import ABC, abstractmethod


class EventListener(ABC):
    """An abstract class that defines the interface for event listeners."""

    @abstractmethod
    def notify(self, event):
        """Receive an event posted to the message queue."""
        pass
