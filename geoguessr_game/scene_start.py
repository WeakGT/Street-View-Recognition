import pygame
from base_scene import Scene
from config import *

class StartScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 60)  # 字體設置
        self.start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 + 240, 250, 75)  # 按鈕大小與位置

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.manager.go_to("round_begin")

    def draw(self, screen):
        # 設置背景
        screen.fill((255, 255, 255))

        # 顯示標題文字
        title_font = pygame.font.SysFont(None, 120)
        title_text = title_font.render("Guess City Game", True, (0, 0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 3 - 90))

        # 顯示標題圖片
        title_image = pygame.image.load("assets/images/title.png")
        title_image = pygame.transform.scale(title_image, (605, 351))
        screen.blit(title_image, (WINDOW_WIDTH // 2 - title_image.get_width() // 2, WINDOW_HEIGHT // 3 + 40))

        # 顯示開始按鈕
        start_button_text = self.font.render("Start", True, (255, 255, 255))
        pygame.draw.rect(screen, (29, 106, 150), self.start_button_rect)
        screen.blit(start_button_text, (
            self.start_button_rect.x + (self.start_button_rect.width - start_button_text.get_width()) // 2,
            self.start_button_rect.y + (self.start_button_rect.height - start_button_text.get_height()) // 2
        ))