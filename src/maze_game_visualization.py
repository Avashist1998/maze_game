import pygame
from typing import Final

from src.tile import Tile
from src.button import Button
from src.maze_game import MazeGameLayer, MazeObject


class MazeGamePygameVisualization:

    def __init__(self, screen_height: int, screen_width: int):

        pygame.init()
        pygame.display.set_caption("Maze")

        self.text_color = pygame.Color("black")
        self.font = pygame.font.SysFont("arialblack", 60)
        self.small_font: Final = pygame.font.SysFont("arialblack", 30)
        self.screen_height, self.screen_width, = screen_height, screen_width
        self.screen: pygame.Surface = pygame.display.set_mode(
            [screen_width, screen_height])

    def draw_text(self, text: str, text_col: pygame.Color, x: int, y: int):

        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def draw_main_menu(self):
        exit_img = pygame.image.load("img/exitButton.png").convert_alpha()
        single_play_img = pygame.image.load(
            "img/playButton.png").convert_alpha()
        twitch_play_img = pygame.image.load(
            "img/twitchButton.png").convert_alpha()

        exit_button = Button(225, 450, exit_img, 1)
        single_play_button = Button(225, 150, single_play_img, 1)
        twitch_play_button = Button(225, 300, twitch_play_img, 1)

        self.screen.fill((255, 255, 255))
        self.draw_text("Menu Screen", self.text_color,
                       self.screen_width // 2 - 145, 50)
        single_play_button.draw(self.screen)
        twitch_play_button.draw(self.screen)
        exit_button.draw(self.screen)

    def draw_game_over(self):

        pygame.draw.rect(
            self.screen, pygame.Color("white"),
            pygame.Rect(self.screen_width // 2 - 350 // 2,
                        self.screen_height // 2 - 100 // 2, 350, 100), 0, 10)

        img = self.font.render("Game Over", True, pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(img, (self.screen_width // 2 - text_width // 2,
                               self.screen_height // 2 - text_height // 2))

        img = self.small_font.render("Press Enter to restart", True,
                                     pygame.Color("Blue"))
        text_width, text_height = img.get_width(), img.get_height()
        self.screen.blit(img,
                         (self.screen_width // 2 - text_width // 2,
                          self.screen_height // 2 - text_height // 2 + 30))

    def draw_tile(self, board_x: int, board_y: int, tile: Tile):
        x, y = tile.col * tile.width, tile.row * tile.height
        pygame.draw.rect(
            self.screen, tile.tile_color,
            pygame.Rect(board_x + x, board_y + y, tile.width, tile.height), 0)
        pygame.draw.rect(
            self.screen, tile.border_color,
            pygame.Rect(board_x + x, board_y + y, tile.width, tile.height), 3)

    def draw_maze(self, maze: MazeGameLayer):
        self.screen.fill((255, 255, 255))
        tile_width, tile_height = maze.tile_width, maze.tile_height
        board = maze.get_board()
        row, col = len(board), len(board[0])

        for i in range(row):
            for j in range(col):

                tile_border = pygame.Color("black")
                if board[i][j] == MazeObject.WALL.value:
                    tile_color = pygame.Color("blue")
                elif board[i][j] == MazeObject.GOAL.value:
                    tile_color = pygame.Color("red")
                elif board[i][j] == MazeObject.VISITED_TILE.value:
                    tile_color = pygame.Color("pink")
                elif board[i][j] == MazeObject.PLAYER_TILE.value:
                    tile_color = pygame.Color("green")
                else:
                    tile_color = pygame.Color("white")

                tile = Tile(i, j, tile_width, tile_height, tile_color,
                            tile_border)
                self.draw_tile(50, 50, tile)
        pygame.draw.rect(
            self.screen, pygame.Color("black"),
            pygame.Rect(50, 50, col * tile_width, row * tile_height), 3)
