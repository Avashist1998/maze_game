"""Testing the OptionsLayer class."""
from unittest import TestCase

from src.maze_game.layers.options_layer import OptionsLayer


class OptionsLayerTest(TestCase):
    """Test the OptionsLayer class."""

    def setUp(self):
        """Setup the test."""
        self.options = {"option1": "value1", "option2": "value2"}
        self.default = "option1"
        self.options_layer = OptionsLayer(self.options, self.default)

    def test_get_current_option(self):
        """Test that the current option is correctly returned."""
        self.assertEqual(self.options_layer.get_current_option(), self.default)

    def test_move_up(self):
        """Test that the current option is correctly moved up."""

        self.options_layer.move_up()
        self.assertEqual(self.options_layer.get_current_option(), "option2")

        self.options_layer.move_up()
        self.assertEqual(self.options_layer.get_current_option(), "option1")

    def test_move_down(self):
        """Test that the current option is correctly moved up."""

        self.options_layer.move_down()
        self.assertEqual(self.options_layer.get_current_option(), "option2")

        self.options_layer.move_down()
        self.assertEqual(self.options_layer.get_current_option(), "option1")
