"""Draw text function definition."""

from dataclasses import dataclass
from pygame.font import Font
from pygame import Color, Surface


@dataclass
class MazeText:
    """Maze Text dataclass"""
    text: str
    color: Color
    font: Font
    top_left_x: int
    top_left_y: int


@dataclass
class ScreenSize:
    """Screen size dataclass"""
    width: int
    height: int
    top_left_x: int
    top_left_y: int


def draw_text(text: MazeText, screen: Surface):
    """Draws text on the screen.

    Args:
        text: MazeText Object contain the text data
        screen: Surface that the text is drawn
    """

    img = text.font.render(text.text, True, text.color)
    screen.blit(img, (text.top_left_x, text.top_left_y))
