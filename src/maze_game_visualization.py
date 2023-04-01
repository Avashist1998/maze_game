"""Defines Pygame visualization of the maze"""
from typing import Final
import pygame

from src.button import Button
from src.maze_game import MazeGameLayer
from src.maze_game_object import MazeGameObject
from src.utils import draw_text, MazeText
from src.tile import Tile
from src.maze_game import MazeGame, MazeGameState


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
        self.font = pygame.font.SysFont("arialblack", 60)
        self.small_font: Final = pygame.font.SysFont("arialblack", 30)
        self.screen_height, self.screen_width, = screen_height, screen_width
        self.screen: pygame.Surface = pygame.display.set_mode(
            [screen_width, screen_height])

    def draw_main_menu(self):
        """Draws the main menu on the screen."""

        exit_img = pygame.image.load("img/exitButton.png").convert_alpha()
        single_play_img = pygame.image.load(
            "img/playButton.png").convert_alpha()
        twitch_play_img = pygame.image.load(
            "img/twitchButton.png").convert_alpha()

        exit_button = Button(225, 450, exit_img, 1)
        single_play_button = Button(225, 150, single_play_img, 1)
        twitch_play_button = Button(225, 300, twitch_play_img, 1)

        self.screen.fill((255, 255, 255))
        img = self.font.render("Menu Screen", True, pygame.Color("Blue"))
        text_width, _ = img.get_width(), img.get_height()

        title_text = MazeText("Menu Screen", self.text_color, self.font,
                              self.screen_width // 2 - text_width // 2, 50)
        draw_text(title_text, self.screen)
        single_play_button.draw(self.screen)
        twitch_play_button.draw(self.screen)
        exit_button.draw(self.screen)

    def draw_game_over(self):
        """Draws the game move message."""

        pygame.draw.rect(
            self.screen, pygame.Color("white"),
            pygame.Rect(self.screen_width // 2 - 350 // 2,
                        self.screen_height // 2 - 100 // 2, 350, 100), 0, 10)

        img = self.font.render("Game Over", True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        game_over_text_left_x = self.screen_width // 2 - text_width // 2
        game_over_text_text_left_y = self.screen_height // 2 - text_height // 2
        game_over_text = MazeText("Game Over", pygame.Color("Blue"), self.font,
                                  game_over_text_left_x,
                                  game_over_text_text_left_y)
        draw_text(game_over_text, self.screen)

        img = self.small_font.render("Press down arrow to start next level",
                                     True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        next_level_message_left_x = self.screen_width // 2 - text_width // 2
        next_level_message_left_y = self.screen_height // 2 - text_height // 2 + 30
        next_level_message = MazeText("Press down arrow to start next level",
                                      pygame.Color("Blue"), self.small_font,
                                      next_level_message_left_x,
                                      next_level_message_left_y)
        draw_text(next_level_message, self.screen)

    def draw_tile(self, board_x: int, board_y: int, tile: Tile):
        """Draws the game tile on the screen.

        Args:
            board_x: top left x pixel location of the maze board.
            board_y: top left y pixel location of the maze board.
            tile: tile that needs to be drawn.
        """
        top_left_x, top_left_y = tile.col * tile.width, tile.row * tile.height
        pygame.draw.rect(
            self.screen, tile.tile_color,
            pygame.Rect(board_x + top_left_x, board_y + top_left_y, tile.width,
                        tile.height), 0)
        pygame.draw.rect(
            self.screen, tile.border_color,
            pygame.Rect(board_x + top_left_x, board_y + top_left_y, tile.width,
                        tile.height), 3)

    def draw_maze(self, maze: MazeGameLayer):
        """Draws the maze game board on the screen.
        Args:
            maze: MazeGameLayer object.
        """
        self.screen.fill((255, 255, 255))
        tile_width, tile_height = maze.tile_width, maze.tile_height
        board = maze.get_board()
        row, col = len(board), len(board[0])

        for i in range(row):
            for j in range(col):

                tile_border = pygame.Color("black")
                if board[i][j] == MazeGameObject.WALL.value:
                    tile_color = pygame.Color("blue")
                elif board[i][j] == MazeGameObject.GOAL.value:
                    tile_color = pygame.Color("red")
                elif board[i][j] == MazeGameObject.VISITED_TILE.value:
                    tile_color = pygame.Color("pink")
                elif board[i][j] == MazeGameObject.PLAYER_TILE.value:
                    tile_color = pygame.Color("green")
                else:
                    tile_color = pygame.Color("white")

                tile = Tile(i, j, tile_width, tile_height, tile_color,
                            tile_border)
                self.draw_tile(50, 50, tile)
        pygame.draw.rect(
            self.screen, pygame.Color("black"),
            pygame.Rect(50, 50, col * tile_width, row * tile_height), 3)

    def draw_level_counter(self, maze: MazeGameLayer):
        """Draws the level on the screen.

        Args:
            maze: MazeGameLayer Object with the level number

        """
        img = self.font.render(f"Level {maze.level_count}.", True,
                               pygame.Color("Black"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(
            img,
            (self.screen_width // 2 - text_width // 2, text_height // 2 - 15))

    def draw_step_counter(self, maze: MazeGameLayer):
        """Draws the steps on the screen.

        Args:
            maze: MazeGameLayer object with the step count

        """

        img = self.font.render(f"Step Counter: {maze.step_count}.", True,
                               pygame.Color("Black"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(img, (self.screen_width // 2 - text_width // 2,
                               self.screen_height - text_height // 2 - 25))

    def draw_game(self, game: MazeGame):
        """Draws the game on the screen.

        Args:
            game: MazeGame object contain game state
        """

        if game.state == MazeGameState.MENU:
            self.draw_main_menu()

        elif game.state == MazeGameState.PAUSED:
            print("we have paused the game!")

        else:
            self.draw_maze(game.curr_level_maze)
            self.draw_level_counter(game.curr_level_maze)
            self.draw_step_counter(game.curr_level_maze)
            if game.solved:
                self.draw_game_over()
