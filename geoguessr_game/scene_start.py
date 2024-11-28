import pygame
import random
from base_scene import Scene
from config import *

class StartScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.audio_manager.load_music("geoguessr_game/assets/audio/music/background.mp3")
        self.alpha = 0  # 文字透明度
        self.fade_in = True  # 是否正在漸入

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.audio_manager.play_sound("click")
                self.manager.go_to("round_begin")

    def draw(self, screen):
        """繪製畫面內容"""
        super().draw(screen)

        # 繪製標題文字
        title_font = pygame.font.Font(FONT_PATHS["title"], 72)
        title_text = title_font.render("Guess Country Game", True, (0, 0, 0))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 3 - title_text.get_height() // 2))

        # 繪製 "Click to Start" 漸入漸出的文字
        start_text_font = pygame.font.Font(FONT_PATHS["default"], 48)
        start_text = start_text_font.render("Click to Start", True, (0, 0, 0))
        text_surface = start_text.convert_alpha()
        text_surface.set_alpha(self.alpha)
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT * 2 // 3))

    def update(self):
        """更新畫面狀態"""
        super().update()

        # 控制文字透明度漸變
        if self.fade_in:
            self.alpha += 10
            if self.alpha >= 255:
                self.alpha = 255
                self.fade_in = False
        else:
            self.alpha -= 10
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = True