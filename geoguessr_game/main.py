import pygame
import sys
from scene_manager import SceneManager
from config import *

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 遊戲主迴圈
def main():
    scene_manager = SceneManager()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        scene_manager.handle_events(events)
        scene_manager.update()
        scene_manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)

# 啟動遊戲
if __name__ == "__main__":
    main()