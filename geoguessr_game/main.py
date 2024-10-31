import pygame
import sys
from game_logic import Game
from config import *

# 初始化 Pygame
pygame.init()

# 設置窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Geoguessr Clone")

# 主遊戲循環
def main():
    game = Game(window)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(30)  # 控制每秒幀數 (FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()