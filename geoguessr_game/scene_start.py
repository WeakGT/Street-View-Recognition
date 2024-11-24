import pygame
from base_scene import Scene
from config import *

class StartScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.audio_manager.load_music("geoguessr_game/assets/audio/music/background.mp3")
        self.alpha = 0  # 當前透明度
        self.fade_in = True  # 是否正在漸入

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 當玩家點擊螢幕時開始遊戲
                self.audio_manager.play_sound("click")
                self.manager.go_to("round_begin")

    def draw(self, screen):
        # 設置背景
        screen.fill((255, 255, 255))

        # 顯示標題文字
        title_font = pygame.font.Font(FONT_PATHS["title"], 72)
        title_text = title_font.render("Guess Country Game", True, (0, 0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 6 - title_text.get_height() // 2))

        # 顯示標題圖片
        title_image = pygame.image.load("geoguessr_game/assets/images/title.png")
        title_image = pygame.transform.scale(title_image, (480, 320))
        screen.blit(title_image, (WINDOW_WIDTH // 2 - title_image.get_width() // 2, WINDOW_HEIGHT // 2 - title_image.get_height() // 2 + 40))

        # 顯示 "Click to Start" 文字
        start_text_font = pygame.font.Font(FONT_PATHS["default"], 48)
        start_text = start_text_font.render("Click to Start", True, (0, 0, 0))

        # 創建一個可修改透明度的 Surface
        text_surface = start_text.convert_alpha()
        text_surface.set_alpha(self.alpha)  # 設定透明度

        screen.blit(text_surface, (
            WINDOW_WIDTH // 2 - text_surface.get_width() // 2,
            WINDOW_HEIGHT * 6 // 7
        ))

    def update(self):
        # 控制漸入漸出的邏輯
        if self.fade_in:
            self.alpha += 10  # 增加透明度
            if self.alpha >= 255:  # 到達最大透明度，切換為漸出
                self.alpha = 255
                self.fade_in = False
        else:
            self.alpha -= 10  # 減少透明度
            if self.alpha <= 0:  # 到達最小透明度，切換為漸入
                self.alpha = 0
                self.fade_in = True