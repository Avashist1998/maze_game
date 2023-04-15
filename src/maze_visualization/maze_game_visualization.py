"""Defines Pygame visualization of the maze"""
from typing import Final, Tuple
import pygame

from src.maze_game.layers.maze_layer import MazeLayer
from src.maze_game.layers.options_layer import OptionsLayer
from src.maze_game import MazeGame, MazeGameState, MazeGameObject

from src.maze_visualization.tile import Tile
from src.maze_visualization.utils import draw_text, MazeText, ScreenSize
from src.maze_visualization.game_color import (GAME_OVER_TEXT_COLOR,
                                               MESSAGE_BACKGROUND_COLOR,
                                               TILE_BORDER_COLOR, PLAYER_COLOR,
                                               PATH_COLOR, GOAL_COLOR,
                                               VISITED_COLOR, WALL_COLOR,
                                               SELECTED_BACKGROUND_COLOR)


class MazeGameVisualization:
    """Maze Game visualization class"""

    def __init__(self, screen_height: int, screen_width: int):
        """Maze Game visualization class constructor.

        Args:
            screen_height: pixel height of user screen
            screen_width: pixel width of the user screen
        """

        pygame.init()
        pygame.display.set_caption("Maze")
        self.text_color = pygame.Color("black")
        # Museo Sans Cyrillic 500 WhatFontIs.com
        self.font = pygame.font.SysFont("sans", 60)
        self.small_font: Final = pygame.font.SysFont("sans", 40)
        self.screen_height, self.screen_width, = screen_height, screen_width
        self.screen: pygame.Surface = pygame.display.set_mode(
            [screen_width, screen_height])

    def draw_image(self,
                   top_left_x: int,
                   top_left_y: int,
                   image_path: str,
                   scale: float = 1):
        """Draws an image on a given surface"""

        img = pygame.image.load(image_path).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        scaled_image = pygame.transform.scale(
            img, (int(width * scale), int(height * scale)))
        self.screen.blit(scaled_image, (top_left_x, top_left_y))

    def draw_background(self):
        """Draws the background of on the screen."""

        bg_img = pygame.image.load("img/background.jpg")
        background = pygame.transform.scale(
            bg_img, (self.screen_width, self.screen_height))
        self.screen.blit(background, (0, 0))

    def draw_option(self,
                    option_text: str,
                    option_space: ScreenSize,
                    selected: bool = False):
        """Draws an option on the screen."""
        bg_color = MESSAGE_BACKGROUND_COLOR
        if selected:
            bg_color = SELECTED_BACKGROUND_COLOR

        pygame.draw.rect(
            self.screen, bg_color,
            pygame.Rect(option_space.top_left_x, option_space.top_left_y,
                        option_space.width, option_space.height))

        pygame.draw.rect(
            self.screen, TILE_BORDER_COLOR,
            pygame.Rect(option_space.top_left_x, option_space.top_left_y,
                        option_space.width, option_space.height), 5)

        img = self.font.render(option_text, True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        option = MazeText(
            option_text, self.text_color, self.font, option_space.top_left_x +
            option_space.width // 2 - text_width // 2,
            option_space.top_left_y + option_space.height // 2 -
            text_height // 2)
        draw_text(option, self.screen)

    def draw_options(self,
                     options: OptionsLayer,
                     options_space: ScreenSize,
                     padding: Tuple[int, int] = (50, 10)):
        """Draws the options on the screen."""

        number_of_options = len(options.options.keys())
        option_width = options_space.width - padding[0] * 2
        option_height = (options_space.height -
                         padding[1]) // number_of_options - padding[1]

        # # print(option_space.height - padding[1])
        # # print(number_of_options, option_width, option_height)
        # print(options_space.top_left_x)

        for i, option_text in enumerate(options.options.keys()):
            top_left_x = options_space.top_left_x + padding[0]
            top_left_y = options_space.top_left_y + padding[1] + i * (
                option_height + padding[1])
            option_space = ScreenSize(option_width, option_height, top_left_x,
                                      top_left_y)
            self.draw_option(option_text, option_space,
                             option_text == options.current_option)

    def draw_main_menu(self, menu_layer: OptionsLayer):
        """Draws the main menu on the screen."""

        img = self.font.render("Menu Screen", True, pygame.Color("Blue"))
        text_width, _ = img.get_width(), img.get_height()

        title_text = MazeText("Menu Screen", self.text_color, self.font,
                              self.screen_width // 2 - text_width // 2, 50)

        draw_text(title_text, self.screen)
        x_padding = 100
        y_padding = 50 + img.get_height()
        menu_option_space = ScreenSize(self.screen_width - 2 * x_padding,
                                       self.screen_height - 2 * y_padding,
                                       x_padding, y_padding)

        self.draw_options(menu_layer, menu_option_space, (250, 50))

    def draw_pause_screen(self, pause_layer: OptionsLayer):
        """Draws the pause menu on the screen."""

        img = self.font.render("Paused", True, pygame.Color("Blue"))
        text_width, _ = img.get_width(), img.get_height()

        title_text = MazeText("Paused", self.text_color, self.font,
                              self.screen_width // 2 - text_width // 2, 50)

        draw_text(title_text, self.screen)

        x_padding = 150
        y_padding = 100 + img.get_height()
        menu_option_space = ScreenSize(self.screen_width - 2 * x_padding,
                                       self.screen_height - 2 * y_padding,
                                       x_padding, y_padding)

        self.draw_options(pause_layer, menu_option_space, (250, 50))

    def draw_game_over(self):
        """Draws the game move message."""
        bg_width, bg_height = 800, 300
        pygame.draw.rect(
            self.screen, MESSAGE_BACKGROUND_COLOR,
            pygame.Rect(self.screen_width // 2 - bg_width // 2,
                        self.screen_height // 2 - bg_height // 2, bg_width,
                        bg_height))

        pygame.draw.rect(
            self.screen, GAME_OVER_TEXT_COLOR,
            pygame.Rect(self.screen_width // 2 - bg_width // 2,
                        self.screen_height // 2 - bg_height // 2, bg_width,
                        bg_height), int(150 * 0.1))

        img = self.font.render("Game Over", True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        game_over_text_left_x = self.screen_width // 2 - text_width // 2
        game_over_text_text_left_y = self.screen_height // 2 - text_height // 2
        game_over_text = MazeText("Game Over", GAME_OVER_TEXT_COLOR, self.font,
                                  game_over_text_left_x,
                                  game_over_text_text_left_y)
        draw_text(game_over_text, self.screen)

        img = self.small_font.render("Press down arrow to start next level",
                                     True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        next_level_message_left_x = self.screen_width // 2 - text_width // 2
        next_level_message_left_y = self.screen_height // 2 - text_height // 2 + 75
        next_level_message = MazeText("Press down arrow to start next level",
                                      GAME_OVER_TEXT_COLOR, self.small_font,
                                      next_level_message_left_x,
                                      next_level_message_left_y)
        draw_text(next_level_message, self.screen)

    def draw_tile(self, tile: Tile):
        """Draws the game tile on the screen.

        Args:
            board_x: top left x pixel location of the maze board.
            board_y: top left y pixel location of the maze board.
            tile: tile that needs to be drawn.
        """

        pygame.draw.rect(
            self.screen, tile.tile_color,
            pygame.Rect(tile.tile_space.top_left_x, tile.tile_space.top_left_y,
                        tile.tile_space.width, tile.tile_space.height), 0)
        if int(tile.tile_space.width * 0.1) > 0:
            pygame.draw.rect(
                self.screen, tile.border_color,
                pygame.Rect(tile.tile_space.top_left_x,
                            tile.tile_space.top_left_y, tile.tile_space.width,
                            tile.tile_space.height),
                int(tile.tile_space.width * 0.1))

    def draw_maze(self, maze: MazeLayer):
        """Draws the maze game board on the screen.
        Args:
            maze: MazeGameLayer object.
        """

        board = maze.get_board()
        row, col = len(board), len(board[0])
        maze_screen_width, maze_screen_height = self.screen_width - 100, self.screen_height - 100
        tile_width, tile_height = maze_screen_width // col, maze_screen_height // row

        for i in range(row):
            for j in range(col):
                if board[i][j] == MazeGameObject.WALL.value:
                    tile_color = WALL_COLOR
                elif board[i][j] == MazeGameObject.GOAL.value:
                    tile_color = GOAL_COLOR
                elif board[i][j] == MazeGameObject.VISITED_TILE.value:
                    tile_color = VISITED_COLOR
                elif board[i][j] == MazeGameObject.PLAYER_TILE.value:
                    tile_color = PLAYER_COLOR
                else:
                    tile_color = PATH_COLOR
                tile_space = ScreenSize(tile_width, tile_height,
                                        50 + j * tile_width,
                                        75 + i * tile_height)
                tile = Tile(tile_color, TILE_BORDER_COLOR, tile_space)
                self.draw_tile(tile)

    def draw_level_counter(self, maze: MazeLayer):
        """Draws the level on the screen.

        Args:
            maze: MazeGameLayer Object with the level number

        """
        img = self.small_font.render(f"Level: {maze.level_count}", True,
                                     pygame.Color("Black"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(img, (50 + text_width // 2, text_height // 2))

    def draw_step_counter(self, maze: MazeLayer):
        """Draws the steps on the screen.

        Args:
            maze: MazeGameLayer object with the step count

        """

        img = self.small_font.render(f"Steps: {maze.step_count}", True,
                                     pygame.Color("Black"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(
            img,
            (3 * self.screen_width // 4 - text_width // 2, text_height // 2))

    def draw_game(self, game: MazeGame):
        """Draws the game on the screen.

        Args:
            game: MazeGame object contain game state
        """

        self.draw_background()
        if game.state == MazeGameState.MENU:
            self.draw_main_menu(game.main_menu_layer)

        elif game.state == MazeGameState.PAUSED:
            self.draw_pause_screen(game.pause_menu_layer)

        else:
            self.draw_maze(game.curr_level_maze)
            self.draw_level_counter(game.curr_level_maze)
            self.draw_step_counter(game.curr_level_maze)
            if game.solved:
                self.draw_game_over()
