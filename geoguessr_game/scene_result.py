import pygame
from base_scene import Scene
from config import *

class ResultScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("Result Scene", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 300))
        self.start_time = pygame.time.get_ticks()

    def on_enter(self):
        self.start_time = pygame.time.get_ticks()  # 每次進入場景重置開始時間

    def update(self):
        if pygame.time.get_ticks() - self.start_time > 5000:
            if self.manager.round_count < NUM_ROUNDS:
                self.manager.round_count += 1
                self.manager.go_to("round_begin")
            else:
                self.manager.go_to("final_result")

    def draw(self, screen):
        screen.fill((255, 0, 0))
        screen.blit(self.text, self.text_rect)
