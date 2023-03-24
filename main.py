import pygame
from typing import Final

from src.maze_game import MazeGame, MazeGameState
from src.maze_game_visualization import MazeGamePygameVisualization

SCREEN_WIDTH: Final = 800
SCREEN_HEIGHT: Final = 600
MAZE_WIDTH: Final = SCREEN_WIDTH - 100
MAZE_HEIGHT: Final = SCREEN_HEIGHT - 100

if __name__ == "__main__":

    running = True
    game = MazeGame(MAZE_WIDTH, MAZE_HEIGHT)
    visualizer = MazeGamePygameVisualization(SCREEN_HEIGHT, SCREEN_WIDTH)

    while running:
        if game.state == MazeGameState.MENU:
            visualizer.draw_main_menu()

        elif game.state == MazeGameState.PAUSED:
            print("we have paused the game!")

        else:
            visualizer.draw_maze(game.curr_level_maze)
            visualizer.draw_level_counter(game.curr_level_maze)
            visualizer.draw_step_counter(game.curr_level_maze)
            if game.solved:
                visualizer.draw_game_over()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                continue

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.set_state(MazeGameState.PLAYING)
                    if game.solved:
                        game.get_next_level()
                elif event.key == pygame.K_ESCAPE:
                    game.set_state(MazeGameState.MENU)
                elif event.key == pygame.K_SPACE:
                    game.set_state(MazeGameState.PAUSED)
                elif (event.key == pygame.K_UP or event.key
                      == pygame.K_w) and game.state == MazeGameState.PLAYING:
                    game.move_up()
                elif (event.key == pygame.K_DOWN or event.key
                      == pygame.K_s) and game.state == MazeGameState.PLAYING:
                    game.move_down()
                elif (event.key == pygame.K_RIGHT or event.key
                      == pygame.K_d) and game.state == MazeGameState.PLAYING:
                    game.move_right()
                elif (event.key == pygame.K_LEFT or event.key
                      == pygame.K_a) and game.state == MazeGameState.PLAYING:
                    game.move_left()

        pygame.display.update()

    pygame.quit()
