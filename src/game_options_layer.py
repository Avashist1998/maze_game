"""This module contains the GameOptionsLayer class."""
from typing import Dict


class GameOptionsLayer:
    """GAME OPTIONS LAYER CLASS"""

    def __init__(self, options: Dict[str, str], default: str):
        """GAME OPTIONS LAYER CLASS CONSTRUCTOR"""

        self.options = options
        self.default = default
        self.keys = list(options.keys())
        self.current_option = default
        self.current_option_index = self.keys.index(default)

    def get_current_option(self):
        """Returns the current option"""
        return self.current_option

    def move_up(self):
        """Moves the player one place up."""
        if self.current_option_index != 0:
            self.current_option_index -= 1
            self.current_option = self.keys[self.current_option_index]
        else:
            self.current_option_index = len(self.keys) - 1
            self.current_option = self.keys[self.current_option_index]

    def move_down(self):
        """Moves the player one place down."""
        if self.current_option_index != len(self.keys) - 1:
            self.current_option_index += 1
            self.current_option = self.keys[self.current_option_index]
        else:
            self.current_option_index = 0
            self.current_option = self.keys[self.current_option_index]
