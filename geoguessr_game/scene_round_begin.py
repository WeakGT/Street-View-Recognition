import pygame
from base_scene import Scene
from config import *

class RoundBeginScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.Font(None, 96)
        self.start_time = pygame.time.get_ticks()  # 初始化開始時間
        self.duration = 2000  # 倒數計時 2 秒

    def on_enter(self):
        self.start_time = pygame.time.get_ticks()  # 每次進入場景重置開始時間
        self.manager.round_count += 1  # 回合數加 1

    def update(self):
        # 檢查是否超過 2 秒或是滑鼠點擊，超過則進入遊戲場景
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.manager.go_to("game")
        # 按下滑鼠也可以進入遊戲場景
        if pygame.time.get_ticks() - self.start_time > 500:
            if pygame.mouse.get_pressed()[0]:
                self.manager.go_to("game")

    def draw(self, screen):
        screen.fill((255, 255, 255))  # 設定背景顏色

        # 顯示回合標題
        title_text = self.font.render(f"Round {self.manager.round_count}", True, (0, 0, 0))
        # 將文字置中
        title_text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
        screen.blit(title_text, title_text_rect)

        # 計算倒數時間的剩餘比例
        elapsed_time = pygame.time.get_ticks() - self.start_time
        remaining_ratio = max(0, (self.duration - elapsed_time) / self.duration)

        # 繪製倒數計時的進度條
        progress_bar_width = 300  # 進度條寬度
        progress_bar_height = 20   # 進度條高度
        # 進度條位置在畫面中央下方
        progress_bar_x = WINDOW_WIDTH // 2 - progress_bar_width // 2
        progress_bar_y = WINDOW_HEIGHT // 2 + 100

        # 繪製進度條的背景（灰色）
        pygame.draw.rect(screen, (209, 237, 225), (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))

        # 繪製剩餘的進度條（藍色）
        remaining_bar_width = int(progress_bar_width * remaining_ratio)
        pygame.draw.rect(screen, (2, 140, 106), (progress_bar_x, progress_bar_y, remaining_bar_width, progress_bar_height))
