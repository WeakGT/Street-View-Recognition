import pygame
from base_scene import Scene
from config import *

class StartScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT * 6 // 7, 200, 60)  # 按鈕大小與位置

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    self.manager.go_to("round_begin")

    def draw(self, screen):
        # 設置背景
        screen.fill((255, 255, 255))

        # 顯示標題文字
        title_font = pygame.font.SysFont(None, 96)
        title_text = title_font.render("Guess Country Game", True, (0, 0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 6))

        # 顯示標題圖片
        title_image = pygame.image.load("geoguessr_game/assets/images/title.png")
        title_image = pygame.transform.scale(title_image, (480, 320))
        screen.blit(title_image, (WINDOW_WIDTH // 2 - title_image.get_width() // 2, WINDOW_HEIGHT // 2 - title_image.get_height() // 2 + 40))

        # 顯示開始按鈕
        start_button_font = pygame.font.Font(None, 36)
        start_button_text = start_button_font.render("Start", True, (255, 255, 255))
        start_button_color = (29, 106, 150) if not self.start_button_rect.collidepoint(pygame.mouse.get_pos()) else (45, 135, 190)
        pygame.draw.rect(screen, start_button_color, self.start_button_rect, border_radius=10)

        screen.blit(start_button_text, (
            self.start_button_rect.x + (self.start_button_rect.width - start_button_text.get_width()) // 2,
            self.start_button_rect.y + (self.start_button_rect.height - start_button_text.get_height()) // 2
        ))